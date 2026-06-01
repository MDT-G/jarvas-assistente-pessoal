import sqlite3
from datetime import datetime

agora = datetime.now()

import os
DB_PATH = os.environ.get('JARVAS_DB', 'jarvas.db')

def get_conexao():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boleto_apartamento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recebedor TEXT,
            valor REAL,
            vencimento TEXT,
            status TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS minhas_despesas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            despesa TEXT,
            valor REAL,
            status TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lista_desejos_ap(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            valor REAL,
            marca TEXT
        );
    """)
    conn.commit()
    conn.close()

def resumo_geral():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(valor) FROM boleto_apartamento WHERE status = "Pago"')
    pago = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(valor) FROM boleto_apartamento WHERE status = "Pendente"')
    pendente = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(valor) FROM lista_desejos_ap')
    desejos = cursor.fetchone()[0] or 0.0

    cursor.execute("""
        SELECT recebedor, valor, vencimento
        FROM boleto_apartamento
        WHERE status = "Pendente"
        ORDER BY vencimento ASC
        LIMIT 1
    """)
    proximo = cursor.fetchone()

    conn.close()

    nome_mes = agora.strftime("%B")
    print(f'Total investido no seu imovel: R$ {pago:.2f}')
    print(f'Total ainda pendente de pagamento para o mês de {nome_mes}: R$ {pendente:.2f}')
    print(f'Meta para mobilia e desejos: R$ {desejos:.2f}')
    print(f'\nCusto total do projeto: R$ {(pago + pendente + desejos):.2f}')

    if proximo:
        print(f'Proximo boleto a vencer: {proximo[0]} R$ {proximo[1]} em {formatar_data(proximo[2])}')
    else:
        print('Proximo boleto a vencer: Tudo em dia Senhor!')

def pagar_boleto_ap(id_boleto):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('UPDATE boleto_apartamento SET status = "Pago" WHERE id = ?', (id_boleto,))
    conn.commit()
    conn.close()
    print(f'JARVAS: Boleto ID: {id_boleto} alterado para PAGO com sucesso!')

def retirar_item_lista(id_item):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lista_desejos_ap WHERE id = ?', (id_item,))
    conn.commit()
    conn.close()
    print(f'Item {id_item} retirado com sucesso!')

def ler_sql_lista_desejos():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lista_desejos_ap')
    resultado = cursor.fetchall()
    conn.close()
    for i in resultado:
        print(f'ID: {i[0]} | Item: {i[1]} | Valor: {i[2]} | Marca: {i[3]}')

def ler_sql_boletos_ap():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boleto_apartamento')
    resultado = cursor.fetchall()
    conn.close()
    if not resultado:
        print('A tabela de boletos esta vazia no momento.')
    else:
        for i in resultado:
            print(f'ID: {i[0]} | Recebedor: {i[1]} | Valor: {i[2]} | Vencimento: {formatar_data(i[3])} | Status: {i[4]}')

def adicionar_sql_boletos_ap(recebedor, valor, vencimento, status):
    resultado = converter_data(vencimento)
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO boleto_apartamento(recebedor, valor, vencimento, status) VALUES(?,?,?,?)',
        (recebedor, valor, resultado, status)
    )
    conn.commit()
    conn.close()
    print(f'Boleto de {recebedor} adicionado com sucesso!')

def adicionar_sql_lista_desejos(item, valor, marca):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO lista_desejos_ap(item, valor, marca) VALUES(?,?,?)',
        (item, valor, marca)
    )
    conn.commit()
    conn.close()

def adicionar_boleto_despesas(despesa, valor, status):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO minhas_despesas(despesa, valor, status) VALUES(?,?,?)',
        (despesa, valor, status)
    )
    conn.commit()
    conn.close()
    print('Boleto adicionado com sucesso!')

def ler_boleto_despesas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM minhas_despesas')
    resultado = cursor.fetchall()
    conn.close()
    for i in resultado:
        print(f'ID: {i[0]} | Despesa: {i[1]} | Valor: {i[2]} | Status: {i[3]}')

def pagar_boleto_despesas(id_boleto):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('UPDATE minhas_despesas SET status = "Pago" WHERE id = ?', (id_boleto,))
    conn.commit()
    conn.close()

def total_boleto_despesas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT COALESCE(SUM(valor), 0) FROM minhas_despesas')
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total

def total_boleto_imovel():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(valor) FROM boleto_apartamento WHERE status = "Pendente"')
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total
def formatar_data(data):
    data = datetime.strptime(data,'%Y-%m-%d')# entrada
    resultado = data.strftime('%d/%m/%Y')#saida
    return resultado
def converter_data(data):
    data = datetime.strptime(data, '%d/%m/%Y')#entrada
    resultado = data.strftime('%Y-%m-%d')#saida
    return resultado