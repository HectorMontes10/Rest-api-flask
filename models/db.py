import pandas as pd

class DB:
    def __init__(self):

        self.allevents_pipe = None
        self.allusers_pipe = None
        self.category_pipe = None
        self.date2008_pipe = None
        self.listings_pipe = None
        self.sales_tab = None
        self.venue_pipe = None

    @staticmethod
    def map_to_bool(x):
            if x=='TRUE':
                return True
            if x=='FALSE':
                return False
            else:
                return pd.NA
    @staticmethod
    def map_to_int(x):
            if x==r'\N':
                return None
            else:
                return int(x)

    def load_tables(self):

        '''
        Esta función carga las diferentes tablas que conforman la base de datos a partir de los txt
        correspondientes, y asigna tipos de datos convenientes de acuerdo a lo referido en la documentación
        del dataset.
    
        '''

        #Cargamos tabla de eventos:

        self.allevents_pipe = pd.read_csv("database/allevents_pipe.txt",
                                           sep="|",
                                           header=None,
                                           names=['eventid','venueid','catid','dateid','eventname','starttime'],
                                           dtype = {
                                                'eventid':int,
                                                'venueid':int,
                                                'catid': int,
                                                'dateid': int,
                                                'eventname':str,
                                                'startime': str
                                                }
                                            )
        self.allevents_pipe['starttime']=[pd.Timestamp(x) for x in self.allevents_pipe['starttime']]
        
        #Cargamos tabla de usuarios:
        
        self.allusers_pipe = pd.read_csv("database/allusers_pipe.txt",
                                         sep="|",
                                         header=None,
                                         names = ['userid','username','firstname',
                                                  'lastname','city','state','email',
                                                  'phone','likesports','liketheatre',
                                                  'likeconcerts','likejazz',
                                                  'likeclassical','likeopera',
                                                  'likerock','likevegas','likebroadway',
                                                  'likemusicals'],
                                         dtype = { 
                                            'userid': int,
                                            'username': str,
                                            'firstname': str,
                                            'lastname': str,
                                            'city': str,
                                            'state': str,
                                            'email': str,
                                            'phone': str,
                                            'likesports': str,
                                            'liketheatre': str,
                                            'likeconcerts': str,
                                            'likejazz': str,
                                            'likeclassical': str,
                                            'likeopera': str,
                                            'likerock': str,
                                            'likevegas': str,
                                            'likebroadway': str,
                                            'likemusicals': str
                                            }
                                        )

        bool_columns = ['likesports','liketheatre','likeconcerts','likejazz',
                        'likeclassical','likeopera','likerock',
                        'likevegas','likebroadway',
                        'likemusicals']

        for col in bool_columns:
            self.allusers_pipe[col] = pd.array([self.map_to_bool(x) for x in self.allusers_pipe[col]],
                                        dtype="boolean")
        
        #Cargamos tabla de categorías:
        
        self.category_pipe = pd.read_csv("database/category_pipe.txt",
                                         sep="|",
                                         header = None,
                                         names = ['catid','catgroup','catname','catdesc'],
                                         dtype={
                                            'catid': int,
                                            'catgroup': str,
                                            'catname': str,
                                            'catdesc': str
                                            }
                                        )

        #Cargamos tabla de fechas:
         
        self.date2008_pipe = pd.read_csv("database/date2008_pipe.txt",
                                         sep="|",
                                         header=None,
                                         names = ['dateid','caldate','day','week',
                                                  'month','qtr','year','holiday'],
                                         dtype = {
                                            'dateid': int,
                                            'caldate': str,
                                            'day': str,
                                            'week': int,
                                            'month': str,
                                            'qtr': str,
                                            'year': int,
                                            'holiday': str
                                            }
                                        )

        self.date2008_pipe['holiday'] = pd.array([self.map_to_bool(x) for x in self.date2008_pipe['holiday']],
                                        dtype="boolean")

        #Cargamos la tabla de lista de tiquetes para cada evento

        listings_pipe = pd.read_csv("database/listings_pipe.txt",
                                    sep="|",
                                    header=None,
                                    names = ['listid','sellerid','eventid','dateid',
                                             'numtickets','priceperticket',
                                             'totalprice', 'listtime'],
                                    dtype = {
                                        'listid': int,
                                        'sellerid': int,
                                        'eventid': int,
                                        'dateid': int,
                                        'numtickets': int,
                                        'priceperticket': float,
                                        'totalprice': float,
                                        'listtime': str
                                        }
                                    )

        listings_pipe['listtime']=[pd.Timestamp(x) for x in listings_pipe['listtime']]

        #Cargamos la tabla de ventas

        self.sales_tab = pd.read_csv("database/sales_tab.txt",
                                     sep="\t",
                                     header = None,
                                     names = ['salesid', 'listid','sellerid',
                                              'buyerid','eventid','dateid','qtysold',
                                              'pricepaid','commission','saletime'],
                                     dtype = {
                                        'salesid': int,
                                        'listid': int,
                                        'sellerid': int,
                                        'buyerid': int,
                                        'eventid': int,
                                        'dateid': int,
                                        'qtysold': int,
                                        'pricepaid':float,
                                        'commission':float,
                                        'saletime': str
                                        }
                                    )

        self.sales_tab['saletime']=[pd.Timestamp(x) for x in self.sales_tab['saletime']]

        self.venue_pipe = pd.read_csv("database/venue_pipe.txt",
                                      sep="|",
                                      header = None,
                                      names = ['venueid','venuename',
                                               'venuecity','venuestate','venueseats'],
                                      dtype = {
                                        'venueid': int,
                                        'venuename': str,
                                        'venuecity': str,
                                        'venuestate': str,
                                        'venueseats': str
                                        }
                                )

        self.venue_pipe['venueseats'] = pd.array([self.map_to_int(x) for x in self.venue_pipe['venueseats']], dtype="Int64")
        