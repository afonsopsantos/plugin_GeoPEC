#-------------------------------------------------------------------------------------------------------- 
#   GeoPEC - Software científico para avaliação da acurácia posicional em dados cartográficos
#   Funções para a construção do relatório de processamento
#   Setembro de 2024
#   autores: Afonso P. Santos; João Vítor A. Gonçalves; Luis Philippe Ventura
#-------------------------------------------------------------------------------------------------------- 

#o que ta rodando atualmente

from ..libs.reportlab.lib.pagesizes import A4
from ..libs.reportlab.lib.styles import getSampleStyleSheet
from ..libs.reportlab.platypus import SimpleDocTemplate, Paragraph

from ..libs.reportlab.lib.styles import ParagraphStyle
from ..libs.reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
#from .libs.reportlab.platypus.doctemplate import PageCount
##############################################
# para definir o template

from ..libs.reportlab.lib.pagesizes import A4
from ..libs.reportlab.lib.units import inch
from ..libs.reportlab.platypus import SimpleDocTemplate, PageTemplate, BaseDocTemplate,  Frame, PageBreak #Image

# para fazer as tabelas
from ..libs.reportlab.lib.pagesizes import A4
from ..libs.reportlab.platypus import SimpleDocTemplate, Paragraph, Table , Image as RLImage
from ..libs.reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ..libs.reportlab.lib.units import inch
from ..libs.reportlab.lib import colors

#########################
#Para ler a imagem da memória
from ..libs.reportlab.lib.utils import ImageReader

####################
#Para mexer com as imagens
from PIL import Image

#########################
# Para fazer o gráfico

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import tempfile
import os

###################
#pra colocar a fonte Calibri

from ..libs.reportlab.pdfbase.ttfonts import TTFont
from ..libs.reportlab.pdfbase import pdfmetrics
# Registrar as fontes

from ..libs.reportlab.lib import fonts
from ..libs.reportlab.pdfbase.ttfonts import TTFont

#importando a data e hora atuais

from datetime import datetime

# Obter a data e hora atual - mudar e colocar na função geral por que se não pega a primeira hora
# que rodou o programa, ao invés de pegar a hora aual
now = datetime.now()

# Formatar a data e hora em uma string
current_time = now.strftime("%d/%m/%Y - %H:%M:%S")

#IMPORTANDO FUNCTIONS

from .normas_pec import *

import os
import platform
import subprocess

#Declarando variáveis globais

linha_traco = "_______________________________________________________________________________"

# Estilo para o texto
body_style = ParagraphStyle(
'Normal',
fontName = 'Helvetica',
fontSize = 10,
alignment = 4,  # Justificado
leading = 1.5,  # Espaçamento entre linhas em pontos
)

# Estilo para linhas centralizadas
text_style = body_style
centered_style = ParagraphStyle(
'Centered',
parent=text_style,
alignment=TA_CENTER,  # Centralizado
)


#--------------------------------------------------------------------------------------------------------
# Função principal para o processamento do relatório, controla todo o fluxo de geração de raltório, gerando
#os relatórios correspondentes as opções escolhidas pelo usuário
#

def fProcessamento_relatorio(dict_var):
    
    #obtendo a opção de processamento
    op = dict_var['op']
    
    now = datetime.now()
    # Formatar a data e hora em uma string
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    
    
    if (op==0) or (op==1) or (op==2): #ET CDQG   
        
        conteudo_relatorio_ETCQDG(dict_var, current_time)
        
    elif (op==3) or (op==4) or (op==5): #NBR 13133
        
        conteudo_relatorio_NBR(dict_var, current_time)
        
    elif (op==6): #INCRA
        
        conteudo_relatorio_INCRA(dict_var, current_time)
        
    else: #ANM
        
        conteudo_relatorio_ANM(dict_var, current_time)

#--------------------------------------------------------------------------------------------------------
# Função para abrir o pdf gerado no relatório
#        
def open_pdf(file_path):

    if platform.system() == 'Windows':
        os.startfile(file_path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file_path))
    else:  # Linux
        subprocess.call(('xdg-open', file_path))
        
#--------------------------------------------------------------------------------------------------------
# Função para gerar as tabelas de outliers para o relatório
#        
def tab_outliers_relatorio(op, dict_out):
#Este método gera as tabelas de outlier para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )   
    
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        if dict_out['var_metodo'] == 'Diagrama Boxplot':
        
            table_data = [
                [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
                [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_2D']}</b>", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)]
                ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 100, 100, 140] ) #colWidths=[120, 120, 120, 200])
            #colWidths=[100, 100, 100, 180]
            return table
        
        else:
            
            table_data = [
                [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Classe utilizada</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
                [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_classe_3_sigma']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_2D']}</b>", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)]
                ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88, 88] ) #colWidths=[120, 120, 120, 200])
            #colWidths=[100, 100, 100, 180]
            return table
            
    
    elif (op==1) or (op==4) or (op==8): #z
        
        if dict_out['var_metodo'] == 'Diagrama Boxplot':
        
            table_data = [ 
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_Z']}</b>", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
            ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 100, 100, 140])
            
            return table
        
        else:
            
            table_data = [
                [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Classe utilizada</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
                [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_classe_3_sigma']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_Z']}</b>", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
                ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88, 88] ) #colWidths=[120, 120, 120, 200])
            #colWidths=[100, 100, 100, 180]
            return table
    
    
    else: #2d e z
        
        if dict_out['var_metodo'] == 'Diagrama Boxplot':
        
            table_data = [ 
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table),  Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_2D']}</b>", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"<b>{dict_out['var_qtd_outliers_Z']}</b>", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
            ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 100, 100, 140])
            
            return table
        
        else:
            
            table_data = [ 
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Classe utilizada</b>", style_table),  Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_classe_3_sigma']}", style_table),  Paragraph(f"<b>{dict_out['var_qtd_outliers_2D']}</b>", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_classe_3_sigma']}", style_table),  Paragraph(f"<b>{dict_out['var_qtd_outliers_Z']}</b>", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
            ]
            
            table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88, 88])
            
            return table

