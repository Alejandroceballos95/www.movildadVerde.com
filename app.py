from flask import Flask, render_template, send_from_directory, request, jsonify
import json
import numpy as np
import matplotlib.pyplot as plt
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
@app.route('/guardar_experiencia', methods=['POST'])
def guardar_experiencia():
    """
    Recibe los datos enviados desde un formulario, los guarda en un archivo JSON y genera un gráfico
    de barras basado en las evaluaciones.

    Returns:
        str: HTML de la página opinion.html.
    """
    # Recoger los datos enviados por el formulario
    experiencia = {
        "vehiculo": request.form['vehiculo'],  # Tipo de vehículo evaluado
        "satisfaccion": int(request.form['satisfaccion']),  # Calificación de satisfacción (1-5)
        "rendimiento": int(request.form['rendimiento']),  # Calificación de rendimiento (1-5)
        "ahorro": int(request.form['ahorro']),  # Calificación de ahorro (1-5)
        "usabilidad": int(request.form['usabilidad']),  # Calificación de usabilidad (1-5)
        "historia": request.form['historia']  # Breve descripción de la experiencia
    }

    # Cargar experiencias existentes desde un archivo JSON, si existe
    if os.path.exists('experiencias.json'):
        with open('experiencias.json', 'r') as f:
            experiencias = json.load(f)
    else:
        experiencias = []  # Crear una lista vacía si el archivo no existe

    # Agregar la nueva experiencia a la lista
    experiencias.append(experiencia)

    # Guardar las experiencias actualizadas en el archivo JSON
    with open('experiencias.json', 'w') as f:
        json.dump(experiencias, f, indent=4)  # Sobrescribe el archivo con el nuevo contenido

    # Generar un gráfico basado en las nuevas experiencias
    generar_grafico(experiencias)

    # Renderizar la página de opiniones
    return render_template('opinion.html')

# Función auxiliar para generar gráficos a partir de las experiencias
def generar_grafico(experiencias):
    """
    Genera un gráfico de barras basado en las evaluaciones de satisfacción, rendimiento,
    ahorro y usabilidad de las experiencias guardadas.

    Args:
        experiencias (list): Lista de experiencias extraídas de un archivo JSON.
    """
    # Inicializar contadores para calificaciones de cada categoría (1-5)
    satisfaccion = [0] * 5
    rendimiento = [0] * 5
    ahorro = [0] * 5
    usabilidad = [0] * 5

    # Contar las calificaciones en cada categoría
    for experiencia in experiencias:
        satisfaccion[experiencia['satisfaccion'] - 1] += 1
        rendimiento[experiencia['rendimiento'] - 1] += 1
        ahorro[experiencia['ahorro'] - 1] += 1
        usabilidad[experiencia['usabilidad'] - 1] += 1

    # Configuración de categorías y datos
    categories = ['Satisfacción', 'Rendimiento', 'Ahorro', 'Usabilidad']
    data = [satisfaccion, rendimiento, ahorro, usabilidad]

    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(8, 6))  # Crear la figura y el eje
    width = 0.2  # Ancho de las barras
    x = np.arange(5)  # Posiciones de las barras (1 a 5)

    # Dibujar barras para cada categoría
    for i, category in enumerate(categories):
        ax.bar(x + i * width, data[i], width, label=category)

    # Etiquetas y título del gráfico
    ax.set_xlabel('Calificación (1-5)')
    ax.set_ylabel('Número de respuestas')
    ax.set_title('Evaluación de vehículos')
    ax.set_xticks(x + 1.5 * width)
    ax.set_xticklabels([1, 2, 3, 4, 5])
    ax.legend()

    # Guardar el gráfico como archivo PNG en el directorio estático
    plt.savefig('static/images/grafico.png')
    plt.close()  # Cierra la figura para liberar memoria

# Ejecutar la aplicación si el archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)