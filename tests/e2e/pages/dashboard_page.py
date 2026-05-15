class DashboardPage:
    def __init__(self, page):
        self.page = page
    
    def submit(self):
        self.page.click("#upgrade-btn")
    def active_premium_status(self):
        return self.page.locator("#premium-status")
    
    