import pandas as pd
import sqlite3

conn = sqlite3.connect('jarvas.db')
df = pd.read_sql('SELECT * FROM boleto_apartamento', conn)
print(df.groupby('status')['valor'].sum())