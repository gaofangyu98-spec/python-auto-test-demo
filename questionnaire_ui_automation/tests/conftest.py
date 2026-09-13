import os

import pytest
from playwright.async_api import BrowserContext
from playwright.sync_api import Browser, Page


@pytest.fixture(scope="session")
def logged_context(browser: Browser) -> BrowserContext:
    """
    全局 session 级别的 Context，注入登录
    """
    state_path = os.path.join("state", "auth_normal_user.json")

    if not os.path.exists(state_path):
        raise FileNotFoundError(f"未找到状态文件 '{state_path}'，请先在根目录运行 python build_auth.py")

    context = browser.new_context(storage_state=state_path)
    yield context
    context.close()

@pytest.fixture(scope="function")
def logged_page(logged_context) -> Page:
    page = logged_context.new_page()
    yield page
    page.close()