# Importando o render_template
# Motor para renderizar as páginas
from flask import render_template, request, redirect, url_for

from models.database import Game, db, Console, Usuario

from werkzeug.security import generate_password_hash


# Criando a função para receber o Flask (app)

def init_app(app):
    # SIMULANDO UM BANCO DE DADOS
    listaGames = [{"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}]

    # A partir daqui virão as rotas

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route('/')
    # def serve para criar funções no Python
    def home():
        return render_template('index.html')

    # CRIANDO A ROTA DE GAMES
    @app.route('/games')
    def games():
        # Criando variáveis para passar as informações de um jogo
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroid Van"

        # Criando um objeto Python (dicionário) para representar as propriedades de um jogo
        game = {
            "Título": "Minecraft",
            "Ano": 2012,
            "Categoria": "Sandbox"
        }
        # Criando vetor (lista)
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Vitor', 'Antônio']
        return render_template('games.html',
                               # Enviando as variáveis para página HTML
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores,
                               game=game)

    # CRIANDO A ROTA DE CONSOLES
    @app.route('/consoles')
    def consoles():
        # Criando vetor (lista)
        consoles = ['Xbox', 'Playstation 5',
                    'Super Nintendo', 'Gameboy', 'Atari']
        return render_template('consoles.html',
                               consoles=consoles)

    # ROTA DE CADASTRO DE JOGOS
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        # Verificando se o método da requisição é POST
        if request.method == 'POST':
            # Recebendo os dados do formulário e gravando na lista
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria')})
            # o método append() adiciona valores a lista
            return redirect(url_for('cadgames'))    
        return render_template('cadgames.html',
                               listaGames = listaGames)
        
    # rota de estoque de jogos (crud)
    @app.route("/estoque_jogos", methods=['GET', 'POST'])
    # criando um parametro na rota (ID) para excluir um registro
    @app.route("/estoque_jogos/delete/<int:id>")
    def estoque_jogos(id=None):
        #verificando se esta sendo enviado o parametro id para a rota
        if id:
            game = Game.query.get(id) #SELECT no banco
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        #verificando se a requisição é do tipo post
        if request.method == 'POST':
            # coletando os dados preenchidos no formulario
            dados_form = request.form.to_dict()
            #enviando dados para Model
            newGame = Game(
                dados_form['titulo'],
                dados_form['ano'],
                dados_form['categoria'],
                dados_form['plataforma'],
                dados_form['preco'],
                dados_form['quantidade'],
            )
            #Método do SQLAlchemy para grravar os dados no banco
            db.session.add(newGame)
            #confirmando a alteração no banco
            db.session.commit()
            #redirecionando o usuario para a pagina de estoque
            return redirect(url_for('estoque_jogos'))
            
            
        #selecionando toddos os jogos do banco
        #select * from games
        games = Game.query.all()
        return render_template('estoque_jogos.html', games=games)
    
    @app.route('/editar_jogos/<int:id>', methods=['GET'])
    def editar_jogos(id):
        return render_template('editar_jogos.html')
        game = Game.query.get(id)

        if request.method == 'POST':
            dados_form = request.form.to_dict()
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editar_jogos.html', game=game)
        
        #Tentativa de criar ESTOQUE CONSOLES
        
    # rota de estoque de jogos (crud)
    @app.route("/estoque-consoles", methods=['GET', 'POST'])
    # criando um parametro na rota (ID) para excluir um registro
    @app.route("/estoque-consoles/delete/<int:id>")
    def estoque_console(id=None):
        #verificando se esta sendo enviado o parametro id para a rota
        if id:
            Console = Console.query.get(id) #SELECT no banco
            db.session.delete(Console)
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
        #verificando se a requisição é do tipo post
        if request.method == 'POST':
            # coletando os dados preenchidos no formulario
            dados_form = request.form.to_dict()
            #enviando dados para Model
            newConsole = Console(
                dados_form['nome'],
                dados_form['fabricante'],
                dados_form['ano'],
                dados_form['preco'],
                dados_form['quantidade']
            )
            #Método do SQLAlchemy para grravar os dados no banco
            db.session.add(newConsole)
            #confirmando a alteração no banco
            db.session.commit()
            #redirecionando o usuario para a pagina de estoque
            return redirect(url_for('estoque_consoles'))
            
            
        #selecionando toddos os console do banco
        #select * from games
        consoles = Console.query.all()
        return render_template('estoque-consoles.html', consoles=consoles)
    
    @app.route("/cadastro", methods=['GET', 'POST'])
    def cadastro():
        if request.method =='POST':
            email = request.form['email']
            senha = request.form['senha']

            senha_criptografia = generator_password_hash(senha, method='scrypt')
            #enviando para o model
            novo_usuario = Usuario(email=email, senha=senha_criptografia)
            #jogando no banco
            db.session.add(novo_usuario)
            db.session.commit()
            #validar os dados
            #salvar os dados no banco de dados
            return redirect(url_for('login'))
        return render_template('cadastro.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return "Bem-vindo a página de login"
    

