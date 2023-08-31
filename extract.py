from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


import telebot
import os
import time


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))



def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def autoAbsensi(driver: webdriver.Chrome) -> str:
    # driver.get("https://www.google.com")
    # return driver.page_source
    driver.set_window_size(375, 812)  # iPhone X size


    url = os.getenv("URL")

    # Opening the website
    driver.get(url)

    npm = driver.find_element(By.NAME, "username")
    npm.send_keys(os.getenv('NPM'))

    pw = driver.find_element(By.NAME, "password")
    pw.send_keys(os.getenv('PASSWORD'))

    pw.send_keys(Keys.ENTER)

    menu = driver.find_element(By.ID, "mobile-collapse")

    menu.click()

    list = driver.find_elements(By.CLASS_NAME, "pcoded-item")

    for x in list:
        li = x.find_elements(By.TAG_NAME, "li")
        li[1].click()
    
    try:
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "konfirmasi-kehadiran")))
        button.click()
        time.sleep(1)  # Delay for 1 seconds.
        bot.send_message(os.getenv('GROUP_ID'), 'Berhasil absen')
    
                
        confirm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "confirm")))
        confirm.send_keys(Keys.ENTER)
        confirm.click()
    
        return {"message": "berhasil absen...!!"}
    except:
        
        bot.send_message(os.environ['GROUP_ID'], 'belum waktunya absen')
        return {"message": "belum waktu absen...!!"}
            
    

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")
