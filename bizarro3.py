def menu():
    'Abre o menu com texto explicando as opções'
    print('\n---------- Menu ----------\n')
    print('1- Cadastrar motor')
    print('2- Exibir motores cadastrados')
    print('3- Exibir relatório')
    print('4- Alterar valor da tarifa de energia')
    print('0- Sair\n')
    opcao = input('Escolha uma opção: ')
    return opcao

def cadastrar_motor(custo_energia):
    'Cadastra os dados de um motor novo na forma de um dicionário'
    print('')
    nome = input('Insira um nome identificador para o motor: ')
    potencia = recebedor_inputs_numericos('Insira a potência nominal do motor (em kW): ')
    eficiencia = recebedor_inputs_numericos('Insira a eficiência do motor (em decimal): ')
    tempo_operacao = recebedor_inputs_numericos('Insira o tempo de operação diária (em horas): ') 

    potencia_util = potencia * eficiencia
    energia_mensal = potencia * tempo_operacao * 30
    custo_mensal = energia_mensal * custo_energia
    custo_kwu = custo_energia / eficiencia

    motor = {'nome': nome, 'potencia': potencia, 'eficiencia': eficiencia, 
             'potencia_util': potencia_util, 'energia_mensal': energia_mensal, 
             'custo_mensal': custo_mensal, 'custo_kwu': custo_kwu}
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

def atualizar_relatorio(relatorio, novo_motor, ha_motores):
    'Recebe o motor recém adicionado e o compara com os melhores/piores em cada categoria do relatório para atualizá-lo'
    if ha_motores:            # Se já tivermos motores cadastrados, faz as comparações
        if relatorio['min_kwu']['custo_kwu'] > novo_motor['custo_kwu']:
            relatorio['min_kwu'] = novo_motor
        elif relatorio['max_kwu']['custo_kwu'] < novo_motor['custo_kwu']:
            relatorio['max_kwu'] = novo_motor
        
        if relatorio['min_pot_nom']['potencia'] > novo_motor['potencia']:
            relatorio['min_pot_nom'] = novo_motor
        elif relatorio['max_pot_nom']['potencia'] < novo_motor['potencia']:
            relatorio['max_pot_nom'] = novo_motor
        
        if relatorio['min_pot_util']['potencia_util'] > novo_motor['potencia_util']:
            relatorio['min_pot_util'] = novo_motor
        elif relatorio['max_pot_util']['potencia_util'] < novo_motor['potencia_util']:
            relatorio['max_pot_util'] = novo_motor
        
        if relatorio['min_custo_mensal']['custo_mensal'] > novo_motor['custo_mensal']:
            relatorio['min_custo_mensal'] = novo_motor
        elif relatorio['max_custo_mensal']['custo_mensal'] > novo_motor['custo_mensal']:
            relatorio['max_custo_mensal'] = novo_motor
    else:                           # Se não houver nenhum motor cadastrado, coloca o motor como o max/min das duas categorias
        relatorio['min_kwu'] = novo_motor
        relatorio['max_kwu'] = novo_motor
        relatorio['min_pot_nom'] = novo_motor
        relatorio['max_pot_nom'] = novo_motor
        relatorio['min_pot_util'] = novo_motor
        relatorio['max_pot_util'] = novo_motor
        relatorio['min_custo_mensal'] = novo_motor
        relatorio['max_custo_mensal'] = novo_motor

