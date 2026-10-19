import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from views.base_view import BrowserView

class DialogView(BrowserView):
    simple = '#pum-1318'
    form = '#pum-674'
    name = '#pum-674 input.name'
    email = '#pum-674 input.email'
    message = '#pum-674 textarea.grunion-field'

    @allure.step('Открыть модальное окно {kind}')
    def open_dialog(self, kind):
        self.click('#simpleModal' if kind == 'simple' else '#formModal')
        self.visible(self.simple if kind == 'simple' else self.form)

    def dismiss(self, css):
        self.click(css + ' .pum-close')
        self.wait_closed(css)

    @allure.step('Получить список Automation Tools средствами Selenium')
    def read_automation_tools(self):
        original = self.driver.current_window_handle
        self.driver.switch_to.new_window('tab')
        try:
            self.navigate('form-fields')
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//label[normalize-space()="Automation tools"]/following-sibling::ul[1]/li')))
            values = [e.text.strip() for e in items if e.text.strip()]
            assert values, 'Раздел Automation Tools найден, но список пуст'
            return values
        finally:
            self.driver.close()
            self.driver.switch_to.window(original)

    @allure.step('Заполнить форму; Message — список Automation Tools через запятую')
    def complete_contact_form(self, name='UI Test', email='ui-test@example.com'):
        text = ', '.join(self.read_automation_tools())
        for css, value in [(self.name, name), (self.email, email), (self.message, text)]:
            element = self.visible(css)
            element.clear()
            if value:
                element.send_keys(value)
        return text

    def send_form(self):
        self.click(self.form + ' button[type="submit"]')

    def expect_confirmation(self):
        self.wait.until(lambda d: any((e.is_displayed() and 'Thank you' in e.text for e in d.find_elements(By.CSS_SELECTOR, '#pum-674 .contact-form-submission, #pum-674 .jetpack-contact-form-success'))))

    def expect_validation_error(self, css):
        self.wait.until(lambda d: self.visible(css).get_attribute('aria-invalid') == 'true' or any((e.is_displayed() and e.text.strip() for e in d.find_elements(By.CSS_SELECTOR, '#pum-674 .contact-form__input-error, #pum-674 .contact-form__error'))))
        assert self.visible(css).is_displayed()
