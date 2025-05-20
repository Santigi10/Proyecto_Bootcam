from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io 
import base64 # Para codificar la imagen en base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre_nosotros')#Se enlaza la ruta con la plantilla HTML 
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/Energia_eolica')
def energia_eolica():
    return render_template('Energia_eolica.html')

@app.route('/Energia_hidroelectrica')
def energia_hidroelectrica():
    return render_template('Energia_hidroelectrica.html')

@app.route('/Energia_solar')
def energia_solar():
    return render_template('Energia_solar.html')

@app.route('/energias')
def energias():
    return render_template('energias.html')

@app.route('/impacto')
def impacto():
    return render_template('impacto.html')

def grafico_barras():
    try:
        # Leer datos de los archivos CSV
        df_wind = pd.read_csv('08 wind-generation.csv')
        df_hydro = pd.read_csv('05 hydropower-consumption.csv')
        df_solar = pd.read_csv('12 solar-energy-consumption.csv')
        df_biofuel = pd.read_csv('16 biofuel-production.csv')
    except FileNotFoundError as e:
        return f"Error: {e}"

    # Filtrar datos para Colombia
    dfColombia_wind = df_wind[df_wind['Entity'] == 'Colombia']
    dfColombia_hydro = df_hydro[df_hydro['Entity'] == 'Colombia']
    dfColombia_solar = df_solar[df_solar['Entity'] == 'Colombia']
    dfColombia_biofuel = df_biofuel[df_biofuel['Entity'] == 'Colombia']

    # Gráfico de barras
    fuentes = ['Wind', 'Hydro', 'Solar', 'Biofuel']
    produccion = [
        dfColombia_wind.select_dtypes(include='number').sum().iloc[1],
        dfColombia_hydro.select_dtypes(include='number').sum().iloc[1],
        dfColombia_solar.select_dtypes(include='number').sum().iloc[1],
        dfColombia_biofuel.select_dtypes(include='number').sum().iloc[1]
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(fuentes, produccion, color=['blue', 'green', 'yellow', 'brown'])
    plt.title('Producción de Energía Renovable en Colombia por Fuente')
    plt.xlabel('Fuente de Energía')
    plt.ylabel('Producción (GWh)')
    plt.grid(axis='y')
    plt.xticks(rotation=45)  # Rotar etiquetas del eje x
    plt.tight_layout() # Ajustar el diseño

    # Guardar la figura en un buffer
    buf = io.BytesIO() # Guardar la figura en un buffer o sea en memoria
    plt.savefig(buf, format='png')
    buf.seek(0) # Mover el cursor al inicio del buffer o sea al principio
    imagen = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return imagen

@app.route('/grafico', methods=['POST'])
def grafico():
    if request.method == 'POST':
        imagen = grafico_barras()
        return render_template('index.html', imagen=imagen)
    return render_template('index.html')

def grafico_torta():
    try:
        # Leer datos de los archivos CSV
        df_wind = pd.read_csv('08 wind-generation.csv')
        df_hydro = pd.read_csv('05 hydropower-consumption.csv')
        df_solar = pd.read_csv('12 solar-energy-consumption.csv')
        df_biofuel = pd.read_csv('16 biofuel-production.csv')
    except FileNotFoundError as e:
        return f"Error: {e}"

    # Filtrar datos para Colombia
    dfColombia_wind = df_wind[df_wind['Entity'] == 'Colombia']
    dfColombia_hydro = df_hydro[df_hydro['Entity'] == 'Colombia']
    dfColombia_solar = df_solar[df_solar['Entity'] == 'Colombia']
    dfColombia_biofuel = df_biofuel[df_biofuel['Entity'] == 'Colombia']

    # Gráfico de torta
    fuentes = ['Wind', 'Hydro', 'Solar', 'Biofuel']
    produccion = [
        dfColombia_wind.select_dtypes(include='number').sum().iloc[1],
        dfColombia_hydro.select_dtypes(include='number').sum().iloc[1],
        dfColombia_solar.select_dtypes(include='number').sum().iloc[1],
        dfColombia_biofuel.select_dtypes(include='number').sum().iloc[1]
    ]

    Produccion_otros = [produccion[1], (produccion[0] + produccion[2] + produccion[3])]
    plt.figure(figsize=(8, 8))
    plt.pie(Produccion_otros, labels=['Hidroeléctrica', 'Otras Fuentes - Solar, Viento, Biomasa'], autopct='%1.1f%%', startangle=140,
            colors=['blue', 'green'], shadow=True)
    plt.title('Participación de Energías Renovables en Colombia')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Guardar la figura en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imagen = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return imagen

@app.route('/grafico_torta', methods=['POST'])
def grafico_torta_route():
    if request.method == 'POST':
        imagen = grafico_torta()
        return render_template('energia_solar.html', imagen=imagen)
    return render_template('index.html')

@app.route('/energia_hidroelectrica', methods=['POST'])
def Diagrama_de_area():
    file_path_wind = '08 wind-generation.csv'
    df = pd.read_csv(file_path_wind)

    Grupos_wind = df.groupby('Entity')
    Year_wind = df.groupby('Year')
    dfColombia_wind = Grupos_wind.get_group('Colombia')

    file_path_hydro = '05 hydropower-consumption.csv'
    cf = pd.read_csv(file_path_hydro)

    Grupos_hydro = cf.groupby('Entity')
    Year_hydro = cf.groupby('Year')
    dfColombia_hydro = Grupos_hydro.get_group('Colombia')

    file_path_solar = '12 solar-energy-consumption.csv'
    sf = pd.read_csv(file_path_solar)
    Grupos_solar = sf.groupby('Entity')
    Year_solar = sf.groupby('Year')
    dfColombia_solar = Grupos_solar.get_group('Colombia')

    file_path_biofuel = '16 biofuel-production.csv'
    bf = pd.read_csv(file_path_biofuel)

    Grupos_biofuel = bf.groupby('Entity')
    Year_biofuel = bf.groupby('Year')
    dfColombia_biofuel = Grupos_biofuel.get_group('Colombia')

    fuentes = ['Wind', 'Hydro', 'Solar', 'Biofuel']
    produccion = [
        dfColombia_wind.select_dtypes(include='number').sum().iloc[1],
        dfColombia_hydro.select_dtypes(include='number').sum().iloc[1],
        dfColombia_solar.select_dtypes(include='number').sum().iloc[1],
        dfColombia_biofuel.select_dtypes(include='number').sum().iloc[1]
    ]
#Diagrama de area sobre cada energia en el tiempo
    plt.figure(figsize=(10, 6))
    plt.fill_between(dfColombia_wind['Year'], dfColombia_wind.select_dtypes(include='number').sum().iloc[1], color='blue', alpha=0.5, label='Wind')
    plt.fill_between(dfColombia_hydro['Year'], dfColombia_hydro.select_dtypes(include='number').sum().iloc[1], color='green', alpha=0.5, label='Hydro')
    plt.fill_between(dfColombia_solar['Year'], dfColombia_solar.select_dtypes(include='number').sum().iloc[1], color='yellow', alpha=0.5, label='Solar')
    plt.fill_between(dfColombia_biofuel['Year'], dfColombia_biofuel.select_dtypes(include='number').sum().iloc[1], color='brown', alpha=0.5, label='Biofuel')
    plt.title('Producción de Energía Renovable en Colombia por Fuente a lo largo del Tiempo')
    plt.xlabel('Año')
    plt.ylabel('Producción (GWh)')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Guardar la figura en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imagen = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return imagen

@app.route('/diagrama_area', methods=['POST'])
def diagrama_area_route():
    if request.method == 'POST':
        imagen = Diagrama_de_area()
        return render_template('energia_hidroelectrica.html', imagen=imagen)
    return render_template('index.html')

@app.route('/energia_eolica', methods=['POST'])
def grafico_lineas():
    try:
        # Leer datos de los archivos CSV
        df_wind = pd.read_csv('08 wind-generation.csv')
        df_hydro = pd.read_csv('05 hydropower-consumption.csv')
        df_solar = pd.read_csv('12 solar-energy-consumption.csv')
        df_biofuel = pd.read_csv('16 biofuel-production.csv')
    except FileNotFoundError as e:
        return f"Error: {e}"

    # Filtrar datos para Colombia
    dfColombia_wind = df_wind[df_wind['Entity'] == 'Colombia']
    dfColombia_hydro = df_hydro[df_hydro['Entity'] == 'Colombia']
    dfColombia_solar = df_solar[df_solar['Entity'] == 'Colombia']
    dfColombia_biofuel = df_biofuel[df_biofuel['Entity'] == 'Colombia']

    # Gráfico de barras
    fuentes = ['Wind', 'Hydro', 'Solar', 'Biofuel']
    produccion = [
        dfColombia_wind.select_dtypes(include='number').sum().iloc[1],
        dfColombia_hydro.select_dtypes(include='number').sum().iloc[1],
        dfColombia_solar.select_dtypes(include='number').sum().iloc[1],
        dfColombia_biofuel.select_dtypes(include='number').sum().iloc[1]
    ]
    # Gráfico de líneas
    plt.figure(figsize=(10, 6))
    # Se asume que los años están en la columna 'Year' y que la suma de las columnas numéricas por fila es produccion anual
    plt.plot(dfColombia_wind['Year'], dfColombia_wind.select_dtypes(include='number').sum(axis=1), color='blue', label='Eólica', alpha=0.7)
    plt.plot(dfColombia_hydro['Year'], dfColombia_hydro.select_dtypes(include='number').sum(axis=1), color='green', label='Hidráulica', alpha=0.7)
    plt.plot(dfColombia_solar['Year'], dfColombia_solar.select_dtypes(include='number').sum(axis=1), color='gold', label='Solar', alpha=0.7)
    plt.plot(dfColombia_biofuel['Year'], dfColombia_biofuel.select_dtypes(include='number').sum(axis=1), color='brown', label='Biocombustibles', alpha=0.7)
    plt.title('Tendencia en la Capacidad Instalada de Energías Renovables en Colombia', fontsize=16)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Capacidad Instalada (MW)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64
@app.route('/grafico_lineas', methods=['POST'])

def grafico_lineas_route():
    if request.method == 'POST':
        imagen = grafico_lineas()
        return render_template('energia_eolica.html', imagen=imagen)
    return render_template('index.html')


@app.route("/contacto", methods=["GET", "POST"])
def calcular():
    # Tu lógica aquí
    porcentaje = None
    if request.method == "POST":
        try:
            total = float(request.form["consumo_total"])
            renovable = float(request.form["consumo_renovable"])
            if total == 0:
                porcentaje = "El consumo total no puede ser cero."
            else:
                porcentaje = round((renovable / total) * 100, 2)
        except:
            porcentaje = "Error al procesar los datos."
    return render_template("contacto.html", porcentaje=porcentaje)



if __name__ == '__main__':
    app.run(debug=True) # Cambia a False en producción
# Para ejecutar la aplicación, guarda este archivo como app.py y ejecuta el siguiente comando en la terminal:
# python app.py
