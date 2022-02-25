import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator
import pickle

class DummyEstimator(BaseEstimator):

    '''
    Esta clase es especialmente útil cuando se quiera probar con estimadores diferentes a Gradient Boosting Tree
    pues permite la inyección de un estimador genérico al espacio de búsqueda del GridSearch.

    '''
    def fit(self): pass
    def score(self): pass

class TrainModel:

    def __init__(self,df_model, target_var, catname):

        self.df_model = df_model
        self.target_var = target_var
        self.catname = catname
        self.flag_model = True
        self.features = [x for x in df_model.columns if x not in ['catname','qtysold','pricepaid']]
        self.model = None
        self.X_test = None
        self.y_test = None
        self.r2 = None
        self.rmse = None
    
    def train_model(self):

        '''
        Con esta función estimamos un modelo de pronóstico para la variable objetivo, y para el conjunto
        de categorias de eventos pasadas por el usuario.

        El usuario puede suministrar o bien una única categoría de evento sobre la cual estimar el modelo
        (usando el input catname), o bien decidir ajustar un modelo global usando todas las categorias
        (catname="Todas")

        Como resultado se entrega el mejor estimador de un modelo Gradient Boosting Tree usando GridSearch
        y validación cruzada basada en RepeatKFold. Esta función también almacena valores predichos sobre un
        subconjunto de datos de prueba separados del data set original.
        
        '''
        
        flg_target = self.target_var in ['qtysold','pricepaid']

        if ((self.catname == "Todas") and flg_target):
            X_matrix = self.df_model[self.features]
            y_matrix = self.df_model[[self.target_var]]
        elif ((self.catname in ['Musicals','Opera','Plays','Pop']) and flg_target):
            X_matrix = self.df_model[self.features][self.df_model['catname']==self.catname]
            y_matrix = self.df_model[[self.target_var]][self.df_model['catname']==self.catname]
        else:
            self.flag_model = False
        
        if self.flag_model:

            #Partimos el set de datos en un conjunto de prueba y otro de entrenamiento
            
            X_train, self.X_test, y_train, self.y_test = train_test_split(
                                                    X_matrix,
                                                    y_matrix,
                                                    random_state = 123
                                                )
            
            #Con el fin de tunear los hiperparámetros del modelo usamos GridSearch sobre un diccionario de
            #opciones para cada parámetro relevante:

            search_space = [{'clf': [GradientBoostingRegressor()],
                    'clf__n_estimators': [10,15,20,25],
                    'clf__loss': ['squared_error'],
                    'clf__learning_rate': [0.05,0.1,0.15,0.20],
                    'clf__random_state' : [123],
                    'clf__max_depth': [2,3,5,10]
                    }
                   ]

            pipeline = Pipeline([
             ('clf', DummyEstimator())])

            cv = GridSearchCV(pipeline,
                             param_grid=search_space, 
                             n_jobs=-1,
                             cv = RepeatedKFold(n_splits=3, n_repeats=1, random_state=123),
                             refit = True
                             )

            #Predecimos sobre los datos de prueba con el mejor modelo arrojado por GridSearch

            cv.fit(X_train, y_train.values.ravel())
            
            self.model = cv.best_estimator_
            self.compute_metrics()
            
            dict_model = {
                'catname': self.catname,
                'best_model': self.model,
                'target_var': self.target_var,
                'list_var': X_train.columns,
                'rmse': self.rmse,
                'r2': self.r2
            }

            #Usamos pickel para serializar un objeto que contenga el modelo y las condiciones bajo las cuales
            #fue generado

            pickle.dump(dict_model, open('./trained_models/regressor_'+self.catname+"_"+self.target_var+'.pkl', 'wb'))
            
    def compute_metrics(self):

        '''
        Con esta función computamos las métricas rmse y r2 para el mejor modelo estimado resultante del
        tuneo de hiperparámetros usando GridSearch y validación cruzada RepeatedKfold

        Si el ajuste del modelo no es posible porque el usuario no entregó categoría de evento válida se imprime
        un valor en consola indicando la situación.

        '''
        
        if self.flag_model:
            
            predicciones = self.model.predict(X = self.X_test)
            
            rmse = mean_squared_error(
            y_true  = self.y_test,
            y_pred  = predicciones,
            squared = False
            )

            r2 = r2_score(
                y_true  = self.y_test,
                y_pred  = predicciones 
            )
            
            self.rmse = rmse
            self.r2 = r2
            
            print(f"El error (rmse) de test es: {self.rmse} y el r2 es: {self.r2}")

        else:
            print("No hay métricas disponibles")
