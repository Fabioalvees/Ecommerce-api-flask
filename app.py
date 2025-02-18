from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#instancia por padrão
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
"""
Modelagem -> [Produto = id, name, price, description]
"""
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
# para criar a base de dados ->abri terminal python -m flask shell > db.creat_all() >db.session.commit()

@app.route('/api/products/add', methods=["POST"])  #methods se nao colocar ele nao vai limitar, mas e uma boa pratica coloca
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data["description"] )
        db.session.add(product)
        db.session.commit()
        return jsonify ({"messege": "Successfully Registered!"})
    return jsonify ({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
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



#rotas ( pagina inicial ) e a função qie sera executada ao requisitar
@app.route('/')
def helllo_word():
    return "Hello word"

if __name__ == "__main__":
    app.run(debug=True)
    
