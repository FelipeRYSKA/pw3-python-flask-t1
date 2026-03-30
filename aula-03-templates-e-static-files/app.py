from flask import Flask, render_template
from controllers import routes

app = Flask(__name__, template_folder='views')

#enviando a variavel APP (flask) para as rota
routes.init_app(app)
    
if __name__ == '__main__':
    app.run(debug=True)