import pandas as pd
class ConstructDataSet:

    def __init__(self,db):

        self.ventas = db.sales_tab
        self.dias = db.date2008_pipe
        self.categorias = db.category_pipe
        self.eventos = db.allevents_pipe

    def generate(self):

        '''

        Esta función genera un data frame formateado para ser usado en un modelo de predicción. El dataframe
        contiene las cantidades totales vendidas por cada día del año y cada categoría de evento. Esto con el
        fin de ofrecer pronósticos a nivel de días pero tambien a nivel de días-tipo_evento.       
        
        '''

        #Hacemos join de tablas para tener la información completa en un único dataset
        
        ventas_dias = pd.merge(self.ventas, self.dias, on = 'dateid')
        ventas_dias_eventos = pd.merge(ventas_dias, self.eventos, on = "eventid")
        ventas_dias_eventos_categorias = pd.merge(ventas_dias_eventos, self.categorias, on = "catid")
        ventas_dias_eventos_categorias.sort_values(by=['saletime'],inplace=True)

        #Como se desean predicciones a nivel de día totalizamos para cada día en el año tanto el precio cobrado
        #como la cantidad total vendida. Sin embargo conservamos subtotales por cada categoría de evento para
        #ofrecer pronosticos individuales para cada tipo de evento.

        data_for_model = ventas_dias_eventos_categorias[['dateid_x','catname','qtysold',
                                                         'pricepaid','day','month','week']]
        
        #Defino el diccionario de agregaciones que deseo realizar
        aggregations = {
            'qtysold':'sum',
            'pricepaid': 'sum',
            'day': 'max',
            'month': 'max',
            'week' : 'max'
        }

        df_summary = data_for_model.groupby(by=['dateid_x','catname']).agg(aggregations).sort_values(by=['dateid_x'])
        df_summary = df_summary.reset_index()
        
        #Creamos variables dummies para los features categóricos y las agregamos al dataframe original
        
        dummies_for_day = pd.get_dummies(df_summary['day'],drop_first=True)
        dummies_for_month = pd.get_dummies(df_summary['month'],drop_first=True)
        df_summary_full = pd.concat([df_summary[['dateid_x','catname','qtysold','pricepaid','week']],
                                            dummies_for_day,dummies_for_month],axis=1)
        
        return df_summary_full
