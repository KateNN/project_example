from page_objects.LoginPage import LoginPage
import pytest
import allure


@pytest.mark.regression
@allure.feature("Roles and Permissions")
@allure.title("Users with PitStop role can log in to PitStop and see the content")
def test_pitstop_user_can_log_in(driver):
    with allure.step("Going to log in page"):
        page = LoginPage(driver)
        page.open()
        page.check_page_title(page.LOGIN_PAGE_TITLE)

    with allure.step("Logging to PitStop as a PitStop Authorized user (Administrator)"):
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step(f"Asserting that welcome text '{page.WELCOME_TEXT}' is displayed for the user"):
        welcome = page.locate_element(page.WELCOME_TO_PITSTOP)
        assert welcome.text == page.WELCOME_TEXT, \
            [f"Wrong message displayed for the user: {welcome} instead of {page.WELCOME_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Roles and Permissions")
@allure.title("Users with no PitStop role can log in to PitStop, but not allowed to see the content")
def test_user_with_no_pitstop_role_cannot_see_content(driver):
    with allure.step("Going to log in page"):
        page = LoginPage(driver)
        page.open()
        page.check_page_title(page.LOGIN_PAGE_TITLE)

    with allure.step("Logging to PitStop as a User with no PitStop role"):
        page.log_in(username=page.USER_WITH_NO_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Asserting that 403 is displayed for the user"):
        result = page.locate_element(page.NOT_AUTHORIZED)
        assert result.text == '403',\
            [f"Wrong message displayed for the user: {result} instead of '403'", page.make_screenshot()]
