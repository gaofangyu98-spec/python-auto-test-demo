import subprocess
import os

def run_all_test_and_open_allure_report():
    #拿到 run.py 的完整绝对路径   **\mall_api_automation\run.py
    path = os.path.abspath(__file__)

    #去掉文件名，只拿到run.py 所在的文件夹路径    **\mall_api_automation
    root = os.path.dirname(path)

    #把程序的当前工作文件夹，切换到 run.py 所在的文件夹
    os.chdir(root)

    # 执行用例，生成allure原始数据
    subprocess.run(["pytest", "-q", "--alluredir=reports/allure-results"])

    # 调用本地2.45版本allure serve自动起服务+打开http报告
    allure = r"D:\Game101\allure-2.45.0\bin\allure.bat"

    subprocess.run([allure, "serve", "reports/allure-results"])

if __name__ == '__main__':
    run_all_test_and_open_allure_report()
