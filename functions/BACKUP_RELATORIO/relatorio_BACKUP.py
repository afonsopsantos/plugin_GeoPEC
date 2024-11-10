#o que ta rodando atualmente

from .libs.reportlab.lib.pagesizes import A4
from .libs.reportlab.lib.styles import getSampleStyleSheet
from .libs.reportlab.platypus import SimpleDocTemplate, Paragraph

from .libs.reportlab.lib.styles import ParagraphStyle
from .libs.reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
#from .libs.reportlab.platypus.doctemplate import PageCount
##############################################
# para definir o template



from .libs.reportlab.lib.pagesizes import A4
from .libs.reportlab.lib.units import inch
from .libs.reportlab.platypus import SimpleDocTemplate, PageTemplate, BaseDocTemplate,  Frame #Image


# para fazer as tabelas
from .libs.reportlab.lib.pagesizes import A4
from .libs.reportlab.platypus import SimpleDocTemplate, Paragraph, Table , Image as RLImage
from .libs.reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .libs.reportlab.lib.units import inch
from .libs.reportlab.lib import colors

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



def tab_outliers_relatorio(op, dict_out):
#Este método gera as tabelas de outlier para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    op = 0
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        '''table_data = [ 
        [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
        [Paragraph("Planimetria", style_table), Paragraph("VAR_METODO", style_table), Paragraph("VAR_QTD_OUTLIERS_2D", style_table), Paragraph("VAR_LIMITE_2D", style_table)]
        ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table'''
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_qtd_outliers_2D']}", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[120, 120, 120, 200] ) #colWidths=[120, 120, 120, 200])
        
        return table
    
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data = [ 
        [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
        [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_qtd_outliers_Z']}", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
        ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[120, 120, 120, 200])
        
        return table
    
    else: #2d e z
        
        table_data = [ 
        [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Método</b>", style_table), Paragraph("<b>Outliers detectados</b>", style_table), Paragraph("<b>Valor limite - detecção</b>", style_table)],
        [Paragraph("Planimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_qtd_outliers_2D']}", style_table), Paragraph(f"{dict_out['var_limite_2D']}", style_table)],
        [Paragraph("Altimetria", style_table), Paragraph(f"{dict_out['var_metodo']}", style_table), Paragraph(f"{dict_out['var_qtd_outliers_Z']}", style_table), Paragraph(f"{dict_out['var_limite_Z']}", style_table)]
        ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")], colWidths=[120, 120, 120, 200])
        
        return table

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
        
        '''table = [[fMedia(dz)],
                 [ fMediana(dz)],
                 [ fMinimo(dz) ],
                 [ fMaximo(dz)],
                 [ fDevPad(dz)],
                 [ fRms(dz)],
                 [ fCalcQ1(dz)],
                 [ fCalcQ3(dz)],  
                 [ fCalcMAD(dz)]] '''
       
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
                

def tab_est_descritivas_relatorio(op, dx,dy,dz,d2D,d3D):
#Este método gera as tabelas de estátisticas descritivas para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=11,
    alignment=1,  # Centralizado
    leading= 16.5,  # Espaçamento entre linhas em pontos
    )   
    
    #chama a função gera table para receber a tabela
    
    tabela = self.gera_table(op, dx,dy,dz,d2D,d3D)
    print('olha tabela', tabela)
    
    
    if (op==0) or (op==3) or (op==6) or (op==7): #2D
    
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>d2D</b>", style_table)],
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
        
        for i in range(1,10):
            for j in range(1,4):
                valor = tabela[i-1][j-1]
                table_data[i].append( Paragraph(f"{valor}", style_table))     
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
     
     
    
    elif (op==1) or (op==4) or (op==8): #Z
        
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dZ</b>", style_table) ],
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
        
        for i in range(1,10):
            valor = tabela[i-1]
            table_data[i].append( Paragraph(f"{valor}", style_table))     
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
    
    
    else: #2D e Z
    
    
    
        table_data = [
        [Paragraph("<b>Estatísticas</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>d2D</b>", style_table), Paragraph("<b>d3D</b>", style_table) ],
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
        
        for i in range(1,10):
            for j in range(1,6):
                valor = tabela[i-1][j-1]
                table_data[i].append( Paragraph(f"{valor}", style_table))     
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
    
def tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D):
#Este método gera as tabelas de normalidade para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    
    op = 0
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        result_dx = fTesteDeNormalidade(dx, niv_conf)
        result_dy = fTesteDeNormalidade(dy, niv_conf)
        result_d2D = fTesteDeNormalidade(d2D, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("N", style_table), Paragraph(f"{result_dy[0]:.3f}", style_table), Paragraph(f"{result_dy[1]:.3f}", style_table), Paragraph(f"<b>{result_dy[2]}</b>", style_table)],
            [Paragraph("E", style_table), Paragraph(f"{result_dx[0]:.3f}", style_table), Paragraph(f"{result_dx[1]:.3f}", style_table), Paragraph(f"<b>{result_dx[2]}</b>", style_table)],
            [Paragraph("2D", style_table), Paragraph(f"{result_d2D[0]:.3f}", style_table), Paragraph(f"{result_d2D[1]:.3f}", style_table), Paragraph(f"<b>{result_d2D[2]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")] ) #colWidths=[120, 120, 120, 200])
        
        return table
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        result_dz = fTesteDeNormalidade(dz, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{result_dz[0]:.3f}", style_table), Paragraph(f"{result_dz[1]:.3f}", style_table), Paragraph(f"<b>{result_dz[2]}</b>", style_table)]                
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")] )#colWidths=[120, 120, 120, 200])
        
        return table
    
    else: #2d e z
        
        result_dx = fTesteDeNormalidade(dx, niv_conf)
        result_dy = fTesteDeNormalidade(dy, niv_conf)
        result_dz = fTesteDeNormalidade(dz, niv_conf)
        result_d2D = fTesteDeNormalidade(d2D, niv_conf)
        result_d3D = fTesteDeNormalidade(d2D, niv_conf)
        
        table_data = [
            [Paragraph("<b>Componente</b>", style_table), Paragraph("<b>Estatística W</b>", style_table), Paragraph("<b>P-value</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("N", style_table), Paragraph(f"{result_dy[0]:.3f}", style_table), Paragraph(f"{result_dy[1]:.3f}", style_table), Paragraph(f"<b>{result_dy[2]}</b>", style_table)],
            [Paragraph("E", style_table), Paragraph(f"{result_dx[0]:.3f}", style_table), Paragraph(f"{result_dx[1]:.3f}", style_table), Paragraph(f"<b>{result_dx[2]}</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{result_dz[0]:.3f}", style_table), Paragraph(f"{result_dz[1]:.3f}", style_table), Paragraph(f"<b>{result_dz[2]}</b>", style_table)],
            [Paragraph("2D", style_table), Paragraph(f"{result_d2D[0]:.3f}", style_table), Paragraph(f"{result_d2D[1]:.3f}", style_table), Paragraph(f"<b>{result_d2D[2]}</b>", style_table)],
            [Paragraph("3D", style_table), Paragraph(f"{result_d3D[0]:.3f}", style_table), Paragraph(f"{result_d3D[1]:.3f}", style_table), Paragraph(f"<b>{result_d3D[2]}</b>", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")] ) # colWidths=[120, 120, 120, 200])
        
        return table

def tab_precisao_relatorio(op, tab_precisao):
#Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    op = 0
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC</b>", style_table),Paragraph("<b>EP</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{tab_precisao[0][0]:.3f}", style_table),Paragraph(f"{tab_precisao[0][1]:.3f}", style_table), Paragraph(f"{tab_precisao[0][2]}", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC</b>", style_table),Paragraph("<b>EP</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{tab_precisao[1][0]:.3f}", style_table),Paragraph(f"{tab_precisao[1][1]:.3f}", style_table), Paragraph(f"{tab_precisao[1][2]}", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
    
    else: #2d e z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>PEC</b>", style_table),Paragraph("<b>EP</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph(f"{tab_precisao[0][0]:.3f}", style_table),Paragraph( f"{tab_precisao[0][1]:.3f}", style_table), Paragraph( f"{tab_precisao[0][2]}", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph(f"{tab_precisao[1][0]:.3f}", style_table),Paragraph( f"{tab_precisao[1][1]:.3f}", style_table), Paragraph( f"{tab_precisao[1][2]}", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
    
def tab_tendencia_relatorio(op, tab_t, tab_med):
#Este método gera as tabelas do teste de tendência para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    op = 0
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table) , Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("E", style_table), Paragraph(f"{tab_t[0][0]:.3f}", style_table), Paragraph(f"{tab_t[0][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[0][2]}</b>", style_table)],
            [Paragraph("N", style_table), Paragraph(f"{tab_t[1][0]:.3f}", style_table), Paragraph(f"{tab_t[1][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[1][2]}</b>", style_table)]                  
            ]
        
        table_data_med = [
            [Paragraph("<b>Somatório sen(Az)</b>", style_table), Paragraph("<b>Somatório cos(Az)</b>", style_table),Paragraph("<b>Média direcional </b>", style_table), Paragraph("<b>Variância circular</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph(f"{tab_med[0]:.3f}", style_table), Paragraph(f"{tab_med[1]:.3f}", style_table),Paragraph(f"{tab_med[2]:.3f}", style_table), Paragraph(f"{tab_med[3]:.3f}", style_table), Paragraph(f"<b>{tab_med[4]}</b>", style_table) ]
            ]
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        table_med = Table(table_data_med, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table_t, table_med
        
    
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table), Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{tab_t[0]:.3f}", style_table), Paragraph(f"{tab_t[1]:.3f}", style_table), Paragraph(f"<b>{tab_t[2]}</b>", style_table)]   
            ]         
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")])

        return table_t
    
    else: #2d e z
        
        table_data_t = [ 
            [Paragraph("<b>Componente</b>",style_table), Paragraph("<b>t tabelado</b>", style_table), Paragraph("<b>t calculado</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("E", style_table), Paragraph(f"{tab_t[0][0]:.3f}", style_table), Paragraph(f"{tab_t[0][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[0][2]}</b>", style_table)],
            [Paragraph("N", style_table), Paragraph(f"{tab_t[1][0]:.3f}", style_table), Paragraph(f"{tab_t[1][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[1][2]}</b>", style_table)],
            [Paragraph("Z", style_table), Paragraph(f"{tab_t[2][0]:.3f}", style_table), Paragraph(f"{tab_t[2][1]:.3f}", style_table), Paragraph(f"<b>{tab_t[2][2]}</b>", style_table)]    
            ]
        
        
        
        table_data_med = [
            [Paragraph("<b>Somatório sen(Az)</b>", style_table), Paragraph("<b>Somatório cos(Az)</b>", style_table),Paragraph("<b>Média direcional </b>", style_table), Paragraph("<b>Variância circular</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph(f"{tab_med[0]:.3f}", style_table), Paragraph(f"{tab_med[1]:.3f}", style_table),Paragraph(f"{tab_med[2]:.3f}", style_table), Paragraph(f"{tab_med[3]:.3f}", style_table), Paragraph(f"<b>{tab_med[4]}</b>", style_table) ]
            ]
        
        table_t = Table(table_data_t, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        table_med = Table(table_data_med, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table_t, table_med

def tab_pontos_utilizados_relatorio( op, data, excluidos, outliers_2D, outliers_Z ):
#Este método gera as tabelas de pontos utilizados para o relatório de processamento
# Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    #tem que passar dx,dy,dz, outliers, excluidos e etc
    dx, dy, dz = fDiscrepancia(data)
    
    d2D = fDiscrepancia2D(dx, dy)
    d3D = fDiscrepancia3D(dx, dy, dz)
    azimutes2D = fAzimute2D(dx,dy)

    outliers_2D = set()
    excluidos = set()
    op = 0
    if (op==0) or (op==3) or (op==6) or (op==7): #2d
        
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>d2D</b>", style_table),  Paragraph("<b>Azim.2D</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
    
        
        for pt in dx.keys(): #depois vai mudar a forma de iterar
            
            if (pt in outliers_2D) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Sim", style_table) ])
            
            elif (pt in outliers_2D) and not(pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Não", style_table) ])
            
            elif not(pt in outliers_2D) and (pt in excluidos):
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Sim", style_table) ])
            
            else:
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        return table
        
        
    elif (op==1) or (op==4) or (op==8): #z
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
    
        
        for pt in dz.keys(): #depois vai mudar a forma de iterar
            
            if (pt in outliers_Z) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Sim", style_table) ])
            
            elif (pt in outliers_Z) and not(pt in excluidos):
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Não", style_table) ])
       
            elif not(pt in outliers_Z) and (pt in excluidos):
              
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Sim", style_table) ])
            
            else:
                
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        return table
    
    
    
    else: #2d e z
    
        
        table_data = [[Paragraph("<b>ID</b>", style_table), Paragraph("<b>dX</b>", style_table), Paragraph("<b>dY</b>", style_table), Paragraph("<b>dZ</b>", style_table), Paragraph("<b>d2D</b>", style_table), Paragraph("<b>d3D</b>", style_table), Paragraph("<b>Azim.2D</b>", style_table), Paragraph("<b>Outlier</b>", style_table), Paragraph("<b>Excluido</b>", style_table) ]]
        
        for pt in dx.keys(): #depois vai mudar a forma de iterar, depois ver soma de conjuntos 
        #Para não ter que fazer or em outliers
            
            if ((pt in outliers_2D) or (pt in outliers_Z)) and (pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Sim", style_table) ])
            
            elif ((pt in outliers_2D) or (pt in outliers_Z)) and not(pt in excluidos):
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Sim", style_table), Paragraph("Não", style_table) ])
            
            elif not((pt in outliers_2D) or (pt in outliers_Z)) and (pt in excluidos):
              
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Sim", style_table) ])
            
            else:
            
                table_data.append([Paragraph(f"{pt}", style_table), Paragraph(f"{dx[pt]:.3f}", style_table), Paragraph(f"{dy[pt]:.3f}", style_table),Paragraph(f"{dz[pt]:.3f}", style_table), Paragraph(f"{d2D[pt]:.3f}", style_table), Paragraph(f"{d3D[pt]:.3f}", style_table),  Paragraph(f"{azimutes2D[pt]:.3f}", style_table), Paragraph("Não", style_table), Paragraph("Não", style_table) ])
            

        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        return table
        
def conteudo_relatorio(dict_var):
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  dict_var['dados']
    print('dx é:' , dx)
    print('dx é:' , dy)
    print('dx é:' , dz)
    
    #Depois vamos declaras content fora dos ifs
    
    op = dict_var['op']
    
    if (op==0): #2D
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        f"Produto: {dict_var['var_produto']}",
        f"Local: {dict_var['var_local']}",
        f"Data: {dict_var['var_data']}",
        f"Responsável Técnico: {dict_var['var_resp_tecnico']}",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 - Análise Planimétrica",
        f"Metodologia: {dict_var['var_metodologia']}",
        "<br/>"]
        
        op_decreto = [
        f"O produto {dict_var['var_produto']}, foi classificado com PEC-PCD VAR_CLASSE, na escala 1/{dict_var['var_escala_2D']}, de",
        "acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas ",
        "cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "<br/><br/>"]
        
        op_etal = [
        f"O produto {dict_var['var_produto']}, NÃO É ACURADO para a escala de 1/{dict_var['var_escala_2D']}. ",
        "O resultado do PEC-PCD foi VAR_CLASSE, de acordo com o Decreto n. 89.817",
        "de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        f"O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: {dict_var['var_precisao_2D']} e {dict_var['var_tendencia_2D']}.",
        "<br/><br/>"
        ]
        
        if op ==0:
            
            content = content + op_etal
        
        continua_content = [
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        f"RMS das discrepâncias (m): {dict_var['var_rms_2D']}",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 ",
        "Análise Planimétrica",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        f"Escala de Referência: 1/{dict_var['var_escala_2D']}",
        f"Pontos de checagem inseridos: {dict_var['var_pts_inseridos']}",
        f"Pontos de checagem utilizados: {dict_var['var_pts_utilizados']}",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        
        content = content + continua_content
        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName='Times-Roman',
        fontSize=12,
        alignment=4,  # Justificado
        leading= 18,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) for text in content]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(op,dx,dy,dz,d2D,d3D)
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio(op, dict_var['dict_outliers'])
        
        print('Olha a tabela de outliers:', table_outliers)
        
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio(op,dx,dy,dz,d2D,d3D)
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                    
                             
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio(op, dict_var['table t'],dict_var['table med'] )
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio(op, dict_var['table_precisao'])
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão 
        
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3 = rl_img2
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img3,
                             Paragraph(espc, body_style)
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = self.tab_pontos_utilizados_relatorio(op, data, dict_var['pts_excluidos'], dict_var['dict_outliers']['outliers_2D'], dict_var['dict_outliers']['outliers_Z'] )
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos
    
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio00.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 9
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
          
          
    elif (op==1): #Z
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 - Análise Altimétrica",
        "Metodologia: VAR_METODOLOGIA"    ,
        "<br/>"]
        
        op_decreto = [
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', foi classificado com PEC-PCD VAR_CLASSE, para a equidistância vertical de EQUISTm, de",
        "acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas ",
        "cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "<br/><br/>"]
        
        op_etal = [
        "O produto aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm, NÃO É ACURADO para a equidistância vertical de EQUISTm. ",
        "O resultado do PEC-PCD foi VAR_CLASSE, de acordo com o Decreto n. 89.817",
        "de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: VAR_PRECISO e VAR_TENDENCIA.",
        "<br/><br/>"
        ]
        
        continua_content = [
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 ",
        "Análise Altimétrica",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Equidistância vertical: 1/VAR_ESCALA",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]

        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas            
        #table_est
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de outliers            
        #table_outliers
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de teste de normalidade
        #table_normalidade
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de precisão            
        #table_precisao
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de tendênca            
        #table_t
        #table_med
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
        
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        '''img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img3,
                             Paragraph(espc, body_style)
                             ] 
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        #table_pontos
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]


            
    else: #2D e Z
    
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984 - Análise Planimétrica",
        "Metodologia: VAR_METODOLOGIA"    ,
        "<br/>"]
        
        op_decreto = [
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', foi classificado com PEC-PCD VAR_CLASSE, na escala 1/VAR_ESCALA, de",
        "acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas ",
        "cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "<br/><br/>"]
        
        op_etal = [
        "O produto aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm, NÃO É ACURADO para a escala de 1/VAR_ESCALA. ",
        "O resultado do PEC-PCD foi VAR_CLASSE, de acordo com o Decreto n. 89.817",
        "de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: VAR_PRECISO e VAR_TENDENCIA.",
        "<br/><br/>"
        ]
        
        continua_content1 = [
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS_2D",
        "_________________________________________________________________________",        
        "<br/><br/>",
        ]
        
        continua_content2 = ["_________________________________________________________________________",
                                "Padrão de acurácia utilizado: Decreto n. 89.817/1984 - Análise Altimétrica",
                                "Metodologia: VAR_METODOLOGIA",
                                "<br/>"
                            ]
        
        op_decreto_z = [
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', foi classificado com PEC-PCD VAR_CLASSE, para a equidistância vertical de EQUISTm, de",
        "acordo com o Decreto n. 89.817 de 20 de junho de 1984, que regulamenta as normas ",
        "cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "<br/><br/>"]
        
        op_etal_z = [
        "O produto aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm, NÃO É ACURADO para a equidistância vertical de EQUISTm. ",
        "O resultado do PEC-PCD foi VAR_CLASSE, de acordo com o Decreto n. 89.817",
        "de 20 de junho de 1984, que regulamenta as normas cartográficas brasileiras, aliada às tolerâncias da ET-CQDG.",
        "O produto foi submetido a análise de tendência e precisão em suas componentes posicionais, onde os resultados foram: VAR_PRECISO e VAR_TENDENCIA.",
        "<br/><br/>"
        ]
        
        continua_content3 = [
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS_Z",
        "_________________________________________________________________________",        
        "<br/><br/>",
        ]
        
        
        continua_content4 = [
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Decreto n. 89.817/1984",
        "Análise planimétrica e altimétrica",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Escala de Referência: 1/VAR_ESCALA",
        "Equidistância vertical: 1/VAR_ESCALA",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        
        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas            
        #table_est
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de outliers            
        #table_outliers
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de teste de normalidade
        #table_normalidade
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de precisão            
        #table_precisao
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de tendênca            
        #table_t
        #table_med
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragrapfh(espc, body_style)]
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        '''img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3
        rl_img4
        rl_img5'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão planimetria<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Dispersão altimetria<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Outliers planimetria<br/>", body_style),
                             rl_img3,
                             Paragraph("<br/>Outliers altimetria<br/>", body_style),
                             rl_img4,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img5,
                             Paragraph(espc, body_style)
                             ] 
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        #table_pontos
        #
        
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
                             
# Fazendo a ANM


def conteudo_relatorio_ANM():
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  self.var_relatorio
    print('dx é:' , dx)
    print('dx é:' , dy)
    print('dx é:' , dz)
    
    #Depois vamos declaras content fora dos ifs
    
    op = 0
    if (op==0): #2D
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n. 123 de 2022 - ANM [Planimetria]",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', <b>NÃO ATENDE</b> o processo de avaliação da acurácia posicional planimétrico da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        "O produto foi classificado com PEC-PCD VAR_CLASSE, na escala VAR_ESCALA, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        "O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: Amostra NÃO Normal e  NÃO TENDENCIOSO.",
        "<br/><br/>",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM ",
        "Análise da Acurácia Posicional Planimétrica Absoluta",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Escala de Referência: 1/VAR_ESCALA",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        

        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName='Times-Roman',
        fontSize=12,
        alignment=4,  # Justificado
        leading= 18,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) for text in content]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(dx,dy,dz,d2D,d3D)
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio()
        
        print('Olha a tabela de outliers:', table_outliers)
        
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio()
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                                         
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio()
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_precisao = tab_precisao_relatorio()
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_precisão
        
        '''#Colocar os gráficos no relatório
         # Caminho para as imagens
        img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        #rl_img3 = rl_img2'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img2,
                             Paragraph(espc, body_style)
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(data)
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
          
          
    elif (op==1): #Z
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n. 123 de 2022 - ANM [Altimetria]",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' <b>NÃO ATENDE</b> o processo de avaliação da acurácia posicional altimétrica da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        "O produto foi classificado com PEC-PCD VAR_CLASSE, para a equidistância vertical entre curvas de nível de 100m, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        "O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: Amostra NÃO Normal e  NÃO TENDENCIOSO.",
        "<br/><br/>",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM ",
        "Análise da Acurácia Posicional Altimétrica Absoluta",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Equidistância vertical: 1/VAR_ESCALA",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]

        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas            
        #table_est
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de outliers            
        #table_outliers
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de teste de normalidade
        #table_normalidade
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
               
      
        #recebe a tabela de tendênca            
        #table_t
        #table_med
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
                             
        #recebe a tabela de precisão            
        #table_precisao
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)]  
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        '''img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img3,
                             Paragraph(espc, body_style)
                             ] 
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        #table_pontos
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
          

            
    else: #2D e Z
    
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n. 123 de 2022 - ANM [Planimetria]",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', <b>NÃO ATENDE</b> o processo de avaliação da acurácia posicional planimétrico da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
        "O produto foi classificado com PEC-PCD VAR_CLASSE, na escala VAR_ESCALA, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
        "O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: Amostra NÃO Normal e  NÃO TENDENCIOSO.",
        "<br/><br/>",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "RMS das discrepâncias (m): VAR_RMS",
        "_________________________________________________________________________",        
        "<br/><br/>"
        ]
        
        continua_content1 = [
            "_________________________________________________________________________",
            "<br/>",
            "Padrão de acurácia utilizado: Resolução n. 123 de 2022 - ANM [Altimetria]",
            "<br/>",        
            "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' <b>NÃO ATENDE</b> o processo de avaliação da acurácia posicional altimétrica da ANM, em relação aos artigos 9° e 12° da Resolução n.123 de 2022 da ANM (Agência Nacional de Mineração).",
            "O produto foi classificado com PEC-PCD VAR_CLASSE, para a equidistância vertical entre curvas de nível de 100m, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." ,
            "O produto foi submetido a análise de normalidade e tendência em suas componentes posicionais, onde os resultados foram: Amostra NÃO Normal e  NÃO TENDENCIOSO.",
            "<br/><br/>",
            "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
            "RMS das discrepâncias (m): VAR_RMS",
            "_________________________________________________________________________",        
            "<br/>"    
            ]
        
        
        
        
        continua_content2 = [
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: Resolução n.123 de 2022 - ANM",
        "Análise da Acurácia Posicional Planimétrica e Altimétrica Absoluta",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Escala de Referência: 1/VAR_ESCALA",
        "Equidistância vertical: 1/VAR_ESCALA",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        
        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas            
        #table_est
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de outliers            
        #table_outliers
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de teste de normalidade
        #table_normalidade
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                
      
        #recebe a tabela de tendênca            
        #table_t
        #table_med
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragrapfh(espc, body_style)]
        
        #recebe a tabela de precisão            
        #table_precisao
        
        content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                             table_precisao,
                             Paragraph(espc, body_style)] 
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        '''img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3
        rl_img4
        rl_img5'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão planimetria<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Dispersão altimetria<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Outliers planimetria<br/>", body_style),
                             rl_img3,
                             Paragraph("<br/>Outliers altimetria<br/>", body_style),
                             rl_img4,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img5,
                             Paragraph(espc, body_style)
                             ] 
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        #table_pontos
        #
        
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        
        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer

#Fazendo a NBR 13133

def tab_NBR_relatorio():
    
    #Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
    
    
    if (op==3): #2d
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>Porcentagem de discrepâncias menores ou iguais à Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph("<b>100000</b>", style_table),Paragraph("<b>100000</b>", style_table), Paragraph("<b>9000</b>", style_table), Paragraph("Reprovado", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
        
    
    elif (op==4): #z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>Porcentagem de discrepâncias menores ou iguais à Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph("<b>100000</b>", style_table),Paragraph("<b>100000</b>", style_table), Paragraph("<b>9000</b>", style_table), Paragraph("Reprovado", style_table)]
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table
    
    else: #2d e z
        
        table_data = [
            [Paragraph("<b>Processamento</b>", style_table), Paragraph("<b>Precisão testada (m)</b>", style_table),Paragraph("<b>Tolerância (m)</b>", style_table), Paragraph("<b>Porcentagem de discrepâncias menores ou iguais à Tolerância</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
            [Paragraph("Planimetria", style_table), Paragraph("<b>100000</b>", style_table),Paragraph("<b>100000</b>", style_table), Paragraph("<b>9000</b>", style_table), Paragraph("Reprovado", style_table)],
            [Paragraph("Altimetria", style_table), Paragraph("<b>100000</b>", style_table),Paragraph("<b>100000</b>", style_table), Paragraph("<b>9000</b>", style_table), Paragraph("Reprovado", style_table)]            
            ]
        
        table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
        
        return table

def conteudo_relatorio_NBR():
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  self.var_relatorio
    print('dx é:' , dx)
    print('dx é:' , dy)
    print('dx é:' , dz)
    
    #Depois vamos declaras content fora dos ifs
    
    op = 0
    if (op==0): #2D
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021 - Análise Planimétrica ",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' foi <b>REPROVADO</b> no processo de inspeção topográfica planimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.2.",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021  ",
        "Análise da Acurácia Posicional Planimétrica",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        

        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName='Times-Roman',
        fontSize=12,
        alignment=4,  # Justificado
        leading= 18,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) for text in content]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(dx,dy,dz,d2D,d3D)
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio()
        
        print('Olha a tabela de outliers:', table_outliers)
        
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio()
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                                         
      
        #recebe a tabela de tendênca            
        table_t , table_med = tab_tendencia_relatorio()
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de precisão            
        table_aceitacao = tab_NBR_relatorio()
        
        content_aceitacao = [Paragraph("Aceitação relativa<br/>", body_style),
                             table_aceitacao,
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        '''#Colocar os gráficos no relatório
         # Caminho para as imagens
        img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        #rl_img3 = rl_img2'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img2,
                             Paragraph(espc, body_style)
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(data)
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
          
          
    elif (op==1): #Z
        
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021 - Análise Altimétrica ",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' foi <b>REPROVADO</b> no processo de inspeção topográfica altimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.3.",
        "_________________________________________________________________________",        
        "<br/>",
        "<b>Relatório estatístico</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021  ",
        "Análise da Acurácia Posicional Altimétrica",
        "_________________________________________________________________________",
        "<br/>",
        "<b>Processamento</b>",
        "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
        "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
        "_________________________________________________________________________",
        "<br/><br/>",
        "_________________________________________________________________________"
        ]
        

        
        # Estilo para o texto
        body_style = ParagraphStyle(
        'Normal',
        fontName='Times-Roman',
        fontSize=12,
        alignment=4,  # Justificado
        leading= 18,  # Espaçamento entre linhas em pontos
        )
        
        # Estilo para linhas centralizadas
        text_style = body_style
        centered_style = ParagraphStyle(
        'Centered',
        parent=text_style,
        alignment=TA_CENTER,  # Centralizado
        )
        
        # Convertendo o conteúdo em parágrafos formatados
        formatted_content = [Paragraph(text, body_style) for text in content]
    
        
    
        # Aplicando o estilo centralizado às linhas desejadas
        formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas  
        
        table_est = tab_est_descritivas_relatorio(dx,dy,dz,d2D,d3D)
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_estatisticas 
        
        #recebe a tabela de outliers            
        table_outliers = tab_outliers_relatorio()
        
        print('Olha a tabela de outliers:', table_outliers)
        
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                             Paragraph(espc, body_style)]         
      
        formatted_content = formatted_content + content_outliers
        
        #recebe a tabela de teste de normalidade
        table_normalidade = tab_normalidade_relatorio()
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                             
        formatted_content = formatted_content + content_normalide                                         
                 
        #recebe a tabela de tendênca            
        #table_t
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph(espc, body_style)]
        
        formatted_content = formatted_content + content_tendencia
        
        #recebe a tabela de aceitação            
        table_aceitacao = tab_NBR_relatorio()
        
        content_aceitacao = [Paragraph("Aceitação relativa<br/>", body_style),
                             table_aceitacao,
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        '''#Colocar os gráficos no relatório
         # Caminho para as imagens
        img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        #rl_img3 = rl_img2'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Outliers<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img2,
                             Paragraph(espc, body_style)
                             ]    
        
        formatted_content = formatted_content + content_graficos
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        table_pontos = tab_pontos_utilizados_relatorio(data)
        #
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        formatted_content = formatted_content + content_pontos

        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
          
            
    else: #2D e Z
    
        content = [
        "<b>RELATÓRIO DE PROCESSAMENTO</b>",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>DADOS DO PRODUTO</b>",
        "_________________________________________________________________________",
        "<br/>",
        "Produto: var_produto",
        "Local: var_local",
        "Data: var_data",
        "Responsável Técnico: var_resp_tecnico",
        "_________________________________________________________________________",
        "<br/><br/>",
        "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
        "<br/>",
        "_________________________________________________________________________",
        "<br/>",
        "Padrão de acurácia utilizado: NBR 13.133 de 2021 - Análise Planimétrica ",
        "<br/>",        
        "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' foi <b>REPROVADO</b> no processo de inspeção topográfica planimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.2.",
        "_________________________________________________________________________",                         
        "<br/>"
        ]
        
        
        continua_content = [
            "_________________________________________________________________________",
            "<br/>",
            "Padrão de acurácia utilizado: NBR 13.133 de 2021 - Análise Altimétrica ",
            "<br/>",        
            "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' foi <b>REPROVADO</b> no processo de inspeção topográfica altimétrica descrita na NBR 13.133 de 2021, de acordo com o item 7.3.",           
            "_________________________________________________________________________",        
            "<br/>",       
            "<b>Relatório estatístico</b>",
            "_________________________________________________________________________",
            "<br/>",
            "Padrão de acurácia utilizado: NBR 13.133 de 2021  ",
            "Análise da Acurácia Posicional Planimétrica e Altimétrica",
            "_________________________________________________________________________",
            "<br/>",
            "<b>Processamento</b>",
            "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
            "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
            "_________________________________________________________________________",
            "<br/><br/>",
            "_________________________________________________________________________"
            ]
        
        
        
        espc = "_________________________________________________________________________"
        #recebe a tabela de estátisticas descritivas            
        #table_est
        
        content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                             table_est,
                             Paragraph(espc, body_style)]
        
        #recebe a tabela de outliers            
        #table_outliers
        
        content_outliers = [Paragraph("Outliers<br/>", body_style),
                             table_outliers,
                             Paragraph(espc, body_style)]         
      
        #recebe a tabela de teste de normalidade
        #table_normalidade
        
        content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                             table_normalidade,
                             Paragraph(espc, body_style)]
                
      
        #recebe a tabela de tendênca            
        #table_t
        #table_med
        
        content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                             table_t,
                             Paragraph("<br/>Estatistica espacial<br/>", body_style),
                             table_med,
                             Paragrapfh(espc, body_style)]
        
        #recebe a tabela de aceitação            
        table_aceitacao = tab_NBR_relatorio()
        
        content_aceitacao = [Paragraph("Aceitação relativa<br/>", body_style),
                             table_aceitacao,
                             Paragraph(espc, body_style)]

        formatted_content = formatted_content + content_aceitacao
        
        #Colocar os gráficos no relatório
         # Caminho para as imagens
        '''img1_path = self.plugin_dir +  "\\images\\image01.png" 
        img2_path = self.plugin_dir +  "\\images\\image02.png"


        # Carregando e redimensionando as imagens
        img1 = Image.open(img1_path)
        img1 = img1.resize((525, 300))

        img2 = Image.open(img2_path)
        img2 = img2.resize((525, 300))

        # Criando objetos Image do ReportLab para as imagens
        rl_img1 = RLImage(img1_path, width=525, height=300)
        rl_img2 = RLImage(img2_path, width=525, height=300)
        rl_img3
        rl_img4
        rl_img5'''
        
        content_graficos = [Paragraph("Gráficos<br/>Dispersão planimetria<br/>", body_style),
                             rl_img1,
                             Paragraph("<br/>Dispersão altimetria<br/>", body_style),
                             rl_img2,
                             Paragraph("<br/>Outliers planimetria<br/>", body_style),
                             rl_img3,
                             Paragraph("<br/>Outliers altimetria<br/>", body_style),
                             rl_img4,
                             Paragraph("<br/>Discrepâncias<br/>", body_style),
                             rl_img5,
                             Paragraph(espc, body_style)
                             ] 
        
        
        #Colocar agora a tabela de discrepâncias e pontos de checagem
        #recebe a tabela dos pontos            
        #table_pontos
        #
        
        content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                             table_pontos,
                             Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                             ]
        
        
        def add_header_footer(canvas, doc):
            # Adicionar cabeçalho
            cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
            canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
        
            espc = "_________________________________________________________________________"
            # Adicionar rodapé
            rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
            #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
            #rodape_text += f'<br/>20/05/2024 - 16:56:23'

            styles = getSampleStyleSheet()
            rodape_style = styles['Normal']
            rodape_style.fontName = 'Times-Roman'
            rodape_style.fontSize = 12
            rodape_style.alignment = 4  #Justificado

            rodape = Paragraph(rodape_text, rodape_style)
            rodape.wrap(doc.width, inch)
            rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
        
        #criando o arquivo PDF
    
        file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        #print('Olha o conteudo formatado', formatted_content)
        
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer

# Fazendo o modelo do INCRA

def tab_INCRA_relatorio():
#Este método gera as tabelas do teste de precisão para o relatório de processamento
    
    # Estilo para o texto das tabelas
    style_table = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=1,  # Centralizado
    leading= 18,  # Espaçamento entre linhas em pontos
    )   
        
    table_data = [
        [Paragraph("<b>Limites</b>", style_table), Paragraph("<b>Resultado</b>", style_table)],
        [Paragraph("Artificial (0,5m)", style_table), Paragraph("Reprovado", style_table)],
        [Paragraph("Natural (3,0m)", style_table), Paragraph("Reprovado", style_table)],
        [Paragraph("Inacessível (7,5m)", style_table), Paragraph("Reprovado", style_table)],
        ]
    
    table = Table(table_data, style=[('GRID', (0,0), (-1,-1), 1, "black")])
    
    return table
    

def conteudo_relatorio_INCRA():
    #Testando um método para criar o conteúdo de cada modelo de relatório de processamento
    
    dx,dy,dz,d2D,d3D, data =  self.var_relatorio
    print('dx é:' , dx)
    print('dx é:' , dy)
    print('dx é:' , dz)
    
    #Depois vamos declaras content fora dos ifs
    

        
    content = [
    "<b>RELATÓRIO DE PROCESSAMENTO</b>",
    "_________________________________________________________________________",
    "<br/><br/>",
    "<b>DADOS DO PRODUTO</b>",
    "_________________________________________________________________________",
    "<br/>",
    "Produto: var_produto",
    "Local: var_local",
    "Data: var_data",
    "Responsável Técnico: var_resp_tecnico",
    "_________________________________________________________________________",
    "<br/><br/>",
    "<b>CLASSIFICAÇÃO FINAL DO PRODUTO</b>",
    "<br/>",
    "_________________________________________________________________________",
    "<br/>",
    "Padrão de acurácia utilizado: Manual Técnico para Georreferenciamento de Imóveis Rurais - 2a edição - 2022 - INCRA",
    "<br/>",        
    "O produto 'aammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', <b>NÃO ATENDE</b> o processo de avaliação da acurácia posicional absoluta do INCRA, em relação à alínea "b" do item 3.4.1 do Manual Técnico para Georreferenciamento do INCRA (2ª edição - 2022).",
    "O produto foi classificado com PEC-PCD VAR_CLASSE, na escala VAR_ESCALA, de acordo com os critérios do Decreto 89.817 e da ET-CQDG." 
    ]
    
    n_atende = [ "O posicionamento por este produto NÃO é adequado aos tipos de limites definidos na normativa do INCRA."
    ]
    
    atende = [ "O valor do PEC-PCD corresponde à VAL_PECPCD metros, sendo ADEQUADA à precisão do(s) limite(s) VAR_LIMITES. "
    ]
    

    continua_content = [
    "<br/><br/>Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
    "RMS das discrepâncias (m): VAR_RMS",
    "_________________________________________________________________________",        
    "<br/>",
    "<b>Relatório estatístico</b>",
    "_________________________________________________________________________",
    "<br/>",
    "Padrão de acurácia utilizado: Manual Técnico para Georreferenciamento de Imóveis Rurais - 2a edição - 2022 - INCRA ",
    "Análise da Acurácia Posicional Planimétrica Absoluta",
    "_________________________________________________________________________",
    "<br/>",
    "<b>Processamento</b>",
    "Escala de Referência: 1/VAR_ESCALA",
    "Pontos de checagem inseridos: VAR_PTS_INSERIDOS",
    "Pontos de checagem utilizados: VAR_PTS_UTILIZADOS",
    "_________________________________________________________________________",
    "<br/><br/>",
    "_________________________________________________________________________"
    ]
    

    
    # Estilo para o texto
    body_style = ParagraphStyle(
    'Normal',
    fontName='Times-Roman',
    fontSize=12,
    alignment=4,  # Justificado
    leading= 18,  # Espaçamento entre linhas em pontos
    )
    
    # Estilo para linhas centralizadas
    text_style = body_style
    centered_style = ParagraphStyle(
    'Centered',
    parent=text_style,
    alignment=TA_CENTER,  # Centralizado
    )
    
    # Convertendo o conteúdo em parágrafos formatados
    formatted_content = [Paragraph(text, body_style) for text in content]

    

    # Aplicando o estilo centralizado às linhas desejadas
    formatted_content[0] = Paragraph(content[0], centered_style)  # Centraliza a primeira linha



    espc = "_________________________________________________________________________"
    #recebe a tabela de estátisticas descritivas  
    
    table_est = tab_est_descritivas_relatorio(dx,dy,dz,d2D,d3D)
    
    content_estatisticas = [Paragraph("Estatísticas descritivas<br/>", body_style),
                         table_est,
                         Paragraph(espc, body_style)]
                         
    formatted_content = formatted_content + content_estatisticas 
    
    #recebe a tabela de outliers            
    table_outliers = tab_outliers_relatorio()
    
    print('Olha a tabela de outliers:', table_outliers)
    
    
    content_outliers = [Paragraph("Outliers<br/>", body_style),
                         table_outliers,                          # o erro só ocorre ao adicionar essa tabela
                         Paragraph(espc, body_style)]         
  
    formatted_content = formatted_content + content_outliers
    
    #recebe a tabela de teste de normalidade
    table_normalidade = tab_normalidade_relatorio()
    
    content_normalide = [Paragraph(f"Teste de normalidade<br/>Teste de Normalidade Shapiro-Wilk, com 95%VAR NC de confiança<br/>", body_style),
                         table_normalidade,
                         Paragraph(espc, body_style)]
                         
    formatted_content = formatted_content + content_normalide                                         
  
    #recebe a tabela de tendênca            
    table_t , table_med = tab_tendencia_relatorio()
    
    content_tendencia = [Paragraph("Teste de tendência<br/>Teste t de Student<br/>", body_style),
                         table_t,
                         Paragraph("<br/>Estatistica espacial<br/>", body_style),
                         table_med,
                         Paragraph(espc, body_style)]
    
    formatted_content = formatted_content + content_tendencia
    
    #recebe a tabela de precisão            
    table_precisao = tab_precisao_relatorio()
    
    content_precisão = [Paragraph("Teste de precisão<br/>", body_style),
                         table_precisao,
                         Paragraph(espc, body_style)]

    formatted_content = formatted_content + content_precisão
    
    #recebe a tabela de vértices do INCRA            
    table_INCRA = tab_INCRA_relatorio()
    
    content_limites = [Paragraph("Tipos de limites<br/>", body_style),
                         table_INCRA,
                         Paragraph(espc, body_style)]

    formatted_content = formatted_content + content_limites
    
    
    
    '''#Colocar os gráficos no relatório
     # Caminho para as imagens
    img1_path = self.plugin_dir +  "\\images\\image01.png" 
    img2_path = self.plugin_dir +  "\\images\\image02.png"


    # Carregando e redimensionando as imagens
    img1 = Image.open(img1_path)
    img1 = img1.resize((525, 300))

    img2 = Image.open(img2_path)
    img2 = img2.resize((525, 300))

    # Criando objetos Image do ReportLab para as imagens
    rl_img1 = RLImage(img1_path, width=525, height=300)
    rl_img2 = RLImage(img2_path, width=525, height=300)
    #rl_img3 = rl_img2'''
    
    content_graficos = [Paragraph("Gráficos<br/>Dispersão<br/>", body_style),
                         rl_img1,
                         Paragraph("<br/>Outliers<br/>", body_style),
                         rl_img2,
                         Paragraph("<br/>Discrepâncias<br/>", body_style),
                         rl_img2,
                         Paragraph(espc, body_style)
                         ]    
    
    formatted_content = formatted_content + content_graficos
    
    
    #Colocar agora a tabela de discrepâncias e pontos de checagem
    #recebe a tabela dos pontos            
    table_pontos = tab_pontos_utilizados_relatorio(data)
    #
    content_pontos = [Paragraph("<b>Discrepâncias - Pontos de checagem</b><br/>", body_style),
                         table_pontos,
                         Paragraph("<br/><br/><br/><br/><br/>Relatorio gerado em: 08/05/2024 - 15:50:51<br/>Plugin GeoPEC - versão 1.0 - 2024", body_style)
                         ]
    
    formatted_content = formatted_content + content_pontos

    def add_header_footer(canvas, doc):
        # Adicionar cabeçalho
        cabecalho = self.plugin_dir + "\\icon\\cabecalho.png"
        canvas.drawImage(cabecalho, doc.leftMargin, doc.height + 75, width=doc.width, height=50)
    
        espc = "_________________________________________________________________________"
        # Adicionar rodapé
        rodape_text = f"{espc}<br/>Relatório de Processamento do GeoPEC{'&nbsp;'*65}Página {canvas.getPageNumber()}<br/>20/05/2024 - 16:56:23<br/>{espc}"
        #rodape_text += f'/{doc.page}' {'&nbsp;'*12}
        #rodape_text += f'<br/>20/05/2024 - 16:56:23'

        styles = getSampleStyleSheet()
        rodape_style = styles['Normal']
        rodape_style.fontName = 'Times-Roman'
        rodape_style.fontSize = 12
        rodape_style.alignment = 4  #Justificado

        rodape = Paragraph(rodape_text, rodape_style)
        rodape.wrap(doc.width, inch)
        rodape.drawOn(canvas, doc.leftMargin  , 25)  # Posição do rodapé'''
    
    #criando o arquivo PDF

    file_path = self.plugin_dir + "\\pdfs\\relatorio34.pdf"  # Caminho para salvar o arquivo PDF
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    #print('Olha o conteudo formatado', formatted_content)
    
    doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
      