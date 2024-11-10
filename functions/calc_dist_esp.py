#-------------------------------------------------------------------------------------------------------- 
#   GeoPEC - Software científico para avaliação da acurácia posicional em dados cartográficos
#   Funções para o cálculo de Padrão de Distribuição Espacial no controle de qualidade cartográfica
#   abril de 2024
#   autores: Afonso P. Santos; João Vítor A. Gonçalves; Luis Philippe Ventura
#-------------------------------------------------------------------------------------------------------- 

from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QLabel
from qgis.core import *
####from qgis.core import QgsProject, QgsWkbTypes
# Geração de relatorio
'''import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas'''


#------------------------------------------------------------------------------------------
#Bibliotecas para gerar o PDF

###import os
import platform
import subprocess
from datetime import datetime

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

####################
#Para usar a função de erro
from qgis.PyQt.QtGui import QIcon



#--------------------------------------------------------------------------------------------------------
# Função para o cálculos estatísticos: R, r observado, r esperado, SEr, Z calculado e Z tabelado, 
# referentes às ordens 1, 2 e 3.
#
 
def fCalculaEstatistica(dlg, area):

# Recebe como parâmetro o valor de área, fornecida pela função "calculaArea" no código principal.
        
        # Testando se o valor de área é None, e avisa, se for.
        
        if area is None:
            return

        # Testando se a camada de pontos foi selecionada.
        
        layer_name = dlg.comboBox_3.currentText()
        if not layer_name:
            
            show_messagebox_erro('erro', 'Por favor, selecione uma camada de pontos.')
            
            return None

        # Testando se a camada era realmente de pontos e informando ao usuário caso não for.
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        if layer.geometryType() != QgsWkbTypes.PointGeometry:
            
            show_messagebox_erro('erro', 'A camada selecionada não possui geometria de ponto.')

            return None

        # Lê os pontos, inclusive sua geometria e numero de pontos, e avisa caso a camada tenha menos que 3 pontos.

        points = [feature.geometry().asPoint() for feature in layer.getFeatures()]
        num_points = len(points)
        
        if num_points < 3:
            
            show_messagebox_erro('erro', 'A camada deve conter pelo menos três pontos.')

            return None
 

        # Criando uma lista para os dados de distancias das ordens 1, 2 e 3.
        
        distancias_primeira_ordem = []
        distancias_segunda_ordem = []
        distancias_terceira_ordem = []
        
        # Atribuindo valores à lista criada anteriormente.
        
        for i, point in enumerate(points):
            distancias = []
            for j, other_point in enumerate(points):
                if i != j:
                    distancias.append(point.distance(other_point))
            distancias.sort()
            distancias_primeira_ordem.append(distancias[0])
            distancias_segunda_ordem.append(distancias[1] if len(distancias) > 1 else 0)
            distancias_terceira_ordem.append(distancias[2] if len(distancias) > 2 else 0)

        # Somando os valores das distancias das ordens 1, 2 e 3, o que serve de base para o cálculo
        # do r obervado.
        
        soma_primeira_ordem = sum(distancias_primeira_ordem)
        soma_segunda_ordem = sum(distancias_segunda_ordem)
        soma_terceira_ordem = sum(distancias_terceira_ordem)

        # Calculando o r observado
        
        r_obs_primeira_ordem = soma_primeira_ordem / num_points
        r_obs_segunda_ordem = soma_segunda_ordem / num_points
        r_obs_terceira_ordem = soma_terceira_ordem / num_points

        # Calculando r_esperado
        r_esperado_primeira_ordem = 0.5 * (area / num_points) ** 0.5
        r_esperado_segunda_ordem = 0.75 * (area / num_points) ** 0.5
        r_esperado_terceira_ordem = 0.9375 * (area / num_points) ** 0.5


        # Calculando R
        
        R_primeira_ordem = r_obs_primeira_ordem / r_esperado_primeira_ordem
        R_segunda_ordem = r_obs_segunda_ordem / r_esperado_segunda_ordem
        R_terceira_ordem = r_obs_terceira_ordem / r_esperado_terceira_ordem

        # Obtendo o valor de Nível de Confiança, escolhido pelo usuário.
        
        nivel_confianca = float(dlg.comboBox_9.currentText().replace('%', ''))

        #Definindo Ztabelado, referente ao Nível de Confiança inserido pelo usuário.
        
        if nivel_confianca == 95:
            Ztabelado = 1.9599639845400536
        elif nivel_confianca == 90:
            Ztabelado = 1.6448536269514715
        elif nivel_confianca == 99:
            Ztabelado = 2.5758293035488999
        # Caso de erro.
        else:
            
            show_messagebox_erro('erro', 'Nível de confiança não suportado.')

            return None

        # Calculando SE_r
        
        SE_r_primeira_ordem = 0.2613 * (area / num_points ** 2) ** 0.5
        SE_r_segunda_ordem = 0.2722 * (area / num_points ** 2) ** 0.5
        SE_r_terceira_ordem = 0.2757 * (area / num_points ** 2) ** 0.5

        # Calculando Zcalculado
        
        Zcalculado_primeira_ordem = (r_obs_primeira_ordem - r_esperado_primeira_ordem) / SE_r_primeira_ordem
        Zcalculado_segunda_ordem = (r_obs_segunda_ordem - r_esperado_segunda_ordem) / SE_r_segunda_ordem
        Zcalculado_terceira_ordem = (r_obs_terceira_ordem - r_esperado_terceira_ordem) / SE_r_terceira_ordem
        
        ###
        # Determinando o tipo de padrão, entre DISPERSO, ALEATÓRIO ou AGRUPADO com base nos valores de R para cada uma das 3 ordens.
        ###
        
        # Primeira ordem
        
        if R_primeira_ordem > 1:
            padrao_primeira_ordem = "Padrão DISPERSO"
        elif R_primeira_ordem == 1:
            padrao_primeira_ordem = "Padrão ALEATÓRIO"
        else:
            padrao_primeira_ordem = "Padrão AGRUPADO"

        # Segunda ordem
        
        if R_segunda_ordem > 1:
            padrao_segunda_ordem = "Padrão DISPERSO"
        elif R_segunda_ordem == 1:
            padrao_segunda_ordem = "Padrão ALEATÓRIO"
        else:
            padrao_segunda_ordem = "Padrão AGRUPADO"
        
        # Terceira ordem
        
        if R_terceira_ordem > 1:
            padrao_terceira_ordem = "Padrão DISPERSO"
        elif R_terceira_ordem == 1:
            padrao_terceira_ordem = "Padrão ALEATÓRIO"
        else:
            padrao_terceira_ordem = "Padrão AGRUPADO"
            

        # Comparação DE Zcalculado com Ztabelado para dizer sobre a 
        #  SIGNIFICÂNCIA ESTATÍSTICA
        
        significancia_primeira_ordem = "(significativo estatisticamente)" if abs(Zcalculado_primeira_ordem) > Ztabelado else "(NÃO é significativo estatisticamente)"
        significancia_segunda_ordem = "(significativo estatisticamente)" if abs(Zcalculado_segunda_ordem) > Ztabelado else "(NÃO é significativo estatisticamente)"
        significancia_terceira_ordem = "(significativo estatisticamente)" if abs(Zcalculado_terceira_ordem) > Ztabelado else "(NÃO é significativo estatisticamente)"


        # Funções para determinar o padrão e o resultado final
        def determinaPadrao(R):
            if R > 1:
                return "Padrão DISPERSO"
            elif R == 1:
                return "Padrão ALEATÓRIO"
            else:
                return "Padrão AGRUPADO"

        def resultadoFinal(Zcalculado, Ztabelado, padrao):
            if abs(Zcalculado) <= Ztabelado:
                return "Padrão ALEATÓRIO"
            else:
                return padrao

        # Calculando os padrões finais (que aparecem em vermelho nos resultados de Distribuição Espacial) para as três ordens
        padrao_final_primeira_ordem = resultadoFinal(Zcalculado_primeira_ordem, Ztabelado, determinaPadrao(R_primeira_ordem))
        padrao_final_segunda_ordem = resultadoFinal(Zcalculado_segunda_ordem, Ztabelado, determinaPadrao(R_segunda_ordem))
        padrao_final_terceira_ordem = resultadoFinal(Zcalculado_terceira_ordem, Ztabelado, determinaPadrao(R_terceira_ordem))


        # Inserção de resultados em uma lista  -  que é chamado em outras funções  
        
        resultados = (R_primeira_ordem, R_segunda_ordem, R_terceira_ordem,
            r_obs_primeira_ordem, r_obs_segunda_ordem, r_obs_terceira_ordem,
            r_esperado_primeira_ordem, r_esperado_segunda_ordem, r_esperado_terceira_ordem,
            Zcalculado_primeira_ordem, Zcalculado_segunda_ordem, Zcalculado_terceira_ordem,
            SE_r_primeira_ordem, SE_r_segunda_ordem, SE_r_terceira_ordem,
            padrao_primeira_ordem, padrao_segunda_ordem, padrao_terceira_ordem,
            significancia_primeira_ordem, significancia_segunda_ordem, significancia_terceira_ordem,
            Ztabelado, nivel_confianca, 
            padrao_final_primeira_ordem, padrao_final_segunda_ordem, padrao_final_terceira_ordem)
   

        return resultados
      
      
      
