import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='jarvas_db',
    user='postgres',
    password='giovanni1',
    port='5432'
)

print('Conectado com sucesso!')
conn.close()