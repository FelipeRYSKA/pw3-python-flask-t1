from flask import Flask, render_template

app = Flask(__name__, template_folder='views')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/killers')
def kill():
    return render_template('killers.html')

@app.route('/survivors')
def surv():
    return render_template('survivors.html')

@app.route('/formulario')
def form():
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)