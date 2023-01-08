#!/usr/bin/env python3

#*******************************************************************************#
#                                                                               #
# Escrito por Yuri H. Galvao <yuri@galvao.ca> em dezembro de 2022               #   
#                                                                               #
#*******************************************************************************#

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from basic_functions import *

# Declarando as funções
def expande_menu(driver)->None:
    """"""
    
    try:
        nav_menu = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''//div[img[@role="presentation"]]'''))
        nav_menu.click()
    except:
        try:
            nav_menu = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''(//div[img[@role="presentation"]])[2]'''))
        except Exception as e:
            erro_critico(f'Erro! Não foi possível localizar o menu!\nExceção: {repr(e)}')
        else:
            try:
                nav_menu.click()
            except Exception as e:
                erro_critico(f'Erro! Não foi possível expandir o menu!\nExceção: {repr(e)}')            

    time.sleep(1)

def manipula_pagina(driver:object, base_uri:str)->None:
    """"""

    ## Acessando a página do TSE para baixar os arquivos das urnas
    driver.get(base_uri)
    
    ## Expandindo o menu lateral
    expande_menu(driver)

    ### Manipulando os elementos da página para baixar os arquivos das urnas do 2ª turno
    select_eleicao = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-select[@formcontrolname="eleicao"]'''))
    select_eleicao.click()
    eleicoes_federais_2_turno = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-option[span=" Eleição Ordinária Federal - 2022 2º Turno "]'''))
    eleicoes_federais_2_turno.click()

    time.sleep(1)

    select_tipo = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-select[@formcontrolname="visualizacao"]'''))
    select_tipo.click()
    rdv = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-option[span=" Registro Digital de Votos "]'''))
    rdv.click()

    time.sleep(1)

def baixa_arquivos(driver:object, contagem:int)->int:
    """"""

    botao_consultar = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//ion-button[@type="submit"]'''))
    botao_consultar.click()

    time.sleep(1)
    todos_arquivos = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//a[.="Todos Arquivos"]'''))
    todos_arquivos.click()

    time.sleep(1.75)

    contagem += 1

    return contagem

def seleciona_urna(driver:object)->int:
    """"""

    def select(variavel:str)->object:
        """"""

        return WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//mat-select[@formcontrolname="{variavel}"]'''))

    opcoes = lambda x: x.find_elements(by=By.XPATH, value='''//div/mat-option/span[@class="mat-option-text"]''')
    actions = ActionChains(driver)
    contagem = 0

    time.sleep(1.5)

    select_abrangencias = select('uf')
    select_abrangencias.click()
    
    lista_de_abrangencias =  [abrangencia.text for abrangencia in WebDriverWait(driver, timeout=7).until(opcoes)]
    for abrangencia in lista_de_abrangencias:
        abrangencia_objeto = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//span[.=" {abrangencia} "]'''))
        abrangencia_objeto.click()

        info_passo = lambda x: info(f'{x} selecionado(a)')
        info_passo(abrangencia)

        time.sleep(3)
        select_municipio = select('municipioBU')
        select_municipio.click()

        lista_de_municipios = [municipio.text for municipio in WebDriverWait(driver, timeout=7).until(opcoes)]
        for municipio in lista_de_municipios:
            municipio_objeto = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//span[.=" {municipio} "]'''))
            municipio_objeto.click()

            info_passo(municipio)

            time.sleep(3)
            select_zona = select('zonaEleitoralBU')
            select_zona.click()

            lista_de_zonas = [zona.text for zona in WebDriverWait(driver, timeout=7).until(opcoes)]
            for zona in lista_de_zonas:
                zona_objeto = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//span[.=" {zona} "]'''))
                zona_objeto.click()

                info_passo(zona)

                time.sleep(3)
                select_secao = select('secaoEleitoralBU')
                select_secao.click()

                lista_de_secoes = [secao.text for secao in WebDriverWait(driver, timeout=7).until(opcoes)]
                for secao in lista_de_secoes:
                    secao_objeto = WebDriverWait(driver, timeout=7).until(lambda x: x.find_element(by=By.XPATH, value=f'''//span[.=" {secao} "]'''))
                    #actions.move_to_element(secao_).perform()
                    secao_objeto.click()

                    info_passo(secao)

                    time.sleep(.25)
                    contagem = baixa_arquivos(driver, contagem)

                    info('Arquivo Zip baixado!\n')
                    info(f'Total de arquivos baixados: {contagem}\n')

                    expande_menu(driver)

                    if secao != lista_de_secoes[-1]:
                        select_secao = select('secaoEleitoralBU')
                        select_secao.click()

                        time.sleep(1)

                if zona != lista_de_zonas[-1]:
                    select_zona = select('zonaEleitoralBU')
                    select_zona.click()

            if municipio != lista_de_municipios[-1]:
                select_municipio = select('municipioBU')
                select_municipio.click()

        if abrangencia != lista_de_abrangencias[-1]:
            select_abrangencias = select('uf')
            select_abrangencias.click()

    return contagem

def iniciar()->None:
    """"""

    # Declarando algumas constantes
    LINUX_USERAGENT = "Mozilla/5.0  (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    OPTIONS = Options()
    PREFS = {"profile.default_content_settings.popups": 0,    
            "download.default_directory":"/home/yhgalvao/Desktop/AI/Notebooks/Brazil_2022_Elections/formato-arquivos-bu-rdv-ass-digital/BU_e_RDV",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True}
    OPTIONS.add_experimental_option("prefs", PREFS)
    OPTIONS.add_argument(f'user-agent={LINUX_USERAGENT}')

    # Declarando algumas variáveis
    base_uri = 'https://resultados.tse.jus.br/oficial/app/index.html#/divulga;e=545'
    headless = confirm('Você deseja que o navegador seja "headless"? ')
    if headless:
        OPTIONS.add_argument('--headless')

    info('Iniciando o Web Scraper dos RDV, BU, e Logs das Eleições Federais de 2022 (2ª turno)\n')

    ## Declarando variáveis e objetos locais
    driver = webdriver.Chrome(options = OPTIONS)
    driver.set_window_size(1920,1040)

    manipula_pagina(driver, base_uri)

    time.sleep(2)

    info(f'Download concluído! Foram baixados os arquivos referentes a {seleciona_urna(driver)} urnas!')
    info('Programa finalizado com sucesso!')


if __name__ == '__main__':
    iniciar()
