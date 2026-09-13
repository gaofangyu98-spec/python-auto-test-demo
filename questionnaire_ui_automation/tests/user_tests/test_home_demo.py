from time import time

from playwright.sync_api import Page

from config.config import Config
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_home_demo(page: Page):
    login_page = LoginPage(page)
    home_page = HomePage(page)

    # 登录系统
    login_page.navigate(Config.BASE_URL)
    login_page.login(Config.NORMAL_USER, Config.NORMAL_PASS)

    #测试左边组件

    #我的项目
    home_page.click_menu_my_project()

    #我的练习
    home_page.click_menu_my_practice()

    #题库中心
    home_page.click_menu_repo_center()

    #我的题库
    home_page.click_submenu_my_repo()

    #问题管理
    home_page.click_submenu_question_manage()

    #我的笔记
    home_page.click_submenu_my_notes()

    # 题库中心
    home_page.click_menu_repo_center()

    #模板广场
    home_page.click_menu_template_market()

    #系统管理
    home_page.click_menu_system_manage()

    #组织机构
    home_page.click_submenu_org_manage()

    #岗位设置
    home_page.click_submenu_post_setting()

    #字典管理
    home_page.click_submenu_dict_manage()

    #个人设置
    home_page.click_submenu_personal_setting()

    # 系统管理
    home_page.click_menu_system_manage()

    #首页
    home_page.click_menu_home()

    #我的问卷
    home_page.click_tab_my_survey()

    #问卷记录
    home_page.click_tab_survey_record()

    #考试记录
    home_page.click_tab_exam_record()

    #我的考试
    home_page.click_tab_my_exam()







