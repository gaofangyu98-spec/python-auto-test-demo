from config.config import BASE_URL


class TestUserCheckoutModule:

    def test_01_user_submit_order(self,user_session):
        """
        结算提交订单
        """
        #先加商品到购物车里
        test_01_user_submit_order_url = f"{BASE_URL}/?s=cart/save&system_type=default"
        payload = {
            "goods_data": "W3siZ29vZHNfaWQiOjgsInN0b2NrIjoxLCJzcGVjIjpbeyJ0eXBlIjoi6aKc6ImyIiwidmFsdWUiOiLnuqLoibIifV19XQ%3D%3D"
        }
        response = user_session.post(test_01_user_submit_order_url, data=payload)
        res = response.json()
        assert res.get("code") == 0, f"购物车添加商品测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"

        #结算
        test_01_user_submit_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        user_session.get(test_01_user_submit_order_url)

        print("\n[用例 01] 开始执行：提交商品订单测试...")
        test_01_user_submit_order_url = f"{BASE_URL}/?s=buy/add&system_type=default"
        payload = {
            'buy_type': (None, 'cart'),
            'goods_data': (None, ''),
            'ids': (None, '1155'),
            'address_id': (None, '437'),
            'payment_id': (None, '45'),
            'user_note': (None, '尽快发货'),
            'site_model': (None, '0'),
            'appoint_time': (None, ''),
            'extraction_contact_name': (None, ''),
            'extraction_contact_tel': (None, ''),
        }
        response = user_session.post(test_01_user_submit_order_url, files = payload)
        res = response.json()
        assert res.get("code") == 0, f"提交商品订单测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_user_view_order(self,user_session):
        """
        查看购物车订单
        """
        print("\n[用例 02] 开始执行：查看购物车订单测试...")
        test_02_user_view_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.post(test_02_user_view_order_url)
        res = response.json()
        assert res.get("code") == 0, f"查看购物车订单测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_user_pay_order(self,user_session):
        """
        支付订单
        """
        print("\n[用例 03] 开始执行：支付订单订单测试...")
        test_03_user_pay_order_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.post(test_03_user_pay_order_url)
        res = response.json()
        assert res.get("code") == 0, f"支付订单订单测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_04_user_view_address(self,user_session):
        """
        查看订单地址
        """
        print("\n[用例 04] 开始执行：查看订单地址测试...")
        test_04_user_view_address_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.post(test_04_user_view_address_url)
        res = response.json()
        assert res.get("code") == 0, f"查看订单地址测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")

