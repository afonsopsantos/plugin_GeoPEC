#-------------------------------------------------------------------------------------------------------- 
#   GeoPEC - Software científico para avaliação da acurácia posicional em dados cartográficos
#   Funções para o cálculo da acurácia posicional no controle de qualidade cartográfica
#   abril de 2024
#   autores: Afonso P. Santos; João Vítor A. Gonçalves; Luis Philippe Ventura
#-------------------------------------------------------------------------------------------------------- 

import math 
import statistics
import numpy as np
from scipy import stats
from scipy.stats import t

#--------------------------------------------------------------------------------------------------------
# Função para o cálculo das discrepâncias posicionais em x,y e z
#

def fDiscrepancia(data):

# A função recebe como parâmetro o dicionário contendo todos os dados de teste e de referência
#após a junção espacial. 
    
    # Criando os dicionários para as discrepâncias em x, y e z.
    
    disc_x = {}
    disc_y = {}
    disc_z = {}
  
    # iterando sobre os dados, a partir das chaves do dicionário. Cada chave representa o id do ponto.
    
    for pt in data.keys():
        
        
        disc_x[pt] = data[pt]['Xtest'] - data[pt]['Xref']  #Discrepância em x
        
        disc_y[pt] = data[pt]['Ytest'] - data[pt]['Yref']  #Discrepância em y
        
        disc_z[pt] = data[pt]['Ztest'] - data[pt]['Zref']  #Discrepância em z
        
        
        # Acrescentando as discrepâncias as listas de discrepâncias
        
        #disc_x.append(dx)
        #disc_y.append(dy)
        #disc_z.append(dz)
        
    return (disc_x, disc_y, disc_z)


#--------------------------------------------------------------------------------------------------------
# Função para o cálculo das discrepâncias posicionais 2D
#   

def fDiscrepancia2D(disc_x, disc_y):

    disc_2D = {}
    
    #iterando sobre os dicionários de discrepâncias
    
    for pt in disc_x.keys():
    
        disc_2D[pt] = math.sqrt((disc_x[pt]**2) + (disc_y[pt]**2))
    
    return disc_2D
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo das discrepâncias posicionais 3D
#

def fDiscrepancia3D(disc_x, disc_y, disc_z):

    disc_3D = {}
    
    #iterando sobre os dicionários de discrepâncias
    
    for pt in disc_x.keys():
    
        disc_3D[pt] = math.sqrt((disc_x[pt]**2) + (disc_y[pt]**2) + (disc_z[pt]**2) )
    
    return disc_3D  

#--------------------------------------------------------------------------------------------------------
# Função para o cálculo da média
#

def fMedia(dados):
    
    soma = 0
    
    for pt in dados.keys():
        
        soma = soma + dados[pt]
    
    media = soma/len(dados.keys())
    
    return media 
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo da mediana
#

def fDevPad(dados):
    
    media = fMedia(dados)
    
    soma = 0
    
    for pt in dados.keys():
        
        soma = soma + ((dados[pt] - media)**2)
    
    n = len(dados.keys())    #obtendo o tamanho da amosta
    
    desvpad = math.sqrt(soma/ (n-1))
    
    return desvpad
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo da mediana
#

def fMediana(dados):   
    
    dados_lista = list(dados.values())
   
    mediana = statistics.median(dados_lista)
    
    return mediana
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo do RMS
#

def fRms(dados):
    
    soma = 0
    
    for pt in dados.keys():
    
        soma = soma + (dados[pt]**2)
    
    
    n = len(dados.keys())     #obtendo o tamanho da amostra
    
    rms = math.sqrt(soma/n)
    
    return rms
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo do valor mínimo
#

def fMinimo(dados):

    dados_lista = list(dados.values())
    
    menor = dados_lista[0]
    
    for valor in dados_lista:
        
        if valor < menor: 
            menor = valor
    
    return menor
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo do valor máximo
#

def fMaximo(dados):

    dados_lista = list(dados.values())
    
    maior = dados_lista[0]
    
    for valor in dados_lista:
    
        if valor > maior: 
            maior = valor
    
    return maior


#--------------------------------------------------------------------------------------------------------
# Função para calcular Q1, quartil do método BoxPlot
#

def fCalcQ1(dados):
    
    tam = len(dados)
    q1 = 0.25*tam
    q1 = math.ceil(q1)
    dados_lista = sorted(list(dados.values()))
        
    return dados_lista[q1-1]

#--------------------------------------------------------------------------------------------------------
# Função para calcular Q3, quartil do método BoxPlot
#

def fCalcQ3(dados):
    
    tam = len(dados)
    q3 = 0.75*tam
    q3 = math.ceil(q3)
    dados_lista = sorted(list(dados.values()))
      
    return dados_lista[q3-1]

