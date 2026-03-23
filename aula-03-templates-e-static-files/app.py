from flask import Flask, render_template
from controllers import routes

app = Flask(__name__, template_folder='views')

#enviando a variavel APP (flask) para as rota
routes.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/games')
def games():
    # criaando variaveis para passar as informacoes de um jogo
    titulo = 'Dead By Daylight'
    ano = 2016
    categoria = "Asymetric Horror"
    
    #criando um objeto python (dicionario) para representar as propriedades de um jogo
    #criando vetor (lista)
    
    game = {
        "Titulo" : "minecraft",
        "Ano" : "2012",
        "Categoria" : "Sandbox/Survival"
    }
    jogadores = ['Felipe', 'Akemi', 'Heitor', 'Guilherme']

    return render_template('games.html',
    titulo=titulo,
    ano=ano,
    categoria=categoria,
    jogadores=jogadores,
    game=game)
    
@app.route('/consoles')
def consoles():
    consoles = ['PS4','PS5','Xbox One','Switch','Switch 2','Steam Deck']
    
    return render_template('consoles.html',
    consoles=consoles)
    
if __name__ == '__main__':
    app.run(debug=True)