def exibir_relatorio(relatorio, custo_energia, ha_motores):
    'Apresenta o relatório para o usuário'
    if(ha_motores):                 # Se já tivermos motores cadastrados, imprime o relatório
        print(f'\n=============== RELATÓRIO ===============\n')
        print('----- Potência Nominal -----\n')
        print(f'Motor de maior potência nominal: {relatorio['max_pot_nom']['nome']} - {relatorio['max_pot_nom']['potencia']:.2f} kW')
        print(f'Motor de menor potência nominal: {relatorio['min_pot_nom']['nome']} - {relatorio['min_pot_nom']['potencia']:.2f} kW')
        print('\n----- Potência Útil -----\n')
        print(f'Motor de maior potência útil: {relatorio['max_pot_util']['nome']} - {relatorio['max_pot_util']['potencia_util']:.2f} kW')
        print(f'Motor de menor potência útil: {relatorio['min_pot_util']['nome']} - {relatorio['min_pot_util']['potencia_util']:.2f} kW')
        print('\n----- Eficiência Energética -----')
        print(f'Custo local da energia elétrica: {custo_energia:.2f} R$/kWh\n')
        print(f'Motor de maior eficiência energética: {relatorio['min_kwu']['nome']} - {relatorio['min_kwu']['custo_kwu']:.2f} R$/kWh')
        print(f'Motor de menor eficiência energética: {relatorio['max_kwu']['nome']} - {relatorio['max_kwu']['custo_kwu']:.2f} R$/kWh')
        print('\n----- Custo Mensal -----')
        print(f'Custo local da energia elétrica: {custo_energia:.2f} R$/kWh\n')
        print(f'Motor de menor custo mensal: {relatorio['min_custo_mensal']['nome']} - R$ {relatorio['min_custo_mensal']['custo_mensal']:.2f}')
        print(f'Motor de maior custo mensal: {relatorio['max_custo_mensal']['nome']} - R$ {relatorio['max_custo_mensal']['custo_mensal']:.2f}')
    else:                           # Caso contrário, imprime uma mensagem de aviso
        print('\nNenhum motor cadastrado.\n')


def main():
    print('========== Sistema de análise de eficiência energética de sistemas industriais ==========\n')
    motores = [] # Variável que acumula todos os motores registrados
    ha_motores = False # Valor booleano utilizado pelas funções que exibem e atualizam o relatório para saberem se algum motor já foi cadastrado
    relatorio = {'min_kwu': None, 'max_kwu': None, 'min_pot_nom': None, # Dicionário que guarda os motores de melhor/pior performance em cada categoria
                 'max_pot_nom': None, 'min_pot_util': None, 'max_pot_util': None, 
                 'min_custo_mensal': None, 'max_custo_mensal': None } 
    custo_energia = recebedor_inputs_numericos('Insira o custo da energia elétrica local (em R$/kWh): ')
    while True:
        opcao = menu()
        if opcao == '0':
            print('Tchau')
            break
        elif opcao == '1':  # Cadastrar novos motores
            novo_motor = cadastrar_motor(custo_energia)
            atualizar_relatorio(relatorio, novo_motor, ha_motores)
            motores.append(novo_motor)
            ha_motores = True
        elif opcao == '2':  # Listar motores cadastrados
            if ha_motores:
                for motor in motores:
                    print('')
                    print(f'===== {motor['nome']} =====')
                    print(f'Potência: {motor['potencia']} KW')
                    print(f'Eficiência: {motor['eficiencia']}')
                    print(f'Potência útil: {motor['potencia_util']}')
                    print(f'Consumo mensal de energia elétrica: {motor['energia_mensal']:.2f} KWh/mês')
                    print(f'Custo operacional mensal: R$ {motor['custo_mensal']:.2f}')
            else:
                print('\nNenhum motor cadastrado.\n')
        elif opcao == '3':  # Exibir relatório
            exibir_relatorio(relatorio, custo_energia, ha_motores)
        elif opcao == '4':  # Alterar tarifa de energia
            custo_energia = recebedor_inputs_numericos('Insira o custo da energia elétrica local (em R$/kWh): ')
            for motor in motores: # Calcula novamente os atributos dos motores relacionados ao custo da energia elétrica
                motor['custo_mensal'] = motor['energia_mensal'] * custo_energia
                motor['custo_kwu'] = custo_energia / motor['eficiencia']
        else: 
            print('Insira uma das opções apresentadas.')
    return 

if __name__ == '__main__':
    main()
