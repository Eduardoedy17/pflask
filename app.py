from flask import Flask, render_template

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
def aluno_listar():
    return render_template('aluno/lista_A.html')

@app.route('/professor')
def professor_listar():
    return render_template('professor/lista_P.html')






#Método 'main' sempre no final do arquivo.
if __name__ == '__main__':
    app.run(debug=True)
