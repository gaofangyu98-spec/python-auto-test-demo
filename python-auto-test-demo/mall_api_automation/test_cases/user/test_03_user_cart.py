import pytest

from config.config import BASE_URL

COUNT = 1153

@pytest.fixture(scope="session")
def car_count():
    num = [1153]
    yield num


class TestUserCartModule:
    """
    购物车模块
    """
    def test_01_user_add_goods_to_cart(self,user_session):
        """
        商品添加到购物车
        """
        print("\n[用例 01] 开始执行：购物车添加商品测试...")
        test_01_user_add_goods_to_cart_url = f"{BASE_URL}/?s=cart/save&system_type=default"
        payload = {
            "goods_data" : "W3siZ29vZHNfaWQiOjgsInN0b2NrIjoxLCJzcGVjIjpbeyJ0eXBlIjoi6aKc6ImyIiwidmFsdWUiOiLnuqLoibIifV19XQ%3D%3D"
        }
        response = user_session.post(test_01_user_add_goods_to_cart_url,data=payload)
        res = response.json()
        assert res.get("code") == 0, f"购物车添加商品测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_user_get_goods_car(self,user_session):
        """
        获取购物车
        """
        print("\n[用例 02] 开始执行：获取购物车商品测试...")
        test_02_user_get_goods_car_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.post(test_02_user_get_goods_car_url)
        res = response.json()
        assert res.get("code") == 0, f"购物车添加商品测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_user_update_car_count(self,user_session):
        """
        更新购物车数量
        """
        print("\n[用例 03] 开始执行：更新购物车数量测试...")
        test_03_user_update_car_count_url = f"{BASE_URL}/?s=cart/stock&system_type=default"
        payload = {
            "id":"1162",
            "goods_id":"8",
            "stock":"3"
        }
        response = user_session.post(test_03_user_update_car_count_url,data=payload)
        res = response.json()
        assert res.get("code") == 0, f"更新购物车数量测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")


    def test_04_user_delete_car_goods(self,user_session,car_count):
        """
        删除购物车商品
        """
        print("\n[用例 04] 开始执行：删除购物车商品测试...")
        test_04_user_delete_car_goods_url = f"{BASE_URL}/?s=cart/stock&system_type=default"
        payload = {
            "id": "1162",
            "goods_id": "8",
            "stock": "2"
        }
        response = user_session.post(test_04_user_delete_car_goods_url, data=payload)
        res = response.json()
        assert res.get("code") == 0, f"删除购物车商品测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")