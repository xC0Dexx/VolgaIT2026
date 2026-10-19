from datetime import date
import allure
import pytest
from views.date_selection import DateSelectionView

@pytest.fixture
def screen(web_driver, configuration):
    return DateSelectionView(web_driver, configuration).open('calendars')

@allure.feature('Календарь')
@pytest.mark.positive
@allure.title('CAL-P01: календарь открывается при нажатии на поле')
def test_scenario_open(screen):
    screen.click(screen.field)
    assert screen.visible(screen.picker).is_displayed()

@allure.feature('Календарь')
@pytest.mark.positive
@pytest.mark.parametrize('direction,reverse', [('next', 'prev'), ('prev', 'next')], ids=['CAL-P02', 'CAL-P03'])
@allure.title('Пагинация календаря: {direction} и возврат')
def test_scenario_month_navigation(screen, direction, reverse):
    screen.click(screen.field)
    before = screen.month_caption()
    screen.click('.dp-' + direction)
    screen.wait.until(lambda _: screen.month_caption() != before)
    screen.click('.dp-' + reverse)
    screen.wait.until(lambda _: screen.month_caption() == before)

@allure.feature('Календарь')
@pytest.mark.positive
@pytest.mark.parametrize('month,day', [(1, 1), (12, 31), (4, 30), (2, 29)], ids=['CAL-P04', 'CAL-P05', 'CAL-P06', 'CAL-P07'])
@allure.title('Выбор граничной даты: месяц {month}, день {day}')
def test_scenario_select_boundary_date(screen, month, day):
    year = date.today().year
    if month == 2:
        while year % 4 or (year % 100 == 0 and year % 400 != 0):
            year += 1
    target = date(year, month, day)
    screen.choose_date(target)
    assert screen.read_date() == target.isoformat()

@allure.feature('Календарь')
@pytest.mark.negative
@pytest.mark.parametrize('value', ['not-a-date', '2025-02-29', '2026-13-01'], ids=['CAL-N01', 'CAL-N02', 'CAL-N03'])
@allure.title('Некорректная дата {value} отклоняется')
def test_scenario_invalid_date(screen, value):
    screen.type_date(value)
    screen.send_form()
    screen.expect_validation_error()
