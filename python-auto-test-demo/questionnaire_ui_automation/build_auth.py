import os
import time

from playwright.sync_api import sync_playwright

from config.config import Config
from pages.login_page import LoginPage


def generate_auth_state():
    """
    生成普通用户的登录状态文件（Session/Cookie）
    """
    if not os.path.exists("state"):
        os.makedirs("state")

    with sync_playwright() as p:
        #启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("正在进行初始化登录...")
        login_page = LoginPage(page)

        # 1. 打开登录页
        login_page.navigate(Config.BASE_URL)

        # 2. 调用你的 LoginPage 进行登录
        login_page.login(Config.NORMAL_USER, Config.NORMAL_PASS)

        # 3. 保存登录状态至 state/auth_normal_user.json
        state_path = os.path.join("state", "auth_normal_user.json")
        context.storage_state(path=state_path)
        print(f"✅ 登录状态保存成功！文件路径：{state_path}")
        browser.close()




if __name__ == "__main__":
    generate_auth_state()
