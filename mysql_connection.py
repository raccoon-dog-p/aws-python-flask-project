import mysql.connector
from mysql.connector.errors import Error

def get_connection():
    connection = mysql.connector.connect(
        host = 'my-db.cfbeyhqoz6o8.ap-northeast-2.rds.amazonaws.com',
        database = 'Project_db',
        user = 'project_user_1',
        password = '1234')
    return connection