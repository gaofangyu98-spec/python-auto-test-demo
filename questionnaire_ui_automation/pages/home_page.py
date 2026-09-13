from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self,page):
        super().__init__(page)

        # ---------------- 1. 左侧一级导航菜单 ----------------
        #首页
        self.menu_home = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[1]"
        #我的项目
        self.menu_my_project = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[2]"
        #我的练习
        self.menu_my_practice = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[3]"
        #题库中心
        self.menu_repo_center = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[4]/div/span/div/span[2]"
        #模板广场
        self.menu_template_market = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[5]"
        #系统管理
        self.menu_system_manage = "//*[@id='sk-layout']/div/div/section/aside/div/div[1]/ul/li[6]/div/span/div/span[2]"

        # ---------------- 2. 左侧二级展开菜单 ----------------
        # 题库中心子菜单
        self.submenu_my_repo = "//*[starts-with(@id,'rc-menu-')]/li[1]"
        self.submenu_question_manage = "//*[starts-with(@id,'rc-menu-')]/li[2]"
        self.submenu_my_notes = "//*[starts-with(@id,'rc-menu-')]/li[3]"

        # 系统管理子菜单
        self.submenu_org_manage = "//*[contains(@id,'system-popup')]/li[1]"
        self.submenu_post_setting = "//*[contains(@id,'system-popup')]/li[2]"
        self.submenu_dict_manage = "//*[contains(@id,'system-popup')]/li[3]"
        self.submenu_personal_setting = "//*[contains(@id,'system-popup')]/li[4]"

        # ---------------- 3. 首页 Tab 页签 ----------------
        self.tab_my_exam = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]"
        self.tab_my_survey = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]"
        self.tab_survey_record = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[3]"
        self.tab_exam_record = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[4]"

        # ---------------- 4. 右侧快捷入口 ----------------
        self.btn_create_survey = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[2]/div/div[2]/div/a[1]"
        self.btn_create_exam = "//*[@id='sk-layout']/div/div/section/div[2]/main/div/div[2]/div/div/div/div[2]/div/div[2]/div/a[2]"

    def click_menu_home(self):
        """
        点击首页
        """
        self.click(self.menu_home)

    def click_menu_my_project(self):
        """
        点击我的项目
        """
        self.click(self.menu_my_project)

    def click_menu_my_practice(self):
        """
        点击我的练习
        """
        self.click(self.menu_my_practice)

    def click_menu_repo_center(self):
        """
        点击题库中心
        """
        self.click(self.menu_repo_center)

    def click_submenu_my_repo(self):
        """
        点击我的题库
        """
        self.click(self.submenu_my_repo)

    def click_submenu_question_manage(self):
        """
        点击问题管理
        """
        self.click(self.submenu_question_manage)

    def click_submenu_my_notes(self):
        """
        点击我的笔记
        """
        self.click(self.submenu_my_notes)

    def click_menu_template_market(self):
        """
        点击模板广场
        """
        self.click(self.menu_template_market)

    def click_menu_system_manage(self):
        """
        点击系统管理
        """
        self.click(self.menu_system_manage)

    def click_submenu_org_manage(self):
        """
        点击组织机构
        """
        self.click(self.submenu_org_manage)

    def click_submenu_post_setting(self):
        """
        点击岗位设置
        """
        self.click(self.submenu_post_setting)

    def click_submenu_dict_manage(self):
        """
        点击字典管理
        """
        self.click(self.submenu_dict_manage)

    def click_submenu_personal_setting(self):
        """
        点击个人设置
        """
        self.click(self.submenu_personal_setting)

    def click_tab_my_exam(self):
        """
        我的考试
        """
        self.click(self.tab_my_exam)

    def click_tab_my_survey(self):
        """
        我的问卷
        """
        self.click(self.tab_my_survey)

    def click_tab_survey_record(self):
        """
        问卷记录
        """
        self.click(self.tab_survey_record)

    def click_tab_exam_record(self):
        """
        考试记录
        """
        self.click(self.tab_exam_record)


    def click_btn_create_survey(self):
        """
        点击创建问卷
        """
        self.click(self.btn_create_survey)

    def click_btn_create_exam(self):
        """
        点击创建考试
        """
        self.click(self.btn_create_exam)