#--------------------------------------------------------------------------------------------------------
#Função que abre PDF, nas sistemas Windows, macOS ou Linux.
# 

def open_pdf(file_path):

    if platform.system() == 'Windows':
        os.startfile(file_path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file_path))
    else:  # Linux
        subprocess.call(('xdg-open', file_path))
        


#--------------------------------------------------------------------------------------------------------
# Função para a geração de relatório referente aos resultados de cálculos estatísticos: R, r observado, 
# r esperado, SEr, Z calculado e Z tabelado, etc, gerados pela função fCalculaEstatistica.
#

def fGeraRelatorio(resultados):
    """
    Gera um relatório em PDF com os resultados das análises.
    """

    
    # Desempacotando os valores de resultados calculados em fCalculaEstatistica para usá-los nesta função

    (
        R_primeira_ordem, R_segunda_ordem, R_terceira_ordem,
        r_obs_primeira_ordem, r_obs_segunda_ordem, r_obs_terceira_ordem,
        r_esperado_primeira_ordem, r_esperado_segunda_ordem, r_esperado_terceira_ordem,
        Zcalculado_primeira_ordem, Zcalculado_segunda_ordem, Zcalculado_terceira_ordem,
        SE_r_primeira_ordem, SE_r_segunda_ordem, SE_r_terceira_ordem,
        padrao_primeira_ordem, padrao_segunda_ordem, padrao_terceira_ordem,
        significancia_primeira_ordem, significancia_segunda_ordem, significancia_terceira_ordem,
        Ztabelado, nivel_confianca,
        padrao_final_primeira_ordem, padrao_final_segunda_ordem, padrao_final_terceira_ordem
    ) = resultados
    
    
    # Verificação se os resultados são None (nulos)
    
    if resultados is None:
        
        show_messagebox_erro('erro', 'Não foram gerados resultados.')
        
        # Interrompe o processo se não houver resultados
        return  
        
        
    # Solicitando ao usuário o local para salvar o relatório PDF
       
    options = QFileDialog.Options()
    filePath, _ = QFileDialog.getSaveFileName(None, "Salvar Relatório PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
    
    # Caso de o usuário cancelar a janela o diálogo
    
    if not filePath:
        return  

    
    #obtendo a data e a hora
    
    now = datetime.now()
    

    # Formatando a data e hora em uma string
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    
   
    #obtendo o caminho do diretorio
    ###------ OBSERVAÇÃO: essa linha está chamando o diretório deste arquivo .py, e este está na pasta functions! Atenção.
    plugin_dir = os.path.dirname(__file__)   
    
    # A linha abaixo tira a parte 'functions' do caminho do diretório atual, e deixa so do diretório pai do plugin,
    # que é uma pasta acima da 'functions'.
    plugin_dir_pai = os.path.dirname(plugin_dir)  
      
    
    #Função que gera o cabeçalho, não alterar, deixar desse jeito
    
    def add_header_footer(canvas, doc):
        
        # Adicionar cabeçalho


        ## Definido como plugin_dir_pai pois o plugin_dir chama a pasta functions, mas o que queremos é a pasta icon, com 
        ## a imagem do 'cabecalho'.
        cabecalho_path = plugin_dir_pai + "\\icon\\cabecalho.png"
        
        canvas.drawImage(cabecalho_path, doc.leftMargin, doc.height + 75, width=doc.width, height=50)  
    
        espc = "____________________________________________________________________________________________________"
        
        
        # Adicionar rodapé
        
        
        rodape_text = f"{espc}<br/>GeoPEC: Relatório de Processamento do Padrão de Distribuição Espacial{'&nbsp;'*67}Página {canvas.getPageNumber()}<br/>{current_time}"
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
    
    #Primeiro bloco de conteúdo, colocar as variáveis dentro das chaves
  
    content_ordem1 = [
    "<b>RELATÓRIO DE PROCESSAMENTO DO PADRÃO DE DISTRIBUIÇÃO ESPACIAL</b>",
    linha_traco + "<br/><br/>",
    "Método: Estatística do Vizinho Mais Próximo",
    f"Nível de confiança: {nivel_confianca:.0f}%",
    f"Z tabelado = {Ztabelado:.2f}".replace('.', ','),
    linha_traco,
    "<br/>",
    "<b>RESULTADO DA 1ª ORDEM</b> <br/><br/>",
    f"R observado = {r_obs_primeira_ordem:.4f}".replace('.', ','),
    f"R esperado = {r_esperado_primeira_ordem:.4f}".replace('.', ','),
    f"Índice R = {R_primeira_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Z calculado = {Zcalculado_primeira_ordem:.4f}".replace('.', ','),
    f"SE = {SE_r_primeira_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Resultado = {padrao_final_primeira_ordem}",
    linha_traco,
    "<br/>"
    ]
    
    #segundo bloco de conteúdo, colocar as variáveis dentro das chaves
    
    content_ordem2 = [
    "<b>RESULTADO DA 2ª ORDEM</b> <br/><br/>",
    f"R observado = {r_obs_segunda_ordem:.4f}".replace('.', ','),
    f"R esperado = {r_esperado_segunda_ordem:.4f}".replace('.', ','),
    f"Índice R = {R_segunda_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Z calculado = {Zcalculado_segunda_ordem:.4f}".replace('.', ','),
    f"SE = {SE_r_segunda_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Resultado = {padrao_final_segunda_ordem}",
    linha_traco,
    "<br/>"
    ]
    
    #terceiro bloco de conteúdo, colocar as variáveis dentro das chaves
    
    content_ordem3 = [
    "<b>RESULTADO DA 3ª ORDEM</b> <br/><br/>",
    f"R observado = {r_obs_terceira_ordem:.4f}".replace('.', ','),
    f"R esperado = {r_esperado_terceira_ordem:.4f}".replace('.', ','),
    f"Índice R = {R_terceira_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Z calculado = {Zcalculado_terceira_ordem:.4f}".replace('.', ','),
    f"SE = {SE_r_terceira_ordem:.4f} <br/><br/>".replace('.', ','),
    f"Resultado = {padrao_final_terceira_ordem}",
    linha_traco,
    f"<br/><br/><br/>Relatorio gerado em: {current_time}<br/>Plugin GeoPEC - versão 1.0 - 2024"
    ]
    
    #transformando os blocos de conteúdo em apenas um bloco
    
    content = content_ordem1 + content_ordem2 + content_ordem3
    

    
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


    #criando o arquivo PDF 
    
    file_path = filePath # Caminho para salvar o arquivo PDF


    try:
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        doc.build(formatted_content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        
    
        
        show_messagebox_erro('sucesso', 'Relatório gerado com sucesso!') 
        
        
    
        ## Uma vez dando certo a criação do relatório, abrirá automaticamente após o salvamento.
        open_pdf(file_path)
        
    except Exception as e:
        show_messagebox_erro('erro', 'Ocorreu um erro ao gerar o relatório.')
        


#--------------------------------------------------------------------------------------------------------
# Função para a exibição de mensagem de erro ou sucesso no padrão plugin GeoPEC.
#
  
def show_messagebox_erro(tipo, mensagem):
    

    
    #Função para exibir mensagem de erro ou sucesso
    
    ## A função abaixo chama a pasta com final /functions, ja que este arquivo esta na pasta functions.
    plugin_dir = os.path.dirname(__file__)
    
    
    # A linha abaixo tira a parte 'functions' do caminho do diretório atual, e deixa so do diretorio pai do plugin,
    # que é uma pasta acima da 'functions'.
    plugin_dir_pai = os.path.dirname(plugin_dir)
    

    
    if  (tipo == 'erro'):
    
        # Crie uma instância do QMessageBox
        msg_box = QMessageBox()

        # Defina o ícone da janela
        msg_box.setWindowIcon(QIcon(plugin_dir_pai + "/icon/geopec.png"))  

        # Configure a mensagem de erro
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle('Erro')
        msg_box.setText(mensagem)

        # Exiba a mensagem
        msg_box.exec_()
    
        
    else: # tipo igual sucesso
        
        # Crie uma instância do QMessageBox
        msg_box = QMessageBox()

        # Defina o ícone da janela
        msg_box.setWindowIcon(QIcon(plugin_dir_pai + "/icon/geopec.png"))  

        # Configure a mensagem de erro
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle('Sucesso')
        msg_box.setText(mensagem)

        # Exiba a mensagem
        msg_box.exec_()
   
