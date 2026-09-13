import pytest
import requests

from config.config import BASE_URL, ADMIN_USER, ADMIN_PASSWORD, USER_USER, USER_PASSWORD


# 管理员登录 Session
@pytest.fixture(scope="session")
def admin_session():
    """
    【pytest 夹具】
    全局只执行一次登录，返回一个带有登录状态（Cookie/Token）的 session 对象。
    供后面的所有测试用例直接使用，避免每个用例都重新登录
    """
    # 1. 创建一个 Session 对象（自动管理 Cookie）
    session = requests.Session()
    # 2. 设置通用的 Headers（根据你 F12 抓包看到的补充）
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    })
    # 3. 拼接登录接口地址（依据 F12 抓到的 Request URL）
    login_url = f"{BASE_URL}/adminkpeyv4.php?s=admin/login&system_type=default"
    # 4. 构建提交参数（依据 F12 抓到的 Payload 字段）
    payload = {
        "accounts" : (None,ADMIN_USER),
        "pwd" : (None,ADMIN_PASSWORD),
        "type": (None,"username")
    }
    print("\n[前置准备] 正在发起【管理员】登录......")
    # 5. 发起登录请求
    response = session.post(login_url, files = payload)
    # 6. 断言登录成功
    assert response.json().get("code") == 0, f"管理员端登录请求异常，状态码：{response.status_code}"
    print("[前置准备] 管理员登录成功")
    # 7. 返回 session 对象
    yield session
    # 8. 测试用例执行完毕，关闭 session 对象
    session.close()

# 用户登录 Session
@pytest.fixture(scope="session")
def user_session():
    """
    【普通买家端登录夹具】
    为 gfy 用户建立登录 Session 会话，供所有买家端用例共享
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest"
    })
    login_url = f"{BASE_URL}/?s=user/login&system_type=default"
    payload = {
        "accounts": USER_USER,
        "pwd": USER_PASSWORD,
        "type" : "username"
    }
    print("\n[前置准备] 正在发起【用户】登录......")
    response = session.post(login_url, data = payload)
    res = response.json()
    assert res.get("code") == 0, f"用户登录异常,异常码:{res.get("code")},异常信息:{res.get("msg")}"
    print("[前置准备] 用户登录成功")
    yield session
    session.close()
