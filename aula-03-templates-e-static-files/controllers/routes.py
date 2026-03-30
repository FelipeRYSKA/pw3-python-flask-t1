# importando o redner_templates
# motor para renderizar o flask na aplicação
from flask import render_template, request, redirect, url_for


def init_app(app):
    # simulando um banco de dados
    listaGames = [{"titulo": "CS-GO", "ano" : 2012, "categoria" : "FPS Online" }]
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
        titulo = "Consoles"
        consoles = ['PS4','PS5','Xbox One','Switch','Switch 2','Steam Deck']
        
        return render_template('consoles.html',
        titulo=titulo,
        consoles=consoles
        )
    
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        #verificando se o métodp da requisição é POST
        if request.method == 'POST': 
            #recebendo os dados do formulario e gravando na lista
            listaGames.append({'titulo' : request.form.get ('titulo'),
            'ano' : request.form.get('ano'),
            'categoria' : request.form.get('categoria')})
            # o método append() adiciona valores a lista
            return redirect(url_for('cadgames'))
        
        return render_template('cadgames.html',
        listaGames=listaGames)