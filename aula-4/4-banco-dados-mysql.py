import pymysql
import pandas as pd

conn = pymysql.connect(
    host = 'localhost',
    user = 'postgress',
    password = 'kise',
    database = 'seu-banco'
)

df = pd.read_sql_query('SELECT * FROM alunos,', conn)
conn.close()

print(df)