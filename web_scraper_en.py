#!/usr/bin/env python3

#*******************************************************************************#
#                                                                               #
# Written by Yuri H. Galvao <yuri@galvao.ca>, December 2022                     #   
#                                                                               #
#*******************************************************************************#

# Importing from modules / packages
import time, logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from basic_functions_en import *

# Declaring some important variables, like the scope (Brazilian state), the log file name, and the basic configuration for the log system
scope = input('Please, enter the name of the state for this instance of the web scraper (e.g. Rio de Janeiro): ').strip()
log_file_name = scope

if confirm('Do you want to customize the name of the log file? [y/n] '):
    log_file_name = input('Enter the name for the log file, without the extension: ')

log_file_name = log_file_name.replace(' ', '_') + '.log'
logging.basicConfig(
    filename='./logs/'+log_file_name,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
info = lambda x: logging.info(x)
warning = lambda x: logging.warning(x)
error = lambda x: logging.error(x)
critical_error = lambda x: logging.critical(x)

# Declaring functions
def get_webdriver(headless:bool)->object:
    """"""

    # Declaring some important variables for the Gecko Webdriver (Firefox)
    options = Options()
    #linux_useragent = "Mozilla/5.0  (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", "/home/yhgalvao/Desktop/AI/Notebooks/Brazil_2022_Elections/formato-arquivos-bu-rdv-ass-digital/BU_e_RDV")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    #options.add_argument(f'user-agent={linux_useragent}')
    options.add_argument('--no-sandbox')

    if headless is True:
        options.add_argument('--headless')

    driver = webdriver.Firefox(options = options)
    driver.set_window_size(1920,1040)

    return driver

def expand_menu(driver:object)->None:
    """"""
    
    try:
        nav_menu = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''//div[img[@role="presentation"]]'''))
        nav_menu.click()
    except:
        try:
            nav_menu = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''(//div[img[@role="presentation"]])[2]'''))
        except Exception as e:
            critical_error(f'Error! Unable to locate menu!\nException: {repr(e)}')
        else:
            try:
                nav_menu.click()
            except Exception as e:
                critical_error(f'Error! Unable to expand menu!\nException: {repr(e)}')            

    time.sleep(1)

def get_page_ready(driver:object, base_uri:str)->None:
    """"""

    ## Accessing the TSE page to download EVM files
    driver.get(base_uri)

    ## Expanding the side menu
    expand_menu(driver)

    ### Manipulating necessary page elements prior to the EVM files download
    select_election = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-select[@formcontrolname="eleicao"]'''))
    select_election.click()
    federal_elections_2nd_round = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-option[span=" Eleição Ordinária Federal - 2022 2º Turno "]'''))
    federal_elections_2nd_round.click()

    time.sleep(1)

    select_type = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-select[@formcontrolname="visualizacao"]'''))
    select_type.click()
    rdv = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value='''//mat-option[span=" Registro Digital de Votos "]'''))
    rdv.click()

    time.sleep(1)

    return driver

def download_files(driver:object, count:int)->int:
    """"""

    query_button = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value=f'''//ion-button[@type="submit"]'''))
    query_button.click()

    time.sleep(1)
    all_files = WebDriverWait(driver, timeout=15).until(lambda x: x.find_element(by=By.XPATH, value=f'''//a[.="Todos Arquivos"]'''))
    all_files.click()

    time.sleep(1.25)

    count += 1

    return count

