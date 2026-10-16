from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# 1. Rota da Página de Entrada (Ecrã inicial do site)
@app.route('/index-entrada')
def index_entrada():
    return render_template('index.html')

# 2. Rota Principal da Casa do Ló (Onde aparecem todos os doces)
@app.route('/')
def index():
    # Lista de doces que já tinhas configurada para a página principal
    doces = [
        {"nome": "Pastéis de Nata", "imagem": "pictures/pasteis-de-nata.jpg", "preco": "1.20"},
        {"nome": "Arrufadas", "imagem": "pictures/arrufadas.jpg", "preco": "1.50"},
        {"nome": "Folar", "imagem": "pictures/folar.jpg", "preco": "8.00"},
        {"nome": "Marmelada", "imagem": "pictures/marmelada.jfif", "preco": "4.50"}
    ]
    return render_template('casa-de-lo.html', doces=doces)

# 3. Rota da Página A Nossa História
@app.route('/historia')
def historia():
    return render_template('historia.html')

# 4. Rota da Página de Receitas
@app.route('/receitas')
def receitas():
    return render_template('receitas.html')

# 5. Rota da Página do Blog e Dicas
@app.route('/blog')
def blog():
    return render_template('blog.html')

# 6. Rota para Visualizar o Carrinho de Compras
@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

# 7. NOVA ROTA: Processar a Finalização da Compra e o Pagamento
@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    # O Flask agora consegue ler corretamente o método selecionado porque importámos o 'request' no topo
    metodo = request.form.get('metodo_pagamento')
    
    # Validação simples caso nada tenha sido selecionado por segurança
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

# A inicialização do servidor fica SEMPRE no final absoluto do ficheiro
if __name__ == '__main__':
    app.run(debug=True)
