import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RzdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Настройка WebDriver перед запуском тестов."""
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get("https://rzd.ru/")
        cls.accept_cookies(cls.driver)

    @classmethod
    def accept_cookies(cls, driver):
        """Метод для принятия cookie-файлов."""
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять')]"))
            )
            cookie_button.click()
        except Exception as e:
            print("Кнопка принятия cookie-файлов не найдена или уже была обработана.")

    def setUp(self):
        """Обновление страницы перед каждым тестом и принятие cookie-файлов."""
        self.driver.refresh()
        self.accept_cookies(self.driver)

    def test_search_tickets(self):
        """Тест на поиск билетов."""
        search_button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Купить билет')]")
        search_button.click()
        self.assertIn("Купить билет", self.driver.title)

    def test_find_station(self):
        """Тест на поиск станции."""
        try:
            # Найти поле ввода "Откуда"
            station_input = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Откуда']"))
            )
            station_input.click()
            station_input.send_keys("Москва")

            # Подождать, пока появится список подсказок
            results = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@id='rzd-search-widget']/div[1]/div[1]/div[1]/div[1]/ul")
                )
            )
            self.assertGreater(len(results), 0, "Список станций не отображён.")

            # Выбрать первый элемент в списке
            results[0].click()

            # Проверить, что поле заполнено выбранной станцией
            selected_station = station_input.get_attribute("value")
            self.assertIn("Москва", selected_station, "Станция не выбрана корректно.")

        except TimeoutException:
            self.fail("Не удалось найти или выбрать станцию. Проверьте структуру страницы и XPath.")

    def test_check_timetable(self):
        """Тест на проверку расписания."""
        timetable_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Купить билет')]")
        timetable_link.click()
        self.assertIn("Купить билет", self.driver.title)

    def test_services_info(self):
        """Тест на проверку информации об услугах."""
        services_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Услуги и сервисы')]")
        services_link.click()
        self.assertIn("Услуги и сервисы", self.driver.title)

    def test_news_section(self):
        """Тест на проверку секции новостей."""
        news_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Информация')]")
        news_link.click()
        news_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Информация')]"))
        )
        self.assertTrue(news_title.is_displayed(), "Секция новостей недоступна.")

    @classmethod
    def tearDownClass(cls):
        """Закрытие WebDriver после завершения тестов."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
