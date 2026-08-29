from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class PaymentPage:

    PAYMENT_BUTTON = (By.XPATH, '//*[@id="root"]/div/button[1]')
    CREDIT_BUTTON = (By.XPATH, '//*[@id="root"]/div/button[2]')
    CARD_INPUT = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[1]/span/span/span[2]/input')
    MONTH_INPUT = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[1]/span/span/span[2]/input')
    YEAR_INPUT = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[2]/span/span[2]/span/span/span[2]/input')
    OWNER = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[1]/span/span/span[2]/input')
    CVV_INPUT = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[3]/span/span[2]/span/span/span[2]/input')
    CONTINUE_BUTTON = (By.XPATH, '//*[@id="root"]/div/form/fieldset/div[4]/button')
    NTF= (By.CSS_SELECTOR, 'div[class*="notification"]')
    CLOSE_NTF_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/button/span/span/span')
    INPUT_SUB = (By.CLASS_NAME, 'input__sub')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def login_page(self):
        self.driver.get('http://localhost:8080/')
        return self.driver

    def click_payment_button(self, payment_method):
        method = payment_method
        if method == 'card':
            self.driver.find_element(*self.PAYMENT_BUTTON).click()
        elif method == 'credit':
            self.driver.find_element(*self.CREDIT_BUTTON).click()

    def click_continue_button(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def enter_card_number(self, card_number):
        self.driver.find_element(*self.CARD_INPUT).send_keys(card_number)

    def enter_month_number(self, month_number):
        self.driver.find_element(*self.MONTH_INPUT).send_keys(month_number)

    def enter_year_number(self, year_number):
        self.driver.find_element(*self.YEAR_INPUT).send_keys(year_number)

    def enter_owner(self, owner):
        self.driver.find_element(*self.OWNER).send_keys(owner)

    def enter_cvv(self, cvv):
        self.driver.find_element(*self.CVV_INPUT).send_keys(cvv)

    def send_form(self, payment_method, card_number, month_number, year_number, owner, cvv):
        self.click_payment_button(payment_method)
        self.enter_card_number(card_number)
        self.enter_month_number(month_number)
        self.enter_year_number(year_number)
        self.enter_owner(owner)
        self.enter_cvv(cvv)
        self.click_continue_button()

    def find_notification(self):
        self.wait.until(
            ec.visibility_of_element_located(self.NTF)
        )
        return self.driver.find_element(*self.NTF).text

    def close_notification(self):
        self.driver.find_element(*self.CLOSE_NTF_BUTTON).click()

    def find_error_sub(self):
        return self.driver.find_element(*self.INPUT_SUB).text
