from config.config import Config
from pages.home_page import HomePage
from pages.repo_page import RepoPage


def test_create_repo(logged_page):

    logged_page.goto(f"{Config.BASE_URL}/home")

    repo_page = RepoPage(logged_page)
    home_page = HomePage(logged_page)

    home_page.click_menu_repo_center()
    home_page.click_submenu_my_repo()

    name = "111"
    biao = "222"
    type = "333"
    death = "444"
    repo_page.create_repository(name,biao,type,death)
