from flask import request
from flask_restful import Resource
from http import HTTPStatus

from mysql_connection import get_connection
from mysql.connector.errors import Error

from flask_jwt_extended import jwt_required, get_jwt_identity

import pandas as pd

class MovieSearchResource(Resource):
    
    def get(self):
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        keyword = request.args.get('keyword')
       
        try :
            connection = get_connection()

            query = '''select title,release_year,urls,poster,provider
                        from movie
                        where title like %s
                        limit '''+offset+','+limit+''';'''
            
            trans_keyword = '%'+keyword+'%'
            
            param = (trans_keyword,)
            
            
            cursor = connection.cursor(dictionary = True)
            
            cursor.execute(query,param)
            
            # select 문은 아래 내용이 필요하다.
            record_list = cursor.fetchall()
            print(record_list)
            
            ### 중요. 파이썬의 시간을, JSON으로 보내기 위해서
            ### 문자열로 바꿔준다.
            i = 0
            for record in record_list :
                record_list[i]['release_year'] = str(record['release_year'])
                i = i+1
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
    
    
class AddFavoriteResource(Resource):
    @jwt_required()
    def post(self,movie_id):
        
        user_id = get_jwt_identity()
        
        try:
            # 1. db에 연결
            connection = get_connection()
            
            # 2. 쿼리문 만들고
            query = '''insert into select
                        (user_id,movie_id)
                        values
                        (%s,%s);'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는
            # 콤마를 꼭 써준다
            record = (user_id,movie_id)
            # 3. 커넥션으로부터 커서를 가져온다            
            cursor = connection.cursor()
            
            # 4. 쿼리문을 커서에 넣어서 실행한다.
            cursor.execute(query,record)
            
            # 5. 커넥션을 커밋한다.=> 디비에 영구정으로 반영하라는 뜻
            connection.commit()
        except Error as e :
            print('Error',e)
            return {'error':'이미 이 영화는 즐겨찾기 했습니다.'},HTTPStatus.BAD_REQUEST
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
        
        return {'result':'추가 완료'}
    
class DeleteFavoriteResource(Resource):
    @jwt_required
    def delete(self,movie_id):
        
        user_id = get_jwt_identity()
        
        try:
            # 1. db에 연결
            connection = get_connection()
            
            # 2. 쿼리문 만들고
            query = '''delete from select
                        where movie_id = %s and user_id = %s;'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는
            # 콤마를 꼭 써준다
            record = (movie_id,user_id)
            # 3. 커넥션으로부터 커서를 가져온다            
            cursor = connection.cursor()
            
            # 4. 쿼리문을 커서에 넣어서 실행한다.
            cursor.execute(query,record)
            
            # 5. 커넥션을 커밋한다.=> 디비에 영구정으로 반영하라는 뜻
            connection.commit()
        except Error as e :
            print('Error',e)
            return {'error':str(e)},HTTPStatus.BAD_REQUEST
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
        return {'result':'삭제.'},HTTPStatus.OK
    
    
