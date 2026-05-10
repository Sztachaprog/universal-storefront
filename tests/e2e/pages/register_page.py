class RegisterPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("http://localhost:5000/register")

    def fill_username(self, username):
        self.page.fill("input[name='username']", username)

    def fill_password(self, password):
        self.page.fill("input[name='password']", password)

    def fill_email(self, email):
        self.page.fill("input[name='email']", email)

    def submit(self):
        self.page.click("#register-button")
    
    def success_register(self):
        return self.page.locator("#register-success")