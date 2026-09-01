import time

from pages.base_page import BasePage


class ProjectPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # ---------------- 5个核心组件定位 ----------------
        # 1. 视图切换 - 左（网格/卡片视图）
        self.btn_view_grid = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[1]/div[2]/div/div/div/div/div/div/div/div/label[1]/span[1]"

        # 2. 视图切换 - 右（列表视图）
        self.btn_view_list = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[1]/div[2]/div/div/div/div/div/div/div/div/label[2]/span[1]"

        # 3. 搜索输入框
        self.search_input = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[1]/div[2]/div/div/div/div/div/div/div/span/span"

        # 4. 搜索按钮（放大镜图标）
        self.btn_search = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[1]/div[2]/div/div/div/div/div/div/div/span/span/span"

        # 5. 新建按钮
        self.btn_create = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[1]/div[1]/span/div/div/button"

        # 6. 文件夹
        self.opt_create_folder = "//li[contains(@data-menu-id, 'newFolder')]"

        # 7. 输入框
        self.input_folder_name = "//*[@id='name']"

        # 8. 确定
        self.btn_confirm = "//div[contains(@class,'ant-modal-footer')]/button[2]"

        # 9. 取消
        self.btn_cancel = "//div[contains(@class,'ant-modal-footer')]/button[1]"

    def create_folder(self, folder_name: str):
        """
        点击新建 -> 选择新建文件夹 -> 输入名称 -> 点击确定
        """
        self.click(self.btn_create)

        self.click(self.opt_create_folder)

        self.fill(self.input_folder_name,folder_name)

        self.click(self.btn_confirm)

        time.sleep(5)



