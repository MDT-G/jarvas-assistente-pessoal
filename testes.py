from database import get_conexao

conn = get_conexao()
cursor = conn.cursor()
cursor.execute('SELECT status, SUM(valor) FROM boleto_apartamento GROUP BY status')
resultado = cursor.fetchall()
for i in resultado:
    print(f'Status: {i[0]} | Total: R$ {i[1]:.2f}')
conn.close()
