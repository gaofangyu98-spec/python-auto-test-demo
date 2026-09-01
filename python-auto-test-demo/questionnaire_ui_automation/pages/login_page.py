from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        #页面元素定位
        self.username_input = "//*[@id='username']"
        self.password_input = "//*[@id='password']"
        self.login_button = "//*[@id='root']/div/div[2]/div[2]/div/form/button"

        # 增加 Toast 提示定位器
        self.success_toast = ".ant-message-success"

    def navigate(self, base_url: str):
        """
        打开登录页
        """
        self.navigate_to(f"{base_url}")

    def login(self,username: str,password: str):
        """
        输入账号密码并点击登录
        """
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

        #等待加载
        self.page.wait_for_selector(self.success_toast)