# Comentário no Python
# Importando o Flask para a aplicação
import pymysql.cursors
from flask import Flask, render_template
# Importando PYMYSQL
import pymysql
# Importando o SQLAlchemy e o Model
from models.database import db, Game

# Definindo um nome para o banco
DB_NAME = 'thegames'

# Importando o Controller (rotas)
from controllers import routes

# Carregando o Flask na variável "app"
app = Flask(__name__, template_folder='views')
# Variáveis com __ são variáveis de ambiente do Python
# __name__ representa o nome da aplicação

# Passando o nome do banco para o Flask
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco para o Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# DEFININDO UMA CHAVE SECRETA (flash messages e sessões)
app.config['SECRET_KEY'] = 'meusegredo'

# DEFININDO O TEMPO DA SESSÃO
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 1 hora

#definindo a pasta que recebera os uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'

#definindo tamanho maximo de arquivos
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 #32MBs 1024 2x é para traduzir o tamanho 32 para MB

# Enviando a variável app para as rotas
routes.init_app(app)

# Iniciando o servidor na porta 5000
if __name__ == '__main__':
    # Conectando-se ao MYSQL para criar o banco de dados
    # Passando os dados de conexão
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # Tentando a conexão
    try:
        with connection.cursor() as cursor:
            # Enviando a QUERY para criar o banco
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print("O banco de dados está criado!")
    except Exception as error:
        print(f"Ocorreu um erro ao criar o banco de dados! {error}")
    # Fechando a conexão
    finally:
        connection.close()
    # Inicializando o FLASK-SQLALCHEMY
    db.init_app(app=app)
    # Enviando a requisição para criar as tabelas
    with app.test_request_context():
        db.create_all()    
    # Inicializando o servidor:
    app.run(host='0.0.0.0', port=5000, debug=True) # O método .run() inicia o servidor