#--------------------------------------------------------------------------------------------------------
# Função para auxiliar a gerar a tabela de estátisticas para o relatório
#        
def gera_table(op,dx,dy,dz,d2D,d3D):
    
    
    
    if (op==0) or (op==3) or (op==6) or (op==7):
        
        table = [[fMedia(dx), fMedia(dy),fMedia(d2D)],
                 [fMediana(dx), fMediana(dy), fMediana(d2D)],
                 [fMinimo(dx), fMinimo(dy), fMinimo(d2D)],
                 [fMaximo(dx), fMaximo(dy), fMaximo(d2D)],
                 [fDevPad(dx), fDevPad(dy), fDevPad(d2D)],
                 [fRms(dx), fRms(dy), fRms(d2D)],
                 [fCalcQ1(dx), fCalcQ1(dy), fCalcQ1(d2D)],
                 [fCalcQ3(dx), fCalcQ3(dy), fCalcQ3(d2D)],  
                 [fCalcMAD(dx), fCalcMAD(dy), fCalcMAD(d2D)]] 
    

        for i in range(len(table)):
        
            for j in range(3):
                    
                item = f"{table[i][j]:.3f}"
                table[i][j] = item

        
        return table
    
    elif (op==1) or (op==4) or (op==8):
     
        table = [fMedia(dz),
                fMediana(dz),
                fMinimo(dz),
                fMaximo(dz),
                fDevPad(dz),
                fRms(dz),
                fCalcQ1(dz),
                fCalcQ3(dz),  
                fCalcMAD(dz)] 
             
    
    
        for i in range(len(table)):

            item = f"{table[i]:.3f}"
            table[i] = item
        
        return table

    else:
        
        table = [[fMedia(dx), fMedia(dy), fMedia(dz), fMedia(d2D), fMedia(d3D)],
                 [fMediana(dx), fMediana(dy), fMediana(dz), fMediana(d2D), fMediana(d3D)],
                 [fMinimo(dx), fMinimo(dy), fMinimo(dz), fMinimo(d2D), fMinimo(d3D)],
                 [fMaximo(dx), fMaximo(dy), fMaximo(dz), fMaximo(d2D), fMaximo(d3D)],
                 [fDevPad(dx), fDevPad(dy), fDevPad(dz), fDevPad(d2D), fDevPad(d3D)],
                 [fRms(dx), fRms(dy), fRms(dz), fRms(d2D), fRms(d3D)],
                 [fCalcQ1(dx), fCalcQ1(dy), fCalcQ1(dz), fCalcQ1(d2D), fCalcQ1(d3D)],
                 [fCalcQ3(dx), fCalcQ3(dy), fCalcQ3(dz), fCalcQ3(d2D), fCalcQ3(d3D)],  
                 [fCalcMAD(dx), fCalcMAD(dy), fCalcMAD(dz), fCalcMAD(d2D), fCalcMAD(d3D)]] 
    
    
        for i in range(len(table)):            
            for j in range(5):
            
                item = f"{table[i][j]:.3f}"
                table[i][j] = item
        
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela de estátisticas descritivas do relatório
#
   
