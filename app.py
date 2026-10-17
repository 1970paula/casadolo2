from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)
# Chave secreta obrigatória para permitir o uso de sessões (session) no Flask
app.secret_key = 'chave_segura_casa_de_lo_2026'

# Dicionário global para mapear os IDs aos dados dos produtos
PRODUTOS = {
    1: {"nome": "Pastéis de Nata uni.", "preco": 1.50},
    2: {"nome": "Pão de Ló de Margaride", "preco": 20.00},      # Atualizado (€20.00)
    3: {"nome": "Toucinho do Céu Conventual", "preco": 26.00},  # Atualizado (€26.00)
    4: {"nome": "Queijadas de Sintra uni.", "preco": 1.20},
    5: {"nome": "Ovos Moles uni.", "preco": 2.00},
    6: {"nome": "Bolo de Mel da Madeira", "preco": 16.00},      # Atualizado (€16.00)
    7: {"nome": "Brisas do Lis uni.", "preco": 1.50},
    8: {"nome": "Arrufadas uni.", "preco": 1.20},
    9: {"nome": "Folar", "preco": 4.80},
    10: {"nome": "Marmelada de Marmelo/Kg", "preco": 5.80},
    11: {"nome": "Geleia de Marmelo/Kg", "preco": 6.50},
    12: {"nome": "Compotas/Várias", "preco": 4.50}
}

@app.route('/index-entrada')
def index_entrada():
    return render_template('index.html')

@app.route('/')

def index():
    # Conta quantos itens estão guardados no carrinho da sessão do utilizador
    quantidade_itens = len(session.get('carrinho', []))
    
    # Renderiza o seu ficheiro HTML diretamente, enviando apenas a quantidade
    return render_template('casa-de-lo.html', quantidade=quantidade_itens)

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
    # Obtém a lista de itens guardados no carrinho da sessão (ou lista vazia se não houver nenhum)
    itens_no_carrinho = session.get('carrinho', [])
    
    # Calcula a soma total de todos os produtos presentes no carrinho
    total = sum(item['preco'] for item in itens_no_carrinho)
    
    # Passa os produtos e o valor total para o template HTML
    return render_template('carrinho.html', produtos=itens_no_carrinho, total=total)

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    metodo = request.form.get('metodo_pagamento')
    if not metodo:
        metodo = "Não selecionado"
        
    # Limpa o carrinho da sessão após a compra ser finalizada com sucesso
    session.pop('carrinho', None)
        
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

@app.route('/adicionar_ao_carrinho/<int:produto_id>')
def adicionar_ao_carrinho(produto_id):
    # Garante que a lista de carrinho existe dentro da sessão do utilizador
    if 'carrinho' not in session:
        session['carrinho'] = []
    
    # Verifica se o ID clicado corresponde a um produto existente no nosso dicionário
    if produto_id in PRODUTOS:
        # Cria uma cópia dos dados e anexa o ID para controlo posterior no HTML
        novo_item = PRODUTOS[produto_id].copy()
        novo_item['id'] = produto_id
        
        # Adiciona o item à lista guardada na sessão
        session['carrinho'].append(novo_item)
        session.modified = True  # Notifica explicitamente o Flask de que a sessão sofreu alterações

    return redirect(url_for('index'))

@app.route('/remover_do_carrinho/<int:produto_id>')
def remover_do_carrinho(produto_id):
    if 'carrinho' in session:
        # Percorre a lista do carrinho e remove apenas a primeira ocorrência do ID encontrado
        for item in session['carrinho']:
            if item['id'] == produto_id:
                session['carrinho'].remove(item)
                session.modified = True
                break
                
    return redirect(url_for('carrinho'))

if __name__ == '__main__':
    app.run(debug=True)