#--------------------------------------------------------------------------------------------------------
# Função para a identificação de outliers pelo método BoxPlot
#   

def fBoxPlot(dados,fator):
    
    fator = float(fator)
    
    #dados_lista = list(dados.values())
    
    
    #for pt in dados.keys():
        
        #dados_lista.append(dados[pt])
    
    # Calculando os quartis
    Q1 = fCalcQ1(dados)
    mediana = fMediana(dados)
    Q3 = fCalcQ3(dados)

    # Calculando o intervalo interquartil (IQR)
    IQR = Q3 - Q1
    
    #calculando os limites superiores e inferiores
    
    LS = Q3 + (fator*IQR)   #Limite superior
    
    LI = Q1 - (fator*IQR)   #Limite inferior
    
    #Criando um conjunto vazio para armazenar os outliers
    outliers = set()
    
    #Identificando os outliers
    
    for pt in dados.keys():
        
        if (dados[pt]>LS) or (dados[pt]<LI):
            
            outliers.add(pt)
    
    return outliers, LI, LS

#--------------------------------------------------------------------------------------------------------
# Função para a identificação de outliers pelo método 3sigma
#        

def f3sigma(dados, fator, escala, classe, op):

    #passando o fator e a escala para float
    
    fator = float(fator)
    
    escala = float(escala)
    
    #Calculando a tolerância com base no EP e na escala do produto 
    
    if (op ==1): #2d
        
        if classe ==0:
        
            maximo = fator * ((0.170/1000) * escala)
    
        elif classe ==1:
        
            maximo = fator * ((0.3/1000) * escala)
    
        elif classe == 2:
        
            maximo = fator * ((0.5/1000) * escala)
    
        else:
        
            maximo = fator * ((0.6/1000) * escala)
        
    
    else: #z
        
        if classe ==0:
        
            maximo = fator * ((1/6) * escala)
    
        elif classe ==1:
        
            maximo = fator * ((1/3) * escala)
    
        elif classe == 2:
        
            maximo = fator * ((2/5) * escala)
    
        else:
        
            maximo = fator * ((1/2) * escala)
  
    #Criando um conjunto vazio para armazenar os outliers
    outliers = set()
    
    #Identificando os outliers
    
    for pt in dados.keys():
        
        if (abs(dados[pt])> maximo):
            
            outliers.add(pt)
    
    return outliers, maximo
    
#--------------------------------------------------------------------------------------------------------
# Função para a realização do teste de normalidade
#  

def fTesteDeNormalidade(dados, niv_conf):
    
    # Atribuindo um nivel de significância com base no nível de confiança escolhido pelo usuário
    
    if niv_conf ==0:
        
        alfa = 0.25
    
    elif niv_conf ==1:
        
        alfa = 0.1
    
    elif niv_conf ==2:
        
        alfa = 0.05
        
    elif niv_conf ==3:
        
        alfa = 0.025
    
    else:
        
        alfa = 0.01
    
    #transformando os dados para lista e depois vetores(array)
    
    dados_lista = list(dados.values())

    dados_array = np.array(dados_lista)
    
    #Calculando as estáticas do teste e o p-value
    
    est, p_valor = stats.shapiro(dados_array)
    
    #Verificando a normalidade
    
    if p_valor > alfa:
        
        normalidade = 'Amostra Normal'
    
    else:
        
        normalidade = 'Amostra NÃO Normal'

    
    result = (est, p_valor, normalidade)

    return result

#Função para calcular o valor de t 
'''def valor_t_tabelado(probabilidade, graus_de_liberdade):
    # Calcula o valor t tabelado para a probabilidade e graus de liberdade especificados
    valor_t = t.ppf(probabilidade, graus_de_liberdade)
    return valor_t'''
 
 
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo dos azimutes das discrepâncias posicionais
# 
def fAzimute2D(dx,dy):
    
    azimutes2D = {}
    for pt in dx.keys():
        
        a = dx[pt]
        b =dy[pt]
        
        
        if a>0 and b>0:  #1º quadrante 
            
            az2D = math.atan(a/b)
            azimutes2D[pt] = math.degrees(az2D)
        
        elif a>0 and b<0: #2º quadrante
            
            az2D = math.atan(a/b)
            azimutes2D[pt] = math.degrees(az2D) + 180
        
        elif a<0 and b<0: #3º quadrante
            
            az2D = math.atan(a/b)
            azimutes2D[pt] = math.degrees(az2D) + 180
        
        elif a<0 and b>0: #4º quadrante
            
            az2D = math.atan(a/b)
            azimutes2D[pt] = math.degrees(az2D) + 360
        
        elif a==0 and b==0: # Não existe existe azimute
            
            azimutes2D[pt] = 0
            
        elif a>0 and b==0: #igual a 90 graus
            
            azimutes2D[pt] = 90
        
        elif a<0 and b==0: #igual a 270 graus
            
            azimutes2D[pt] = 270
        
        elif a==0 and b>0: #igual a 0 graus, os pontos formam uma reta na direção do norte, para cima
            
            azimutes2D[pt] = 0
        
        else: #igual a 180 graus, os pontos formam uma reta na direção do norte, para baixp
            
            azimutes2D[pt] = 180
        
    return azimutes2D    
            
