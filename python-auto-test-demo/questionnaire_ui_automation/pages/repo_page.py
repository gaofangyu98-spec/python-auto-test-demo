from pages.base_page import BasePage


class RepoPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # ---------------- 题库列表页 ----------------
        self.btn_create_repo = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div/button"

        # 1. 题库名称（输入框）
        self.input_repo_name = "//div[contains(@class,'ant-drawer-body')]//input[@id='name']"
        # 2. 标签（输入框）
        self.input_repo_tag = "//div[contains(@class,'ant-drawer-body')]//input[@id='tag']"
        # 3. 题库分类（输入框）
        self.input_repo_category = "//*[@id='category']"
        # 4. 题库类型（下拉选择框）
        self.select_repo_type = "//div[contains(@class,'ant-drawer-body')]//input[@id='mode']/ancestor::div[contains(@class,'ant-select-selector')]"

        # 下拉菜单选项
        self.option_questionnaire = "//div[contains(@class,'ant-select-item-option-content') and text()='问卷']"
        self.option_exam = "//div[contains(@class,'ant-select-item-option-content') and text()='考试']"

        # 5. 共享题库 (Switch 开关)
        self.switch_is_share = "//*[@id='shared']"

        # 6. 添加到练习题库 (Switch 开关)
        self.switch_is_practice = "//*[@id='isPractice']"

        # 7. 题库描述 (Textarea 文本域)
        self.textarea_description = "//*[@id='description']"

        # 底部确定按钮
        self.btn_confirm = "//div[contains(@class,'ant-drawer-footer')]/div/div/div[2]/button"

    def create_repository(self,name: str,biao: str,type: str,death: str):

        self.click(self.btn_create_repo)

        self.fill(self.input_repo_name,name)

        self.fill(self.input_repo_tag,biao)

        self.fill(self.input_repo_category,type)

        self.click(self.select_repo_type)

        self.click(self.option_questionnaire)

        self.click(self.switch_is_share)
        self.click(self.switch_is_practice)

        self.fill(self.textarea_description, death)

        self.click(self.btn_confirm)