def tab_est_descritivas_relatorio(op, dx,dy,dz,d2D,d3D, pts_utilizados):
#Este método gera as tabelas de estátisticas descritivas para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
    
    #chama a função gera table para receber a tabela
    
    tabela = gera_table(op, dx,dy,dz,d2D,d3D)
    print('olha tabela', tabela)
    
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2D
    
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>d2D</b>", style_table)],
        [Paragraph("<b>nº de pontos (n)</b>", style_table)],
        [Paragraph("<b>Média</b>", style_table)],
        [Paragraph("<b>Mediana</b>", style_table)],
        [Paragraph("<b>Min</b>", style_table)],
        [Paragraph("<b>Max</b>", style_table)],
        [Paragraph("<b>Desv.padrão</b>", style_table)],
        [Paragraph("<b>RMS</b>", style_table)],
        [Paragraph("<b>Q1</b>", style_table)],
        [Paragraph("<b>Q3</b>", style_table)],
        [Paragraph("<b>MAD</b>", style_table)]
     ]
        
        #Inserindo o nº de pontos
        
       
        
        for i in range(3):
        
           table_data[1].append( Paragraph(f"{pts_utilizados}", style_table)) 
            
        for i in range(2,11):
            for j in range(0,3):                                   
                    valor = tabela[i-2][j]
                    table_data[i].append( Paragraph(f"{valor}", style_table)) 
                    
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")] , colWidths=[110, 110, 110, 110])
        
        #colWidths=[100, 70, 70, 100, 100]
        
        return table
     
     
    
    elif (op==1) or (op==4) or (op==8): #Z
        
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dZ</b>", style_table) ],
        [Paragraph("<b>nº de pontos (n)</b>", style_table), Paragraph(f"{pts_utilizados}", style_table)],
        [Paragraph("<b>Média</b>", style_table)],
        [Paragraph("<b>Mediana</b>", style_table)],
        [Paragraph("<b>Min</b>", style_table)],
        [Paragraph("<b>Max</b>", style_table)],
        [Paragraph("<b>Desv.padrão</b>", style_table)],
        [Paragraph("<b>RMS</b>", style_table)],
        [Paragraph("<b>Q1</b>", style_table)],
        [Paragraph("<b>Q3</b>", style_table)],
        [Paragraph("<b>MAD</b>", style_table)]
        ]
        
        for i in range(2,11):
            valor = tabela[i-2]
            table_data[i].append( Paragraph(f"{valor}", style_table))     
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[220, 220])
        
        return table
    
    
    else: #2D e Z
    
    
    
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>d2D</b>", style_table), Paragraph("<b>d3D</b>", style_table) ],
        [Paragraph("<b>nº de pontos (n)</b>", style_table)],
        [Paragraph("<b>Média</b>", style_table)],
        [Paragraph("<b>Mediana</b>", style_table)],
        [Paragraph("<b>Min</b>", style_table)],
        [Paragraph("<b>Max</b>", style_table)],
        [Paragraph("<b>Desv.padrão</b>", style_table)],
        [Paragraph("<b>RMS</b>", style_table)],
        [Paragraph("<b>Q1</b>", style_table)],
        [Paragraph("<b>Q3</b>", style_table)],
        [Paragraph("<b>MAD</b>", style_table)]
     ]
        
        #Inserindo o nº de pontos
        
        for i in range(5):
        
           table_data[1].append( Paragraph(f"{pts_utilizados}", style_table)) 
                              
                
        for i in range(2,11):
            for j in range(0,5):
                valor = tabela[i-2][j]
                table_data[i].append( Paragraph(f"{valor}", style_table))     
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 68, 68, 68, 68, 68])
        
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela de normalidade do relatório
#    
def tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, niv_conf):
#Este método gera as tabelas de normalidade para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
    
    #if op == 7 or op == 8 or op == 9:
    #niv_conf = 95
    # mudar aqui pra quando for ANM fazer com 95
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        result_dx = fTesteDeNormalidade(dx, niv_conf)
        result_dy = fTesteDeNormalidade(dy, niv_conf)
        result_d2D = fTesteDeNormalidade(d2D, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("X", style_table), Paragraph(f"{result_dx[0]:.3f}", style_table), Paragraph(f"{result_dx[1]:.3f}", style_table), Paragraph(f"<b>{result_dx[2]}</b>", style_table)],
            [Paragraph("Y", style_table), Paragraph(f"{result_dy[0]:.3f}", style_table), Paragraph(f"{result_dy[1]:.3f}", style_table), Paragraph(f"<b>{result_dy[2]}</b>", style_table)],           
            [Paragraph("2D", style_table), Paragraph(f"{result_d2D[0]:.3f}", style_table), Paragraph(f"{result_d2D[1]:.3f}", style_table), Paragraph(f"<b>{result_d2D[2]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110] ) #colWidths=[120, 120, 120, 200])
        
        return table
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        result_dz = fTesteDeNormalidade(dz, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{result_dz[0]:.3f}", style_table), Paragraph(f"{result_dz[1]:.3f}", style_table), Paragraph(f"<b>{result_dz[2]}</b>", style_table)]                
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110] )#colWidths=[120, 120, 120, 200])
        
        return table
    
    else: #2d e z
        
        result_dx = fTesteDeNormalidade(dx, niv_conf)
        result_dy = fTesteDeNormalidade(dy, niv_conf)
        result_dz = fTesteDeNormalidade(dz, niv_conf)
        result_d2D = fTesteDeNormalidade(d2D, niv_conf)
        result_d3D = fTesteDeNormalidade(d2D, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("X", style_table), Paragraph(f"{result_dx[0]:.3f}", style_table), Paragraph(f"{result_dx[1]:.3f}", style_table), Paragraph(f"<b>{result_dx[2]}</b>", style_table)],
            [Paragraph("Y", style_table), Paragraph(f"{result_dy[0]:.3f}", style_table), Paragraph(f"{result_dy[1]:.3f}", style_table), Paragraph(f"<b>{result_dy[2]}</b>", style_table)],           
            [Paragraph("Z", style_table), Paragraph(f"{result_dz[0]:.3f}", style_table), Paragraph(f"{result_dz[1]:.3f}", style_table), Paragraph(f"<b>{result_dz[2]}</b>", style_table)],
            [Paragraph("2D", style_table), Paragraph(f"{result_d2D[0]:.3f}", style_table), Paragraph(f"{result_d2D[1]:.3f}", style_table), Paragraph(f"<b>{result_d2D[2]}</b>", style_table)],
            [Paragraph("3D", style_table), Paragraph(f"{result_d3D[0]:.3f}", style_table), Paragraph(f"{result_d3D[1]:.3f}", style_table), Paragraph(f"<b>{result_d3D[2]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110] ) # colWidths=[120, 120, 120, 200])
        
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela de precisão do relatório
#
def tab_precisao_relatorio(op, tab_precisao):
#Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
    
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC(m)</b>", style_table),Paragraph("<b>EP(m)</b>", style_table), Paragraph("<b>%di <= PEC</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{tab_precisao[0][0]:.3f}", style_table),Paragraph(f"{tab_precisao[0][1]:.3f}", style_table),Paragraph(f"{tab_precisao[0][2]:.3f}", style_table), Paragraph(f"<b>{tab_precisao[0][3]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 70, 70, 100, 100])
        
        return table
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC(m)</b>", style_table),Paragraph("<b>EP(m)</b>", style_table),Paragraph("<b>%di <= PEC</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{tab_precisao[1][0]:.3f}", style_table),Paragraph(f"{tab_precisao[1][1]:.3f}", style_table),Paragraph(f"{tab_precisao[1][2]:.3f}", style_table), Paragraph(f"<b>{tab_precisao[1][3]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 70, 70, 100, 100])
        
        return table
    
    else: #2d e z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC(m)</b>", style_table),Paragraph("<b>EP(m)</b>", style_table), Paragraph("<b>%di <= PEC</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{tab_precisao[0][0]:.3f}", style_table),Paragraph( f"{tab_precisao[0][1]:.3f}", style_table), Paragraph(f"{tab_precisao[0][2]:.3f}", style_table), Paragraph( f"<b>{tab_precisao[0][3]}</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{tab_precisao[1][0]:.3f}", style_table),Paragraph( f"{tab_precisao[1][1]:.3f}", style_table), Paragraph(f"{tab_precisao[1][2]:.3f}", style_table), Paragraph( f"<b>{tab_precisao[1][3]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[100, 70, 70, 100, 100])
        
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela de tendência do relatório
#    
def tab_tendencia_relatorio(op, tab_t, tab_med):
#Este método gera as tabelas do teste de tendência para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
    
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table) , Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("X", style_table), Paragraph(f"{tab_t[0][0]:.3f}", style_table), Paragraph(f"{tab_t[0][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[0][2]}</b>", style_table)],
            [Paragraph("Y", style_table), Paragraph(f"{tab_t[1][0]:.3f}", style_table), Paragraph(f"{tab_t[1][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[1][2]}</b>", style_table)]                  
            ]
        
        table_data_med = [
            [Paragraph("<b>Somatório sen(Az)</b>", style_table), Paragraph("<b>Somatório cos(Az)</b>", style_table),Paragraph("<b>Média direcional </b>", style_table), Paragraph("<b>Variância circular</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph(f"{tab_med[0]:.3f}", style_table), Paragraph(f"{tab_med[1]:.3f}", style_table),Paragraph(f"{tab_med[2]:.2f}º", style_table), Paragraph(f"{tab_med[3]:.3f}", style_table), Paragraph(f"<b>{tab_med[4]}</b>", style_table) ]
            ]
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110])
        table_med = Table(table_data_med, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88, 88])
        
        return table_t, table_med
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table), Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{tab_t[0]:.3f}", style_table), Paragraph(f"{tab_t[1]:.3f}", style_table), Paragraph(f"<b>{tab_t[2]}</b>", style_table)]   
            ]         
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110])

        return table_t
    
    else: #2d e z
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table), Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("X", style_table), Paragraph(f"{tab_t[0][0]:.3f}", style_table), Paragraph(f"{tab_t[0][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[0][2]}</b>", style_table)],
            [Paragraph("Y", style_table), Paragraph(f"{tab_t[1][0]:.3f}", style_table), Paragraph(f"{tab_t[1][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[1][2]}</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{tab_t[2][0]:.3f}", style_table), Paragraph(f"{tab_t[2][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[2][2]}</b>", style_table)]    
            ]
        
        
        
        table_data_med = [
            [Paragraph("<b>Somatório sen(Az)</b>", style_table), Paragraph("<b>Somatório cos(Az)</b>", style_table),Paragraph("<b>Média direcional </b>", style_table), Paragraph("<b>Variância circular</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph(f"{tab_med[0]:.3f}", style_table), Paragraph(f"{tab_med[1]:.3f}", style_table),Paragraph(f"{tab_med[2]:.2f}º", style_table), Paragraph(f"{tab_med[3]:.3f}", style_table), Paragraph(f"<b>{tab_med[4]}</b>", style_table) ]
            ]
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110, 110])
        table_med = Table(table_data_med, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88, 88])
        
        return table_t, table_med

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela de pontos utilizados do relatório
#
def tab_pontos_utilizados_relatorio( op, data, excluidos, outliers_2D, outliers_Z ):
#Este método gera as tabelas de pontos utilizados para o relatório de processamento

    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    ) 
    
    #tem que passar dx,dy,dz, outliers, excluidos e etc
    dx, dy, dz = fDiscrepancia(data)
    
    d2D = fDiscrepancia2D(dx, dy)
    d3D = fDiscrepancia3D(dx, dy, dz)
    azimutes2D = fAzimute2D(dx,dy)

    
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>d2D</b>", style_table),  Paragraph("<b>Azim.2D</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
    
        
        for pt in dx.keys(): #depois vai mudar a forma de iterar
            
            if (pt in outliers_2D) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            elif (pt in outliers_2D) and not(pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("Não", style_table) ])
            
            elif not(pt in outliers_2D) and (pt in excluidos):
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            else:
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[62.85,62.85,62.85,62.85,62.85,62.85,62.85])
        return table
        
        
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
    
        
        for pt in dz.keys(): #depois vai mudar a forma de iterar
            
            if (pt in outliers_Z) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            elif (pt in outliers_Z) and not(pt in excluidos):
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("Não", style_table) ])
       
            elif not(pt in outliers_Z) and (pt in excluidos):
              
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            else:
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[110, 110, 110,110 ])
        return table
    
    
    
    else: #2d e z
    
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>d2D</b>", style_table), Paragraph("<b>d3D</b>", style_table), Paragraph("<b>Azim.2D</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
        
        for pt in dx.keys(): #depois vai mudar a forma de iterar, depois ver soma de conjuntos 
        #Para não ter que fazer or em outliers
            
            if ((pt in outliers_2D) or (pt in outliers_Z)) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            elif ((pt in outliers_2D) or (pt in outliers_Z)) and not(pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("<b>Sim</b>", style_table), Paragraph("Não", style_table) ])
            
            elif not((pt in outliers_2D) or (pt in outliers_Z)) and (pt in excluidos):
              
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("<b>Sim</b>", style_table) ])
            
            else:
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[43.3,43.3 , 43.3, 43.3, 43.3, 43.3,60,60,60 ])
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar o relatório da norma ET-CQDG
#        
def conteudo_relatorio_ETCQDG(dict_var, current_time):
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  dict_var['dados']
    
    #obtendo a opção de processamento
    op = dict_var['op']
    #obtendo o caminho do diretorio
    plugin_dir = dict_var['plugin_dir'] 
    
    def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>GeoPEC: Relatório de Processamento da Acurácia Posicional{'&nbsp;'*82}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'
            #'GeoPEC: Relatório de processamento da Acurácia Posicional'
            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
            
    
    linha_traco = "_______________________________________________________________________________"
    
    if (op==0): #2D
 
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Decreto n. 89.817/1984 - Análise Planimétrica</b>",
        f"Metodologia: {dict_var['var_metodologia']}<br/><br/>"
        ]
        
        op_decreto = [
        f"O produto \"{dict_var['var_produto']}\", foi classificado com PEC-PCD <b>{dict_var['var_classe_2D']}</b>, na escala <b>1/{dict_var['var_escala_2D']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.<br/><br/>"
        ]
        
        op_etal = [
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_acurado2D']}</b> para a escala de <b>1/{dict_var['var_escala_2D']}</b>. O resultado do PEC-PCD foi <b>{dict_var['var_classe_2D']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        f"O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_precisao_2D']}</b> e <b>{dict_var['var_tendencia_2D']}</b>.<br/><br/>"

        ]
        
        if dict_var['opc'] ==1:
            
            content = content + op_etal
            
        else: 
            
            content = content + op_decreto
            
        
        
        continua_content = [
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_2D']:.3f}",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 ",
        "Análise Planimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>"
        
        ]
        
        content = content + continua_content
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D,dict_var['var_pts_utilizados'] )
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/><br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão 
        
        
        '''#Colocar os gráficos no relatório
        # Caminho para as imagens
        
        
        img1_path = plugin_dir +  "\\images\\image01.png" 
        img2_path = plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3 = rl_img2'''
        
        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img3 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias", body_style),
                             rl_img2,
                             PageBreak(),
                             Paragraph("<br/>Outliers", body_style),
                             rl_img3
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho'] # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        # Remover o arquivo temporário
        '''if os.path.exists(dict_var['imagem']):
            os.remove(dict_var['imagem'])'''
        
        open_pdf(file_path)
          
    elif (op==1): #Z
        
       
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Decreto n. 89.817/1984 - Análise Altimétrica</b>",
        f"Metodologia: {dict_var['var_metodologia']}<br/><br/>"
        ]
        
        
        op_decreto = [
        f"O produto \"{dict_var['var_produto']}\", foi classificado com PEC-PCD <b>{dict_var['var_classe_Z']}</b>, para a equidistância vertical de <b>{dict_var['var_escala_Z']}m</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "<br/><br/>"]
        
        op_etal = [
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_acuradoZ']}</b> para a equidistância vertical de <b>{dict_var['var_escala_Z']}m</b>. O resultado do PEC-PCD foi <b>{dict_var['var_classe_Z']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        f"O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_precisao_Z']}</b> e <b>{dict_var['var_tendencia_Z']}</b>.<br/><br/>"
        ]
        
        if dict_var['opc'] ==1:
            
            content = content + op_etal
            
        else: 
            
            content = content + op_decreto
 
        
        continua_content = [
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_Z']:.3f}",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 ",
        "Análise Altimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Equidistância vertical: {dict_var['var_escala_Z']}m",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>"
        ]
        
        content = content + continua_content
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        
        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas            
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_estatisticas
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])
        
        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]   
        
        formatted_content = formatted_content + content_outliers
      
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                
        formatted_content = formatted_content + content_normalide
        
        #recebe a tabela de tendênca            
        
        table_t  = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]        
        
        formatted_content = formatted_content + content_precisão
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        
        '''img1_path = plugin_dir +  "\\images\\image01.png" 
        img2_path = plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3 = rl_img2'''
        
        rl_img1 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img2 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)

        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Discrepâncias", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers", body_style),
                             rl_img2
                             ]    
        
        formatted_content = formatted_content + content_graficos
         
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho']  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        open_pdf(file_path) 

            
    else: #2D e Z
        
        
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Decreto n. 89.817/1984 - Análise Planimétrica</b>",
       f"Metodologia: {dict_var['var_metodologia']}<br/><br/>"
        ]
        
        op_decreto = [
        f"O produto \"{dict_var['var_produto']}\", foi classificado com PEC-PCD <b>{dict_var['var_classe_2D']}</b>, na escala <b>1/{dict_var['var_escala_2D']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.<br/><br/>"
        ]
        
        op_etal = [
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_acurado2D']}</b> para a escala de <b>1/{dict_var['var_escala_2D']}</b>. O resultado do PEC-PCD foi <b>{dict_var['var_classe_2D']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        f"O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_precisao_2D']}</b> e <b>{dict_var['var_tendencia_2D']}</b>.<br/><br/>"
        ]
        
        if dict_var['opc'] ==1:
            
            content = content + op_etal
            
        else: 
            
            content = content + op_decreto
        
        continua_content1 = [
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_2D']:.3f}",
        linha_traco        
        ]
        #"<br/><br/>"
        continua_content2 = ["<br/><br/>",
                            linha_traco,
                                "Padrão de acurácia utilizado: <b>Decreto n. 89.817/1984 - Análise Altimétrica</b>",
                                f"Metodologia: {dict_var['var_metodologia']}<br/><br/>"                               
                            ]
        
        
        content = content + continua_content1 + continua_content2
        
        op_decreto_z = [
        f"O produto \"{dict_var['var_produto']}\", foi classificado com PEC-PCD <b>{dict_var['var_classe_Z']}</b>, para a equidistância vertical de <b>{dict_var['var_escala_Z']}m</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.<br/><br/>"
        ]
        
        op_etal_z = [
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_acuradoZ']}</b> para a equidistância vertical de <b>{dict_var['var_escala_Z']}m</b>. O resultado do PEC-PCD foi <b>{dict_var['var_classe_Z']}</b>, de acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG."
        f"O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_precisao_Z']}</b> e <b>{dict_var['var_tendencia_Z']}</b>.<br/><br/>"
        ]
        
        if dict_var['opc'] ==1:
            
            content = content + op_etal_z
            
        else: 
            
            content = content + op_decreto_z
        
            
        continua_content3 = [
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_Z']:.3f}",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984",
        "Análise planimétrica e altimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
        f"Equidistância vertical: {dict_var['var_escala_Z']}m",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>"        
        ]
        
        content = content + continua_content3 
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]     
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
       
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc,body_style )]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])
        
          
        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]          
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/><br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão 
        
        #Colocar os gráficos no relatório
        
        
        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        rl_img3 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)
        rl_img4 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        rl_img5 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão planimetria", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             PageBreak(),
                             Paragraph("<br/>Discrepâncias planimetria", body_style),
                             rl_img2,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias altimetria", body_style),
                             rl_img3,
                             PageBreak(),
                             Paragraph("<br/>Outliers planimetria", body_style),
                             rl_img4,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers altimetria", body_style),
                             rl_img5
                             ] 
                     
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho']  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4) 
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        open_pdf(file_path)

