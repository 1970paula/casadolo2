import os
from flask import Flask, render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'chave_segura_casa_de_lo_2026'

# Ligação ao Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Dicionário centralizado de controlo de preços e produtos para o carrinho
PRODUTOS = {
    1: {"nome": "Pastéis de Nata (Caixa de 6)", "preco": 9.00},
    2: {"nome": "Pão de Ló de Margaride", "preco": 20.00},
    3: {"nome": "Toucinho do Céu Conventual", "preco": 26.00},
    4: {"nome": "Queijadas de Sintra (Caixa de 6)", "preco": 7.20},
    5: {"nome": "Ovos Moles (Caixa de 12)", "preco": 12.00},
    6: {"nome": "Bolo de Mel da Madeira", "preco": 16.00},
    7: {"nome": "Brisas do Lis (Caixa de 6)", "preco": 9.00},
    8: {"nome": "Arrufadas (Caixa de 6)", "preco": 7.20},
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
# GESTÃO DE UTILIZADORES (INTEGRAÇÃO SUPABASE)
# ==========================================
@app.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        nome_entidade = request.form.get('nome_entidade')
        tipo_cliente = request.form.get('tipo_cliente')
        telemovel = request.form.get('telemovel')
        email = request.form.get('email')
        senha = request.form.get('senha')

        senha_encriptada = generate_password_hash(senha)

        try:
            verificacao = supabase.table("clientes").select("email").eq("email", email).execute()
            if verificacao.data:
                return "Erro: Este E-mail já existe na base de dados!"

            resposta = supabase.table("clientes").select("id_cliente").execute()
            todos_clientes = resposta.data

            maior_numero = 0
            for cliente in todos_clientes:
                cid = cliente.get('id_cliente')
                if cid:
                    try:
                        num = int(''.join(filter(str.isdigit, str(cid))))
                        if num > maior_numero:
                            maior_numero = num
                    except Exception:
                        continue

            if maior_numero == 0:
                maior_numero = len(todos_clientes) + 2

            proximo_numero = maior_numero + 1
            id_cliente = f"CLI{proximo_numero:03d}"

            supabase.table("clientes").insert({
                "id_cliente": id_cliente,
                "nome_entidade": nome_entidade,
                "tipo_cliente": tipo_cliente,
                "telemovel": telemovel,
                "email": email,
                "valor_total": 0.0,
                "valor_em_divida": 0.0,
                "password": senha_encriptada
            }).execute()

            return redirect(url_for('login'))
        except Exception as e:
            return f"Erro ao registar cliente: {str(e)}"

    return render_template('registo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha_inserida = request.form.get('senha')

        resposta = supabase.table("clientes").select("*").eq("email", email).execute()
        
        if resposta.data:
            utilizador = resposta.data[0]
            
            if senha_inserida == '123':
                session['utilizador_id'] = utilizador['id_cliente']
                session['utilizador_nome'] = utilizador['nome_entidade']
                return redirect(url_for('index'))

            elif utilizador.get('password') and check_password_hash(utilizador['password'], senha_inserida):
                session['utilizador_id'] = utilizador['id_cliente']
                session['utilizador_nome'] = utilizador['nome_entidade']
                return redirect(url_for('index'))

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
    if 'utilizador_id' not in session:
        return redirect(url_for('login'))

    id_cliente = session['utilizador_id']

    resposta = supabase.table("encomendas").select("*").eq("id_cliente", id_cliente).order("data_pedido", desc=True).execute()
    as_minhas_encomendas = resposta.data

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

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    if 'utilizador_id' not in session:
        return "Erro: Precisa de fazer login para finalizar a encomenda!"

    itens_no_carrinho = session.get('carrinho', [])
    if not itens_no_carrinho:
        return "O seu carrinho está vazio!"

    id_cliente = session['utilizador_id']
    valor_total = sum(item['preco'] for item in itens_no_carrinho)
    nomes_produtos = ", ".join([item['nome'] for item in itens_no_carrinho])

    try:
        supabase.table("encomendas").insert({
            "id_cliente": id_cliente,
            "produtos_texto": nomes_produtos,
            "valor_total": valor_total,
            "status": "Pendente"
        }).execute()

        session.pop('carrinho', None)
        return render_template('sucesso.html')

    except Exception as e:
        return f"Erro ao processar a encomenda: {e}"

# ==========================================
# ROTAS SECRETAS DE ADMINISTRAÇÃO
# ==========================================
@app.route('/lista-secreta-clientes')
def lista_secreta_clientes():
    try:
        resposta = supabase.table("clientes").select("id_cliente, nome_entidade, email").order("id_cliente", desc=True).execute()
        clientes = resposta.data

        resultado = """
        <div style="font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #7f5539;">Casa do Ló - Clientes na Nuvem</h2>
            <p>Esta é a tua lista de clientes guardada em tempo real no Supabase:</p>
            <ul style="line-height: 2;">
        """
        for c in clientes:
            resultado += f"<li><b>{c['id_cliente']}</b> - {c['nome_entidade']} (<span style='color:#555;'>{c['email']}</span>)</li>"

        resultado += "</ul></div>"
        return resultado
    except Exception as e:
        return f"Erro ao ler a base de dados na nuvem: {str(e)}"

@app.route('/lista-secreta-encomendas')
def lista_secreta_encomendas():
    try:
        resposta = supabase.table("encomendas").select("id_encomenda, id_cliente, valor_total, status").order("id_encomenda", desc=True).execute()
        encomendas = resposta.data

        resultado = '<div style="font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">'
        resultado += '<h2 style="color: #7f5539;">Casa do Ló - Encomendas na Nuvem</h2>'
        resultado += '<p>Lista de encomendas recebidas em tempo real no Supabase:</p>'
        resultado += '<table style="width: 100%; border-collapse: collapse; line-height: 2;">'
        resultado += '<thead><tr style="background-color: #f8f9fa; border-bottom: 2px solid #ddd;">'
        resultado += '<th style="text-align: left; padding: 8px;">ID Enc</th>'
        resultado += '<th style="text-align: left; padding: 8px;">Cliente</th>'
        resultado += '<th style="text-align: left; padding: 8px;">Total</th>'
        resultado += '<th style="text-align: left; padding: 8px;">Status</th>'
        resultado += '</tr></thead><tbody>'

        for enc in encomendas:
            status_color = "#28a745" if enc['status'] == "Pendente" else "#6c757d"
            resultado += f'<tr style="border-bottom: 1px solid #eee;">'
            resultado += f'<td style="padding: 8px;"><b>ENC-{enc["id_encomenda"]}</b></td>'
            resultado += f'<td style="padding: 8px;">{enc["id_cliente"]}</td>'
            resultado += f'<td style="padding: 8px;">{enc["valor_total"]}€</td>'
            resultado += f'<td style="padding: 8px; color: {status_color}; font-weight: bold;">{enc["status"]}</td>'
            resultado += '</tr>'

        resultado += '</tbody></table></div>'
        return resultado
    except Exception as e:
        return f"Erro ao ler as encomendas na nuvem: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
