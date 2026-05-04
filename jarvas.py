from datetime import datetime 
import json
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
agora = datetime.now()
boletos_do_imovel = []
lista_desejos_imovel = []
#no try ele vai tentar ler o arquivo do json, se o arquivo ainda não existir, ele vai criar o arquivo json no except
try:
    with open('boletos_do_imovel.json', 'r') as f:
        boletos_do_imovel = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):# o erro de JSON vazio.
    boletos_do_imovel = []
try:
    with open('lista_desejos_imovel.json', 'r') as f:
        lista_desejos_imovel = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):# o erro de JSON vazio.
    lista_desejos_imovel = []
#função para adicionar boletos na lista boletos.json
def adicionar_boletos_do_imovel(novo_boleto):
    boletos_do_imovel.append(novo_boleto)
    with open('boletos_do_imovel.json', 'w') as f:
        json.dump(boletos_do_imovel, f, indent=4)
def visualizar_boletos_do_imovel():
    print ('Aqui estão alguns boletos do senhor, listado por data de vencimento e valores! ')
    with open ('boletos_do_imovel.json', 'r') as f:
        lista_boletos = json.load(f)
        for i in lista_boletos:
            print (f'Recebedor: {i['recebedor']}\nValor: {i['valor']}\nVencimento: {i['vencimento']}')
    return
def voltar_pro_menu():
        continuar = input('Gostaria de voltar ao menu principal? s/n: ').lower()
        if continuar == 'n':
            print('Encerrado JARVAS...\n ATÉ BREVE! ')
            return False
        else:
            return True
def adicionar_itens_lista_desejos(novo_item):
    lista_desejos_imovel.append(novo_item)
    with open('lista_desejos_imovel.json', 'w') as f:
        json.dump(lista_desejos_imovel, f, indent=4)
        print('Item adicionado com sucesso! ')
def visualizar_lista_de_desejos():
    print ('Aqui esta a sua lista de desejos para o imovel! ')
    with open ('lista_desejos_imovel.json', 'r') as f:
        lista_desejos_imovel = json.load(f)
        for i in lista_desejos_imovel:
            print (f'Nome do item: {i['nome_do_item']}\nValor: {i['valor_do_item']}')
    return
print (f'Inicializando JARVAS...\n Olá Senhor! Agora são {agora.hour} horas e {agora.minute} minutos.')
print ('=' * 40)
executando = True
while executando:
    opcoes = input('1- Imovel\n2- Minhas despesas\n Qual? ')
    if opcoes == '1':
        imovel = input ('Sobre oque gostaria de resolver do seu imovel?\n1- Visualizar boletos\n2- Adicionar boletos\n3- Aumento com avanço de obra\n4- Lista de desejos\n5- Tempo restante pro prazo final\n Qual? ')
        if imovel == '1':
            visualizar_boletos_do_imovel()
            executando = voltar_pro_menu()
        elif imovel == '2':
            recebedor = input('Qual empresa recebe?\n ')
            valor = input('Qual valor? ex: 189,37\n ')
            vencimento= input('Qual vencimento do boleto? ex: 03/05/2026\n' )
            ficha_de_boletos = {
            'recebedor': recebedor,
            'valor': valor, 
            'vencimento': vencimento,
            }
            adicionar_boletos_do_imovel(ficha_de_boletos)
            executando = voltar_pro_menu()
        elif imovel == '3':
            avanco_obra = input('Qual valor do avanço de obra desse mês?\n ')
        elif imovel == '4':
            soma_total = 0.0
            for item in lista_desejos_imovel:
                valor_texto = item['valor_do_item'].replace(',', '.')
                soma_total += float(valor_texto)
            visualizar_lista_de_desejos()
            print(f'A lista total está com o valor de R$ {soma_total:.2f}')
            decisao = input('Gostaria de adicionar mais um item? s/n ').lower()        
            if decisao == 's':
                    nome_do_item = input('Qual o nome do item?\n')
                    valor_do_item = input('Qual valor do item?\n')
                    ficha_de_desejos_imovel = {
                    'nome_do_item': nome_do_item,
                    'valor_do_item': valor_do_item
                }
                    adicionar_itens_lista_desejos(ficha_de_desejos_imovel)
            executando = voltar_pro_menu()
    elif opcoes == '2':
        nome_mes = agora.strftime("%B")
        despesas = input (f'Oque gostaria de fazer nas despesas do mes de {nome_mes}? ')
        print ('1- Adicionar boleto\n2- Visualizar boletos\n3- Marcar boleto como pago\n 4- Iniciar outro mês\n Qual?')
