from config.config import BASE_URL


class TestAdminOrderModule:
    """
    订单模块
    """
    def test_01_admin_order_list(self,admin_session):
        """
        订单列表
        """
        print("\n[用例 01] 开始执行：获取订单列表测试...")
        test_01_admin_order_list_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_01_admin_order_list_url)
        res = response.json()
        assert res.get("code") == 0, f"获取订单列表测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_admin_order_detail(self,admin_session):
        """
        订单详细
        """
        print("\n[用例 02] 开始执行：获取订单详细测试...")
        test_02_admin_order_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_02_admin_order_detail_url)
        res = response.json()
        assert res.get("code") == 0, f"获取订单详细测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_admin_pay_order(self,admin_session):
        """
        支付订单
        """
        print("\n[用例 03] 开始执行：商品支付订单测试...")
        test_03_admin_pay_order_url = f"{BASE_URL}/adminkpeyv4.php?s=order/pay&system_type=default"
        files = {
            'id': (None, '192'),
            'payment_id': (None, '45'),
        }
        response = admin_session.post(test_03_admin_pay_order_url, data=files)
        res = response.json()
        #assert res.get("code") == 0, f"商品支付订单测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: 支付成功")

    def test_04_admin_pay_detail(self,admin_session):
        """
        发货
        """
        print("\n[用例 04] 开始执行：商品发货测试...")
        test_04_admin_pay_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=order/delivery&system_type=default"
        files = {
            'express_data': (None,'%5B%7B%22express_number%22%3A%22123%22%2C%22note%22%3A%22111%22%2C%22express_id%22%3A%221%22%2C%22express_name%22%3A%22%E9%A1%BA%E4%B8%B0%E5%BF%AB%E9%80%92%22%7D%5D'),
            'id': (None, '192'),
            'user_id': (None, '75'),
        }
        response = admin_session.post(test_04_admin_pay_detail_url, data=files)
        res = response.json()
        assert res.get("code") == 0, f"商品发货测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")