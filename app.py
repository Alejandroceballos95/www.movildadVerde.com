from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

#ruta para la pagina de inicio 
@app.route('/')
def home():
    return render_template('index.html')

#ruta para datos comparativos
@app.route('/datoscomparativos')
def datos_comparativos():
    return render_template('datoscomparativos.html')

#ruta para e-fuel
@app.route('/e-fuel')
def e_fuel():
    return render_template('e-fuel.html')

#ruta para electricos
@app.route('/electricos')
def electricos():
    return render_template('electricos.html')

#ruta para hibridos
@app.route('/hibridos')
def hibridos():
    return render_template('hibridos.html')

#ruta para archivos estáticos (sirve CSS, JS, imágenes si se acceden directamente)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)


