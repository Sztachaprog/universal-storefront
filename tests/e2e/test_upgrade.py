from playwright.sync_api import (
    expect
)
from src.application import(
    get_user_by_name,
    register_user
)
from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.dashboard_page import DashboardPage



def test_upgrade_to_premium(page, cursor, registered_user):
    
    login_page = LoginPage(page)
    login_page.login(registered_user.username, registered_user.password)
    dashboard_page = DashboardPage(page)
    dashboard_page.submit()
    
    expect(dashboard_page.active_premium_status()).to_have_text("Premium Active")
    
    username = get_user_by_name(registered_user.username, cursor=cursor)
    assert username[3] == True, "Premium should be premium"
    
def test_already_upgraded_user(page, registered_user_with_premium):

    login_page = LoginPage(page)
    login_page.login(registered_user_with_premium.username, registered_user_with_premium.password)


    assert page.locator("#upgrade-btn").is_visible() == False, "User is already premium, shouldn't be able to submit premium"



    