from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from src.funcs import sign_in, new_item_folder, new_item_multibranch_pipeline
from time import sleep

options = FirefoxOptions()
service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)
url = 'http://10.100.100.100:8080/realms/infra/protocol/openid-connect/auth?client_id=jenkins&redirect_uri=http%3A%2F%2F10.100.100.100%3A9090%2FsecurityRealm%2FfinishLogin&state=1d4d38f0-2f1d-45ba-bc6f-5658cd90602c&response_type=code&scope=openid'
driver.get(url)

sign_in(driver, By)
new_item_folder(WebDriverWait, driver, By, EC)
new_item_multibranch_pipeline(WebDriverWait, driver, EC, By)

sleep(1)
driver.save_screenshot('after_all_actions.png')
driver.quit()
