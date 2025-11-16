def menu():
    'Abre o menu com texto explicando as opções'
    print('')
    print('1- Cadastrar motor')
    print('2- Exibir motores cadastrados')
    print('3- Exibir relatório')
    print('0- Sair\n')
    opcao = input('Escolha uma opção: ')
    return opcao

def cadastrar_motor():
    'Cadastra os dados de um motor novo em forma de um dicionário'
    print('')
    nome = input('Insira um nome identificador para o motor: ')
    potencia = recebedor_inputs_numericos('Insira a potência nominal do motor (em kW): ')
    eficiencia = recebedor_inputs_numericos('Insira a eficiência do motor (em decimal): ')
    tempo_operacao = recebedor_inputs_numericos('Insira o tempo de operação diária (em horas): ')
    custo_energia = recebedor_inputs_numericos('Insira o custo da energia elétrica (em R$/kWh): ') 

    energia_mensal = potencia * tempo_operacao * 30 / eficiencia
    custo_mensal = energia_mensal * custo_energia

    motor = {'nome': nome, 'potencia': potencia, 'eficiencia': eficiencia,
             'energia_mensal': energia_mensal, 'custo_mensal': custo_mensal}
    print('')
    print(f'Motor "{motor['nome']}" cadastrado com sucesso.')
    return motor

def recebedor_inputs_numericos(mensagem):
    'Pede um input e verifica se é numérico e se não for pede um input novo'
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
    'Verifica se a string é numérica e retorna True ou False'
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
    motores = [] # Variável que acumula todos os motores registrados
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
        elif opcao == '3':
            atual_min_kwu = float('inf') # Mínimo valor de custo por kw util
            atual_max_kwu = float('-inf') # Máximo valor de custo por kw util
            atual_min_eff_ec = float('inf') # Menor valor de eficiência econômica
            atual_max_eff_ec = float('-inf') # Maior valor  de eficiência econômica
            motor_min_kwu = None # Nome do motor com menor custo por kW util
            motor_max_kwu = None # Nome do motor com maior custo por kW util
            motor_min_eff_ec = None # Nome do motor com menor eficiencia economica
            motor_max_eff_ec = None # Nome do motor com maior eficiencia economica
            
            for motor in motores:
                custo_por_kw_util = motor['custo_mensal'] / (motor['potencia']*motor['eficiencia'])
                eficiencia_economica = motor['eficiencia'] / motor['custo_mensal']
                if custo_por_kw_util < atual_min_kwu:
                    atual_min_kwu = custo_por_kw_util
                    motor_min_kwu = motor['nome']
                if custo_por_kw_util > atual_max_kwu:
                    atual_max_kwu = custo_por_kw_util
                    motor_max_kwu = motor['nome']
                if eficiencia_economica < atual_min_eff_ec:
                    atual_min_eff_ec = eficiencia_economica
                    motor_min_eff_ec = motor['nome']
                if eficiencia_economica > atual_max_eff_ec:
                    atual_max_eff_ec = eficiencia_economica
                    motor_max_eff_ec = motor['nome']
                 
            if atual_min_kwu != float('inf') and atual_max_kwu != float('-inf') and atual_min_eff_ec != float('inf') and atual_max_eff_ec != float('-inf'):
                print('')
                print(f'Motor com maior custo por kW útil: Motor {motor_max_kwu} com valor {atual_max_kwu}')
                print(f'Motor com menor custo por kW útil: Motor {motor_min_kwu} com valor {atual_min_kwu}')
                print(f'Motor com maior eficiência econômica: Motor {motor_max_eff_ec} com valor {atual_max_eff_ec}')
                print(f'Motor com menor eficiência econômica: Motor {motor_min_eff_ec} com valor {atual_min_eff_ec}')
    return 

if __name__ == '__main__':
    main()
