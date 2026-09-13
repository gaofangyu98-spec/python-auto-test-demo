import requests
from config.config import BASE_URL, USER_PASSWORD, USER_USER


class TestUserAuthModule:
    """用户端 - 账号与认证模块接口测试"""

    def setup_method(self):
        """
        前置动作：每个测试用例执行前，创建一个全新的 Session
        （测试登录接口时，不能使用已登录的 session，必须保持干净状态）
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })
        self.user_login_url = f"{BASE_URL}/?s=user/login&system_type=default"

    def teardown_method(self):
        """
        后置动作：每个测试用例执行完后运行。
        回收资源，自动关闭 Session 链接。
        """
        self.session.close()


    ################1.正向测试用例##################
    def test_01_user_login_success(self):
        """
        标准正确登录
        """
        print("\n[用例 01] 开始执行：用户正常登录测试...")
        payload = {
            "accounts": (None, USER_USER),
            "pwd": (None, USER_PASSWORD),
            "type": (None, "username")
        }
        response = self.session.post(self.user_login_url,files = payload)
        res = response.json()
        assert res.get("code") == 0, f"用户正常登录测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 01] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_02_user_account_format_error(self):
        """
        账号格式错误
        """
        print("\n[用例 02] 开始执行：用户账号格式错误登录测试...")
        payload = {
            "accounts": (None, " "+USER_USER+" "),
            "pwd": (None, USER_PASSWORD),
            "type": (None, "username")
        }
        response = self.session.post(self.user_login_url, files=payload)
        res = response.json()
        assert res.get("code") == -3, f"用户账号格式错误登录测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 02] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_03_user_wrong_password(self):
        """
        密码错误
        """
        print("\n[用例 03] 开始执行：用户密码错误登录测试...")
        payload = {
            "accounts": (None, USER_USER),
            "pwd": (None, USER_PASSWORD+"999"),
            "type": (None, "username")
        }
        response = self.session.post(self.user_login_url, files=payload)
        res = response.json()
        assert res.get("code") == -4, f"用户密码错误登录测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 03] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_04_user_account_empty(self):
        """
        账号为空
        """
        print("\n[用例 04] 开始执行：用户账号为空登录测试...")
        payload = {
            "accounts": (None, ""),
            "pwd": (None, USER_PASSWORD),
            "type": (None, "username")
        }
        response = self.session.post(self.user_login_url, files=payload)
        res = response.json()
        assert res.get("code") == -1, f"用户账号为空登录测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 04] 测试通过！服务器响应提示: {res.get("msg")}")

    def test_05_user_sql_injection(self):
        """
        SQL注入攻击
        """
        print("\n[用例 05] 开始执行：用户SQL注入登录测试...")
        payload = {
            "accounts": (None, USER_USER),
            "pwd": (None, "'OR'1'='1"),
            "type": (None, "username")
        }
        response = self.session.post(self.user_login_url, files=payload)
        res = response.json()
        assert res.get("code") == -1, f"用户SQL注入登录测试异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
        print(f"[用例 05] 测试通过！服务器响应提示: {res.get("msg")}")
