from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
# Chave de segurança para o carrinho funcionar temporariamente no navegador
app.secret_key = 'chave_secreta_casa_de_lo_2026'

# Lista oficial de doces e preços da Casa de Ló
PRODUTOS = {
    1: {"nome": "Pastéis de Nata uni.", "preco": 1.50},
    2: {"nome": "Pão de Ló (Fatia/kg)", "preco": 2.00},
    3: {"nome": "Toucinho do Céu (Fatia/kg)", "preco": 2.00},
    4: {"nome": "Queijadas de Sintra uni.", "preco": 1.20},
    5: {"nome": "Ovos Moles uni.", "preco": 2.00},
    6: {"nome": "Bolo de Mel (Fatia/Kg)", "preco": 1.40},
    7: {"nome": "Brisas do Lis uni.", "preco": 1.50},
    8: {"nome": "Arrufadas uni.", "preco": 1.20},
    9: {"nome": "Folar", "preco": 4.80},
    10: {"nome": "Marmelada de Marmelo/Kg", "preco": 5.80},
    11: {"nome": "Geleia de Marmelo/Kg", "preco": 6.50},
    12: {"nome": "Compotas/Várias", "preco": 4.50}
}

# ROTA PRINCIPAL: Abre o seu ficheiro principal (casa-de-lo.html)
@app.route('/')
def index():
    carrinho = session.get('carrinho', {})
    total_itens = sum(carrinho.values())
    return render_template('casa-de-lo.html', produtos=PRODUTOS, total_itens=total_itens)

# ROTAS PARA AS OUTRAS PÁGINAS (Para os links do menu funcionarem)
@app.route('/index-entrada')
def index_entrada():
    return render_template('index.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/receitas')
def receitas():
    return render_template('receitas.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# ADICIONAR PRODUTO AO CARRINHO
@app.route('/adicionar/<int:produto_id>')
def adicionar_ao_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    carrinho = session['carrinho']
    id_str = str(produto_id)

    if id_str in carrinho:
        carrinho[id_str] += 1
    else:
        carrinho[id_str] = 1
        
    session['carrinho'] = carrinho
    return redirect(url_for('index'))

# VER A PÁGINA DO CARRINHO
@app.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', {})
    itens_carrinho = []
    total_pagar = 0.0

    for produto_id, quantity in carrinho.items():
        produto = PRODUTOS.get(int(produto_id))
        if produto:
            subtotal = produto['preco'] * quantity
            total_pagar += subtotal
            itens_carrinho.append({
                'id': produto_id,
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': quantity,
                'subtotal': round(subtotal, 2)
            })

    return render_template('carrinho.html', itens=itens_carrinho, total=round(total_pagar, 2))

# REMOVER APENAS UM DOCE
@app.route('/remover/<int:produto_id>')
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    id_str = str(produto_id)
    if id_str in carrinho:
        carrinho.pop(id_str)
        session['carrinho'] = carrinho
    return redirect(url_for('ver_carrinho'))

# LIMPAR CARRINHO INTEIRO
@app.route('/limpar')
def limpar_carrinho():
    session.pop('carrinho', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
