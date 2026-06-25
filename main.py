"""
LLM 模型评测工具 — 入口
用法: 先配置 config.py，然后运行 python main.py
"""
from config import MODELS_TO_EVAL
from evaluator import run_evaluation, aggregate_scores
from report import generate_report


def main():
    print("=" * 60)
    print("  LLM 模型评测工具")
    print("=" * 60)

    # 检查 API Key
    for m in MODELS_TO_EVAL:
        if not m["api_key"]:
            print(f"[警告] {m['name']} 的 API Key 未配置，请在 config.py 中填写")

    if not any(m["api_key"] for m in MODELS_TO_EVAL):
        print("[错误] 没有配置任何有效的 API Key，退出。")
        return

    # 运行评测
    results = run_evaluation(MODELS_TO_EVAL)

    # 聚合分数
    summary = aggregate_scores(results)

    # 生成报告
    report_path = generate_report(results, summary)

    print(f"\n✅ 评测完成！报告已生成: {report_path}")


if __name__ == "__main__":
    main()
