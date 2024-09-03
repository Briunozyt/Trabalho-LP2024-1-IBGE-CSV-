import pandas as pd
from colorama import Fore, Style, init

# Inicializa o colorama
init(autoreset=True)

# Carregar o arquivo CSV
file_path = 'br_ibge_censo_2022_populacao_grupo_idade_uf.csv'
df = pd.read_csv(file_path)

# Função para mostrar o menu
def mostrar_menu():
    print('\n')
    print(Fore.YELLOW + 'Bem-vindo ao (IBGE) Instituto Brasileiro de Geografia e Estatística' + Style.RESET_ALL)
    print('\n')
    print("Menu de Opções:")
    print("1. Mostrar dados ordenados do maior para o menor em termos de idade.")
    print("2. Mostrar dados ordenados do menor para o maior em termos de idade.")
    print("3. Mostrar dados ordenados do maior para o menor em termos de população.")
    print("4. Mostrar dados ordenados do menor para o maior em termos de população.")
    print("5. Consultar um estado específico e ver o relatório das idades dos grupos populacionais.")
    print("6. Relatório do percentual de pessoas do sexo feminino e masculino de todos os estados do Brasil.")
    print("7. Relatório do percentual de gênero masculino e feminino por estado.")
    print("8. Relatório do percentual de pessoas em cada grupo etário.")
    print("9. Sair")
    try:
        return int(input("Escolha uma opção (1-9): "))
    except ValueError:
        print(Fore.RED + "Entrada inválida. Por favor, digite um número entre 1 e 9." + Style.RESET_ALL)
        return 0  

#1° Condição: ordenada pela coluna Grupo_idade usando "ascending" atrelado opção 1 e 2.
def ordenar_idade(df, ordem):
    df_ordenado = df.sort_values(by='Grupo_idade', ascending=ordem)
    return df_ordenado

#2° Condição: ordenada pela coluna população usando "ascending" atrelado opção 3 e 4.
def ordenar_populacao(df, ordem):
    df_ordenado = df.sort_values(by='populacao', ascending=ordem)
    return df_ordenado

#3° Condição: Sistema de busca determinado pela coluna "UF" atrelado opção 5.
def relatorio_estado(df, estado):
    df_estado = df[df['UF'] == estado]
    return df_estado

#4° Condição: Relatório do percentual de pessoas do sexo feminino e masculino (tds estados) atrelado opção  6.
def porcentagem_sexo_feminino(df):
    total_pessoas = df['populacao'].sum()
    total_feminino = df[df['sexo'] == 'Feminino']['populacao'].sum()
    porcentagem_feminino = (total_feminino / total_pessoas) * 100
    return porcentagem_feminino
def porcentagem_sexo_masculino(df):
    total_pessoas = df['populacao'].sum()
    total_masculino = df[df['sexo'] == 'Masculino']['populacao'].sum()
    porcentagem_masculino = (total_masculino / total_pessoas) * 100
    return porcentagem_masculino

#5° Condição: Para calcular a percentual de pessoas em cada grupo etário atrelado opção 8. 
def porcentagem_por_grupo_etario(df):
    grupos_etarios = df['Grupo_idade'].unique()
    total_pessoas = df['populacao'].sum()
    resultados = {}

    for grupo in grupos_etarios:
        df_grupo = df[df['Grupo_idade'] == grupo]
        total_grupo = df_grupo['populacao'].sum()
        porcentagem_grupo = (total_grupo / total_pessoas) * 100
        resultados[grupo] = porcentagem_grupo
    
    return resultados

#6° Relatório do percentual de pessoas do sexo feminino e masculino (CONSULTA ESTADO ESPECIFICO) atrelado opção  7.
def percentual_genero_estado(df, estado):
    df_estado = df[df['UF'] == estado]
    if df_estado.empty:
        return None, None
    
    total_pessoas = df_estado['populacao'].sum()
    total_feminino = df_estado[df_estado['sexo'] == 'Feminino']['populacao'].sum()
    total_masculino = df_estado[df_estado['sexo'] == 'Masculino']['populacao'].sum()
    
    porcentagem_feminino = (total_feminino / total_pessoas) * 100
    porcentagem_masculino = (total_masculino / total_pessoas) * 100
    
    return porcentagem_feminino, porcentagem_masculino

