from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import os

app = Flask(__name__, template_folder='../views', static_folder='files')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#En esta clase almacenaremos los códigos postales
class PostalCode(db.Model):
    __tablename__ = "codigo_postal"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    cod_postal = db.Column(db.String, nullable=True)
    def __repr__(self):
        return f"PostalCode(cod_postal='{self.cod_postal}', lat='{self.lat}', lon='{self.lon}')"


@app.route('/')
def index():
    return render_template('cargar.html')
 
@app.route('/upload', methods=['POST'])
def leer():
   # df = pd.read_csv('data/postcodegeo.csv')
    #se lee el archivo, si no encuentra error
    if 'file' not in request.files:
        return 'No encuentra archivo'
    file = request.files['file']
    if file.filename == '':
        return 'No encuentra archivo'
    if file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(file)
            df2=df.copy()
            df2["cod_postal"] = np.nan
            # Validar que el archivo tenga las columnas necesarias
            if {'lat', 'lon'}.issubset(df.columns):
                df2.to_sql('codigo_postal', db.engine, if_exists='replace', index=False)
                df_html = df.to_html()
                return render_template('tabla.html', data_var = df_html)
            else:
                return 'el archivo no contiene latitud o longitud'
        except Exception as e:
            return f'Error: {e}'
    else:
        return 'El archivo no tiene extensión csv'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)