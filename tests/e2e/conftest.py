import pytest
import allure
from src.application import register_user
from src.database.database import get_db_connection, close_db_connection
from dataclasses import dataclass

@dataclass
class TestUser:
    username: str
    password: str
    email: str
    is_premium: bool = False


# pytest_runtest_setup — before test
# pytest_runtest_call — while test is running
# pytest_runtest_makereport — after test, when creating report
@pytest.hookimpl(tryfirst=True, hookwrapper=True) # pytest.hookimpl is able to stop test if it fails 
                                                  # tryfirst = True means that this hook will be first than any other hook with the same name
                                                  # hookwrapper = True means that this hook will be able to wrap the test execution and do something before and after the test execution
def pytest_runtest_makereport(item):              # pytest_runtest_makereport function from pytest executed after each test 
    outcome = yield                               # catches the outcome of the test execution | if hook function yield have to be variable to catch the outcome of the test execution
    rep = outcome.get_result()                    # get_result() method from pytest to get the result of the test execution | set rep variable to what is the result of yield (test execution) 

    if rep.when == "call" and rep.failed:         # tells pytest to execute this code only when the test is in the "call" phase (when the test is actually running) and when the test has failed
        page = item.funcargs.get('page')          # get the page fixture from the test function arguments | item.funcargs is a dictionary that contains all the fixtures that are used in the test function | get('page') means that we want to get the page fixture from the test function arguments
        
        if page:
            screenshot = page.screenshot(full_page=True)        
            allure.attach(                                      
                screenshot,                                     
                name="Screenshot of failed test",               
                attachment_type=allure.attachment_type.PNG      
            )


@pytest.fixture(scope="function", autouse=False)
def conn():
    conn = get_db_connection()
    yield conn
    close_db_connection(conn)

@pytest.fixture(scope="function", autouse=True)
def cursor(conn):
    cursor = conn.cursor()

    yield cursor

    cursor.execute("TRUNCATE TABLE users, movies, user_access RESTART IDENTITY CASCADE;")
    conn.commit()
    close_db_connection(conn)

@pytest.fixture(scope="function", autouse=False)
def registered_user(cursor, conn):
    user = TestUser(
        username="testusername", 
        password="testpassword", 
        email="testuser@mail.com"
    )
    register_user(user.username, user.password, user.email, is_premium = False, cursor=cursor)
    conn.commit()
    return user

@pytest.fixture(scope="function", autouse=False)
def registered_user_with_premium(cursor, conn):
    user = TestUser(
        username="testusername", 
        password="testpassword", 
        email="testuser@mail.com",
        is_premium= True
    )
    register_user(user.username, user.password, user.email, user.is_premium, cursor=cursor)
    conn.commit()
    return user
