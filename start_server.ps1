$ErrorActionPreference = "Stop"
$py = "D:\代码\Python\Python 3.12.0\python.exe"
$app = "D:\代码\Codex\llm_eval\app.py"
Write-Host "正在启动 LLM 评测工具..."
Write-Host "访问地址: http://127.0.0.1:5000"
Write-Host "按 Ctrl+C 停止服务器"
Write-Host ""
& $py $app
pause
