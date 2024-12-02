from flask import Flask, render_template, send_from_directory, request, jsonify
import json
import numpy as np
import matplotlib.pyplot as plt
import os

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

#ruta para opinion
@app.route('/opinion')
def opinion():
    return render_template('opinion.html')

#ruta para archivos estáticos (sirve CSS, JS, imágenes si se acceden directamente)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/guardar_experiencia', methods=['POST'])
def guardar_experiencia():
    """
    Ruta que maneja el formulario de experiencia del usuario. Recibe los datos enviados por el formulario,
    los guarda en un archivo JSON y genera un gráfico de barras con los resultados de las evaluaciones.
    """
    
    # Recoger los datos del formulario
    experiencia = {
        "vehiculo": request.form['vehiculo'],  # Tipo de vehículo evaluado
        "satisfaccion": int(request.form['satisfaccion']),  # Calificación de satisfacción general (1-5)
        "rendimiento": int(request.form['rendimiento']),  # Calificación de rendimiento (1-5)
        "ahorro": int(request.form['ahorro']),  # Calificación de ahorro (1-5)
        "usabilidad": int(request.form['usabilidad']),  # Calificación de usabilidad (1-5)
        "historia": request.form['historia']  # Breve historia con el producto
    }
    
    # Cargar los datos existentes en el archivo JSON
    # Si el archivo 'experiencias.json' existe, se cargan los datos ya guardados
    if os.path.exists('experiencias.json'):
        with open('experiencias.json', 'r') as f:
            experiencias = json.load(f)
    else:
        # Si no existe, inicializamos una lista vacía para almacenar las experiencias
        experiencias = []
    
    # Agregar la nueva experiencia a la lista de experiencias
    experiencias.append(experiencia)
    
    # Guardar los datos actualizados en el archivo JSON
    # Usamos 'a' para agregar al archivo sin sobrescribirlo
    with open('experiencias.json', 'a') as f:
        json.dump(experiencias, f, indent=4)

    # Llamar a la función para generar el gráfico con los nuevos datos
    generar_grafico(experiencias)

    # Renderizar la página 'opinion.html' para mostrar el resultado al usuario
    return render_template('opinion.html')


def generar_grafico(experiencias):
    """
    Función que genera un gráfico de barras con los datos de evaluación de los vehículos.
    Los datos son extraídos del archivo JSON y se crea un gráfico para cada categoría (Satisfacción, Rendimiento, Ahorro, Usabilidad).
    """
    
    # Inicializar las listas para contar las calificaciones de cada categoría (1-5)
    satisfaccion = [0] * 5
    rendimiento = [0] * 5
    ahorro = [0] * 5
    usabilidad = [0] * 5
    
    # Recorrer todas las experiencias para contabilizar las calificaciones
    for experiencia in experiencias:
        satisfaccion[experiencia['satisfaccion'] - 1] += 1
        rendimiento[experiencia['rendimiento'] - 1] += 1
        ahorro[experiencia['ahorro'] - 1] += 1
        usabilidad[experiencia['usabilidad'] - 1] += 1
    
    # Crear el gráfico de barras para las cuatro categorías
    categories = ['Satisfacción', 'Rendimiento', 'Ahorro', 'Usabilidad']
    data = [satisfaccion, rendimiento, ahorro, usabilidad]
    
    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura y un eje
    width = 0.2  # Ancho de las barras
    x = np.arange(5)  # Posiciones de las categorías (1 a 5)

    # Crear las barras para cada categoría
    for i, category in enumerate(categories):
        ax.bar(x + i * width, data[i], width, label=category)

    # Configurar etiquetas y leyenda
    ax.set_xlabel('Calificación (1-5)')  # Etiqueta del eje X
    ax.set_ylabel('Número de respuestas')  # Etiqueta del eje Y
    ax.set_title('Evaluación de vehículos')  # Título del gráfico
    ax.set_xticks(x + 1.5 * width)  # Posicionar las etiquetas del eje X
    ax.set_xticklabels([1, 2, 3, 4, 5])  # Etiquetas del eje X (1-5)
    ax.legend()  # Mostrar la leyenda para cada categoría

    # Guardar el gráfico generado como una imagen PNG en el directorio estático
    plt.savefig('static/images/grafico.png')

    # Retornar la ruta de la imagen para mostrarla en la página
    return jsonify({'grafico': 'static/images/grafico.png'})


if __name__ == '__main__':
    app.run(debug=True)