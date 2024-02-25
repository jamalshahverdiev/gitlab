from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# html_content = driver.page_source
# with open('page_source.html', 'w', encoding='utf-8') as file:
#     file.write(html_content)

driver.get("http://10.100.100.100:8081")
driver.find_element(By.ID, "nx-header-signin-1145").click()

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
except TimeoutException:
    print("Timeout waiting for login fields.")
    driver.quit()
    exit(1)

username_field = driver.find_element(By.NAME, 'username')
password_field = driver.find_element(By.NAME, 'password')
username_field.send_keys("admin")
password_field.send_keys("freebsd")

driver.find_element(By.ID, "button-1178-btnInnerEl").click()
driver.find_element(By.ID, "button-1127-btnIconEl").click()

users_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Users')]"))
)
users_button.click()
create_local_user_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create local user')]"))
)
create_local_user_button.click()

try:
    user_id_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='userId' and not(@readonly)]"))
    )
    user_id_field.clear()
    user_id_field.send_keys("newuser")

    sleep(1)
    first_name_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='firstName' and not(@readonly)]"))
    )
    first_name_field.send_keys("FirstName")
    
    last_name_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='lastName' and not(@readonly)]"))
    )
    last_name_field.send_keys("LastName")
    
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='email' and not(@readonly)]"))
    )
    email_field.send_keys("email@example.com")
    
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='password' and not(@readonly)]"))
    )
    password_field.send_keys("password123")
    
    confirm_password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='password'])[2]"))
    )
    confirm_password_field.send_keys("password123")
    
    # Find the dropdown element by its placeholder or other attributes
    # dropdown_element = driver.find_element(By.XPATH, "//input[@placeholder='Select status']")
    # print(dropdown_element.get_attribute('outerHTML'))

    driver.execute_script("document.querySelectorAll(\"input[placeholder='Select status']\")[1].value = 'Active'")
    driver.execute_script("document.querySelectorAll(\"input[placeholder='Select status']\")[1].click()")
    remove_js = """
    var removeLi = document.querySelectorAll('.x-boundlist-list-ct.x-unselectable.x-scroller ul li')[0];
    document.querySelectorAll('.x-boundlist-list-ct.x-unselectable.x-scroller ul:nth-child(1)')[2].removeChild(removeLi);
    """
    driver.execute_script(remove_js)

    add_js = """
    var addLi = document.createElement('li');
    addLi.innerHTML = 'nx-admin';
    addLi.className = 'x-boundlist-item';
    document.querySelectorAll('.x-boundlist-list-ct.x-unselectable.x-scroller ul')[3].appendChild(addLi);
    """
    driver.execute_script(add_js)

    driver.save_screenshot('filled_form.png')

except TimeoutException as e:
    print(f"Timeout encountered: {e}")
    driver.save_screenshot('error_screenshot.png')

driver.quit()

