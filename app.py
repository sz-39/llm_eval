"""
LLM 评测工具 - Web 界面
"""
import os
import sys
import json
from flask import Flask, render_template, jsonify, request

# 确保能找到 llm_eval 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluator import run_evaluation, aggregate_scores
from report import generate_report
from config import MODELS_TO_EVAL

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def api_run():
    """运行评测"""
    # 检查 API Key
    for m in MODELS_TO_EVAL:
        if not m["api_key"]:
            return jsonify({"error": f"请先在 config.py 中填写 {m['name']} 的 API Key"}), 400

    try:
        results = run_evaluation(MODELS_TO_EVAL)
        summary = aggregate_scores(results)
        report_path = generate_report(results, summary)

        # 构建返回数据
        models_data = {}
        for model, dims in summary.items():
            models_data[model] = {
                "dims": dims,
                # 找出该模型的详细结果
                "details": [r for r in results if r["model"] == model]
            }

        return jsonify({
            "success": True,
            "models": list(summary.keys()),
            "data": summary,
            "results": results,
            "report_path": report_path,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/check", methods=["GET"])
def api_check():
    """检查配置是否就绪"""
    config_ok = any(m["api_key"] for m in MODELS_TO_EVAL)
    models = [m["name"] for m in MODELS_TO_EVAL if m["api_key"]]
    return jsonify({"config_ok": config_ok, "models": models})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
