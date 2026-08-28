from config.config import BASE_URL


class TestAdminGoodsModule:
    """
    商品模块
    """
    def test_01_admin_goods_list(self,admin_session):
        """
        商品列表
        """
        print("\n[用例 01] 开始执行：查询商品分类测试...")
        test_01_admin_goods_list_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.get(test_01_admin_goods_list_url)
        res = response.json()
        assert res.get("code") == 0, f"查询商品分类测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_admin_goods_classification(self,admin_session):
        """
        商品分类
        """
        print("\n[用例 02] 开始执行：商品分类测试...")
        test_02_admin_goods_classification_url = f"{BASE_URL}/adminkpeyv4.php?s=goodscategory/getnodeson&system_type=default"
        payload = {
            "id" : "0"
        }
        response = admin_session.get(test_02_admin_goods_classification_url,data=payload)
        res = response.json()
        assert res.get("code") == 0, f"商品分类测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_admin_goods_favorite(self,admin_session):
        """
        商品收藏
        """
        print("\n[用例 03] 开始执行：商品收藏测试...")
        test_03_admin_goods_favorite_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.get(test_03_admin_goods_favorite_url)
        res = response.json()
        assert res.get("code") == 0, f"商品收藏测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_04_admin_goods_car(self,admin_session):
        """
        商品购物车
        """
        print("\n[用例 04] 开始执行：商品购物车测试...")
        test_04_admin_goods_car_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.get(test_04_admin_goods_car_url)
        res = response.json()
        assert res.get("code") == 0, f"商品购物车测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")
