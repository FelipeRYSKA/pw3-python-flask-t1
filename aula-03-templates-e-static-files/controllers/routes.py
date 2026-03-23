# importando o redner_templates
# motor para renderizar o flask na aplicação
from flask import render_template


def init_app(app):
    
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