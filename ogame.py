#! /usr/bin/python3
# ogame.py               uses selenium to bot a ogame play
#                        ressources page


import logging
##logging.basicConfig(filename = 'ogame.log', level=logging.INFO, format='''%(asctime)s -  %(levelname)s
##-  %(message)s''')
logging.basicConfig(level=logging.INFO, format='''%(asctime)s -  %(levelname)s
-  %(message)s''')
logging.info('Start of program')

import time, shelve
from random import shuffle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def wait_page_load(browser):
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'menuTable')))
        logging.info("wait_page_load() : Page is ready.")
    except Exception as err:
        logging.info('wait_page_load() err : Loading took too much time. {err}')

def del_ad():
        try:
            ad = enter = browser.find_element(
                by='xpath',value='/html/body/div[4]/div/div[1]/a')
            ad.click()
            logging.info('del_ad() : Ad deleted')
        except Exception as err:
            logging.info('del_ad() : Ad not found')
    
    
def log_in_game():
    logging.info('''
             #######################
             # Logging in the game #
             #######################''')
    
    browser = webdriver.Firefox()
    browser.minimize_window()
    
    browser.get('https://lobby.ogame.gameforge.com/en_GB/hub')
    htmlElem = browser.find_element(by='tag name',value='html')


    #   logging page
    time.sleep(2)
    log_in = browser.find_element(
        by='xpath',value='/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/ul/li[1]')
    log_in.click()

    email = browser.find_element(
        by='name',value='email')
    email.send_keys('arthur.gires@protonmail.com')

    password = browser.find_element(
        by='name',value='password')
    password.send_keys('8EVWwnQqzksA5XD')

    enter = browser.find_element(
        by='class name',value="button-lg")
    enter.click()

    #   world selection page
    time.sleep(2)
    cookies = browser.find_element(
        by='xpath',value='/html/body/div[3]/div/div/span[2]/button[2]')
    cookies.click()
    time.sleep(2)
    

    enter = browser.find_element(
        by='xpath',value='/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/button')
    enter.click()

    time.sleep(2)
    logging.info(browser.current_window_handle)
    chwd = browser.window_handles
    logging.info(chwd)
    browser.switch_to.window(chwd[1])
    wait_page_load(browser)
    time.sleep(2)
    del_ad()
    
    logging.info('''
                ###########
                # In game #
                ###########''')
    return(browser)

def check_for_upgrades(browser, href):
    try :
            
        upgrade = None
        upgrades_view = browser.find_element_by_xpath(f'//a[@href="{href}"]')
        upgrades_view.click()
        
        wait_page_load(browser)
        del_ad()

        techs = browser.find_elements(
        by='class name',value='technology')
        shuffle(techs)
        unwanted_list = ['Alliance Depot', 'Space Dock','Shipyard',
                         'Solar Satellite', 'Crawler',
                         'Research Lab','Robotics Factory','Missile Silo',
                         'Energy Technology','Laser Technology',
                         'Ion Technology']
        allowed_list = ['Metal Mine','Crystal Mine','Deuterium Synthesizer',
                        'Solar Plant','Fusion Reactor','Metal Storage',
                        'Crystal Storage','Deuterium Tank',
                        'Hyperspace Drive']
        #'Laser Technology','Computer Technology'
        for tech in techs:
            if (tech.get_attribute('data-status') == 'on' and
                tech.get_attribute('aria-label') not in unwanted_list):
                logging.info(f'tech upgraded {tech.get_attribute("aria-label")}')
                upgrade = tech.get_attribute("aria-label")
                tech.click()
                time.sleep(2)
                improve = browser.find_element(
                by='class name',value='upgrade')
                improve.click()
            else:
                continue
                
    except Exception as err:
        logging.info(f'check_for_upgrades() err : {err}')
            
        
    return(upgrade)

def change_planet(planet_name, browser):
    try :
        planet_list = browser.find_elements(
        by='class name',value="smallplanet")
        current_planet = browser.find_element(
            by='class name',value="hightlightPlanet")
        i = planet_list.index(current_planet)
        next_planet = planet_list[i-1]
        planet_name = next_planet.text
        logging.info(f'Changing planet to {planet_name}')
        next_planet.click()
    except Exception as err:
        logging.info(f'''
                #################
                #  Disconected  #
                #################

                last err : {err}
                ''')
        browser.quit()
        browser = log_in_game()
    return(planet_name, browser)
    

####___main___

def main():
    start = time.time()
    browser = log_in_game()

    upgraded = {}
    planet = ''
    i = 0

    while True:
        i+=1
        logging.info(f'i = {i}')
        
        planet, browser = change_planet(planet, browser)
        
        # check for ressources
        up1 = check_for_upgrades(browser, href = 'https://s208-en.ogame.gameforge.com/game/index.php?page=ingame&component=supplies')

        
        # check for facilities
        up2 = check_for_upgrades(browser, href = 'https://s208-en.ogame.gameforge.com/game/index.php?page=ingame&component=facilities')


        # check for research
        up3 = check_for_upgrades(browser, href = 'https://s208-en.ogame.gameforge.com/game/index.php?page=ingame&component=research')



        upgraded.setdefault(planet,[])
        up = list(filter(None, [up1, up2, up3]))
        upgraded[planet].extend(up)
        
        logging.info(f'''
            Planet {planet} done.
            Upgraded list {upgraded}
            time : {round((time.time()-start)/60,1)}mn.
            ------------------------''')

        
        time.sleep(200)

if __name__ =='__main__':
    main()
    



