from selenium.common.exceptions import TimeoutException
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserView:

    def __init__(self, web_driver, configuration):
        self.driver = web_driver
        self.base, timeout = configuration
        self.wait = WebDriverWait(web_driver, timeout)

    @allure.step('Открыть страницу {path}')
    def navigate(self, path):
        self.driver.get(self.base.rstrip('/') + '/' + path.strip('/') + '/')
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'main')))
        return self

    def visible(self, css):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))

    @allure.step('Нажать {css}')
    def click(self, css):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        element.click()

    def wait_closed(self, css):
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css)))

    def verify_stays_open(self, css, seconds=1):
        try:
            WebDriverWait(self.driver, seconds, poll_frequency=0.1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css)))
        except TimeoutException:
            return
        raise AssertionError(f'{css} неожиданно исчез')

    @allure.step('Нажать Escape')
    def press_escape(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    @allure.step('Нажать вне контейнера модального окна')
    def click_backdrop(self, css):
        overlay = self.visible(css)
        ActionChains(self.driver).move_to_element_with_offset(overlay, -overlay.size['width'] // 2 + 5, -overlay.size['height'] // 2 + 5).click().perform()
