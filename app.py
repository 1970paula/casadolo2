import sqlite3
from flask import Flask, render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_segura_casa_de_lo_2026'

# Nome real do seu ficheiro SQLite
DATABASE = 'casa_de_lo.db' 

def ligar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

PRODUTOS = {
    1: {"nome": "Pastéis de Nata uni.", "preco": 1.50},
    2: {"nome": "Pão de Ló de Margaride", "preco": 20.00},
    3: {"nome": "Toucinho do Céu Conventual", "preco": 26.00},
    4: {"nome": "Queijadas de Sintra uni.", "preco": 1.20},
    5: {"nome": "Ovos Moles uni.", "preco": 2.00},
    6: {"nome": "Bolo de Mel da Madeira", "preco": 16.00},
    7: {"nome": "Brisas do Lis uni.", "preco": 1.50},
    8: {"nome": "Arrufadas uni.", "preco": 1.20},
    9: {"nome": "Folar", "preco": 6.00},
    10: {"nome": "Marmelada de Marmelo/Kg", "preco": 5.80},
    11: {"nome": "Geleia de Marmelo/Kg", "preco": 6.50},
    12: {"nome": "Compotas/Várias", "preco": 4.50}
}

@app.route('/')
def index_entrada():
    return render_template('index.html')

@app.route('/doces')
def index():
    quantidade_itens = len(session.get('carrinho', []))
    return render_template('casa-de-lo.html', quantidade=quantidade_itens)

# ==========================================
# ROTA DE REGISTO (Guarda dados no SQLite)
# ==========================================
@app.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        nome_entidade = request.form.get('nome_entidade')
        tipo_cliente = request.form.get('tipo_cliente')
        telemovel = request.form.get('telemovel')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        senha_encriptada = generate_password_hash(senha)
        
        try:
            db = ligar_bd()
            cursor = db.cursor()
            # Mapeamento exato das colunas da sua tabela reais
            cursor.execute(
                """INSERT INTO clientes 
                (id_cliente, nome_entidade, tipo_cliente, telemovel, email, valor_total, valor_em_divida, password) 
                VALUES (?, ?, ?, ?, ?, 0.0, 0.0, ?)""",
                (id_cliente, nome_entidade, tipo_cliente, telemovel, email, senha_encriptada)
            )
            db.commit()
            db.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Erro: O ID de Cliente ou E-mail já existe na base de dados!"
            
    return render_template('registo.html')

# ==========================================
# ROTA DE LOGIN (Valida dados no SQLite)
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha_inserida = request.form.get('senha')
        
        db = ligar_bd()
        cursor = db.cursor()
        cursor.execute("SELECT * clientes WHERE email = ?", (email,))
        utilizador = cursor.fetchone()
        db.close()
        
        # Mapeia com a sua coluna real 'password'
        if utilizador and check_password_hash(utilizador['password'], senha_inserida):
            session['utilizador_id'] = utilizador['id_cliente']
            session['utilizador_nome'] = utilizador['nome_entidade']
            return redirect(url_for('index'))
        else:
            return "E-mail ou palavra-passe incorretos!"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('utilizador_id', None)
    session.pop('utilizador_nome', None)
    return redirect(url_for('index_entrada'))

@app.route('/carrinho')
def carrinho():
    itens_no_carrinho = session.get('carrinho', [])
    total = sum(item['preco'] for item in itens_no_carrinho)
    return render_template('carrinho.html', produtos=itens_no_carrinho, total=total)

@app.route('/adicionar_ao_carrinho/<int:produto_id>')
def adicionar_ao_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = []
    if produto_id in PRODUTOS:
        novo_item = PRODUTOS[produto_id].copy()
        novo_item['id'] = produto_id
        session['carrinho'].append(novo_item)
        session.modified = True 
    return redirect(url_for('index'))

@app.route('/remover_do_carrinho/<int:produto_id>')
def remover_do_carrinho(produto_id):
    if 'carrinho' in session:
        for item in session['carrinho']:
            if item['id'] == produto_id:
                session['carrinho'].remove(item)
                session.modified = True
                break
    return redirect(url_for('carrinho'))

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    session.pop('carrinho', None) 
    return "Compra finalizada!"

if __name__ == '__main__':
    app.run(debug=True)
