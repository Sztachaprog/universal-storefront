class DashboardPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("http://localhost:5000/dashboard")
    
    def submit(self):
        self.page.click("#upgrade-btn")
    def logout(self):
        self.page.click("#logout-btn")
    def active_premium_status(self):
        return self.page.locator("#premium-status")
    
    