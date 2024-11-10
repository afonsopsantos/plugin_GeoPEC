#-------------------------------------------------------------------------------------------------------- 
#   GeoPEC - Software científico para avaliação da acurácia posicional em dados cartográficos
#   Funções para definicao do tamanho amostral no controle de qualidade cartográfica
#   março de 2024
#   autores: Afonso P. Santos; João Vítor A. Gonçalves; Luis Philippe Ventura
#-------------------------------------------------------------------------------------------------------- 

import math 


#--------------------------------------------------------------------------------------------------------
# Função para definir o tamanho amostral de acordo com a norma da ASPRS 2015
#
def fAsprs(area):
    
    # Passando a área digitada pelo usuário para float
    area = float(area)

    # Esta lista contém a tabela presente na norma
    table = [(1,500,750,25,20,10,30), 
             (2,750,1000,30,25,15,40),
             (3,1000,1250,35,30,20,50),
             (4,1250,1500,40,35,25,60),
             (5,1500,1750,45,40,30,70),
             (6,1750,2000,50,45,35,80),
             (7,2000,2250,55,50,40,90),
             (8,2250,2500,60,55,45,100)]
    
    # Calculos do tamanho amostral
    if area<0:
        return error  # Tratamento de erro  se o usuário digitar um valor negativo  
    
    elif area <= 500:
        n2d = 20
        nva = 20
        vva = 5
        n3d = 25

    elif area > 2500:
        d = math.ceil((area-2500)/500)
        n2d = '60*'
        nva =  55 + (d*3)
        vva =  45 + (d*2)
        n3d = 100 + (d*5)
    
    else:      
        for var in table:        
            if area > var[1] and area <= var[2]:           
                n2d = var[3]
                nva = var[4]
                vva = var[5]
                n3d = var[6]
    
    return [n2d,nva,vva,n3d]


#--------------------------------------------------------------------------------------------------------
# Função para definir o tamanho amostral de acordo com a NBR-13133 de 1994
#
def fNbr13133_94(pontos):
    
    # Passando os pontos digitados pelo usuário para float
    pts = float(pontos)
    
    # Calculos do tamanho amostral. A variável "n" é o número de pontos da amostra.
    if pts< 0:   
        return error  # Tratamento de erro  se o usuário digitar um valor negativo  
     
    elif pts <= 500:
        n = math.ceil(pts*0.03)
        if n<10:   
            n = 10
    
    elif pts <= 1000:
        n  = math.ceil(pts*0.02)      
        if n<15:       
            n = 15
    
    else:
        n = math.ceil(pts*0.01)
        if n<20:
            n = 20
    
    return n


#--------------------------------------------------------------------------------------------------------    
# Função para definir o tamanho amostral de acordo com a NBR-13133 de 2021
#
def fNbr13133_21(pontos):
    
    # Passando os pontos digitados pelo usuário para float
    pts = float(pontos)
    
    # Calculos do tamanho amostral. A variável "n" é o número de pontos da amostra.
    if pts< 0:
        return error
    
    elif pts <= 500:
        n = math.ceil(pts*0.03)  
        if n<10:   
            n = 10
    
    elif pts <= 1000:
        n  = math.ceil(pts*0.02)   
        if n<15:      
            n = 15
    
    else:
        n = math.ceil(pts*0.01)
        if n<30:
            n = 30
    
    return n


#-------------------------------------------------------------------------------------------------------- 
# Função para calcular o tamanho amostral pelo método de amostragem probabilística com população infinita
#
def fPopInfinita (desv,erro, index):
    
    # desvio padrão populacional
    desv = float(desv)

    # erro permissivel em porcentagem
    erro = float(erro)
    erro = (erro/100) * desv

    # nivel de confiança 
    index = index + 1
 
    # Verificando erros e atribuido o valor Z (dist. normal) do nível de confiança escolhido
    if desv <0 or erro<0:  
        return error
        
    elif index == 1:   
        z = 0.675

    elif index == 2:   
        z = 1
            
    elif index == 3:  
        z = 1.645
            
    elif index == 4:  
        z = 1.96
            
    else:   
        z = 2.575            
    
    # Cálculo do tamanho amostral 
    amostra = math.ceil ( ((z**2) * (desv**2)) / erro**2)
    
    return amostra


