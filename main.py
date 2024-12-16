from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.nba.com/')

driver.maximize_window()

stats = driver.find_element(By.LINK_TEXT,'Stats')
stats.click()

try:
    time.sleep(2)
    decline = driver.find_element(By.CSS_SELECTOR,'#onetrust-reject-all-handler')
    decline.click()
except:
    pass

time.sleep(2)
all_players_stats = driver.find_element(By.LINK_TEXT,'See All Player Stats')
all_players_stats.click()

time.sleep(2)
per_game = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[3]/label/div/select/option[2]')
per_game.click()

time.sleep(2)
body = driver.find_elements(By.CSS_SELECTOR,'.Crom_body__UYOcU tr')

class_to_remove = 'Crom_stickySecondColumn__29Dwf'
player_names = []
for row in body:
    tds = row.find_elements(By.TAG_NAME, 'td')
    for td in tds:
        if class_to_remove in td.get_attribute('class').split():
            player_names.append(td.text)
            driver.execute_script("""
                var td = arguments[0];
                td.parentNode.removeChild(td);
            """, td)
            break

head = driver.find_elements(By.CSS_SELECTOR,'.Crom_headers__mzI_m th')
visible_head = [th for th in head if th.is_displayed()]

stringg = ''
list_of_lists_body = []
listt = []
for i in body:
    stringg = i.text
    listt = stringg.split(' ')
    listt = listt[1:]
    list_of_lists_body.append(listt)

list_head = []
for i in visible_head:
    stringg = i.text
    list_head.append(stringg)

list_head = list_head[1:]

for i in range(len(list_of_lists_body)):
    list_of_lists_body[i].insert(0, player_names[i])


df = pd.DataFrame(list_of_lists_body, columns=list_head)

df.to_csv("top_50_nba_players_stats.csv",index=False)

print(df)