#--------------------------------------------------------------------------------------------------------
# Função para a realização do teste de tendência t de student
#  
 
def fTdeStudent(dados,niv_conf):
    
    #calculando a média e o desvio padrão dos dados
    media = fMedia(dados)
    desv_pad = fDevPad(dados)
    
    raiz_n = math.sqrt(len(dados))
    
    #calculando o t calculado
    
    if media == 0:
    
        t_calc = 0
    
    elif desv_pad == 0:
        
        t_calc = 999999999
    
    else:
        
        t_calc = (media * raiz_n) / desv_pad
        
    
    #obtendo o t tabelado
    
    if niv_conf ==0:
        
        alfa = 0.25
    
    elif niv_conf ==1:
        
        alfa = 0.1
    
    elif niv_conf ==2:
        
        alfa = 0.05
        
    elif niv_conf ==3:
        
        alfa = 0.025
    
    else:
        
        alfa = 0.01
    
    #Definindo o nível de probabilidade e os graus de liberdade
    
    probabilidade = 1 -(alfa/2)  # A biblioteca trabalha com níveis de probabilidade unicaudal
    graus_de_liberdade = len(dados) -1
    
    t_tabelado = t.ppf(probabilidade, graus_de_liberdade)
    
    #realizando o teste de hipotese
    
    if abs(t_calc)<= t_tabelado:
        
        result = 'Não há tendência'
        return  result, t_calc, t_tabelado, True 
    
    else:
        result = 'Tendência'
        return result, t_calc, t_tabelado, False
        

def fMedia_Dir_e_Var_Circ(dx,dy):
    
    #Cálculo dos azimutes das discrepâncias 2D
    azimutes2D = fAzimute2D(dx,dy)
    
    #Cálculo do somatório dos senos e cossenos
    
    soma_seno = 0
    soma_cosseno = 0
    
    for pt in dx.keys():
        
        az2D = math.radians(azimutes2D[pt])
        soma_seno = soma_seno + math.sin(az2D)
        soma_cosseno = soma_cosseno + math.cos(az2D)
    
    a = soma_seno
    b = soma_cosseno
    
    az2D = math.atan(a/b)
        
    if a>0 and b>0:  #1º quadrante 
            
        az2D = math.degrees(az2D)
        
    elif a>0 and b<0: #2º quadrante
            
        az2D = math.degrees(az2D) + 180
        
    elif a<0 and b<0: #3º quadrante
            
        az2D = math.degrees(az2D) + 180
        
    elif a<0 and b>0: #4º quadrante
            
        az2D = math.degrees(az2D) + 360
    
    elif a==0 and b==0: # Não existe azimute
            
        az2D = 0
            
    elif a>0 and b==0: #igual a 90 graus
            
        az2D = 90
        
    elif a<0 and b==0: #igual a 270 graus
            
        az2D = 270
        
    elif a==0 and b>0: #igual a 0 graus, os pontos formam uma reta na direção do norte, para cima
            
        az2D = 0
        
    else: #igual a 180 graus, os pontos formam uma reta na direção do norte, para baixp
            
        az2D = 180 
    
    media_dir = az2D
    # Calculando o comprimento dos vetores e a variância circular
    
    comp_vetor = math.sqrt( (soma_seno**2) + (soma_cosseno**2))
    
    #obtendo o tamanho da amostra de discrepâncias
    
    n = len(dx)
    
    var_circular = 1 - (comp_vetor/n)
    
    return soma_seno, soma_cosseno, media_dir, var_circular
    
#--------------------------------------------------------------------------------------------------------
# Função para o cálculo do MAD : Mean absolute deviation (Desvio médio absoluto)
# 

def fCalcMAD(dados):
    
    # Obtendo a média dos dados
    media = fMedia(dados)
    soma = 0
    
    for pt in dados.keys():
        
        incremento = abs( dados[pt] - media )
        soma = soma + incremento
    
    n = len(dados) # obtendo o tamanho da amostra
    mad = soma/n
    
    return mad