#-------------------------------------------------------------------------------------------------------- 
# Função para calcular o tamanho amostral pelo método de amostragem probabilística com população finita
#
def fPopFinita (pop,desv,erro, index):

    # tamanho populacional
    pop = float(pop)

    # desvio padrão populacional
    desv = float(desv)

    # erro permissivel em porcentagem
    erro = float(erro)
    erro = (erro/100) * desv

    # nivel de confiança 
    index = index + 1

    # Verificando erros e atribuido o valor Z (dist. normal) do nível de confiança escolhido
    if desv <0 or erro<0 or pop<0:  
        return error

    elif index == 1:    
        z = 0.675

    elif index == 2:  
        z = 1
            
    elif index == 3:   
        z = 1.645
            
    elif index == 4:    
        z = 1.96
            
    else:  
        z = 2.575            
    
    # Cálculo do tamanho amostral
    amostra = math.ceil ( ( (z**2) * (desv**2) * pop ) / ( (erro**2)*(pop-1) + ((z**2) * (desv**2)) ) )
    
    return amostra


#-------------------------------------------------------------------------------------------------------- 
# Função para o cálculo do número de células total conforme a amostragem espacial da ET-CQDG 
#    
def fCelulas(area, escala):
    
    # Passando a a área e a escala para float
    area = float(area)
    escala = float(escala)
    

    if area <0:    
        return error
    
    # Cálculo do número de células
    else:
        tam = (escala * 0.04)**2  # area da celula. lado de 4cm no valor da escala
        area = area * 1000000     # convertendo a área de km² para m²
        celulas = round(area/tam)
    
    return celulas


