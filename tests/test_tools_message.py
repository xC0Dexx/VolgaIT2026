import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from views.dialogs import DialogView

@allure.feature('Дополнительное требование: Message')
@pytest.mark.positive
@allure.title('FORM-P01: заполнить Message списком из раздела Automation tools')
def test_scenario_message_from_tools(web_driver, configuration):
    screen = DialogView(web_driver, configuration).open('form-fields')
    items = screen.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//label[normalize-space()="Automation tools"]/following-sibling::ul[1]/li')))
    values = [item.text.strip() for item in items]
    assert values and all(values)
    with allure.step('Соединить названия через запятую и заполнить Message'):
        expected = ', '.join(values)
        screen.visible('#message').clear()
        screen.visible('#message').send_keys(expected)
    assert screen.visible('#message').get_attribute('value') == expected
