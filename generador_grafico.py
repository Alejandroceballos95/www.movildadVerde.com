import matplotlib.pyplot as plt
import pandas as pd

# Datos de crecimiento anual
data = {
    'Año': [2019, 2020, 2021, 2022],  # Años para los cuales se tiene el crecimiento interanual
    'Crecimiento (%)': [4.0, -2.1, 5.2, 3.4]  # Porcentaje de crecimiento de la demanda por año
}

# Crear DataFrame
df = pd.DataFrame(data)  # Crear un DataFrame de pandas con los datos proporcionados

# Crear gráfico de barras
plt.figure(figsize=(8, 5))  # Configurar el tamaño de la figura (ancho x alto)
plt.bar(
    df['Año'], 
    df['Crecimiento (%)'], 
    color=['green' if x > 0 else 'red' for x in df['Crecimiento (%)']]  # Colorear las barras: verde para positivo, rojo para negativo
)
plt.xlabel('Año')  # Etiqueta para el eje X
plt.ylabel('Crecimiento (%)')  # Etiqueta para el eje Y
plt.title('Cambio Interanual en la Demanda de Electricidad en Colombia (2019-2022)')  # Título del gráfico
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Añadir una rejilla en el eje Y con líneas punteadas y opacidad ajustada

# Añadir etiquetas de porcentaje en las barras
for index, value in enumerate(df['Crecimiento (%)']):
    # Añadir el porcentaje encima de cada barra
    plt.text(
        df['Año'][index],  # Coordenada X (posición de la barra)
        value + 0.2,  # Coordenada Y (ligeramente por encima del valor de la barra)
        f'{value}%',  # Texto a mostrar (porcentaje)
        ha='center'  # Centrar el texto horizontalmente
    )

# Guardar el gráfico en la carpeta static/images
output_path = './static/images/cambio_demanda_electricidad_colombia.png'  # Ruta de salida para guardar el gráfico
plt.savefig(output_path, dpi=300)  # Guardar el gráfico con una resolución de 300 DPI
print(f"Gráfico guardado en {output_path}")  # Confirmación en consola

# Mostrar el gráfico
plt.show()  # Renderizar el gráfico en la pantalla
