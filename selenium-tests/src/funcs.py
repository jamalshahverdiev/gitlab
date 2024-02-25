def sign_in(driver, By):
    username_field = driver.find_element(By.ID, 'username')  
    password_field = driver.find_element(By.ID, 'password')  
    username_field.send_keys('t.owen')
    password_field.send_keys('Foo_b_ar123!')
    sign_in_button = driver.find_element(By.ID, 'kc-login')  
    sign_in_button.click()

def new_item_folder(WebDriverWait, driver, By, EC):
    new_item_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "New Item"))
    )
    new_item_link.click()

    item_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )
    item_name_input.send_keys('BigBang')

    folder_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Folder')]"))
    )
    folder_radio_button.click()

    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    ok_button.click()

    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
    )
    save_button.click()

def new_item_multibranch_pipeline(WebDriverWait, driver, EC, By):
    new_item_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "New Item"))
    )
    new_item_link.click()

    item_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )
    item_name_input.send_keys('Romulan')

    multibranch_pipeline_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Multibranch Pipeline')]"))
    )
    multibranch_pipeline_option.click()

    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    ok_button.click()

    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
    )
    save_button.click()
