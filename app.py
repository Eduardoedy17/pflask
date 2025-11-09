import sqlite3
import psycopg2
from flask import Flask, render_template, request
from dao.aluno_dao import AlunoDAO
from dao.professor_dao import ProfessorDAO
from dao.curso_dao import CursoDAO
from dao.turma_dao import TurmaDAO
from dao.db_config import get_db_connection

# Criação da aplicação Flask.
app = Flask(__name__) 
# Desabilitar o cache do Jinja2 para desenvolvimento.
app.jinja_env.cache = {}

# Rotas da aplicação e navegação entre páginas.
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobre')
def sobre_sistema():
    return render_template('sobre.html')

@app.route('/ajuda')
def ajuda_sistema():
    return render_template('ajuda.html')

@app.route('/contato')
def contato_sistema():
    return render_template('contato.html')

@app.route('/aluno')
def listar_aluno():
    dao = AlunoDAO()
    lista = dao.listar()
    return render_template('aluno/lista.html', lista=lista)

@app.route('/professor')
def listar_professor():
    dao = ProfessorDAO()
    lista = dao.listar()
    return render_template('professor/lista.html', lista=lista)

@app.route('/curso')
def listar_curso():
    dao = CursoDAO()
    lista = dao.listar()
    return render_template('curso/lista.html', lista=lista)

@app.route('/turma')
def listar_turma():
    dao = TurmaDAO()
    lista = dao.listar()
    return render_template('turma/lista.html', lista=lista)

@app.route('/saudacao1/<nome>')
def saudacao1(nome):
    # dao.salvar(nome)
    return render_template('saudacao/saudacao.html', nome_recebido=nome)

@app.route('/saudacao2/')
def saudacao2():
    nome = request.args.get('nome')
    return render_template('saudacao/saudacao.html', nome_recebido=nome)

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    email = request.form['email']
    dados = f"Usuário: {usuario}, Senha: {senha}, E-mail: {email}"
    return render_template('saudacao/saudacao.html', nome_recebido=dados)

# Permita GET e POST
@app.route('/desafio', methods=['GET', 'POST'])
def desafio():
    # Crie a variável para os dados, começando como nula
    dados_recebidos = None 
    
    # Se a requisição for POST (formulário enviado)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        dt_nascimento = request.form['dt_nascimento']
        cpf = request.form['cpf']
        nome_mae = request.form['nome_mae']
        # Preencha a variável com os dados
        dados_recebidos = f"Nome: {nome}, E-mail: {email}, Data de Nascimento: {dt_nascimento}, CPF: {cpf}, Nome da Mãe: {nome_mae}"

    # Renderize a página em AMBOS os casos (GET ou POST)
    # Se for GET, dados_recebidos será None
    # Se for POST, dados_recebidos terá os dados do formulário
    return render_template('desafio/desafio1.html', nome_recebido=dados_recebidos)

#Método 'main' sempre no final do arquivo.
if __name__ == '__main__':
    app.run(debug=True)