# Função para executar o menu e as opções escolhidas
def executar_menu():
    while True:
        opcao = mostrar_menu()
        
        if opcao == 1:
            print(Fore.CYAN + "Ordenando do maior para o menor em termos de idade:" + Style.RESET_ALL)
            resultado = ordenar_idade(df, ordem=False)
            print(resultado.to_string(index=False))
            
        elif opcao == 2:
            print(Fore.CYAN + "Ordenando do menor para o maior em termos de idade:" + Style.RESET_ALL)
            resultado = ordenar_idade(df, ordem=True)
            print(resultado.to_string(index=False))
        
        elif opcao == 3:
            print(Fore.CYAN + "Ordenando do maior para o menor em termos de população:" + Style.RESET_ALL)
            resultado = ordenar_populacao(df, ordem=False)
            print(resultado.to_string(index=False))
        
        elif opcao == 4:
            print(Fore.CYAN + "Ordenando do menor para o maior em termos de população:" + Style.RESET_ALL)
            resultado = ordenar_populacao(df, ordem=True)
            print(resultado.to_string(index=False))
            
        elif opcao == 5:
            estado = input(Fore.GREEN + "Digite a sigla do estado que deseja consultar (ex: SP, RJ): " + Style.RESET_ALL).upper()
            resultado = relatorio_estado(df, estado)
            if resultado.empty:
                print(Fore.RED + f"Nenhum dado encontrado para o estado {estado}." + Style.RESET_ALL)
            else:
                print(Fore.CYAN + f"Relatório para o estado {estado}:" + Style.RESET_ALL)
                print(resultado.to_string(index=False))
                
        elif opcao == 6:
            porcentagem_feminino = porcentagem_sexo_feminino(df)
            porcentagem_masculino = porcentagem_sexo_masculino(df)
            print(Fore.CYAN + f"Porcentagem de pessoas do sexo feminino em todos os estados do Brasil: {porcentagem_feminino:.2f}%" + Style.RESET_ALL)
            print(Fore.CYAN + f"Porcentagem de pessoas do sexo masculino em todos os estados do Brasil: {porcentagem_masculino:.2f}%" + Style.RESET_ALL)
        
        elif opcao == 7:
            estado = input(Fore.GREEN + "Digite a sigla do estado que deseja consultar (ex: SP, RJ): " + Style.RESET_ALL).upper()
            porcentagem_feminino, porcentagem_masculino = percentual_genero_estado(df, estado)
            if porcentagem_feminino is None:
                print(Fore.RED + f"Nenhum dado encontrado para o estado {estado}." + Style.RESET_ALL)
            else:
                print(Fore.CYAN + f"Porcentagem de pessoas do sexo feminino no estado {estado}: {porcentagem_feminino:.2f}%" + Style.RESET_ALL)
                print(Fore.CYAN + f"Porcentagem de pessoas do sexo masculino no estado {estado}: {porcentagem_masculino:.2f}%" + Style.RESET_ALL)
        
        elif opcao == 8:
            porcentagens_grupos = porcentagem_por_grupo_etario(df)
            print(Fore.CYAN + "Porcentagem de pessoas em cada grupo etário:" + Style.RESET_ALL)
            for grupo, porcentagem in porcentagens_grupos.items():
                print(Fore.CYAN + f"{grupo}: {porcentagem:.2f}%" + Style.RESET_ALL)
        
        elif opcao == 9:
            print(Fore.YELLOW + "Saindo... Por favor aguarde..." + Style.RESET_ALL)
            break
            
        else:
            print(Fore.RED + "Opção inválida. Por favor, escolha uma opção válida." + Style.RESET_ALL)

# Executar o menu
executar_menu()
