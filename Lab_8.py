from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

# Инициализация веб-драйвера
driver = webdriver.Chrome()

try:
    # 1. Перейти на страницу
    driver.get("https://demoqa.com/")
    driver.maximize_window()

    # Ожидание и закрытие баннера (если есть)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "fixedban"))
        )
        driver.execute_script("document.getElementById('fixedban').style.display='none';")
    except:
        print("Баннер не найден или уже скрыт.")

    # 2. Перейти в раздел 'Book Store Application'
    book_store = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Book Store Application']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", book_store)  # Скроллинг к элементу
    book_store.click()

    # 3. Выбрать пункт 'Login'
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Login']"))
    )
    login_button.click()

    # 4. Ввести UserName и Password
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userName"))
    )
    username_input.send_keys("test_user")

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("test_password")

    # 5. Нажать Login
    login_button = driver.find_element(By.ID, "login")
    login_button.click()

    # 6. Проверить надпись Invalid username or password!
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[@id='name' and text()='Invalid username or password!']"))
    )
    assert error_message.is_displayed(), "Сообщение об ошибке не отображается!"

    print("Тест пройден: сообщение об ошибке отображается.")

finally:
    # Закрытие браузера
    driver.quit()
