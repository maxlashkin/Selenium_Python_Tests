from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import string
import random
import time

def generate_valid_password(length=12):
    """Генерация валидного пароля под правила DemoQA."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    specials = "!@#$%^&*()_+-=[]{};:,.?/"

    # Гарантируем все типы
    password_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(specials),
    ]

    all_chars = lowercase + uppercase + digits + specials
    while len(password_chars) < length:
        password_chars.append(random.choice(all_chars))

    random.shuffle(password_chars)
    return "".join(password_chars)

def wait_for_recaptcha_solved(driver, timeout=180):
    """Корректная обработка reCAPTCHA: ждём, пока ты вручную поставишь галочку."""
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']")
            )
        )
        anchor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "recaptcha-anchor"))
        )
        print('Поставь галочку "I\'m not a robot" в браузере...')
        WebDriverWait(driver, timeout).until(
            lambda d: anchor.get_attribute("aria-checked") == "true"
        )
        print("reCAPTCHA отмечена.")
    finally:
        driver.switch_to.default_content()


# ---------- ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА ----------

chrome_options = Options()

prefs = {
    # полностью отключаем менеджер паролей
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    # чтобы не лезли нотификации
    "profile.default_content_setting_values.notifications": 2,
    # доп. отключение безопасного просмотра в тестовой среде
    "safebrowsing.enabled": False,
}

#chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("prefs", {
    "profile.password_manager_leak_detection": False
})

# вырубаем связанные фичи через флаги
#chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,PasswordManagerUI,SafetyCheckChromium")
#chrome_options.add_argument("--password-store=basic")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Перейти на страницу
    driver.get("https://demoqa.com/")
    driver.maximize_window()

    # Спрятать баннер, если есть
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "fixedban"))
        )
        driver.execute_script("document.getElementById('fixedban').style.display='none';")
    except:
        pass

    # 2. Перейти в раздел 'Book Store Application'
    book_store = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Book Store Application']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", book_store)
    book_store.click()

    # 3. Выбрать пункт 'Login'
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Login']"))
    )
    login_button.click()

    # 4. Ввести UserName
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userName"))
    )
    username_input.send_keys("test_user")

    # 5. Ввести Password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("test_password")

    # 6. Нажать Login
    login_button = driver.find_element(By.ID, "login")
    login_button.click()

    # 7. Проверить надпись Invalid username or password!
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@id='name' and text()='Invalid username or password!']")
        )
    )
    assert error_message.is_displayed()
    print("Шаг 7: сообщение об ошибке отображается.")

    # ---------- Шаг 8: New User (фикс клика и вкладки) ----------

    # На всякий случай ещё раз убираем баннер
    try:
        driver.execute_script("document.getElementById('fixedban').style.display='none';")
    except:
        pass

    new_user_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "newUser"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", new_user_button)

    try:
        new_user_button.click()
    except ElementClickInterceptedException:
        # если что-то перекрыло — снова прячем баннер и кликаем скриптом
        try:
            driver.execute_script("document.getElementById('fixedban').style.display='none';")
        except:
            pass
        driver.execute_script("arguments[0].click();", new_user_button)

    # Если открылась новая вкладка – переключаемся на неё
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) >= 1)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # 9. Заполнить First Name (здесь раньше был Timeout)
    first_name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "firstname"))
    )
    first_name_input.send_keys("TestFirst")

    # 10. Заполнить Last Name
    last_name_input = driver.find_element(By.ID, "lastname")
    last_name_input.send_keys("TestLast")

    # 11. Заполнить UserName
    reg_username_input = driver.find_element(By.ID, "userName")
    reg_username_input.send_keys("TestUser123")

    # 12. Заполнить Password 1 символом
    reg_password_input = driver.find_element(By.ID, "password")
    reg_password_input.send_keys("a")

    # 13. Нажать Register
    register_button = driver.find_element(By.ID, "register")
    register_button.click()

    # 14. Проверка "Please verify reCaptcha to register!"
    recaptcha_error = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@id='name' and text()='Please verify reCaptcha to register!']")
        )
    )
    assert recaptcha_error.is_displayed()
    print('Шаг 14: "Please verify reCaptcha to register!" отображается.')

    # 15. Поставить чекбокс I'm not a robot (ручками)
    wait_for_recaptcha_solved(driver)

    # 16. Нажать Register
    register_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "register"))
    )
    register_button.click()

    # 17. Проверка сообщения про требования к паролю
    password_rules_error = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//p[@id='name' and contains(., 'Passwords must have at least one non alphanumeric character')]"
            )
        )
    )
    assert password_rules_error.is_displayed()
    print("Шаг 17: сообщение о требованиях к паролю отображается.")

    # 18. Заполнить Password валидным значением
    reg_password_input = driver.find_element(By.ID, "password")
    reg_password_input.clear()
    valid_password = generate_valid_password()
    print(f"Сгенерированный пароль: {valid_password}")
    reg_password_input.send_keys(valid_password)

    # 19. Снова чекбокс I'm not a robot
    wait_for_recaptcha_solved(driver)

    # 20. Нажать Register
    register_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "register"))
    )
    register_button.click()

    # 21. В модальном окне нажать ОК
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print(f"Текст алерта: {alert.text}")
    alert.accept()
    print("Шаг 21: алерт закрыт.")

    print("Сценарий 1–21 выполнен успешно.")

finally:
    time.sleep(3)
    driver.quit()
