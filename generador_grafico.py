import matplotlib.pyplot as plt
import pandas as pd

# Datos de crecimiento anual
data = {
    'Año': [2019, 2020, 2021, 2022],
    'Crecimiento (%)': [4.0, -2.1, 5.2, 3.4]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Crear gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(df['Año'], df['Crecimiento (%)'], color=['green' if x > 0 else 'red' for x in df['Crecimiento (%)']])
plt.xlabel('Año')
plt.ylabel('Crecimiento (%)')
plt.title('Cambio Interanual en la Demanda de Electricidad en Colombia (2019-2022)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Añadir etiquetas de porcentaje en las barras
for index, value in enumerate(df['Crecimiento (%)']):
    plt.text(df['Año'][index], value + 0.2, f'{value}%', ha='center')

# Guardar el gráfico en la carpeta static/images
output_path = './static/images/cambio_demanda_electricidad_colombia.png'
plt.savefig(output_path, dpi=300)
print(f"Gráfico guardado en {output_path}")

# Mostrar el gráfico
plt.show()
