from flask import Flask, render_template, send_from_directory, request, jsonify
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Ruta principal que renderiza la página de inicio
@app.route('/')
def home():
    """
    Renderiza la página principal del sitio web.
    Returns:
        str: HTML de la página index.html.
    """
    return render_template('index.html')

# Ruta para renderizar la página de datos comparativos
@app.route('/datoscomparativos')
def datos_comparativos():
    """
    Renderiza la página de datos comparativos.
    Returns:
        str: HTML de la página datoscomparativos.html.
    """
    return render_template('datoscomparativos.html')

# Ruta para renderizar la página sobre e-fuel
@app.route('/e-fuel')
def e_fuel():
    """
    Renderiza la página de información sobre e-fuel.
    Returns:
        str: HTML de la página e-fuel.html.
    """
    return render_template('e-fuel.html')

# Ruta para renderizar la página de vehículos eléctricos
@app.route('/electricos')
def electricos():
    """
    Renderiza la página de información sobre vehículos eléctricos.
    Returns:
        str: HTML de la página electricos.html.
    """
    return render_template('electricos.html')

# Ruta para renderizar la página de vehículos híbridos
@app.route('/hibridos')
def hibridos():
    """
    Renderiza la página de información sobre vehículos híbridos.
    Returns:
        str: HTML de la página hibridos.html.
    """
    return render_template('hibridos.html')

# Ruta para renderizar la página de opiniones
@app.route('/opinion')
def opinion():
    """
    Renderiza la página de opiniones de usuarios.
    Returns:
        str: HTML de la página opinion.html.
    """
    return render_template('opinion.html')

# Ruta para servir archivos estáticos como CSS, JavaScript o imágenes
@app.route('/static/<path:path>')
def static_files(path):
    """
    Sirve archivos estáticos desde el directorio 'static'.

    Args:
        path (str): Ruta relativa al archivo estático solicitado.

    Returns:
        Response: Archivo estático solicitado.
    """
    return send_from_directory('static', path)

# Ruta para guardar experiencias enviadas por los usuarios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directorio base de la aplicación
JSON_FILE_PATH = os.path.join(BASE_DIR, 'experiencias.json')

@app.route('/guardar_experiencia', methods=['POST'])
def guardar_experiencia():
    experiencia = {
        "vehiculo": request.form['vehiculo'],
        "satisfaccion": int(request.form['satisfaccion']),
        "rendimiento": int(request.form['rendimiento']),
        "ahorro": int(request.form['ahorro']),
        "usabilidad": int(request.form['usabilidad']),
        "historia": request.form['historia']
    }

    # Cargar datos existentes en el archivo JSON
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as f:
            experiencias = json.load(f)
    else:
        experiencias = []

    # Agregar la nueva experiencia
    experiencias.append(experiencia)

    # Guardar datos actualizados
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(experiencias, f, indent=4)

    # Generar gráfico con los nuevos datos
    generar_grafico(experiencias)

    return render_template('opinion.html')

# Función auxiliar para generar gráficos a partir de las experiencias
def generar_grafico(experiencias):
    """
    Genera gráficos de barras independientes para satisfacción, rendimiento, ahorro y usabilidad.
    
    Args:
        experiencias (list): Lista de experiencias extraídas de un archivo JSON.
    """
    # Inicializar contadores de calificaciones (1-5) para cada categoría
    categorias = {
        "Satisfacción": [0] * 5,
        "Rendimiento": [0] * 5,
        "Ahorro": [0] * 5,
        "Usabilidad": [0] *5
    }

    # Contar las calificaciones en cada categoría
    for experiencia in experiencias:
        categorias["Satisfacción"][experiencia['satisfaccion'] - 1] += 1
        categorias["Rendimiento"][experiencia['rendimiento'] - 1] += 1
        categorias["Ahorro"][experiencia['ahorro'] - 1] += 1
        categorias["Usabilidad"][experiencia['usabilidad'] - 1] += 1

    # Ruta base para guardar gráficos
    graph_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)  # Crear la carpeta si no existe

    # Generar gráficos independientes
    for categoria, datos in categorias.items():
        fig, ax = plt.subplots(figsize=(8, 6))  # Crear figura para cada gráfico
        x = np.arange(1, 6)  # Calificaciones de 1 a 5

        # Crear gráfico de barras
        ax.bar(x, datos, color='skyblue', edgecolor='black')

        # Etiquetas y título del gráfico
        ax.set_title(f'Evaluación de {categoria}')
        ax.set_xlabel('Calificación (1-5)')
        ax.set_ylabel('Número de respuestas')
        ax.set_xticks(x)
        ax.set_xticklabels([1, 2, 3, 4, 5])

        # Guardar el gráfico en un archivo PNG
        graph_path = os.path.join(graph_dir, f'{categoria.lower()}.png')
        plt.savefig(graph_path)
        plt.close()  # Cerrar la figura para liberar memoria

# Ejecutar la aplicación si el archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)