import pickle
import pandas as pd

class Predict:
    def __init__(self,path_to_model):

        self.path = path_to_model,
        self.X_to_predict = None,
        self.forecast = None,
        self.rmse = None,
        self.r2 = None
    
    def read_obj_model(self): 

        infile = open(self.path[0],'rb')
        obj = pickle.load(infile)
        infile.close()
        
        model = obj['best_model']
        features = obj['list_var']
        self.rmse = obj['rmse']
        self.r2 = obj['r2']

        self.X_to_predict = pd.DataFrame({
            'dateid_x': [2191,2192,2193,2194,2195,2196,2197],
            'MO': [0,0,0,0,1,0,0],
            'SA': [0,0,1,0,0,0,0],
            'SU': [0,0,0,1,0,0,0],
            'TH': [1,0,0,0,0,0,0],
            'TU': [0,0,0,0,0,1,0],
            'WE': [0,0,0,0,0,0,1],
            'FR': [0,1,0,0,0,0,0],
            'JAN':[1,1,1,1,1,1,1],
            'FEB':[0,0,0,0,0,0,0],
            'MAR':[0,0,0,0,0,0,0],
            'APR':[0,0,0,0,0,0,0],
            'MAY':[0,0,0,0,0,0,0],
            'JUN':[0,0,0,0,0,0,0],
            'JUL':[0,0,0,0,0,0,0],
            'AUG':[0,0,0,0,0,0,0],
            'SEP':[0,0,0,0,0,0,0],
            'OCT':[0,0,0,0,0,0,0],
            'NOV':[0,0,0,0,0,0,0],
            'DEC':[0,0,0,0,0,0,0],
            'week': [1,1,2,2,2,2,2]})
        
        self.X_to_predict = self.X_to_predict[features]
        self.forecast = model.predict(self.X_to_predict)