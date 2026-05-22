from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pedidos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PedidoCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pendente')

    def __repr__(self):
        return f'<Pedido {self.id} - {self.cliente}>'

@app.route('/')
def index():
    pedidos = PedidoCompra.query.all()
    return render_template('index.html', pedidos=pedidos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    cliente = request.form.get('cliente')
    produto = request.form.get('produto')
    quantidade = request.form.get('quantidade')
    preco_total = request.form.get('preco_total')
    status = request.form.get('status', 'Pendente')

    if cliente and produto and quantidade and preco_total:
        novo_pedido = PedidoCompra(
            cliente=cliente,
            produto=produto,
            quantidade=int(quantidade),
            preco_total=float(preco_total),
            status=status
        )
        db.session.add(novo_pedido)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    pedido = PedidoCompra.query.get_or_404(id)
    novo_status = request.form.get('status')
    if novo_status:
        pedido.status = novo_status
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    pedido = PedidoCompra.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
