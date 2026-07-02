# -*- coding: utf-8 -*-
"""LLM 评测工具 - 直接双击启动"""
import webbrowser
import threading
import time
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app
def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5001")
threading.Thread(target=open_browser).start()
print("=" * 50)
print("  LLM 评测工具")
print("=" * 50)
print()
print("  浏览器已自动打开")
print("  如果没打开，手动访问:")
print("  -> http://127.0.0.1:5001")
print()
print("  按 Ctrl+C 停止服务器")
print("=" * 50)
app.run(debug=False, port=5001)
