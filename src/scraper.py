from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.ui as UI
from colorama import Fore, Back, Style
import time 
from poke_dictionary import * 
from consts import *
# from squads import *
from metas import *
import csv


def scrape_some_stuff():
    MY_SQUAD = ["marowak_alolan"] #SINISTER_CONCENTRATED_META
    OPPONENT_SQUAD = ["marowak_alolan"] #SINISTER_CONCENTRATED_META
    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver') # TODO this really works only on MacOS / unix
    result_matrix = []
    counter = 0
    total_number = len(OPPONENT_SQUAD) * len(MY_SQUAD)
    percentage = 0
    for defender in OPPONENT_SQUAD:
        attacker_results = []
        for attacker in MY_SQUAD:
            # just anything, we want to see te table down
            attacker_moveset = POKE_DICTIONARY[attacker]['moveset']
            defender_moveset = POKE_DICTIONARY[defender]['moveset']
            attacker_name = attacker[:-1] if attacker[-1:].isdigit() else attacker
            defender_name =  defender[:-1] if defender[-1:].isdigit() else defender
            url = f'https://pvpoke.com/battle/1500/{attacker_name}/{defender_name}/{SHIELD_SCENARIO}/{attacker_moveset}/{defender_moveset}/'
            driver.get(url)
            delay = 2 # seconds
            try:
                #WebDriverWait(driver, delay) #.until(EC.presence_of_element_located(driver.find_elements_by_xpath('..//elementid')))
                time.sleep(delay) # needed because the page loads with all sims at 100 value and requires between 0.5 to 2 seconds to load
                scenario_0s = [
                    driver.find_element_by_class_name(SHIELD_SCENARIO_00_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_10_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_20_CLASS).get_attribute("innerHTML")
                ]
                scenario_1s = [
                    driver.find_element_by_class_name(SHIELD_SCENARIO_01_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_11_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_21_CLASS).get_attribute("innerHTML")
                ]
                scenario_2s = [
                    driver.find_element_by_class_name(SHIELD_SCENARIO_02_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_12_CLASS).get_attribute("innerHTML"),
                    driver.find_element_by_class_name(SHIELD_SCENARIO_22_CLASS).get_attribute("innerHTML")
                ]

                moves_list = {
                    'attacker': [],
                    'defender': [],
                }

                attacker_moveset_list = attacker_moveset.split('-')
                defender_moveset_list = defender_moveset.split('-')
                move_selects = driver.find_elements_by_xpath(MOVE_SELECTS_XPATH)
                attacker_fast_moves = move_selects[0].find_elements_by_xpath('option')
                attacker_charged_1_moves = move_selects[1].find_elements_by_xpath('option')
                attacker_charged_2_moves = move_selects[2].find_elements_by_xpath('option')
                moves_list['attacker'].append(attacker_fast_moves[int(attacker_moveset_list[0])].get_attribute('value'))
                moves_list['attacker'].append(attacker_charged_1_moves[int(attacker_moveset_list[1])].get_attribute('value'))
                moves_list['attacker'].append(attacker_charged_2_moves[int(attacker_moveset_list[2])].get_attribute('value'))
                defender_fast_moves = move_selects[4].find_elements_by_xpath('option')
                defender_charged_1_moves = move_selects[5].find_elements_by_xpath('option')
                defender_charged_2_moves = move_selects[6].find_elements_by_xpath('option')
                moves_list['defender'].append(defender_fast_moves[int(defender_moveset_list[0])].get_attribute('value'))
                moves_list['defender'].append(defender_charged_1_moves[int(defender_moveset_list[1])].get_attribute('value'))
                moves_list['defender'].append(defender_charged_2_moves[int(defender_moveset_list[2])].get_attribute('value'))               

                results_list = []
                results_list.append(scenario_0s)
                results_list.append(scenario_1s)
                results_list.append(scenario_2s)

                attacker_results.append({
                    'title': f'{attacker} vs {defender}',
                    'moves': moves_list,
                    'url': url,
                    'results': results_list
                })

                raise_alert_100 = False
                for value in scenario_0s:
                    if str(value) == '100':
                        raise_alert_100 = True
                for value in scenario_1s:
                    if str(value) == '100':
                        raise_alert_100 = True
                for value in scenario_2s:
                    if str(value) == '100':
                        raise_alert_100 = True

                counter += 1
                percentage = round((counter / total_number) * 100, 2)
                mins_left, secs_left = divmod((total_number*(delay+1)) - (counter*(delay+1)), 60)
                mins_passed, secs_passed = divmod((counter*(delay+1)), 60)
                if raise_alert_100:
                    print(Fore.RED + f'{attacker} vs {defender} has results = 100, take a look!' + (' '*100)  + Style.RESET_ALL)
                header = f'[ {percentage}% | {counter}/{total_number} | estim. {mins_passed}m{secs_passed}s passed | {mins_left}m{secs_left}s left ]'
                print(f'{header} {attacker} vs {defender}' + (' '*100)  , end='\r')
                
            except TimeoutException:
                print('Could not load the page' + (' '*100)  )
        
        result_matrix.append(attacker_results)
    print('[ 100.0% ] Scraping DONE' + (' '*100)  )
    
    return result_matrix


def export_results(result_matrix):
    with open('result_csv.csv', mode='w') as result_csv:
        result_csv_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for attacker_matches in result_matrix:
            title_row_csv = []
            url_row_csv = []
            scenario_0s_row_csv = []
            scenario_1s_row_csv = []
            scenario_2s_row_csv = []

            for defender in attacker_matches:
                title_row_csv.append(defender['title'])
                title_row_csv.append('')
                title_row_csv.append('')
                url_row_csv.append(defender['url'])
                url_row_csv.append(' / '.join(defender['moves']['attacker']))
                url_row_csv.append(' / '.join(defender['moves']['defender']))
                scenario_0s_row_csv.append(defender['results'][0][0])
                scenario_0s_row_csv.append(defender['results'][0][1])
                scenario_0s_row_csv.append(defender['results'][0][2])
                scenario_1s_row_csv.append(defender['results'][1][0])
                scenario_1s_row_csv.append(defender['results'][1][1])
                scenario_1s_row_csv.append(defender['results'][1][2])
                scenario_2s_row_csv.append(defender['results'][2][0])
                scenario_2s_row_csv.append(defender['results'][2][1])
                scenario_2s_row_csv.append(defender['results'][2][2])
        
            result_csv_writer.writerow(title_row_csv)
            result_csv_writer.writerow(url_row_csv)
            result_csv_writer.writerow(scenario_0s_row_csv)
            result_csv_writer.writerow(scenario_1s_row_csv)
            result_csv_writer.writerow(scenario_2s_row_csv)

    print('CSV created')

if __name__ == "__main__":
    export_results(scrape_some_stuff())
