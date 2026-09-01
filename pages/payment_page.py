import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec, wait


class PaymentPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.payment_button = (By.XPATH, '//*[@id="root"]/div/button[1]')
        self.credit_button = (By.XPATH, '//*[@id="root"]/div/button[2]')
        self.card_input = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[1]/span/span/span[2]/input')
        self.month_input = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[1]/span/span/span[2]/input')
        self.year_input = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[2]/span/span/span[2]/input')
        self.holder = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[1]/span/span/span[2]/input')
        self.cvc_input = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[2]/span/span/span[2]/input')
        self.continue_button = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[4]/button')
        self.notification= (By.CSS_SELECTOR, 'div[class*="notification"]')
        self.close_notification_button = (By.XPATH, '//*[@id="root"]/div/div[3]/button/span/span/span')
        self.card_field_error = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[1]/span/span/span[3]')
        self.month_field_error = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[1]/span/span/span[3]')
        self.year_field_error = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[2]/span/span/span[3]')
        self.holder_field_error = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[1]/span/span/span[3]')
        self.cvc_field_error = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[2]/span/span/span[3]')

    @allure.step('Открыть страницу оплаты')
    def login_page(self):
        self.driver.get('http://localhost:8080/')
        return self.driver


    @allure.step('Выбрать способ оплаты')
    def click_payment_button(self, payment_method):
        method = payment_method
        if method == 'card':
            self.driver.find_element(*self.payment_button).click()
        elif method == 'credit':
            self.driver.find_element(*self.credit_button).click()

    @allure.step('Кликнуть кнопку "Продолжить"')
    def click_continue_button(self):
        self.driver.find_element(*self.continue_button).click()

    @allure.step('Ввести номер карты')
    def enter_card_number(self, card_number):
        self.driver.find_element(*self.card_input).send_keys(card_number)

    @allure.step('Ввести месяц')
    def enter_month_number(self, month_number):
        self.driver.find_element(*self.month_input).send_keys(month_number)

    @allure.step('Ввести год')
    def enter_year_number(self, year_number):
        self.driver.find_element(*self.year_input).send_keys(year_number)

    @allure.step('Ввести владельца')
    def enter_holder(self, holder):
        self.driver.find_element(*self.holder).send_keys(holder)

    @allure.step('Ввести код cvc')
    def enter_cvc(self, cvc):
        self.driver.find_element(*self.cvc_input).send_keys(cvc)

    @allure.step('Отправить запрос на оплату')
    def send_form(self, payment_method, card_number, month_number, year_number, owner, cvc):
        self.click_payment_button(payment_method)
        self.enter_card_number(card_number)
        self.enter_month_number(month_number)
        self.enter_year_number(year_number)
        self.enter_holder(owner)
        self.enter_cvc(cvc)
        self.click_continue_button()

    @allure.step('Отображение уведомления о статусе операции')
    def find_notification(self):
        self.wait.until(
            ec.visibility_of_element_located(self.notification)
        )
        self.get_screenshot()
        try:
            return self.driver.find_element(*self.notification).text
        except NoSuchElementException:
            return False


    @allure.step('Закрыть уведомление')
    def close_notification(self):
        close_button = self.wait.until(
            ec.element_to_be_clickable(self.close_notification_button)
        )
        close_button.click()
        self.get_screenshot()
        try:
            self.wait.until(
                ec.invisibility_of_element_located(self.notification)
            )
            return True
        except TimeoutException:
            return False

    @allure.step('Отображение ошибки ввода в поле')
    def find_field_error(self, field):
        fields = {
            'card' : self.card_field_error,
            'month' : self.month_field_error,
            'year' : self.year_field_error,
            'holder' : self.holder_field_error,
            'cvc' : self.cvc_field_error
        }
        self.get_screenshot()
        try:
            return self.driver.find_element(*fields[field]).text
        except NoSuchElementException:
            print('Объект не найден')

    def get_screenshot(self):
        return allure.attach(
            self.driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
