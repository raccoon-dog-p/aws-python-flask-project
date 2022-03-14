from flask import request
from flask_restful import Resource
from http import HTTPStatus
# res 폴더 안에 있기 때문에 import시 상위 부모경로를 못 찾기 때문에 sys.path에 "." 추가
import sys
sys.path.append(".")
from config import Config
from mysql_connection import get_connection
from mysql.connector.errors import Error

from flask_jwt_extended import jwt_required, get_jwt_identity

import pandas as pd
import boto3
import io
import time 


# boto 연동 코드
# start = time.time()
# s3_client = boto3.client(service_name="s3",
#                          aws_access_key_id=Config.S3_KEY,
#                          aws_secret_access_key=Config.S3_SECRET)

# obj = s3_client.get_object(Bucket=Config.S3_BUCKET, Key="new_cosine_sim.csv")
# new_cosine_sim = pd.read_csv(io.BytesIO(obj["Body"].read()),index_col=0)
# end = time.time()
# print(f"{end - start} sec") 

## rec 함수

## to-do titles => Db안에 Movie_id로 대체

new_cosine_sim=pd.read_csv("C:\\new_cosine_sim.csv")

def movie_REC(movie_id, cosine_sim=new_cosine_sim):
    rating = {}
    m_id_list=[]
    #입력한 영화들로 부터 인덱스 가져오기
    for m_id in movie_id:
      m_id_list.append(m_id)
      # 모든 영화에 대해서 해당 영화와의 유사도를 구하기
      sim_scores = list(enumerate(new_cosine_sim.iloc[m_id]))

      # 유사도에 따라 영화들을 정렬
      sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse = True)
      
      # 가장 유사한 100개의 영화를 받아옴
      sim_scores = sim_scores[1:101]

      for i in range(100):
        id = sim_scores[i][0]
        score = sim_scores[i][1] 
        if id not in rating.keys():
          rating[id] = score
        else:
          rating[id]= rating[id]+score
      for m_id in m_id_list:
        if m_id in rating.keys():
          del rating[m_id]
      
    return sorted(rating.items(), key=lambda x: x[1], reverse=True)[:100]



class MovieRecommandResource(Resource):
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()
        try:
            # 1. db에 연결
            connection = get_connection()
            
            # 2. 쿼리문 만들고
            query = '''select movie_id from favorite
                    where user_id = %s;'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는
            # 콤마를 꼭 써준다
            record = (user_id,)
            # 3. 커넥션으로부터 커서를 가져온다            
            cursor = connection.cursor()
            
            # 4. 쿼리문을 커서에 넣어서 실행한다.
            cursor.execute(query,record)
            
            record_list = cursor.fetchall()
            movie_id=[]
            for i in range(len(record_list)):
                movie_id.append(record_list[i][0])
            


        except Error as e :
            print('Error',e)
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
        
        return {'result':movie_REC(movie_id)}
