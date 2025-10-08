from flask import Flask, render_template

# Criação da aplicação Flask.
app = Flask(__name__)

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




#Método 'main' sempre no final do arquivo.
if __name__ == '__main__':
    app.run(debug=True)
