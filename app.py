import sqlite3
import psycopg2
from flask import Flask, render_template, request, redirect, flash
from dao.aluno_dao import AlunoDAO
from dao.matricula_dao import MatriculaDAO
from dao.professor_dao import ProfessorDAO
from dao.curso_dao import CursoDAO
from dao.turma_dao import TurmaDAO

from dao.db_config import get_db_connection


# Criação da aplicação Flask.
app = Flask(__name__) 

# Configuração da chave secreta para sessões e flash messages.
app.secret_key = 'uma_chave_muito_secreta_e_unica'

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

@app.route('/aluno/form')
def form_aluno():
    return render_template('aluno/form.html', aluno=None)

@app.route('/aluno/salvar/', methods=['POST'])  # Inserção
@app.route('/aluno/salvar/<int:id>', methods=['POST'])  # atualização ✅
def salvar_aluno(id=None):
    nome = request.form['nome']
    idade = request.form['idade']
    cidade = request.form['cidade']
    dao = AlunoDAO()
    result = dao.salvar(id, nome, idade, cidade)

    if result["status"] == "ok":
        flash("Registro salvo com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/aluno')

@app.route('/aluno/editar/<int:id>')
def editar_aluno(id):
    dao = AlunoDAO()
    aluno = dao.buscar_por_id(id)
    return render_template('aluno/form.html', aluno=aluno)

@app.route('/aluno/remover/<int:id>')
def remover_aluno(id):
    dao = AlunoDAO()
    result = dao.remover(id)

    if result["status"] == "ok":
        flash("Registro removido com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/aluno')

# --- ROTAS DE MATRÍCULA ---

@app.route('/matricula')
def listar_matricula():
    dao = MatriculaDAO()
    lista = dao.listar()
    return render_template('matricula/lista.html', lista=lista)

@app.route('/matricula/form')
def form_matricula():
    # Carrega alunos e turmas para os selects
    aluno_dao = AlunoDAO()
    turma_dao = TurmaDAO()
    alunos = aluno_dao.listar()
    turmas = turma_dao.listar() # O ideal aqui seria um listar que mostrasse info da turma
    
    return render_template('matricula/form.html', matricula=None, alunos=alunos, turmas=turmas)

@app.route('/matricula/salvar/', methods=['POST'])
@app.route('/matricula/salvar/<int:id>', methods=['POST'])
def salvar_matricula(id=None):
    aluno_id = request.form['aluno_id']
    turma_id = request.form['turma_id']
    
    # Precisamos descobrir o curso_id através da turma selecionada
    turma_dao = TurmaDAO()
    turma = turma_dao.buscar_por_id(turma_id)
    curso_id = turma[2] # O índice 2 é o curso_id na tabela turma
    
    dao = MatriculaDAO()
    result = dao.salvar(id, aluno_id, curso_id, turma_id)

    if result["status"] == "ok":
        flash("Matrícula realizada com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/matricula')

@app.route('/matricula/editar/<int:id>')
def editar_matricula(id):
    dao = MatriculaDAO()
    matricula = dao.buscar_por_id(id) # Busca a matrícula pelo ID
    
    aluno_dao = AlunoDAO()
    turma_dao = TurmaDAO()
    
    alunos = aluno_dao.listar() # Carrega lista para o select
    turmas = turma_dao.listar() # Carrega lista para o select
    
    return render_template('matricula/form.html', matricula=matricula, alunos=alunos, turmas=turmas)

@app.route('/matricula/remover/<int:id>')
def remover_matricula(id):
    dao = MatriculaDAO()
    result = dao.remover(id)
    if result["status"] == "ok":
        flash("Matrícula removida!", "success")
    else:
        flash(result["mensagem"], "danger")
    return redirect('/matricula')

@app.route('/professor')
def listar_professor():
    dao = ProfessorDAO()
    lista = dao.listar()
    return render_template('professor/lista.html', lista=lista)

@app.route('/professor/form')
def form_professor():
    return render_template('professor/form.html', professor=None)

@app.route('/professor/salvar/', methods=['POST'])  # Inserção
@app.route('/professor/salvar/<int:id>', methods=['POST'])  # atualização
def salvar_professor(id=None):
    nome = request.form['nome']
    disciplina = request.form['disciplina']
    dao = ProfessorDAO()
    result = dao.salvar(id, nome, disciplina) 

    if result["status"] == "ok":
        flash("Registro salvo com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/professor')

@app.route('/professor/editar/<int:id>')
def editar_professor(id):
    dao = ProfessorDAO()
    professor = dao.buscar_por_id(id)
    return render_template('professor/form.html', professor=professor)

@app.route('/professor/remover/<int:id>')
def remover_professor(id): 
    dao = ProfessorDAO()
    result = dao.remover(id)

    if result["status"] == "ok":
        flash("Registro removido com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/professor')

@app.route('/curso')
def listar_curso():
    dao = CursoDAO()
    lista = dao.listar()
    return render_template('curso/lista.html', lista=lista)

@app.route('/curso/form')
def form_curso():
    return render_template('curso/form.html', curso=None)

@app.route('/curso/salvar/', methods=['POST'])  # Inserção
@app.route('/curso/editar/<int:id>', methods=['POST'])  # atualização
def salvar_curso(id=None):
    nome_curso = request.form['nome_curso']
    duracao = request.form['duracao']
    dao = CursoDAO()
    result = dao.salvar(id, nome_curso, duracao) 

    if result["status"] == "ok":
        flash("Registro salvo com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/curso')

@app.route('/curso/editar/<int:id>')
def editar_curso(id):
    dao = CursoDAO()
    curso = dao.buscar_por_id(id)
    return render_template('curso/form.html', curso=curso)

@app.route('/curso/remover/<int:id>')
def remover_curso(id):
    dao = CursoDAO()
    result = dao.remover(id)

    if result["status"] == "ok":
        flash("Registro removido com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/curso')

@app.route('/turma')
def listar_turma():
    dao = TurmaDAO()
    lista = dao.listar()
    return render_template('turma/lista.html', lista=lista)

@app.route('/turma/form')
def form_turma():
    # Carrega as listas para preencher os selects
    curso_dao = CursoDAO()
    professor_dao = ProfessorDAO()
    cursos = curso_dao.listar()
    professores = professor_dao.listar()
    
    return render_template('turma/form.html', turma=None, cursos=cursos, professores=professores)

@app.route('/turma/salvar/', methods=['POST'])  # Inserção
@app.route('/turma/editar/<int:id>', methods=['POST'])  # atualização
def salvar_turma(id=None):
    semestre = request.form['semestre']
    curso_id = request.form['curso_id']
    professor_id = request.form['professor_id']
    dao = TurmaDAO()
    result = dao.salvar(id, semestre, curso_id, professor_id) 

    if result["status"] == "ok":
        flash("Registro salvo com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/turma')

@app.route('/turma/editar/<int:id>')
def editar_turma(id):
    turma_dao = TurmaDAO()
    curso_dao = CursoDAO()
    professor_dao = ProfessorDAO()
    
    # Busca a turma específica
    turma = turma_dao.buscar_por_id(id)
    # Carrega as listas para preencher os selects
    cursos = curso_dao.listar()
    professores = professor_dao.listar()
    
    return render_template('turma/form.html', turma=turma, cursos=cursos, professores=professores)

@app.route('/turma/remover/<int:id>')
def remover_turma(id):
    dao = TurmaDAO()
    result = dao.remover(id)

    if result["status"] == "ok":
        flash("Registro removido com sucesso!", "success")
    else:
        flash(result["mensagem"], "danger")

    return redirect('/turma')

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
