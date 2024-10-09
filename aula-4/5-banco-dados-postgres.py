import psycopg2
import pandas as pd
conn = psycopg2.connect(
    dbname = 'seu-banco',
    user = 'postgress',
    password = 'kise',
    host = 'localhost'
)

df = pd.read_sql_query('SELECT * FROM alunos,', conn)
conn.close()

print(df)