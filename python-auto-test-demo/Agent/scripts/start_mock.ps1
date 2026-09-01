# 启动模拟被测业务接口服务（PowerShell）
# 用法：.\scripts\start_mock.ps1
Write-Host "启动模拟被测游戏业务接口服务 (http://localhost:9000) ..."
python -m uvicorn mock_service.main:app --host 0.0.0.0 --port 9000
