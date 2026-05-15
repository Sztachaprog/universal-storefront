class LoginPage:
    def __init__(self, page):
        self.page = page
    
    def navigate(self):
        self.page.goto("http://localhost:5000/login")
    
    def fill_username(self, username):
        self.page.fill("input[name='username']", username)
    
    def fill_password(self, password):
        self.page.fill("input[name='password']", password)
    
    def submit(self):
        self.page.click("#login-button")
    
    def get_welcome_name(self):
        return self.page.locator(".welcome-name")
    
    def login_error(self):
        return self.page.locator("#login-error")
    
    def login(self, username, password):
        self.navigate()
        self.fill_username(username)
        self.fill_password(password)
        self.submit()