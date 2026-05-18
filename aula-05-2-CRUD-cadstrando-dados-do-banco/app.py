# Comentário em Python
# Importando o Flask na aplicação
from flask import Flask, render_template
# render_template renderiza as páginas HTML
from controllers import routes
# Importando o PyMySQL
import pymysql
# Importando o Model de Games
from models.database import db, Game

# Carregando o Flask em uma variável
app = Flask(__name__, template_folder='views')
# __name__ é uma variável de ambiente do Python que tem o nome do módulo atual.

# Definindo o nome do banco de dados
DB_NAME = 'thegames'
# Passando o nome do banco para o Flask
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco para o Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Enviando a variável APP (FLASK) para as rotas.
routes.init_app(app)

# Iniciando o servidor web
if __name__ == '__main__':
    # Passando os dados e criando a conexão com o banco
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # Tentando a conexão com o banco
    try:
        with connection.cursor() as cursor:
            # Cria o banco se ele não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print("O banco de dados foi criado com sucesso!")
    except Exception as error:
        print(f"Erro ao criar o banco de dados: {error}")
    # Fechando a conexão
    finally:
        connection.close() 
    # Inicializar o SQLAlchemy    
    db.init_app(app=app)
    with app.test_request_context():
        # Criando as tabelas
        db.create_all()    
    # Inicia o servidor
    app.run(debug=True)  
    # Ligando o Modo de Depuração (reinicia automático)
