from flask import Flask
import pandas as pd
from models.db import DB
from modules.construct_dataset import ConstructDataSet
from modules.train_model import TrainModel
from modules.predict import Predict
import os
import json
from modules.encoder import NumpyEncoder

app = Flask(__name__)

@app.route('/targets-var/<target>/categories/<categories>')
def index(target, categories):

    flg_valid_model = ((categories in ['Musicals','Opera','Plays','Pop','Todas']) and 
                        (target in ['qtysold','pricepaid']))

    if flg_valid_model:

        path_to_model = './trained_models/regressor_'+categories+'_'+target+'.pkl'
        flg_model = os.path.exists(path_to_model)
    
        if not flg_model:

            print("Creando modelo de pronóstico...")

            #Cargamos la base de datos:

            database = DB()
            database.load_tables()

            #Formateamos la información para construir un dataset conveniente para labores de pronóstico

            df_model = ConstructDataSet(database).generate()

            #Entrenamos un modelo GBT para pronosticar las cantidades vendidas y el total facturado, tanto general como por
            #categoría de producto.

            #Probando para cantidades vendidas y todas las categorías de eventos:

            model_1 = TrainModel(df_model,target,categories)
            model_1.train_model()
            
            print("Fin de la creación del modelo\n")
            
        print("Pronosticando con el modelo...\n")
            
        forecast_obj = Predict(path_to_model)
        forecast_obj.read_obj_model()

        print("Estos son los resultados del pronostico:\n")
        print(forecast_obj.forecast)

        data = {
        'status': True,
        'msg': "Los parámetros suministrados no son válidos",
        'list_features': forecast_obj.X_to_predict.columns.tolist(),
        'target_var': target,
        'categories': categories,
        'forecasts': forecast_obj.forecast,
        'rmse': forecast_obj.rmse,
        'r2': forecast_obj.r2
        }

    else:
        print("Los parámetros suministrados no son válidos")
        data = {
            'status': False,
            'msg': "Los parámetros suministrados no son válidos",
            'list_features': [],
            'target_var': target,
            'categories': categories,
            'forecasts': [],
            'rmse': None,
            'r2': None
        }
    response = json.dumps(data,cls=NumpyEncoder,ensure_ascii=False).encode('utf-8')
    
    return response
    
def create_app():
    return app

#if __name__ == '__main__': app.run(debug=True)