import requests

from config.config import BASE_URL


class AdminApi:
    """
    管理端后台接口PO封装
    """
    def __init__(self,session: requests.Session):
        self.session = session

        #公告请求头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })

        #管理员登录
        self.login_url = f"{BASE_URL}/adminkpeyv4.php?s=admin/login&system_type=default"


        #接口地址定义 --admin_auth--
        self.admin_login_url = f"{BASE_URL}/adminkpeyv4.php?s=admin/login&system_type=default"

        #接口地址定义 --admin_good--
        self.test_01_admin_goods_list_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_02_admin_goods_classification_url = f"{BASE_URL}/adminkpeyv4.php?s=goodscategory/getnodeson&system_type=default"
        self.test_03_admin_goods_favorite_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_04_admin_goods_car_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"

        #接口地址定义 --admin_order--
        self.test_01_admin_order_list_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_02_admin_order_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_03_admin_pay_order_url = f"{BASE_URL}/adminkpeyv4.php?s=order/pay&system_type=default"
        self.test_04_admin_pay_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=order/delivery&system_type=default"

        #接口地址定义 --admin_user--
        self.test_01_admin_view_user_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_02_admin_user_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_03_admin_user_address_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        self.test_04_admin_detail_address_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"

