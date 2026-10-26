import sqlite3
import os
from flask import Flask, render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Chave secreta obrigatória para o funcionamento seguro das sessões (session)
app.secret_key = 'chave_segura_casa_de_lo_2026'

# Nome exato da sua base de dados SQLite
DATABASE = 'casa_de_lo.db' 

# Função auxiliar para estabelecer ligação com o ficheiro SQLite
def ligar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

# Dicionário centralizado de controlo de preços e produtos para o carrinho
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

# ==========================================
# ROTAS INSTITUCIONAIS E DE NAVEGAÇÃO
# ==========================================
@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/receitas')
def receitas():
    return render_template('receitas.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/')
def index_entrada():
    return render_template('index.html')

@app.route('/doces')
def index():
    quantidade_itens = len(session.get('carrinho', []))
    return render_template('casa-de-lo.html', quantidade=quantidade_itens)

# ==========================================
# GESTÃO DE UTILIZADORES (INTEGRAÇÃO SQLITE)
# ==========================================
@app.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        nome_entidade = request.form.get('nome_entidade')
        tipo_cliente = request.form.get('tipo_cliente')
        telemovel = request.form.get('telemovel')
        email = request.form.get('email')
        senha = request.form.get('senha')  # Mudado para 'senha' porque é o name do HTML

        # Gera o hash criptográfico seguro a partir da palavra-passe digitada
        senha_encriptada = generate_password_hash(senha)

        try:
            db = ligar_bd()
            cursor = db.cursor()

         # Procura o maior ID de cliente existente na tabela
            cursor.execute("SELECT id_cliente FROM clientes ORDER BY id_cliente DESC LIMIT 1")
            ultimo_cliente = cursor.fetchone()
            
            if ultimo_cliente and ultimo_cliente[0]:
                # Extrai apenas os números do ID (ex: de 'CLI0014' extrai 14)
                ultimo_numero = int(''.join(filter(str.isdigit, ultimo_cliente[0])))
                proximo_numero = ultimo_numero + 1
            else:
          # Se a tabela estiver vazia, começa no 1
                proximo_numero = 1
            
          # Cria o próximo ID garantindo o formato correto (ex: CLI0015)
            id_cliente = f"CLI{proximo_numero:04d}"

            # Mapeamento com 'password' adaptado à tua tabela SQLite
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha_inserida = request.form.get('senha')
        
        db = ligar_bd()
        cursor = db.cursor()
        # Procura o e-mail na base de dados em tempo real
        cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
        utilizador = cursor.fetchone()
        db.close()
        
        if utilizador:
            # 🚨 REGRA GERAL PARA A APRESENTAÇÃO:
            # Se a senha for '123', aceita o login para QUALQUER cliente da base de dados!
            if senha_inserida == '123':
                session['utilizador_id'] = utilizador['id_cliente']
                session['utilizador_nome'] = utilizador['nome_entidade']
                return redirect(url_for('index'))
                
            # Validação normal por Hash (para novos registos feitos no site)
            elif utilizador['password'] and check_password_hash(utilizador['password'], senha_inserida):
                session['utilizador_id'] = utilizador['id_cliente']
                session['utilizador_nome'] = utilizador['nome_entidade']
                return redirect(url_for('index'))
                
        # Se o e-mail não existir ou a senha falhar as duas regras acima:
        return "E-mail ou palavra-passe incorretos!"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('utilizador_id', None)
    session.pop('utilizador_nome', None)
    return redirect(url_for('index_entrada'))

# ==========================================
# ÁREA DE CLIENTE (HISTÓRICO DE ENCOMENDAS)
# ==========================================
@app.route('/perfil')
def perfil():
    # Garante que o utilizador iniciou sessão
    if 'utilizador_id' not in session:
        return redirect(url_for('login'))
    
    id_cliente = session['utilizador_id']
    
    # Procura as encomendas feitas por este cliente específico
    db = ligar_bd()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM encomendas WHERE id_cliente = ? ORDER BY data_pedido DESC", 
        (id_cliente,)
    )
    as_minhas_encomendas = cursor.fetchall()
    db.close()
    
    return render_template('perfil.html', encomendas=as_minhas_encomendas)

# ==========================================
# OPERAÇÕES DO CARRINHO DE COMPRAS & ENCOMENDAS
# ==========================================
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

# MUDANÇA: Novas rotas para os botões de ajuste de quantidade (+ e -)
@app.route('/remover_um_do_carrinho/<int:produto_id>')
def remover_um_do_carrinho(produto_id):
    if 'carrinho' in session:
        for item in session['carrinho']:
            if item['id'] == produto_id:
                session['carrinho'].remove(item)
                session.modified = True
                break
    return redirect(url_for('index'))

@app.route('/adicionar_mais_um/<int:produto_id>')
def adicionar_mais_um(produto_id):
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

# MUDANÇA: Rota de finalização alterada para abrir o ficheiro sucesso.html das cores do site
@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    # Verifica se o cliente tem o login ativo
    if 'utilizador_id' not in session:
        return "Erro: Precisa de fazer login para finalizar a encomenda!"
    
    itens_no_carrinho = session.get('carrinho', [])
    if not itens_no_carrinho:
        return "O seu carrinho está vazio!"
    
    id_cliente = session['utilizador_id']
    valor_total = sum(item['preco'] for item in itens_no_carrinho)
    
    # Une os nomes de todos os doces numa única linha (Ex: "Pastéis de Nata uni., Folar")
    nomes_produtos = ", ".join([item['nome'] for item in itens_no_carrinho])
    
    # Insere o registo da encomenda associado a este cliente no SQLite
    try:
        db = ligar_bd()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO encomendas (id_cliente, produtos_texto, valor_total, status) 
               VALUES (?, ?, ?, 'Pendente')""",
            (id_cliente, nomes_produtos, valor_total)
        )
        db.commit()
        db.close()
        
        # Limpa o carrinho de compras após registar com sucesso
        session.pop('carrinho', None) 
        
        # REDIRECIONA PARA A NOVA PÁGINA VINTAGE DE SUCESSO
        return render_template('sucesso.html')
        
    except Exception as e:
        return f"Erro ao processar a encomenda: {e}"

if __name__ == '__main__':
    app.run(debug=True)

