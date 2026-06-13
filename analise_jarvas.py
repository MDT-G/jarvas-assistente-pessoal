import pandas as pd
from database import get_conexao


conn = get_conexao()
#df = pd.read_sql('SELECT * FROM minhas_despesas',conn)
#print('Status e valor somado de minhas despesas')
#print(df.groupby('status')['valor'].sum())


#df2= pd.read_sql('SELECT * FROM boleto_apartamento', conn)
#print('Boletos do apartamento filtrados e organizados do maior pro menor valor.')
#print(df2[['recebedor','valor']].sort_values('valor',ascending=False))
#conn.close()


df3 = pd.read_sql('SELECT * FROM boleto_apartamento',conn)
