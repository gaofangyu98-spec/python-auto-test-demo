from config.config import Config
from pages.home_page import HomePage
from pages.project_page import ProjectPage


def test_create_folder_demo(logged_page):

    logged_page.goto(f"{Config.BASE_URL}/home")

    project_page = ProjectPage(logged_page)
    home_page = HomePage(logged_page)

    folder_name = "111"

    home_page.click_menu_my_project()
    project_page.create_folder(folder_name)





