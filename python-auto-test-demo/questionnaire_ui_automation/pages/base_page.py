from playwright.sync_api import Page

class BasePage:
    """
    封装基础操作
    """

    def __init__(self,page: Page):
        self.page = page

    """
    跳转url
    """
    def navigate_to(self,url: str):
        self.page.goto(url)

    """
    点击元素
    """
    def click(self,selector: str):
        self.page.click(selector)

    """
    输入框填写文本
    """
    def fill(self,selector: str,value: str):
        self.page.fill(selector,value)

    """
    获取元素文本内容
    """
    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector) or ""