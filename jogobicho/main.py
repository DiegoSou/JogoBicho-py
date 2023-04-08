# Como jogar:

# Você vai jogar em um número de 1 a 25 que representa as dezenas dos bixos
# O milhar sorteado vai de 0001 até 9999
# Se alguma dezena do milhar sorteado tiver o animal do grupo que você apostou, vc ganha

# Na dupla você escolhe 2 grupos para apostar na mesma dezena
# 1 real paga 20 reais (do 1º ao 5º premio)
# Apessoa que apostou na dupla procura entre os 5 resultados os seus animais (precisam estar os dois)

import database.animals as db
import controls.maincontrols as c

from pandas import DataFrame
from pandas import Series
from pandas import read_csv
from pandas import isna

from random import random

APOSTAS_CSV = './resources/apostas.csv'
nMilhares = 5

def gerarMilhares():
    results = Series()
    
    for n in range(nMilhares): 
        results[str(n)] = str(random())[4:8]

    return results

def gerarResultados():
    result_df = DataFrame()

    # Sorteia os números de acordo com o range definido no início
    result_df['Milhar_Sorteado'] = gerarMilhares()
    result_df['Resultado'] = Series()

    indexPremios = Series(result_df.index)

    for i in indexPremios:
        # Define o index com 'premio'
        indexPremios[int(i)] = str(int(i)+1) + ' premio' 

        # Define o animal da milha sorteada
        result_df['Resultado'][i] = (
            db.numbers.loc[(
                int(result_df['Milhar_Sorteado'][i][2:])
            )]
        )

    result_df.index = indexPremios
    return result_df

def gerarApostas():
    apostas_df = read_csv(APOSTAS_CSV)

    # Aplica os zeros ao começo das milhas apostadas
    apostas_df = apostas_df.apply(
        lambda serie_pessoa : serie_pessoa.apply(
            lambda aposta: str(aposta).zfill(4)
        )
    )

    # Gera os indexes de acordo com cada pessoa que apostou
    apostas_df.index = apostas_df['Nome'].values

    apostas_df['Aposta Normal'] = Series()
    apostas_df['Aposta Dupla'] = Series()

    # Define quais animais foram apostados através do milhar, 
    for nomePessoa in apostas_df['Nome']:
        # os dois ultimos dígitos representa o animal principal
        apostas_df['Aposta Normal'][nomePessoa] = (
            db.numbers.loc[(
                int(apostas_df['Milhar'][nomePessoa][2:])*4
            )]
        )

        if apostas_df['Tipo'][nomePessoa] == 'dupla':
            # os dois primeiros dígitos representa a dupla 
            apostas_df['Aposta Dupla'][nomePessoa] = (
                db.numbers.loc[(
                    int(apostas_df['Milhar'][nomePessoa][:2])*4
                )]
            )

    del apostas_df['Nome']
    return apostas_df

    
apostas_df = gerarApostas()
resultados_df = gerarResultados()

for nomePessoa in apostas_df.index:
    # Cria colunas para cada apostador
    resultados_df[nomePessoa] = Series()

    # Relaciona com o resultado
    # Compara as tabelas para saber o tipo da aposta
    for index in resultados_df.index:
        resultadoAnimal = resultados_df['Resultado'][index]

        if (not 
                apostas_df['Aposta Normal'][nomePessoa] == resultadoAnimal
            and
            not
                apostas_df['Aposta Dupla'][nomePessoa] == resultadoAnimal 

        ): continue
        
        if (apostas_df['Tipo'][nomePessoa] == 'normal'):
            resultados_df[nomePessoa][index] = 1

        elif (apostas_df['Tipo'][nomePessoa] == 'dupla'):
            if (apostas_df['Aposta Normal'][nomePessoa] == resultadoAnimal) :
                apostas_df['Aposta Normal'][nomePessoa] = '(x) '+ apostas_df['Aposta Normal'][nomePessoa]

            if  (apostas_df['Aposta Dupla'][nomePessoa] == resultadoAnimal) :
                apostas_df['Aposta Dupla'][nomePessoa] = '(x) '+ apostas_df['Aposta Dupla'][nomePessoa]

            if (
                apostas_df['Aposta Normal'][nomePessoa][:3] == '(x)'
                and
                apostas_df['Aposta Dupla'][nomePessoa][:3] == '(x)'
            ): resultados_df[nomePessoa][index] = 3.0

            
print(apostas_df)
print(resultados_df)


# Análises
# Quantas vezes deu determinado animal
# Quantas vezes deu determinada dupla
# Relação animal / premio
# Pontuação geral