def select_evm_and_download_files(driver:object, headless:bool, base_uri:str, revert:bool)->int:
    """"""

    def find_matselect_by_form_control_name(name:str)->object:
        """"""

        element = None
        tries = 0

        time.sleep(1)

        while element is None:
            tries += 1

            if tries == 51:
                critical_error(f'Element {name} not found! Stopping trying after 50 tries.')
                raise Exception("Too many tries!")

            try:
                element = WebDriverWait(driver, timeout=3).until(lambda x: x.find_element(by=By.XPATH, value=f'''//mat-select[@formcontrolname="{name}"]'''))
            except:
                error(f'Element {name} not found! trying again in one second.')
                time.sleep(1)
            else:
                return element

    def get_list_of_options(type_of_options:str, formcontrolname:str)->list:
        """"""

        options = None
        tries = 0

        time.sleep(1.5)

        while options is None:
            tries += 1

            if tries == 50:
                critical_error(f'List of {type_of_options} not found! Stopping trying after 5 tries.')
                raise Exception("Too many tries!")

            try:
                options = WebDriverWait(driver, timeout=12).until(lambda x: x.find_elements(by=By.XPATH, value='''//div/mat-option/span[@class="mat-option-text"]'''))
            except:
                error(f'List of {type_of_options} not found! trying again in one second.')
                time.sleep(1)
            else:
                return options

            if tries % 5 == 0:
                try:
                    select_element = WebDriverWait(driver, timeout=3).until(lambda x: x.find_element(by=By.XPATH, value=f'''//mat-select[@formcontrolname="{formcontrolname}"]'''))
                    select_element.click()
                except:
                    error(f'Element {formcontrolname} not found!')
                    time.sleep(1)

    def find_list_element(name:str, formcontrolname:str)->object:
        """"""

        element = None
        tries = 0

        time.sleep(.5)

        while element is None:
            tries += 1

            if tries == 151:
                critical_error(f'Element {name} not found! Stopping trying after 150 tries.')
                raise Exception("Too many tries!")

            try:
                element = WebDriverWait(driver, timeout=3).until(lambda x: x.find_element(by=By.XPATH, value=f'''//span[.=" {name} "]'''))
            except:
                error(f'Element {name} not found! trying again in one second.')
                time.sleep(1)
            else:
                return element

            if tries % 5 == 0:
                try:
                    select_element = WebDriverWait(driver, timeout=3).until(lambda x: x.find_element(by=By.XPATH, value=f'''//mat-select[@formcontrolname="{formcontrolname}"]'''))
                    select_element.click()
                except:
                    error(f'Element {formcontrolname} not found!')
                    time.sleep(1)

    step_info = lambda x: info(f'{x} selected')

    count = 0

    time.sleep(1.25)

    select_scopes = find_matselect_by_form_control_name('uf')
    select_scopes.click()

    time.sleep(1.5)
    scope_object = find_list_element(scope, 'uf')
    scope_object.click()
    step_info(scope)

    time.sleep(3)
    select_municipality = find_matselect_by_form_control_name('municipioBU')
    select_municipality.click()

    with generator(get_list_of_options('municipalities', 'municipioBU')) as municipalities:
        municipalities_length = len(municipalities)
        municipalities = [municipality.text for municipality in municipalities]
        if revert:
            municipalities.reverse()

        for i_m, municipality in enumerate(municipalities):
            if i_m > 0:
                driver = get_page_ready(get_webdriver(headless), base_uri)
                time.sleep(2)
                select_scopes = find_matselect_by_form_control_name('uf')
                select_scopes.click()

                time.sleep(1.5)
                scope_object = find_list_element(scope, 'uf')
                scope_object.click()
                step_info(scope)

                time.sleep(3)
                select_municipality = find_matselect_by_form_control_name('municipioBU')
                select_municipality.click()

            municipality_object = find_list_element(municipality, 'municipioBU')
            municipality_object.click()

            step_info(municipality)

            time.sleep(3)
            select_zone = find_matselect_by_form_control_name('zonaEleitoralBU')
            select_zone.click()

            with generator(get_list_of_options('zones', 'zonaEleitoralBU')) as zones:
                zones_length = len(zones)
                zones = [zone.text for zone in zones]
                for i_z, zone in enumerate(zones):
                    zone_object = find_list_element(zone, 'zonaEleitoralBU')
                    zone_object.click()

                    step_info(zone)

                    time.sleep(3)
                    select_section = find_matselect_by_form_control_name('secaoEleitoralBU')
                    select_section.click()

                    with generator(get_list_of_options('sections', 'secaoEleitoralBU')) as sections:
                        sections_length = len(sections)
                        sections = [section.text for section in sections]
                        for i_s, section in enumerate(sections):
                            section_object = find_list_element(section, 'secaoEleitoralBU')
                            section_object.click()

                            step_info(section)

                            time.sleep(.25)
                            count = download_files(driver, count)

                            info('Zip file downloaded!\n')
                            info(f'Total of Zip files downloaded: {count}\n')

                            time.sleep(.5)
                            expand_menu(driver)

                            if i_s != (sections_length - 1):
                                select_section = find_matselect_by_form_control_name('secaoEleitoralBU')
                                select_section.click()

                                time.sleep(1)

                    if i_z != (zones_length - 1):
                        select_zone = find_matselect_by_form_control_name('zonaEleitoralBU')
                        select_zone.click()

            if i_m != (municipalities_length - 1):
                select_municipality = find_matselect_by_form_control_name('municipioBU')
                select_municipality.click()

            driver.quit()

    return count

def start()->None:
    """"""

    info(f'Starting the Web Scraper for RDV, BU, and Logs of the 2022 Federal Elections (2nd round), state of {scope}.\n')

    # Declaring other variables and instantiating objects
    base_uri = 'https://resultados.tse.jus.br/oficial/app/index.html#/divulga;e=545'

    headless = confirm('Do you want the browser to be "headless"? [y/n] ')
    revert = confirm('Do you want to reverse the order of the municipalities? [y/n] ')

    driver = get_page_ready(get_webdriver(headless), base_uri)

    time.sleep(2)

    downloaded_total = select_evm_and_download_files(driver, headless, base_uri, revert)

    info(f'''Download complete! Files from {downloaded_total} EVM's from {scope} were downloaded.''')
    info('End of the program. The web scraper will now close.')

if __name__ == '__main__':
    start()
