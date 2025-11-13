def menu():
    print('')
    print('1- Cadastrar motor')
    print('2- Exibir motores cadastrados')
    print('3- Exibir relatório')
    print('0- Sair\n')
    opcao = input('Escolha uma opção: ')
    return opcao

def cadastrar_motor():
    print('')
    nome = input('Insira um nome identificador para o motor: ')
    potencia = recebedor_inputs_numericos('Insira a potência nominal do motor (em kW): ')
    eficiencia = recebedor_inputs_numericos('Insira a eficiência do motor (em decimal): ')
    tempo_operacao = recebedor_inputs_numericos('Insira o tempo de operação diária (em horas): ')
    custo_energia = recebedor_inputs_numericos('Insira o custo da energia elétrica (em R$/kWh): ') 

    energia_mensal = potencia * tempo_operacao * 30 / eficiencia
    custo_mensal = energia_mensal * custo_energia

    motor = {'nome': nome, 'potencia': potencia, 'eficiencia': eficiencia, 'energia_mensal': energia_mensal, 'custo_mensal': custo_mensal}
    print('')
    print(f'Motor "{motor['nome']}" cadastrado com sucesso.')
    return motor

def recebedor_inputs_numericos(mensagem):
    eh_num = False
    num = None
    while not eh_num:
        num = input(mensagem)
        if verificador_numerico(num):
            eh_num = True
        else: 
            print('')
            print('Insira um valor numérico válido.')
    return float(num)

def verificador_numerico(string):
    if string.isdecimal():
        return True
    s = string.strip()
    partes_num = s.split('.')
    if len(partes_num) == 2:
        tem_numero = False
        partes_validas = 0
        for parte in partes_num:
            if parte.isdecimal():
                tem_numero = True
                partes_validas += 1
            elif parte == '':
                partes_validas += 1
    	
        if tem_numero and partes_validas == 2:
            return True
    return False
        

def main():
    print('========== Sistema de análise de eficiência energética de sistemas industriais ==========')
    motores = []
    while True:
        opcao = menu()
        if opcao == '0':
            print('Tchau')
            break
        elif opcao == '1':
            motores.append(cadastrar_motor())
        elif opcao == '2':
            for motor in motores:
                print('')
                print(f'===== {motor['nome']} =====')
                print(f'Potência: {motor['potencia']} KW')
                print(f'Eficiência: {motor['eficiencia']}')
                print(f'Consumo mensal de energia elétrica: {motor['energia_mensal']:.2f} KWh/mês')
                print(f'Custo operacional mensal: R$ {motor['custo_mensal']:.2f}')
    return 

if __name__ == '__main__':
    main()