#--------------------------------------------------------------------------------------------------------
# Função para gerar o relatório da norma ANM
#
def conteudo_relatorio_ANM(dict_var, current_time):
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  dict_var['dados']

    op = dict_var['op']
    #obtendo o caminho do diretorio
    plugin_dir = dict_var['plugin_dir'] 
    
    def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>GeoPEC: Relatório de Processamento da Acurácia Posicional{'&nbsp;'*82}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'
            #'GeoPEC: Relatório de processamento da Acurácia Posicional'
            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
            
    
    linha_traco = "_______________________________________________________________________________"
    
    
    if (op==7): #2D
        
     
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Resolução n. 123 de 2022 - ANM [Planimetria]</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_atende_ANM_2D']}</b> o processo de avaliação da acurácia posicional planimétrico da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        f"O produto foi classificado com PEC-PCD <b>{dict_var['var_classe_2D']}</b>, na escala <b>1/{dict_var['var_escala_2D']}</b>, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        f"O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_normalidade_2D']}</b> e <b>{dict_var['var_tendencia_2D']}</b>.<br/><br/>",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_2D']:.3f}",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM ",
        "Análise da Acurácia Posicional Planimétrica Absoluta",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>"
        ]
        
        ###################################################################################
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        

        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers        
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão
        
        #Colocando os gráficos no relatório 
        
        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img3 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias", body_style),
                             rl_img2,
                             PageBreak(),
                             Paragraph("<br/>Outliers", body_style),
                             rl_img3
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho'] # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)


        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

        open_pdf(file_path)
          
    elif (op==8): #Z
        
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Resolução n. 123 de 2022 - ANM [Altimetria]</b>",
        "<br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_atende_ANM_Z']}</b> o processo de avaliação da acurácia posicional altimétrica da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        f"O produto foi classificado com PEC-PCD <b>{dict_var['var_classe_Z']}</b>, para a equidistância vertical entre curvas de nível de <b>{dict_var['var_escala_Z']}m</b>, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        f"O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_normalidade_Z']}</b> e <b>{dict_var['var_tendencia_Z']}</b>.<br/><br/>",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_Z']:.3f}",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM ",
        "Análise da Acurácia Posicional Altimétrica Absoluta",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Equidistância vertical: {dict_var['var_escala_Z']}m",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>",
        ]

          
        ###################################################################################
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        
        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas            
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D,dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_estatisticas
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])
        
        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]   
        
        formatted_content = formatted_content + content_outliers
      
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                
        formatted_content = formatted_content + content_normalide
        
        #recebe a tabela de tendênca            
        
        table_t  = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]
     
        
        formatted_content = formatted_content + content_precisão
        
        #Colocar os gráficos no relatório
        # Caminho para as imagens
        
        rl_img1 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img2 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)

        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Discrepâncias", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers", body_style),
                             rl_img2
                             ]    
        
        formatted_content = formatted_content + content_graficos
         
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho']  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        open_pdf(file_path) 
            
    else: #2D e Z
        
        #linha_traco = "_______________________________________________________________________________"
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO DA ACURÁCIA POSICIONAL</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Resolução n. 123 de 2022 - ANM [Planimetria]</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_atende_ANM_2D']}</b> o processo de avaliação da acurácia posicional planimétrico da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        f"O produto foi classificado com PEC-PCD <b>{dict_var['var_classe_2D']}</b>, na escala <b>1/{dict_var['var_escala_2D']}</b>, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        f"O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_normalidade_2D']}</b> e <b>{dict_var['var_tendencia_2D']}</b>.<br/><br/>",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_2D']:.3f}",
        linha_traco,        
        "<br/><br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>Resolução n. 123 de 2022 - ANM [Altimetria]</b><br/><br/>",      
        f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_atende_ANM_Z']}</b> o processo de avaliação da acurácia posicional altimétrica da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        f"O produto foi classificado com PEC-PCD <b>{dict_var['var_classe_Z']}</b>, para a equidistância vertical entre curvas de nível de <b>{dict_var['var_escala_Z']}m</b>, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        f"O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: <b>{dict_var['var_normalidade_Z']}</b> e <b>{dict_var['var_tendencia_Z']}</b>.<br/><br/>",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_Z']:.3f}",
        linha_traco,
        PageBreak(),                
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM",
        "Análise da Acurácia Posicional Planimétrica e Altimétrica Absoluta",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
        f"Equidistância vertical: {dict_var['var_escala_Z']}m",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>",
        ]
        
        ############################
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]     
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
       
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc,body_style )]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])
        
          
        content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]          
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão 
        
        
        #Colocar os gráficos no relatório

        #Colocar os gráficos no relatório
        
        
        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        rl_img3 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)
        rl_img4 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        rl_img5 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão planimetria", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             PageBreak(),
                             Paragraph("<br/>Discrepâncias planimetria", body_style),
                             rl_img2,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias altimetria", body_style),
                             rl_img3,
                             PageBreak(),
                             Paragraph("<br/>Outliers planimetria", body_style),
                             rl_img4,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers altimetria", body_style),
                             rl_img5
                             ] 
                     
    
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho']  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        '''def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*117}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    
     
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        open_pdf(file_path)

