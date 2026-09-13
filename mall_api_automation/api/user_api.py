import requests

from config.config import BASE_URL


class UserApi:
    """
    用户端后台接口PO封装
    """
    def __init__(self, session: requests.Session):
        self.session = session

        # 公告请求头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })
        # 用户登录
        login_url = f"{BASE_URL}/?s=user/login&system_type=default"

        # 接口地址定义 --admin_auth--
        self.user_login_url = f"{BASE_URL}/?s=user/login&system_type=default"

        # 接口地址定义 --admin_good--
        self.test_01_user_item_classification_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_02_user_product_search_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_03_user_style_selection_url = f"{BASE_URL}/?s=goods/specdetail&system_type=default"
        self.test_04_user_product_detail_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_05_user_page_search_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"

        # 接口地址定义 --admin_order--
        self.test_01_user_add_goods_to_cart_url = f"{BASE_URL}/?s=cart/save&system_type=default"
        self.test_02_user_get_goods_car_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_03_user_update_car_count_url = f"{BASE_URL}/?s=cart/stock&system_type=default"
        self.test_04_user_delete_car_goods_url = f"{BASE_URL}/?s=cart/stock&system_type=default"

        # 接口地址定义 --admin_user--
        #---
        self.test_01_user_submit_order_url = f"{BASE_URL}/?s=cart/save&system_type=default"
        self.test_01_user_submit_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_01_user_submit_order_url = f"{BASE_URL}/?s=buy/add&system_type=default"
        #---
        self.test_02_user_view_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_03_user_pay_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        self.test_04_user_view_address_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"

