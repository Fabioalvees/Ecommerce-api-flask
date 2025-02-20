from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user


#instancia por padrão
app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

"""
Modelagem -> [Produto = id, name, price, description]
# Usuario ( id, username ,password)
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
# para criar na base de dados ->abri terminal python -m flask shell > db.drop_all > db.create_all() >db.session.commit()
#   drop_all = deleto tudo     /   create_crio tudo novamente     
# # para criar um usuario no banco ->abri terminal python -m flask shell > user = User (username:"admin", password:"123") > db.session.add(user) >db.session.commit()                                                      

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
# para criar a base de dados ->abri terminal python -m flask shell > db.creat_all() >db.session.commit()

# autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    data = request.json # receber os dados

    user = User.query.filter_by(username=data.get("username")).first()

    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"messege": "Logged in Successfully!"})
    
    return jsonify({"messege": "Unauthorized. Invalid credentials"}), 401

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"messege": "Logout in Successfully!"})

@app.route('/api/products/add', methods=["POST"])  #methods se nao colocar ele nao vai limitar, mas e uma boa pratica coloca
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data["description"] )
        db.session.add(product)
        db.session.commit()
        return jsonify ({"messege": "Successfully Registered!"})
    return jsonify ({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    # recuperar o produto da base de dados
    # verificar se o produto existe
    # existir, apahar da base de dados
    # se nao existe, retornar 404 not found
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify ({"messege": "Product deleted!"})
    return jsonify ({"message": "Product not found"}), 404


@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
        product = Product.query.get(product_id)
        if product:
            return jsonify({"id": product.id, 
                            "name": product.name, 
                            "price": product.price, 
                            "description": product.description
            })
        return jsonify ({"messege": "Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data["name"]
    
    if 'price' in data:
        product.price = data["price"]
    
    if 'description' in data:
        product.description = data["description"]
    
    db.session.commit()
    return jsonify({'messege': 'Product update successfully'})

@app.route('/api/products/', methods=["GET"])
def get_all_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price
            })
    return jsonify(products_list)
    

#rotas ( pagina inicial ) e a função qie sera executada ao requisitar
@app.route('/')
def helllo_word():
    return "Hello word"

if __name__ == "__main__":
    app.run(debug=True)
    
