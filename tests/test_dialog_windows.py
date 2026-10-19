import allure
import pytest
from views.dialogs import DialogView

@pytest.fixture
def screen(web_driver, configuration):
    return DialogView(web_driver, configuration).open('modals')

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P01: простое окно содержит ожидаемый текст')
def test_scenario_simple_content(screen):
    screen.open_dialog('simple')
    assert 'Hi, I’m a simple modal.' in screen.visible(screen.simple + ' .pum-content').text

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P02: закрытие простого окна крестиком')
def test_scenario_simple_close(screen):
    screen.open_dialog('simple')
    screen.dismiss(screen.simple)
    assert screen.visible('#formModal').is_enabled()

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P03: повторное открытие простого окна')
def test_scenario_simple_reopen(screen):
    screen.open_dialog('simple')
    screen.dismiss(screen.simple)
    screen.open_dialog('simple')
    assert screen.visible(screen.simple).is_displayed()

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P04: форма открывается, все поля доступны')
def test_scenario_form_fields(screen):
    screen.open_dialog('form')
    for css in [screen.name, screen.email, screen.message]:
        assert screen.visible(css).is_enabled()

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P05: форма закрывается крестиком')
def test_scenario_form_close(screen):
    screen.open_dialog('form')
    screen.dismiss(screen.form)
    assert screen.visible('#simpleModal').is_enabled()

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P06: форма закрывается Escape')
def test_scenario_form_escape(screen):
    screen.open_dialog('form')
    screen.press_escape()
    screen.wait_closed(screen.form)

@allure.feature('Модальные окна')
@pytest.mark.positive
@allure.title('MOD-P07: отправка формы со списком Automation Tools в Message')
def test_scenario_submit_form(screen):
    screen.open_dialog('form')
    expected = screen.complete_contact_form()
    assert screen.visible(screen.message).get_attribute('value') == expected
    screen.send_form()
    screen.expect_confirmation()

@allure.feature('Модальные окна')
@pytest.mark.negative
@allure.title('MOD-N01: пустое обязательное имя блокирует отправку')
def test_scenario_required_name(screen):
    screen.open_dialog('form')
    screen.complete_contact_form(name='')
    screen.send_form()
    screen.expect_validation_error(screen.name)

@allure.feature('Модальные окна')
@pytest.mark.negative
@allure.title('MOD-N02: неверный email блокирует отправку')
def test_scenario_invalid_email(screen):
    screen.open_dialog('form')
    screen.complete_contact_form(email='invalid-address')
    screen.send_form()
    screen.expect_validation_error(screen.email)

@allure.feature('Модальные окна')
@pytest.mark.negative
@allure.title('MOD-N03: Escape не закрывает простое окно')
def test_scenario_simple_ignores_escape(screen):
    screen.open_dialog('simple')
    screen.press_escape()
    screen.verify_stays_open(screen.simple)