#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela do INCRA para o relatório
#
def tab_INCRA_relatorio(var_artificial_INCRA, var_natural_INCRA, var_inacessivel_INCRA):
#Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
        
    table_data = [
        [Paragraph("<b>Limites</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
        [Paragraph("Artificial (0,5m)", style_table), Paragraph(f"<b>{var_artificial_INCRA}</b>", style_table)],
        [Paragraph("Natural (3,0m)", style_table), Paragraph(f"<b>{var_natural_INCRA}</b>", style_table)],
        [Paragraph("Inacessível (7,5m)", style_table), Paragraph(f"<b>{var_inacessivel_INCRA}</b>", style_table)],
        ]
    
    table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
    
    return table
    
#--------------------------------------------------------------------------------------------------------
# Função para gerar o relatório da norma do INCRA
#
def conteudo_relatorio_INCRA(dict_var, current_time):
    
    dx,dy,dz,d2D,d3D, data =  dict_var['dados']
    
    #obtendo a opção de processamento
    op = dict_var['op']
    #obtendo o caminho do diretorio
    plugin_dir = dict_var['plugin_dir'] 
    
    def add_header_footer(canvas, doc):
        # Adicionar cabeçalho
        cabecalho = plugin_dir + "\\icon\\cabecalho.png"
        canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
    
        espc = "____________________________________________________________________________________________________"
        # Adicionar rodapé
        rodape_text = f"{espc}<br/>GeoPEC: Relatório de Processamento da Acurácia Posicional{'&nbsp;'*82}Página {canvas.getPageNumber()}<br/>{current_time}"
        #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
        #rodape_text += f'<br/>20/05/2024 - 16:56:23'
        #'GeoPEC: Relatório de processamento da Acurácia Posicional'
        styles = getSampleStyleSheet()
        rodape_style = styles['Normal']
        rodape_style.fontName = 'Helvetica'
        rodape_style.fontSize = 8
        rodape_style.alignment = 4  #Justificado

        rodape = Paragraph(rodape_text, rodape_style)
        rodape.wrap(doc.width, inch)
        rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé
            
    
    
    linha_traco = "_______________________________________________________________________________"
    
    content = [
    "<b>RELATÓRIO DE PROCESSAMENTO</b>",
    linha_traco,
    "<br/><br/>",
    "<b>DADOS DO PRODUTO</b>",
    linha_traco,
    "<br/>",
    f"Produto: {dict_var['var_produto']}",
    f"Local: {dict_var['var_local']}",
    f"Data: {dict_var['var_data']}",
    f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
    linha_traco,
    "<br/><br/>",
    "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
    "<br/>",
    linha_traco,
    "<br/>",
    "Padrão de acurácia utilizado: <b>Manual Técnico para Georreferenciamento de Imóveis Rurais - 2a edição - 2022 - INCRA</b>",
    "<br/><br/>",        
    f"O produto \"{dict_var['var_produto']}\", <b>{dict_var['var_atende_INCRA']}</b> o processo de avaliação da acurácia posicional absoluta do INCRA, em relação à alínea b do item 3.4.1 do Manual Técnico para Georreferenciamento do INCRA (2ª edição - 2022).",
    f"O produto foi classificado com PEC-PCD <b>{dict_var['var_classe_2D']}</b> , na escala <b>1/{dict_var['var_escala_2D']}</b>, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." 
    ]
    
    n_atende = [ "O posicionamento por este produto NÃO é adequado aos tipos de limites definidos na normativa do INCRA.<br/><br/>"
    ]
    
    atende = [ f"O valor do PEC-PCD corresponde à {dict_var['var_pec_INCRA']:.3f} metros, sendo ADEQUADA à precisão {dict_var['var_limites_INCRA']}.<br/><br/>"
    ]
    
    if (dict_var['var_atende_INCRA'] == 'ATENDE'):
        
        content = content + atende
    else:
        
        content = content + n_atende
    
    
    continua_content = [
    f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
    f"Precisão dos vértices (m): {dict_var['var_rms_2D']:.3f}<br/><br/>Nota: Conforme as normativas do INCRA a precisão dos vértices é igual ao RMS das discrepâncias posicionais.",
    linha_traco,        
    PageBreak(),
    "<br/><b>Relatório estatístico</b>",
    linha_traco,
    "<br/>",
    "Padrão de acurácia utilizado: Manual Técnico para Georreferenciamento de Imóveis Rurais - 2a edição - 2022 - INCRA ",
    "Análise da Acurácia Posicional Planimétrica Absoluta",
    linha_traco,
    "<br/>",
    "<b>Processamento</b><br/><br/>",
    f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
    f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
    f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
    linha_traco,
    "<br/>"
    ]
    
    content = content + continua_content
    
    # Estilo para o texto
    body_style = ParagraphStyle(
    'Normal',
    fontName= 'Helvetica',
    fontSize=10,
    alignment=4,  # Justificado
    leading= 15,  # Espaçamento entre linhas em pontos
    )
    
    # Estilo para linhas centralizadas
    text_style = body_style
    centered_style = ParagraphStyle(
    'Centered',
    parent=text_style,
    alignment=TA_CENTER,  # Centralizado
    )
    
    # Convertendo o conteúdo em parágrafos formatados
    formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]

    

    # Aplicando o estilo centralizado às linhas desejadas
    formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



    espc = linha_traco
    
    #recebe a tabela de estátisticas descritivas  
    
    table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
    
    content_estatisticas = [Paragraph("<br/><b>Estatísticas descritivas</b><br/><br/>", body_style),
                         table_est,
                         Paragraph(espc, body_style)]
                         
    formatted_content = formatted_content + content_estatisticas 
    
    #recebe a tabela de outliers            
    table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

    content_outliers = [Paragraph("<br/><b>Outliers</b><br/><br/>", body_style),
                         table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                         Paragraph(espc, body_style)]         
  
    formatted_content = formatted_content + content_outliers
    
    #recebe a tabela de teste de normalidade
    table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
    
    content_normalide = [PageBreak(),
                         Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                         table_normalidade,
                         Paragraph(espc, body_style)]
                         
    formatted_content = formatted_content + content_normalide                    
                         
  
    #recebe a tabela de tendênca            
    table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
    
    content_tendencia = [Paragraph(f"<br/><b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                         table_t,
                         Paragraph("<br/>Estatistica espacial<br/><br/>", body_style),
                         table_med,
                         Paragraph(espc, body_style)]
    
    formatted_content = formatted_content + content_tendencia
    
    #recebe a tabela de precisão            
    table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
    
    content_precisão = [PageBreak(),
                            Paragraph("<br/><b>Teste de precisão</b><br/><br/>", body_style),
                             table_precisao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= PEC\"</b> corresponde a porcentagem de discrepâncias menores ou iguais ao PEC da classe utilizada."  , body_style),
                             Paragraph(espc, body_style)]

    formatted_content = formatted_content + content_precisão 
    
    
    #recebe a tabela de vértices do INCRA            
    table_INCRA = tab_INCRA_relatorio(dict_var['var_artificial_INCRA'], dict_var['var_natural_INCRA'], dict_var['var_inacessivel_INCRA'])
    
    content_limites = [Paragraph("<br/><b>Tipos de limites</b><br/><br/>", body_style),
                         table_INCRA,
                         Paragraph(espc, body_style)]

    formatted_content = formatted_content + content_limites
    
    rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
    rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
    rl_img3 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
    
    content_graficos = [PageBreak(),
                        Paragraph("<b>Gráficos</b><br/><br/>Dispersão", body_style),
                         rl_img1,
                         Paragraph(espc, body_style),
                         Paragraph("Discrepâncias", body_style),
                         rl_img2,
                         PageBreak(),
                         Paragraph("<br/>Outliers", body_style),
                         rl_img3
                         ]    
    
    formatted_content = formatted_content + content_graficos
    
    
    #Colocar agora a tabela de discrepâncias e pontos de checagem
    #recebe a tabela dos pontos            
    table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
    #
    content_pontos = [PageBreak(),
                        Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                         table_pontos,
                         Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                         ]
    
    formatted_content = formatted_content + content_pontos

    #criando o arquivo PDF

    file_path = dict_var['caminho'] # Caminho para salvar o arquivo PDF
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    open_pdf(file_path)
    
    
#--------------------------------------------------------------------------------------------------------
# Função para gerar a tabela da NBR para o relatório
#    
def tab_NBR_relatorio(op, dict_NBR):
    
    #Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Centralizado
    leading= 15,  # Espaçamento entre linhas em pontos
    )    
    
    
    if (op==3): #2D
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>%di <= Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{dict_NBR['var_precisao_2D']}", style_table),Paragraph(f"{dict_NBR['var_tolerancia_2D']}", style_table), Paragraph(f"{dict_NBR['var_percent_2D']}", style_table), Paragraph(f"<b>{dict_NBR['var_result_2D']}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88,88])
        
        return table
        
    
    elif (op==4): #z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>%d(i) <= Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{dict_NBR['var_precisao_Z']}", style_table),Paragraph(f"{dict_NBR['var_tolerancia_Z']}", style_table), Paragraph(f"{dict_NBR['var_percent_Z']}", style_table), Paragraph(f"<b>{dict_NBR['var_result_Z']}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88,88])
        
        return table
    
    else: #2D e z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>%d(i) <= Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{dict_NBR['var_precisao_2D']}", style_table),Paragraph(f"{dict_NBR['var_tolerancia_2D']}", style_table), Paragraph(f"{dict_NBR['var_percent_2D']}", style_table), Paragraph(f"<b>{dict_NBR['var_result_2D']}</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{dict_NBR['var_precisao_Z']}", style_table),Paragraph(f"{dict_NBR['var_tolerancia_Z']}", style_table), Paragraph(f"{dict_NBR['var_percent_Z']}", style_table), Paragraph(f"<b>{dict_NBR['var_result_Z']}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[88, 88, 88, 88,88])
        
        return table

