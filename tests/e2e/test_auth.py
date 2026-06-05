from playwright.sync_api import (
    expect
)
from tests.e2e.pages.dashboard_page import DashboardPage


def test_unauthorized_dashboard(page):

    dashboard = DashboardPage(page)
    dashboard.navigate()

    assert page.url == "http://localhost:5000/login", "Unauthorized user should be redirected to login page"
