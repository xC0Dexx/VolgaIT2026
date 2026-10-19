import calendar
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from views.base_view import BrowserView

class DateSelectionView(BrowserView):
    field = 'main input.jp-contact-form-date'
    picker = '.dp'

    @allure.step('Ввести дату {value}')
    def type_date(self, value):
        field = self.visible(self.field)
        field.clear()
        field.send_keys(value)
        field.send_keys(Keys.TAB)

    def read_date(self):
        return self.visible(self.field).get_attribute('value')

    def month_caption(self):
        return self.visible('.dp-cal-month').text + ' ' + self.visible('.dp-cal-year').text

    @allure.step('Выбрать дату {target} через пагинацию календаря')
    def choose_date(self, target):
        self.click(self.field)
        for _ in range(240):
            current = (int(self.visible('.dp-cal-year').text), list(calendar.month_name).index(self.visible('.dp-cal-month').text))
            wanted = (target.year, target.month)
            if current == wanted:
                day = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(concat(" ",normalize-space(@class)," ")," dp-day ") and not(contains(@class,"dp-edge-day")) and normalize-space()="{target.day}"]')))
                day.click()
                self.wait_closed(self.picker)
                return
            old = self.month_caption()
            self.click('.dp-next' if current < wanted else '.dp-prev')
            self.wait.until(lambda _: self.month_caption() != old)
        raise AssertionError('Превышен лимит пагинации')

    def send_form(self):
        self.click('main form button[type="submit"]')

    def expect_validation_error(self):
        self.wait.until(lambda d: any((e.is_displayed() and e.text.strip() for e in d.find_elements(By.CSS_SELECTOR, 'main .contact-form__input-error, main .contact-form__error'))) or self.visible(self.field).get_attribute('aria-invalid') == 'true')
        assert self.visible(self.field).is_displayed()
