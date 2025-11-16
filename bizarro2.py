
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
    custo_kwu = custo_mensal / (potencia * eficiencia)
    eficiencia_economica = eficiencia / custo_mensal

    motor = {'nome': nome, 'potencia': potencia, 'eficiencia': eficiencia,
             'energia_mensal': energia_mensal, 'custo_mensal': custo_mensal,
             'custo_kwu': custo_kwu, 'eficiencia_economica': eficiencia_economica}
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
    """Ao invés de guardar o nome dos motores e os valores de min/max, acho melhor guardar o motor em si e recuperar os valores quando necessário.
    Além disso, pra facilitar esse processo de recuperar os valores, adicionei os campos kwu e eficiencia economica aos motores em 'cadastrar_motor()'
    E para evitar ter que percorrer todo o array e fazer diversas comparações sempre que quisermos obter o relatório, achei mais adequado determinar
    os motores com kwu e eff max/min assim que adicionamos um motor novo, evitando assim todo aquele loop da opcao 3"""
    motor_min_kwu = {'custo_kwu': float('inf')} # Placeholder para o motor com menor custo por kW util
    motor_max_kwu = {'custo_kwu': float('-inf')} # Placeholder para o motor com maior custo por kW util
    motor_min_eff_ec = {'eficiencia_economica': float('inf')} # Placeholder para o motor com menor eficiencia economica
    motor_max_eff_ec = {'eficiencia_economica': float('-inf')} # Placeholder para o motor com maior eficiencia economica
    while True:
        opcao = menu()
        if opcao == '0':
            print('Tchau')
            break
        elif opcao == '1':
            novo_motor = cadastrar_motor()
            if len(motores) > 0:            # Se já tivermos motores cadastrados, faz as comparações
                if motor_min_kwu['custo_kwu'] > novo_motor['custo_kwu']:
                    motor_min_kwu = novo_motor
                elif motor_max_kwu['custo_kwu'] < novo_motor['custo_kwu']:
                    motor_max_kwu = novo_motor
                if motor_min_eff_ec['eficiencia_economica'] > novo_motor['eficiencia_economica']:
                    motor_min_eff_ec = novo_motor
                elif motor_max_eff_ec['eficiencia_economica'] < novo_motor['eficiencia_economica']:
                    motor_max_eff_ec = novo_motor
            else:                           # Se não houver nenhum motor cadastrado, coloca o motor como o max/min das duas categorias
                motor_min_kwu = novo_motor
                motor_max_kwu = novo_motor
                motor_min_eff_ec = novo_motor
                motor_max_eff_ec = novo_motor
            motores.append(novo_motor)
            

        elif opcao == '2':
            for motor in motores:
                print('')
                print(f'===== {motor['nome']} =====')
                print(f'Potência: {motor['potencia']} KW')
                print(f'Eficiência: {motor['eficiencia']}')
                print(f'Consumo mensal de energia elétrica: {motor['energia_mensal']:.2f} KWh/mês')
                print(f'Custo operacional mensal: R$ {motor['custo_mensal']:.2f}')
        elif opcao == '3':
            if len(motores) > 0:
                print('')
                print(f'Motor com maior custo por kW útil: Motor {motor_max_kwu['nome']} com valor {motor_max_kwu['custo_kwu']:.2f}')
                print(f'Motor com menor custo por kW útil: Motor {motor_min_kwu['nome']} com valor {motor_min_kwu['custo_kwu']:.2f}')
                print(f'Motor com maior eficiência econômica: Motor {motor_max_eff_ec['nome']} com valor {motor_max_eff_ec['eficiencia_economica']}')
                print(f'Motor com menor eficiência econômica: Motor {motor_min_eff_ec['nome']} com valor {motor_min_eff_ec['eficiencia_economica']}')
            else:
                print('')
                print('Nenhum motor cadastrado.')
    return 

if __name__ == '__main__':
    main()
