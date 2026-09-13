from playwright.sync_api import Page, expect

from config.config import Config
from pages.login_page import LoginPage


def test_user_login(page: Page):
    """
    测试普通用户登录并验证首页界面
    """
    login_page = LoginPage(page)

    #打开登录页面
    login_page.navigate(Config.BASE_URL)

    #执行登录
    login_page.login(Config.NORMAL_USER, Config.NORMAL_PASS)

    #断言
    expect(page.locator(".ant-message-custom-content")).to_contain_text("登录成功！", timeout=5000)
    print("\n登录测试通过！已成功进入首页")