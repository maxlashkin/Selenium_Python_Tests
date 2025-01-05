"""Написать 3 тест
1. Перейти на страницу https://demoqa.com/
2. Перейти в раздел 'Elements'
3. Выбрать пункт 'Radio Button'
4. Выбрать Yes
5. Проверить что появилась надпись Yes
6. Выбрать Impressive
7. Проверить что появилась надпись Impressive
8. Проверить что кнопка No недоступна"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация веб-драйвера
driver = webdriver.Chrome()

try:
    # 1. Перейти на страницу
    driver.get("https://demoqa.com/")
    driver.maximize_window()

    # 2. Перейти в раздел 'Elements'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='card-body']//h5[text()='Elements']"))
    ).click()

    # 3. Выбрать пункт 'Radio Button'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Radio Button']"))
    ).click()

    # 4. Выбрать Yes
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='yesRadio']"))
    ).click()

    # 5. Проверить, что появилась надпись Yes
    yes_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Yes']"))
    )
    assert yes_message.is_displayed(), "Сообщение 'Yes' не отображается!"
    print("Тест: сообщение 'Yes' отображается.")

    # 6. Выбрать Impressive
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='impressiveRadio']"))
    ).click()

    # 7. Проверить, что появилась надпись Impressive
    impressive_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Impressive']"))
    )
    assert impressive_message.is_displayed(), "Сообщение 'Impressive' не отображается!"
    print("Тест: сообщение 'Impressive' отображается.")

    # 8. Проверить, что кнопка No недоступна
    no_button = driver.find_element(By.XPATH, "//input[@id='noRadio']")
    assert not no_button.is_enabled(), "Кнопка 'No' доступна, но должна быть недоступна!"
    print("Тест: кнопка 'No' недоступна.")

finally:
    # Закрытие браузера
    driver.quit()