#--------------------------------------------------------------------------------------------------------
# Função para gerar o relatório da norma NBR 13133
#
def conteudo_relatorio_NBR(dict_var, current_time):
    
    dx,dy,dz,d2D,d3D, data =  dict_var['dados']
    
    #obtendo a opção de processamento
    op = dict_var['op']
    #obtendo o caminho do diretorio
    plugin_dir = dict_var['plugin_dir']
    dict_NBR = dict_var['var_NBR']
    
    linha_traco = "_______________________________________________________________________________"
    
    if (op==3): #2D
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>NBR 13.133 de 2021 - Análise Planimétrica</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\" foi <b>{dict_NBR['var_resultado_2D_NBR']}</b> no processo de inspeção topográfica planimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.2.",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021  ",
        "Análise da Acurácia Posicional Planimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>",
        ]
        
        ###################################################
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]  
            
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

        content_outliers = [Paragraph("<b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/><br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
               
        #############################
        #recebe a tabela de aceitação
        
        table_aceitacao = tab_NBR_relatorio(op, dict_NBR)
        
        content_aceitacao = [Paragraph("<b>Aceitação relativa</b><br/><br/>", body_style),
                             table_aceitacao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= Tolerância\"</b> corresponde a porcentagem de discrepâncias menores ou iguais a tolerância."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        
        #Colocar os gráficos no relatório
        
        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img3 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias", body_style),
                             rl_img2,
                             PageBreak(),
                             Paragraph("<br/>Outliers", body_style),
                             rl_img3
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho'] # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*117}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        # Remover o arquivo temporário
        '''if os.path.exists(dict_var['imagem']):
            os.remove(dict_var['imagem'])'''
        
        open_pdf(file_path)
          
          
    elif (op==4): #Z
        
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>NBR 13.133 de 2021 - Análise Altimétrica</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\" foi <b>{dict_NBR['var_resultado_Z_NBR']}</b> no processo de inspeção topográfica altimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.3.",
        linha_traco,        
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021",
        "Análise da Acurácia Posicional altimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>",
        ]
        
        ###################################################
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]  
            
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

        content_outliers = [Paragraph("<b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                      
        
        #recebe a tabela de tendênca            
        table_t  = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
               
        #############################
        #recebe a tabela de aceitação
        
        table_aceitacao = tab_NBR_relatorio(op, dict_NBR)
        
        content_aceitacao = [Paragraph("<b>Aceitação relativa</b><br/><br/>", body_style),
                             table_aceitacao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= Tolerância\"</b> corresponde a porcentagem de discrepâncias menores ou iguais a tolerância."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        
        #Colocar os gráficos no relatório
         
        rl_img1 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        rl_img2 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)

        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Discrepâncias", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers", body_style),
                             rl_img2
                             ]    
        
        formatted_content = formatted_content + content_graficos
                  
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho'] # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*117}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        # Remover o arquivo temporário
        '''if os.path.exists(dict_var['imagem']):
            os.remove(dict_var['imagem'])'''
        
        open_pdf(file_path)
      
    else: #2D e Z
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        linha_traco,
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        linha_traco,
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        linha_traco,
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>NBR 13.133 de 2021 - Análise Planimétrica</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\" foi <b>{dict_NBR['var_resultado_2D_NBR']}</b> no processo de inspeção topográfica planimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.2.",
        linha_traco,        
        "<br/><br/>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: <b>NBR 13.133 de 2021 - Análise Altimétrica</b><br/><br/>",        
        f"O produto \"{dict_var['var_produto']}\" foi <b>{dict_NBR['var_resultado_Z_NBR']}</b> no processo de inspeção topográfica altimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.3.",
        linha_traco,
        PageBreak(),
        "<br/><b>Relatório estatístico</b>",
        linha_traco,
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021",
        "Análise da Acurácia Posicional Planimétrica e Altimétrica",
        linha_traco,
        "<br/>",
        "<b>Processamento</b><br/><br/>",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        linha_traco,
        "<br/>",
        ]
        
        ###################################################
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName= 'Helvetica',
        fontSize=10,
        alignment=4,  # Justificado
        leading= 15,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) if type(text)== str else text for text in content ]  
            
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha

        espc = linha_traco
        
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['var_pts_utilizados'])
        
        content_estatisticas = [Paragraph("<b>Estatísticas descritivas</b><br/><br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])

        content_outliers = [Paragraph("<b>Outliers</b><br/><br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D, dict_var['niv_conf'])
        
        content_normalide = [PageBreak(),
                             Paragraph(f"<br/><b>Teste de normalidade</b><br/><br/>Teste de normalidade Shapiro-Wilk {dict_var['nc_shapiro']}<br/><br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph(f"<b>Teste de tendência</b><br/><br/>Teste t de Student {dict_var['nc_student']}<br/><br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/><br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
               
        #############################
        #recebe a tabela de aceitação
        
        table_aceitacao = tab_NBR_relatorio(op, dict_NBR)
        
        content_aceitacao = [Paragraph("<b>Aceitação relativa</b><br/><br/>", body_style),
                             table_aceitacao,
                             Paragraph("<br/><br/>Nota: <b>\"%di <= Tolerância\"</b> corresponde a porcentagem de discrepâncias menores ou iguais a tolerância."  , body_style),
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        
        
        #Colocar os gráficos no relatório

        rl_img1 = RLImage(dict_var['imagem_dispersao_2D'], width=525, height=300)
        rl_img2 = RLImage(dict_var['imagem_discrepancias_2D'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        rl_img3 = RLImage(dict_var['imagem_discrepancias_Z'], width=525, height=300)
        rl_img4 = RLImage(dict_var['imagem_outliers_2D'], width=525, height=300)
        rl_img5 = RLImage(dict_var['imagem_outliers_Z'], width=525, height=300)  # Usando o gráfico gerado na memória
        
        content_graficos = [PageBreak(),
                            Paragraph("<b>Gráficos</b><br/><br/>Dispersão planimetria", body_style),
                             rl_img1,
                             Paragraph(espc, body_style),
                             PageBreak(),
                             Paragraph("<br/>Discrepâncias planimetria", body_style),
                             rl_img2,
                             Paragraph(espc, body_style),
                             Paragraph("Discrepâncias altimetria", body_style),
                             rl_img3,
                             PageBreak(),
                             Paragraph("<br/>Outliers planimetria", body_style),
                             rl_img4,
                             Paragraph(espc, body_style),
                             Paragraph("Outliers altimetria", body_style),
                             rl_img5
                             ] 
                     
    
        formatted_content = formatted_content + content_graficos
        
        
        
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [PageBreak(),
                            Paragraph("<br/><b>Discrepâncias - Pontos de checagem</b><br/><br/>", body_style),
                             table_pontos,
                             Paragraph(f"<br/><br/><br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = dict_var['caminho']  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "____________________________________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*117}Página {canvas.getPageNumber()}<br/>{current_time}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Helvetica'
            rodape_style.fontSize = 8
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    

        #print('Olha o conteudo formatado', formatted_content)
        
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        open_pdf(file_path)
          
        
        #########################################################################
        