#--------------------------------------------------------------------------------------------------------
# Função para verificação das condições do decreto 89817
# 

def fVerifica(dados, pec, ep):
   
   
    rms_disc = fRms(dados)
    soma = 0
    
    for pt in dados.keys():
        
        if abs(dados[pt]) <= pec:
            
            soma = soma + 1
    
    percent = soma / len(dados)
    
    if (percent >= 0.9) and (rms_disc <= ep):
        
        return (True, percent*100, 'Passou')
    
    elif (rms_disc <= ep):
        
        return (False, percent*100, 'Passou')
    
    else:
        
        return (False, percent*100, 'Falhou')

#--------------------------------------------------------------------------------------------------------
# Função para preenchimento das tolerâncias das classes previstas na ET-CQDG para planimetria
#

def fClassesETpla(dados,escala):
    
    escala = float(escala)
    
    pec_A = 0.00028 * escala
    pec_B = 0.00050 * escala
    pec_C = 0.00080 * escala
    pec_D = 0.00100 * escala      
    
    EP_A = 0.00017 * escala
    EP_B = 0.00030 * escala
    EP_C = 0.00050 * escala
    EP_D = 0.00060 * escala
    
    classeA = fVerifica(dados, pec_A, EP_A)
    classeB = fVerifica(dados, pec_B, EP_B)
    classeC = fVerifica(dados, pec_C, EP_C)
    classeD = fVerifica(dados, pec_D, EP_D)
    
    resultado = {'A': {'PEC': pec_A, 'EP': EP_A, 'Resultado': classeA[0], 'Percent' : classeA[1], 'TestRMS' : classeA[2] },
                 'B': {'PEC': pec_B, 'EP': EP_B, 'Resultado': classeB[0], 'Percent' : classeB[1], 'TestRMS' : classeB[2] },
                 'C': {'PEC': pec_C, 'EP': EP_C, 'Resultado': classeC[0], 'Percent' : classeC[1], 'TestRMS' : classeC[2] },
                 'D': {'PEC': pec_D, 'EP': EP_D, 'Resultado': classeD[0], 'Percent' : classeD[1], 'TestRMS' : classeD[2] } }
  
    return resultado
        

#--------------------------------------------------------------------------------------------------------
# Função para preenchimento das tolerâncias das classes previstas na ET-CQDG para altimetria
#

def fClassesETalt(dados,escala):
    
    escala = float(escala)
    
    pec_A = 0.27 * escala                        
    pec_B = 0.5 * escala
    pec_C = (3/5) * escala
    pec_D = (3/4) * escala      
    
    EP_A = (1/6) * escala
    EP_B = (1/3) * escala
    EP_C = (2/5) * escala
    EP_D = 0.5*escala
    
    classeA = fVerifica(dados, pec_A, EP_A)
    classeB = fVerifica(dados, pec_B, EP_B)
    classeC = fVerifica(dados, pec_C, EP_C)
    classeD = fVerifica(dados, pec_D, EP_D)
    
    resultado = {'A': {'PEC': pec_A, 'EP': EP_A, 'Resultado': classeA[0], 'Percent' : classeA[1], 'TestRMS' : classeA[2] },
                 'B': {'PEC': pec_B, 'EP': EP_B, 'Resultado': classeB[0], 'Percent' : classeB[1], 'TestRMS' : classeB[2] },
                 'C': {'PEC': pec_C, 'EP': EP_C, 'Resultado': classeC[0], 'Percent' : classeC[1], 'TestRMS' : classeC[2] },
                 'D': {'PEC': pec_D, 'EP': EP_D, 'Resultado': classeD[0], 'Percent' : classeD[1], 'TestRMS' : classeD[2] } }
  
    return resultado
    

#--------------------------------------------------------------------------------------------------------
# Função para verificação das condições da NBR 13133
# 

def fCalcNBR(dados, precisao):
   
    tolerancia = precisao * 3
    
    soma = 0
    
    for pt in dados.keys():
        
        if abs(dados[pt]) <= tolerancia:
            
            soma = soma + 1
    
    percent = soma / len(dados)
    
    if (percent >= 0.9):
        
        percent = percent*100
        return True, percent
    
    else:
    
        percent = percent*100
        return False, percent


#--------------------------------------------------------------------------------------------------------
# Função para realizar as iterações nos dicionários de forma ordenada
# 

def itera(dados):
    
    chaves = list(dados.keys())
    lista = []
    
    for i in chaves:
        
        i = int(i)
        lista.append(i)
    
    lista = sorted(lista)
    lista_itera = []
    
    for pt in lista:
        
        lista_itera.append(str(pt))
    
    
    return lista_itera
    
        
