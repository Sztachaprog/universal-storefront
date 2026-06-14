from playwright.sync_api import (
    expect
)
from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.login_page import LoginPage
import allure


@allure.feature("E2E Authentication")
def test_unauthorized_dashboard(page):

    dashboard = DashboardPage(page)
    dashboard.navigate()

    assert page.url == "http://localhost:5000/login", "Unauthorized user should be redirected to login page"

@allure.feature("E2E Authentication")
def test_logout_clear_session(page, registered_user):

    login_page = LoginPage(page)
    login_page.login(registered_user.username, registered_user.password)
    dashboard = DashboardPage(page)
    dashboard.logout()
    assert page.locator("#login-button").is_visible(), "Login page should appear"

    dashboard.navigate()
    assert page.url == "http://localhost:5000/login", "Session should be cleard, user should be redirected to login page"
    