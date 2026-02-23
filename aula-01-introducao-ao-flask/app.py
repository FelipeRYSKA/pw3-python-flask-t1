# comentario em python
# importando o flask na aplicação
from flask import Flask, render_template #render_template renderiza as paginas html  

# carregando o flask em um variavel
app = Flask(__name__, template_folder='views')
#__name__ é uma variavel de ambiente de python que tem o nome do módulo atual

#criando a rota principal do sit

@app.route('/')
# def serve para criar funcoes no python
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/consoles')
def consoles():
    return render_template('consoles.html')


#iniciando servidor web
if __name__ == '__main__':
    app.run(debug=True)
    
    #verificando se app.py for o arquivo principal, ele inicia o servidor