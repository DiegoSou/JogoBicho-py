import animals as db

from pandas import DataFrame, Series
from pandas import read_csv, isna

from IPython.display import display
from random import random

APOSTAS_CSV = '../resources/apostas.csv'
n_milhares = 5

# Method
def gerar_milhares():
    results = Series()
    for n in range(n_milhares): 
        results[str(n)] = str(random())[4:8]

    return results

# Method
def gerar_resultados():
    result_df = DataFrame()

    # Sorteia os números de acordo com o range definido no início
    result_df['Milhar_Sorteado'] = gerar_milhares()
    
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

# Method
def gerar_apostas():
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

# Method
def gerar_estatisticasResultado(resultados_df, apostas_df, resultados_gerais_df):

    temp_df = DataFrame()

    for nomePessoa in apostas_df.index:
        # Cria colunas para cada apostador
        resultados_df[nomePessoa] = Series()

        # Relaciona com o resultado
        for indexPremio in resultados_df.index:
            resultadoAnimal = resultados_df['Resultado'][indexPremio]

            # Checa as colunas de aposta para saber se o animal do resultado é o mesmo
            if (not 
                    apostas_df['Aposta Normal'][nomePessoa] == resultadoAnimal
                and
                not
                    apostas_df['Aposta Dupla'][nomePessoa] == resultadoAnimal 

            ): continue
            
            # Caso seja, checa o tipo da aposta para saber qual pontuação levar
            if (apostas_df['Tipo'][nomePessoa] == 'normal'):
                resultados_df[nomePessoa][indexPremio] = 1
                temp_df[nomePessoa] = resultados_df[nomePessoa]

            elif (apostas_df['Tipo'][nomePessoa] == 'dupla'):
                if (apostas_df['Aposta Normal'][nomePessoa] == resultadoAnimal) :
                    apostas_df['Aposta Normal'][nomePessoa] = '(x) '+ apostas_df['Aposta Normal'][nomePessoa]

                if (apostas_df['Aposta Dupla'][nomePessoa] == resultadoAnimal) :
                    apostas_df['Aposta Dupla'][nomePessoa] = '(x) '+ apostas_df['Aposta Dupla'][nomePessoa]

                if (apostas_df['Aposta Normal'][nomePessoa][:3] == '(x)'
                    and
                    apostas_df['Aposta Dupla'][nomePessoa][:3] == '(x)'
                ): 
                    resultados_df[nomePessoa][indexPremio] = 3.0
                    temp_df[nomePessoa] = resultados_df[nomePessoa]
        
        if nomePessoa in temp_df:
            for pontuacao in temp_df[nomePessoa]:
                if isna(pontuacao): continue

                if nomePessoa in resultados_gerais_df:
                    resultados_gerais_df[nomePessoa].apply(
                        lambda x: (int(x) + int(pontuacao)) if not isna(x) else (int(pontuacao)) 
                    )

                else:
                    resultados_gerais_df[nomePessoa] = temp_df[nomePessoa]
            
    return resultados_gerais_df


# Method
def gerar_resultadosGerais():
    resultados_gerais = DataFrame()

    for i in range(5):
        apostas_df = gerar_apostas()
        resultados_df = gerar_resultados()
        resultados_gerais = gerar_estatisticasResultado(resultados_df, apostas_df, resultados_gerais)
        
        display(apostas_df)
        display(resultados_df)
        display(resultados_gerais)
                

