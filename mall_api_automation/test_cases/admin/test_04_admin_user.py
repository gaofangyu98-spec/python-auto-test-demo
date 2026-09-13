from config.config import BASE_URL


class TestAdminUserModule:
    """
    管理人员模块
    """
    def test_01_admin_view_user(self,admin_session):
        """
        查询人员
        """
        print("\n[用例 01] 开始执行：查询人员测试...")
        test_01_admin_view_user_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_01_admin_view_user_url)
        res = response.json()
        assert res.get("code") == 0, f"查询人员测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_admin_user_detail(self,admin_session):
        """
        人员详细
        """
        print("\n[用例 02] 开始执行：人员详细测试...")
        test_02_admin_user_detail_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_02_admin_user_detail_url)
        res = response.json()
        assert res.get("code") == 0, f"人员详细测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_admin_user_address(self,admin_session):
        """
        用户地址
        """
        print("\n[用例 03] 开始执行：用户地址测试...")
        test_03_admin_user_address_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_03_admin_user_address_url)
        res = response.json()
        assert res.get("code") == 0, f"用户地址测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_04_admin_detail_address(self,admin_session):
        """
        详细地址
        """
        print("\n[用例 04] 开始执行：详细地址测试...")
        test_04_admin_detail_address_url = f"{BASE_URL}/adminkpeyv4.php?s=ueditor/index/path_type/common.html&action=config"
        response = admin_session.post(test_04_admin_detail_address_url)
        res = response.json()
        assert res.get("code") == 0, f"详细地址测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")