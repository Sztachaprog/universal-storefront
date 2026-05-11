from playwright.sync_api import (
    expect
)
from src.database.database import get_db_connection, close_db_connection
from src.application import(
    get_user_by_id,
    register_user
)
from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.dashboard_page import UpgradeUser



def test_upgrade_to_premium(page, cursor, conn):
    user = register_user("testusername", "testpassword", "testuser@mail.com", is_premium=False, cursor=cursor)
    conn.commit()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_username("testusername")
    login_page.fill_password("testpassword")
    login_page.submit()
    login_page.get_welcome_name()
    update_page = UpgradeUser(page)
    update_page.submit()
    
    expect(update_page.active_premium_status()).to_have_text("Premium Active")
    
    is_premium = get_user_by_id(user, cursor=cursor)
    assert is_premium[3] == True, "Premium should be premium"
    

    