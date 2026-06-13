from datetime import datetime
import locale
from database import *

locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
agora = datetime.now()

criar_tabelas()

def voltar_pro_menu():
    continuar = input('Gostaria de voltar ao menu principal? s/n: ').lower()
    if continuar == 'n':
        print('Encerrado JARVAS...\n ATÉ BREVE!')
        return False
    return True

def formatar_dinheiro(valor_texto):
    # Transforma '150,50' em 150.50
    try:
        return float(str(valor_texto).replace(',', '.'))
    except ValueError:
        print("Valor inválido! Use 0.00")
        return 0.0

executando = True
print(f'Inicializando JARVAS...\n Olá Senhor!\n\nStatus atual em: {agora.strftime("%d/%m/%Y %H:%M")}')

while executando:
    print('=' * 80)
    opcoes = input('\n0- Resumo geral\n1- Imovel\n2- Minhas despesas\n Qual?\n ')

    if opcoes == '0':
        resumo_geral()
        executando = voltar_pro_menu()

    elif opcoes == '1':
        imovel = input(
            'Sobre oque gostaria de resolver do seu imovel?\n'
            '1- Visualizar boletos\n'
            '2- Adicionar boletos\n'
            '3- Alterar status do boleto para Pago\n'
            '4- Aumento com avanço de obra\n'
            '5- Lista de desejos\n'
            'Qual?\n '
        )
        if imovel == '1':
            ler_sql_boletos_ap()
            total_valor = total_boleto_imovel()
            print(f'Valor total pendente: R$ {total_valor:.2f}')
            executando = voltar_pro_menu()

        elif imovel == '2':
            recebedor = input('Qual empresa recebe?\n ')
            valor = input('Qual valor? ex: 189,37\n ')
            valor_corrigido = formatar_dinheiro(valor)
            vencimento = input('Qual vencimento do boleto? ex: 03/05/2026\n')
            status = 'Pendente'
            adicionar_sql_boletos_ap(recebedor, valor_corrigido, vencimento, status)
            executando = voltar_pro_menu()

        elif imovel == '3':
            ler_sql_boletos_ap()
            id_pago = input('Qual o ID do boleto que você pagou?\n')
            pagar_boleto_ap(id_pago)
            executando = voltar_pro_menu()

        elif imovel == '4':
            avanco = input('Qual valor do avanço de obra desse mês?\n ')
            valor_avanco = formatar_dinheiro(avanco)
            adicionar_sql_boletos_ap('Avanço de Obra', valor_avanco, agora.strftime('%d/%m/%Y'), 'Pendente')
            print(f'Avanço de obra de R$ {valor_avanco:.2f} registrado com sucesso!')
            executando = voltar_pro_menu()

        elif imovel == '5':
            ler_sql_lista_desejos()
            decisao = input('Gostaria de adicionar ou remover algum item? s/n\n ').lower()
            if decisao == 's':
                retirar_ou_adicionar = input('Adicionar = s\nRetirar = n\nQual? ')
                if retirar_ou_adicionar == 's':
                    nome_do_item = input('Qual o nome do item?\n')
                    valor_do_item = input('Qual valor do item? ex: 299,90\n')
                    valor_final = formatar_dinheiro(valor_do_item)
                    marca_do_item = input('Qual a marca do item?\n')
                    adicionar_sql_lista_desejos(nome_do_item, valor_final, marca_do_item)
                elif retirar_ou_adicionar == 'n':
                    ler_sql_lista_desejos()
                    id_para_remover = input('Qual ID do item que você quer remover? ')
                    retirar_item_lista(id_para_remover)
            executando = voltar_pro_menu()
    elif opcoes == '2':
        nome_mes = agora.strftime("%B")
        despesas = input(
            f'Oque gostaria de fazer nas despesas do mes de {nome_mes}?\n'
            '1- Adicionar boleto\n'
            '2- Visualizar boletos\n'
            '3- Marcar boleto como pago\n'
            ' Qual?\n '
        )
        if despesas == '1':
            despesa = input('Qual é a despesa?\n')
            valor = input('Qual o valor? ex:189,37\n')
            valor_final = formatar_dinheiro(valor)
            status = 'Pendente'
            vencimento = input('Qual vencimento do boleto? ex: 03/05/2026\n')
            adicionar_boleto_despesas(despesa, valor_final, status, vencimento)
            executando = voltar_pro_menu()

        elif despesas == '2':
            ler_boleto_despesas()
            total_pago = total_boleto_despesas()
            print(f'Valor total das despesas do mês: R$ {total_pago:.2f}')
            executando = voltar_pro_menu()

        elif despesas == '3':
            ler_boleto_despesas()
            id_boleto = input('Qual o ID do boleto? ')
            pagar_boleto_despesas(id_boleto)
            print('Boleto alterado com sucesso!')
            executando = voltar_pro_menu()