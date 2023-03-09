from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from ratelimit import limits, sleep_and_retry

app = Flask(__name__, template_folder='../views', static_folder='files')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# se limita a 1 solicitud por segundo
@sleep_and_retry
@limits(calls=1, period=1) 
def get_postcode(lat, lon):
    # solicitud al API de postcodes.io para obtener información del código postal más cercano
    r = requests.get(f'https://api.postcodes.io/postcodes?lat={lat}&lon={lon}', verify=False)
    if r.status_code == 200:
        json_data = r.json()
        if json_data['result'] != None:
            return str(json_data['result'][0]['postcode'])
        else:
            return "no hay codigo postal"
    else: 
        return "error al hacer la solicitud al api"

@app.route('/')
def index():
    #se obtienen los datos almacenados en la tabla 
    df = pd.read_sql('SELECT lat, lon FROM codigo_postal', db.engine)
    df_html = df.to_html()
    return render_template('tabla_inicial.html',data_var=df_html)

@app.route('/save', methods=['GET'])
def guardar():
    df = pd.read_sql('SELECT * FROM codigo_postal', db.engine)
    result = []
    #se itera sobre cada fila del DataFrame y se hace una solicitud al API de postcodes.io para obtener el codigo postal
    for index, row in df.iterrows():
        lat = row['lat']
        lon = row['lon']
        try:
            result.append(get_postcode(lat, lon))
        except Exception as e:
            result.append(str(e))


   # Actualizar la base de datos con los códigos postales obtenidos
    for postal_code_cercano in result:
        db.session.execute(f"UPDATE codigo_postal SET cod_postal='{str(postal_code_cercano)}'")

    db.session.commit()
    dff = pd.read_sql('SELECT * FROM codigo_postal', db.engine)
    dff_html = dff.to_html()
    return render_template('tabla_final.html',data_var=dff_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
