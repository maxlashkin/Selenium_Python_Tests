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
import time

# Настройка драйвера
driver = webdriver.Chrome()
driver.implicitly_wait(10)

try:
    # 1. Перейти на страницу https://demoqa.com/
    driver.get("https://demoqa.com/")
    driver.maximize_window()

    # 2. Перейти в раздел 'Elements'
    elements_section = driver.find_element(By.CSS_SELECTOR, ".card-body h5")
    elements_section.click()

    # 3. Выбрать пункт 'Radio Button'
    radio_button_option = driver.find_element(By.CSS_SELECTOR, "span[title='Radio Button']")
    radio_button_option.click()

    # 4. Выбрать Yes
    yes_button = driver.find_element(By.CSS_SELECTOR, "label[for='yesRadio']")
    yes_button.click()

    # 5. Проверить, что появилась надпись Yes
    result_text = driver.find_element(By.CLASS_NAME, "text-success").text
    assert result_text == "Yes", "Надпись 'Yes' не отображается"

    # 6. Выбрать Impressive
    impressive_button = driver.find_element(By.CSS_SELECTOR, "label[for='impressiveRadio']")
    impressive_button.click()

    # 7. Проверить, что появилась надпись Impressive
    result_text = driver.find_element(By.CLASS_NAME, "text-success").text
    assert result_text == "Impressive", "Надпись 'Impressive' не отображается"

    # 8. Проверить, что кнопка No недоступна
    no_radio_button = driver.find_element(By.ID, "noRadio")
    assert not no_radio_button.is_enabled(), "Кнопка 'No' доступна, хотя должна быть отключена"

    print("Тест успешно выполнен!")

finally:
    # Закрыть браузер
    driver.quit()

