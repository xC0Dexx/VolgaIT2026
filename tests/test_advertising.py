import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException
from views.advertisements import AdvertisementView

@pytest.fixture
def screen(web_driver, configuration):
    return AdvertisementView(web_driver, configuration).open('ads')

@allure.feature('Реклама')
@pytest.mark.positive
@allure.title('ADS-P01: реклама появляется автоматически')
def test_scenario_auto_open(screen):
    assert screen.wait_for_ad().is_displayed()

@allure.feature('Реклама')
@pytest.mark.positive
@allure.title('ADS-P02: окно содержит рекламный текст')
def test_scenario_content(screen):
    screen.wait_for_ad()
    assert 'I am an ad.' in screen.visible(screen.ad + ' .pum-content').text

@allure.feature('Реклама')
@pytest.mark.positive
@allure.title('ADS-P03: крестик закрывает рекламное окно')
def test_scenario_close(screen):
    screen.wait_for_ad()
    screen.dismiss()
    assert screen.visible('main h1').text == 'Ads'

@allure.feature('Реклама')
@pytest.mark.positive
@allure.title('ADS-P04: реклама появляется после обновления страницы')
def test_scenario_refresh(screen):
    screen.wait_for_ad()
    screen.dismiss()
    screen.driver.refresh()
    assert screen.wait_for_ad().is_displayed()

@allure.feature('Реклама')
@pytest.mark.positive
@pytest.mark.parametrize('width,height', [(390, 844), (768, 1024), (1440, 1000)], ids=['ADS-P05', 'ADS-P06', 'ADS-P07'])
@allure.title('Кнопка закрытия доступна в окне {width}×{height}')
def test_scenario_responsive_close(screen, width, height):
    screen.driver.set_window_size(width, height)
    screen.wait_for_ad()
    button = screen.visible(screen.ad + ' .pum-close')
    rect = button.rect
    viewport = screen.driver.execute_script('return [innerWidth, innerHeight]')
    assert 0 <= rect['x'] and rect['x'] + rect['width'] <= viewport[0]
    top = screen.driver.execute_script('return arguments[0].getBoundingClientRect().top', button)
    assert 0 <= top and top + rect['height'] <= viewport[1]
    screen.dismiss()

@allure.feature('Реклама')
@pytest.mark.negative
@allure.title('ADS-N01: Escape не закрывает рекламу')
def test_scenario_escape_ignored(screen):
    screen.wait_for_ad()
    screen.press_escape()
    screen.verify_stays_open(screen.ad)

@allure.feature('Реклама')
@pytest.mark.negative
@allure.title('ADS-N02: нажатие на подложку не закрывает рекламу')
def test_scenario_overlay_ignored(screen):
    screen.wait_for_ad()
    screen.click_backdrop(screen.ad)
    screen.verify_stays_open(screen.ad)

@allure.feature('Реклама')
@pytest.mark.negative
@allure.title('ADS-N03: реклама блокирует нажатие на фоновую ссылку')
def test_scenario_background_blocked(screen):
    screen.wait_for_ad()
    link = screen.visible('main a')
    url = screen.driver.current_url
    with pytest.raises(ElementClickInterceptedException):
        link.click()
    assert screen.driver.current_url == url
    screen.verify_stays_open(screen.ad)
