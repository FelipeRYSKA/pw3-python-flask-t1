# importado o sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#
#
db = SQLAlchemy()

#criando classe para representar a entidade Games no banco de dados (tabela: games)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(150))
    plataforma = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)

# método contrutor (atributos que serão utilizados pelos objetos)
def __init__(titulo, ano, categoria, plataforma, preco, quantidade):
    