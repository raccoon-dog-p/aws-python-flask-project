import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from msilib.schema import Class
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql_connection import get_connection
from mysql.connector.errors import Error

import pandas as pd

class HomePosterResource(Resource):
    def get(self):
        
        genre = request.args.get("genre")
        providers = request.args.get("providers")
        

        try :
            connection = get_connection()

            query = '''select id,poster from movie_2
                    where genre_ids like %s and provider not like %s
                    limit 7;'''
            
            trans_genre = "%" + genre + "%"
            trans_providers = "%" + providers + "%"                            
    
            param = (trans_genre,trans_providers)
            
            
            cursor = connection.cursor(dictionary = True)
            
            cursor.execute(query,param)
            
            # select 문은 아래 내용이 필요하다.
            record_list = cursor.fetchall()
            print(record_list)
            

        except Error as e  : 
            print('Error while connecting to MySQL',e)
            return {'error':str(e)},HTTPStatus.BAD_REQUEST
        finally :
            cursor.close()
            if connection.is_connected():
                connection.close()
                print('MySQL connection is closed')
            else:
                print('connection does not exist')
            
        return {'count':len(record_list), 'result':record_list}