from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/index-entrada')
def index_entrada():
    return render_template('index.html')

@app.route('/')
def index():
    doces = [
        {"nome": "Pastéis de Nata", "imagem": "pictures/pasteis-de-nata.jpg", "preco": "1.20"},
        {"nome": "Arrufadas", "imagem": "pictures/arrufadas.jpg", "preco": "1.50"},
        {"nome": "Folar", "imagem": "pictures/folar.jpg", "preco": "8.00"},
        {"nome": "Marmelada", "imagem": "pictures/marmelada.jfif", "preco": "4.50"}
    ]
    return render_template('casa-de-lo.html', doces=doces)

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/receitas')
def receitas():
    return render_template('receitas.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    metodo = request.form.get('metodo_pagamento')
    if not metodo:
        metodo = "Não selecionado"
        
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif; color: #8B4513;">
        <h1>🛒 Compra Finalizada com Sucesso!</h1>
        <p style="font-size: 1.2em; color: #333;">Obrigado por comprar na <strong>Casa do Ló</strong>.</p>
        <p style="font-size: 1.1em; background: #f8f9fa; display: inline-block; padding: 10px 20px; border-radius: 5px; border: 1px solid #8B4513;">
            Método de Pagamento Escolhido: <strong>{metodo.upper()}</strong>
        </p>
        <br><br>
        <a href="{url_for('index')}" style="display: inline-block; background: #8B4513; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Voltar à Loja</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)
