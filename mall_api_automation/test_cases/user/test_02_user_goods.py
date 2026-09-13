from config.config import BASE_URL


class TestUserGoodsModule:
    """
    用户商品模块
    """
    def test_01_user_item_classification(self,user_session):
        """
        查询商品分类
        """
        print("\n[用例 01] 开始执行：查询商品分类测试...")
        test_01_user_item_classification_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.get(test_01_user_item_classification_url)
        res = response.json()
        assert res.get("code") == 0, f"查询商品分类测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_user_product_search(self,user_session):
        """
        搜索商品
        """
        print("\n[用例 02] 开始执行：搜索商品测试...")
        test_02_user_product_search_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.get(test_02_user_product_search_url)
        res = response.json()
        assert res.get("code") == 0, f"搜索商品测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")


    def test_03_user_style_selection(self,user_session):
        """
        商品的样式选择
        """
        print("\n[用例 03] 开始执行：商品样式选择测试...")
        test_03_user_style_selection_url = f"{BASE_URL}/?s=goods/specdetail&system_type=default"
        payload = {
            'id': '8',
            'stock': '1',
            'spec[0][type]': '颜色',
            'spec[0][value]': '蓝色',
        }
        response = user_session.post(test_03_user_style_selection_url,data = payload)
        res = response.json()
        assert res.get("code") == 0,  f"商品样式选择测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_04_user_product_detail(self,user_session):
        """
        商品的详细信息
        """
        print("\n[用例 04] 开始执行：商品详细信息测试...")
        test_04_user_product_detail_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.get(test_04_user_product_detail_url)
        res = response.json()
        assert res.get("code") == 0, f"商品详细信息测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_05_user_page_search(self,user_session):
        """
        商品页面查询
        """
        print("\n[用例 05] 开始执行：商品页面查询测试...")
        test_05_user_page_search_url = f"{BASE_URL}/?s=ueditor/index/path_type/user-861.html&action=config"
        response = user_session.get(test_05_user_page_search_url)
        res = response.json()
        assert res.get("code") == 0, f"商品页面查询测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 05] 测试通过！服务器响应提示: {res.get("msg")}")
