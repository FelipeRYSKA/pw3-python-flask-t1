# Importando o Flask para a aplicação
from flask import render_template, request, redirect, url_for, flash, session
# Importando o MARKUPSAFE (permite incluir link nas flash messages)
from markupsafe import Markup
# Importando o Model de Games
from models.database import Game, db, Usuario
# Importando WERKZEUG
from werkzeug.security import generate_password_hash, check_password_hash

import urllib.request  # .request se for Python 3.12
import json
#importando a biblioteca os (manipula o sistema operacional)
import os
#importando a biblioteca uuid (gera um nome aleatorio parav o arquivo)
import uuid

# Criando a função principal para inicializar as rotas
def init_app(app):
    # FUNÇÃO DE MIDDLEWARE
    @app.before_request
    def check_auth():
        # Rotas que não precisam de autenticação
        rotasPermitidas = ['home', 'login', 'cadastro', 'static']
        # Se a rota atual não requer autenticação
        if request.endpoint in rotasPermitidas:
            # Libera o acesso
            return
        # Se o usuário estiver tentando acessar um rota protegida sem estar autenticado
        if 'usuario_id' not in session:
            return redirect(url_for('login'))

    # VARIÁVEIS GLOBAIS
    listaConsoles = ['Playstation 5', 'Xbox One',
                     'Super Nintendo', 'Atari', '3DS']

    listaGames = [{"titulo": "CS-GO", "ano": 2012,
                   "categoria": "FPS Online", "plataforma": "PC (Windows)"}]

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route('/')
    # def cria funções no Python
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        # Criando variáveis para a rota de games
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        # Lista de jogadores (uma lista é um vetor/array)
        jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']
        # Enviando as variáveis para o HTML
        return render_template('games.html',
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores)

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        # Criando um objeto
        console = {"Nome": "Playstation 2",
                   "Fabricante": "Sony",
                   "Ano": 2000}

        # Recendo o valor do formulário
        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))

        return render_template('consoles.html',
                               console=console,
                               listaConsoles=listaConsoles)

    # ROTA PARA CADASTRAR UM JOGO
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():

        # Recebendo os dados do formulário e enviando para página
        # Verificando se a requisição do usuário é do tipo POST
        if request.method == 'POST':
            # Aqui ele irá gravar os dados na lista de jogos
            listaGames.append({'titulo': request.form.get('titulo'), 'ano': request.form.get(
                'ano'), 'categoria': request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
            # Aqui o usuário será redirecionado novamente para a página
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               listaGames=listaGames)

    # ROTA PARA O CRUD (ESTOQUE DE JOGOS)
    @app.route('/estoque', methods=['GET', 'POST'])
    # ADICIONANDO O PARÂMETRO ID A ROTA
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        # VERIFICANDO SE O ID FOI PASSADO PARA ROTA
        if id:
            game = Game.query.get(id)  # SELECIONA O JOGO
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))

        # CONDIÇÃO PARA VERIFICAR SE O USUÁRIO ESTÁ ENVIANDO UMA REQUISIÇÃO POST (cadastro)
        if request.method == 'POST':
            # REALIZA O CADASTRO
            # COLETANDO OS DADOS DO FORMULÁRIO
            # Pega os dados do formulário e transforma em um dicionário (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newgame = Game(
                dados['titulo'],
                dados['ano'],
                dados['categoria'],
                dados['plataforma'],
                dados['preco'],
                dados['quantidade']
            )
            # Método do SQLAlchemy para gravar no banco
            db.session.add(newgame)
            # Confirmação
            db.session.commit()
            return redirect(url_for('estoque'))
        # SELECIONANDO TODOS OS JOGOS DA TABELA
        games = Game.query.all()
        return render_template('estoque.html', games=games)

    @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Selecionando o jogo no banco pelo ID
        game = Game.query.get(id)
        # Verificando se a requisição é POST
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            # Alterando os dados do jogo
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editGame.html', game=game)

    # ROTA DE CADASTRO DE USUÁRIO
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        # Verificando se o método é POST
        if request.method == 'POST':
            # Coletando os dados do Formulário
            email = request.form['email']
            senha = request.form['senha']
            # VERIFICANDO SE USUÁRIO JÁ EXISTE
            usuario = Usuario.query.filter_by(email=email).first()
            # Verificando se a consulta retornou algo
            if usuario:
                msgUsuario = Markup(
                    "Usuário já cadastrado. Faça o <a href='/login'>login</a>")
                # Criando a flash message
                flash(msgUsuario, 'danger')
                return redirect(url_for('cadastro'))

            # GERANDO O HASH DA SENHA (CRIPTOGRAFIA)
            senha_criptografada = generate_password_hash(
                senha, method='scrypt')
            # Enviando os dados para o Model
            novo_usuario = Usuario(email=email, senha=senha_criptografada)
            # Cadastrando no banco
            db.session.add(novo_usuario)
            db.session.commit()

            # GERANDO MENSAGEM DE SUCESSO
            msgCad = Markup(
                "Cadastro realizado com sucesso! Você já pode fazer o <a href='/login'>login</a>.")
            flash(msgCad, 'success')

            return redirect(url_for('cadastro'))

        return render_template('cadastro.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # VERIFICANDO SE O MÉTODO É POST
        if request.method == 'POST':
            # COLETANDO OS DADOS DO USUÁRIO
            email = request.form['email']
            senha = request.form['senha']
            # BUSCANDO O USUÁRIO NO BANCO
            usuario = Usuario.query.filter_by(email=email).first()
            # SE O USUARIO EXISTIR
            if usuario:
                # VERIFICANDO A SENHA (hash)
                if check_password_hash(usuario.senha, senha):
                    # AQUI SERÁ CRIADO A SESSÃO
                    session['usuario_id'] = usuario.id
                    session['usuario_email'] = usuario.email
                    # Mensagem de Feedback
                    msgLogin = "Você foi autenticado com sucesso! Bem-vindo!"
                    flash(msgLogin, 'success')
                    return redirect(url_for('home'))
                # CASO SENHA INCORRETA
                else:
                    flash(
                        'Falha no login. Verifique os dados e tente novamente!', 'danger')
                    return redirect(url_for('login'))
            # SE O USUÁRIO NÃO FOR ENCONTRADO
            else:
                flash('O usuário informado não existe!', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html')

    # ROTA DO CONSUMO DA API
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        # Variável que armazena a URL da API
        url = 'https://www.freetogame.com/api/games'
        req = urllib.request.urlopen(url)
        # Lendo a resposta da requisição
        dados = req.read()
        # Convertendo a resposta da API de JSON para DICIONÁRIO
        listaJogos = json.loads(dados)
        # VERIFICANDO SE FOI PASSADO UMA ID PARA ROTA
        if id:
            jogoInfo = []
            for jogo in listaJogos:
                # Verifique se o ID corresponde
                if jogo['id'] == id:
                    jogoInfo = jogo
                    # Interrompendo o for
                    break
            if jogoInfo:
                return render_template('jogoInfo.html', jogoInfo=jogoInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', listaJogos=listaJogos)

    # ROTA DE LOGOUT
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        # Destruindo a sessão do usuário
        session.clear()
        return redirect(url_for('home'))

    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        #lista de extensoes permitidas
        FILE_TYPES= set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'])
        # funcao para validar o tipo de arquivo enviado
        def arquivos_permitidos(filename):
            return '.' in filename and filename.rsplit
        ('.', 1)[1].lower() in FILE_TYPES

        #recebendo o arquivo do formulario
        if request.method =='POST':
            #guardando o arquivo em uma variavel
            file = request.file['file']
            # verificar se a extensao é valida
            if not arquivos_permitidos(file.filename):
                flash("Arquivo não permitido! Envie somente arquivos de imagem.", 'danger')
            #se a extensao for valida
            # gere um nome aleatorio para o arquivo
            filename = str(uuid.uuid4())
            #salva o arquivo na pasta de uploads
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem recebvida com sucesso!", 'success')
            return redirect(url_for('galeria'))

        return render_template('galeria.html')