#--------------------------------------------------------------------------------------------------------     
# Função para o cálculo amostral da ET-CQDG lote a lote, baseado na ISO 2859-1
#
def fIso2859_1(amost, index01, index02):
    
    # número de células válidas
    amost = float(amost)

    # Verificando erro e definindo as tabelas da ISO
    if amost<0: 
        return error
    
    else:
        table = [(0,2,8), 
            (1,9,15),
            (2,16,25),
            (3,26,50),
            (4,51,90),
            (5,91,150),
            (6,151,280),
            (7,281,500),
            (8,501,1200),
            (9,1201,3200),
            (10,3201,10000),
            (11,10001,35000),
            (12,35001,150000),
            (13,150001,500000)]
            
        nivInsp = [{'I': 1,'II': 1,'III': 2}, 
               {'I': 1,'II': 2,'III': 3}, 
               {'I': 2,'II': 3,'III': 4}, 
               {'I': 3,'II': 4,'III': 5}, 
               {'I': 3,'II': 5,'III': 6}, 
               {'I': 4,'II': 6,'III': 7}, 
               {'I': 5,'II': 7,'III': 8}, 
               {'I': 6,'II': 8,'III': 10},  
               {'I': 7,'II': 10,'III': 11}, 
               {'I': 8,'II': 11,'III': 12}, 
               {'I': 10,'II': 12,'III': 13}, 
               {'I': 11,'II': 13,'III': 14}, 
               {'I': 12,'II': 14,'III': 16},
               {'I': 13,'II': 16,'III': 17},
               {'I': 14,'II': 17,'III': 18}]          
       
        tab = [{'tamost': 2,'letra': 'A','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 0,'2,5': 0,'4': 0,'6,5': 0,'10': 0,'15': 1,'25': 2},
           {'tamost': 3,'letra': 'B','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 0,'2,5': 0,'4': 0,'6,5': 0,'10': 1,'15': 1,'25': 2},
           {'tamost': 5,'letra': 'C','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 0,'2,5': 0,'4': 1,'6,5': 1,'10': 1,'15': 2,'25': 3},
           {'tamost': 8,'letra': 'D','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 0,'2,5': 1,'4': 1,'6,5': 1,'10': 2,'15': 3,'25': 5},
           {'tamost': 13,'letra': 'E','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 0,'2,5': 1,'4': 1,'6,5': 2,'10': 3,'15': 5,'25': 7},
           {'tamost': 20,'letra': 'F','0,4': 0,'0,65': 0,'1,0': 0,'1,5': 1,'2,5': 1,'4': 2,'6,5': 3,'10': 5,'15': 7,'25': 10},
           {'tamost': 32,'letra': 'G','0,4': 0,'0,65': 0,'1,0': 1,'1,5': 1,'2,5': 2,'4': 3,'6,5': 5,'10': 7,'15': 10,'25': 14},
           {'tamost': 50,'letra': 'H','0,4': 0,'0,65': 1,'1,0': 1,'1,5': 2,'2,5': 3,'4': 5,'6,5': 7,'10': 10,'15': 14,'25': 21},
            0,
           {'tamost': 80,'letra': 'J','0,4': 1,'0,65': 1,'1,0': 2,'1,5': 3,'2,5': 5,'4': 7,'6,5': 10,'10': 14,'15': 21,'25': 21},
           {'tamost': 125,'letra': 'K','0,4': 1,'0,65': 2,'1,0': 3,'1,5': 5,'2,5': 7,'4': 10,'6,5': 14,'10': 21,'15': 21,'25': 21},
           {'tamost': 200,'letra': 'L','0,4': 2,'0,65': 3,'1,0': 5,'1,5': 7,'2,5': 10,'4': 14,'6,5': 21,'10': 21,'15': 21,'25': 21},
           {'tamost': 315,'letra': 'M','0,4': 3,'0,65': 5,'1,0': 7,'1,5': 10,'2,5': 14,'4': 21,'6,5': 21,'10': 21,'15': 21,'25': 21},
           {'tamost': 500,'letra': 'N','0,4': 5,'0,65': 7,'1,0': 10,'1,5': 14,'2,5': 21,'4': 21,'6,5': 21,'10': 21,'15': 21,'25': 21},
            0,
           {'tamost': 800,'letra': 'P','0,4': 7,'0,65': 10,'1,0': 14,'1,5': 21,'2,5': 21,'4': 21,'6,5': 21,'10': 21,'15': 21,'25': 21},
           {'tamost': 1250,'letra': 'Q','0,4': 10,'0,65': 14,'1,0': 21,'1,5': 21,'2,5': 21,'4': 21,'6,5': 21,'10': 21,'15': 21,'25': 21},
           {'tamost': 2000,'letra': 'R','0,4': 14,'0,65': 21,'1,0': 21,'1,5': 21,'2,5': 21,'4': 21,'6,5': 21,'10': 21,'15': 21,'25': 21}]
        
        # index01 é o nível de inspeção
        if index01 == 0:
            insp = 'I'
    
        elif index01 == 1:
            insp = 'II'

        else:
            insp = 'III'
        
        # index02 é o LQA  
        if index02 == 0:
            lqa = '0,4'
    
        elif index02 == 1:
            lqa = '0,65'

        elif index02 == 2:
            lqa = '1,0'

        elif index02 == 3:
            lqa = '1,5'

        elif index02 == 4:
            lqa = '2,5'

        elif index02 == 5:
            lqa = '4'

        elif index02 == 6:
            lqa = '6,5'

        elif index02 == 7:
            lqa = '10'

        elif index02 == 8:
            lqa = '15'

        else:
            lqa = '25'        
    
        # Calculo do tamanho amostral
        if amost>= 500001:
            i = 14
            i = nivInsp[i][insp] - 1
    
        else:
            for var in table:
                if amost >= var[1] and amost<=var[2]:
                    i = var[0]
                    i = nivInsp[i][insp] - 1
            
        # definição da letra da tabela
        letra = tab[i]['letra']

        # definição do tamanho amostral e do numero de aceitação
        amostra = tab[i]['tamost']
        ac = tab[i][lqa]
    
        return letra, ac, amostra
       

#--------------------------------------------------------------------------------------------------------     
# Função para o cálculo amostral da ET-CQDG lote isolado, baseado na ISO 2859-2
#
def fIso2859_2(amost, index):
    
    #amost é número de células válidas
    amost = float(amost)
    
    # Verificando erro e definindo as tabelas da ISO referente ao QL. 
    #index é o LQA
    if amost<0: 
        return error
    
    else:
        if index == 0:
            lqa = '1,0'
    
        elif index==1:
            lqa = '4,0'
    
        else:
            lqa = '10'
    
        tabQL = [{'1,0': 12.5,'4,0': 32,'10': 32}, 
             {'1,0': 12.5,'4,0': 20,'10': 32},  
             {'1,0': 8,'4,0': 20,'10': 32},
             {'1,0': 5,'4,0': 20,'10': 32},
             {'1,0': 3.15,'4,0': 12.5,'10': 20}, 
             {'1,0': 3.15,'4,0': 8,'10': 20},
             {'1,0': 8,'4,0': 8,'10': 20}]
    
        tab01 = [(0,16,25),
             (1,26,50),
             (2,51,150),
             (3,151,1200),
             (4,1201,10000),
             (5,10001,150000)]
    
        # Definicao do QL
        if amost>=150001:
            i = 6
            ql = tabQL[i][lqa]
            ql = str(ql)
       
        else:
            for var in tab01:
                if amost>= var[1] and amost<=var[2]:  
                    i = var[0]
                    ql = tabQL[i][lqa]
                    ql = str(ql)
    
        # Definição das tabelas ISO de lote isolado
        table = [(0,16,25),
            (1,26,50),
            (2,51,90),
            (3,91,150),
            (4,151,280),
            (5,281,500),
            (6,501,1200),
            (7,1201,3200),
            (8,3201,10000),
            (9,10001,35000),
            (10,35001,150000),
            (11,150001,500000)]    
    
        tabAmost = [{'2': 50,'3,15': 50,'5': 28,'8': 17,'12,5': 13,'20': 9,'32': 6}, 
                {'2': 50,'3,15': 50,'5': 28,'8': 22,'12,5': 15,'20': 10,'32': 6}, 
                {'2': 50,'3,15': 44,'5': 34,'8': 24,'12,5': 16,'20': 10,'32': 8}, 
                {'2': 80,'3,15': 55,'5': 38,'8': 26,'12,5': 18,'20': 13,'32': 13}, 
                {'2': 95,'3,15': 65,'5': 42,'8': 28,'12,5': 20,'20': 20,'32': 13}, 
                {'2': 105,'3,15': 80,'5': 50,'8': 32,'12,5': 32,'20': 20,'32': 20}, 
                {'2': 125,'3,15': 125,'5': 80,'8': 50,'12,5': 32,'20': 32,'32': 32}, 
                {'2': 200,'3,15': 125,'5': 125,'8': 80,'12,5': 50,'20': 50,'32': 50}, 
                {'2': 200,'3,15': 200,'5': 200,'8': 125,'12,5': 80,'20': 80,'32': 80}, 
                {'2': 315,'3,15': 315,'5': 315,'8': 200,'12,5': 125,'20': 125,'32': 80}, 
                {'2': 500,'3,15': 500,'5': 500,'8': 315,'12,5': 200,'20': 125,'32': 80}, 
                {'2': 800,'3,15': 800,'5': 500,'8': 315,'12,5': 200,'20': 125,'32': 80},
                {'2': 1250,'3,15': 800,'5': 500,'8': 315,'12,5': 200,'20': 125,'32': 80}]
    
        tabAC = [{'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 0,'20': 0,'32': 0},
             {'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 0,'20': 0,'32': 0},
             {'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 0,'20': 0,'32': 0}, 
             {'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 0,'20': 0,'32': 1}, 
             {'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 0,'20': 1,'32': 1},
             {'2': 0,'3,15': 0,'5': 0,'8': 0,'12,5': 1,'20': 1,'32': 3}, 
             {'2': 0,'3,15': 1,'5': 1,'8': 1,'12,5': 1,'20': 3,'32': 5}, 
             {'2': 1,'3,15': 1,'5': 3,'8': 3,'12,5': 3,'20': 5,'32': 10}, 
             {'2': 1,'3,15': 3,'5': 5,'8': 5,'12,5': 5,'20': 10,'32': 18}, 
             {'2': 3,'3,15': 5,'5': 10,'8': 10,'12,5': 10,'20': 18,'32': 18}, 
             {'2': 5,'3,15': 10,'5': 18,'8': 18,'12,5': 18,'20': 18,'32': 18}, 
             {'2': 10,'3,15': 18,'5': 18,'8': 18,'12,5': 18,'20': 18,'32': 18}, 
             {'2': 18,'3,15': 18,'5': 18,'8': 18,'12,5': 18,'20': 18,'32': 18}]
             
        # Calculo do tamanho amostral
        # definição do tamanho amostral e do numero de aceitação
        if amost >= 500001: 
            amostra = tabAmost[12][ql]
            ac = tabAC[12][ql]
        
        else:
            for var in table:
                if amost>= var[1] and amost<= var[2]:  
                    i = var[0]
                    amostra = tabAmost[i][ql]
                    ac = tabAC[i][ql]
                
        return ql, amostra, ac
        


#--------------------------------------------------------------------------------------------------------    
# Função para definir o tamanho amostral de acordo com a norma de Portugal
#
def fCartTopPortugal(area,esc):
    
    # área. convertendo área de km² para has_key
    area = float(area)
    area = (area *100)

    # escala
    esc = float(esc)
    
    # Calculo do tamanho amostral
    if area>0:  
        if esc<=5000:  
            if area<1000:    
                amostra = 30
                return amostra
                
            else:   
                amostra = math.ceil(area/1000) * 20
                return amostra
        
        else:
            if area<25000:  
                amostra = 30
                return amostra
        
            else:  
                amostra = math.ceil(area/25000) * 20
                return amostra
    
    else:
        return error
                
            
           