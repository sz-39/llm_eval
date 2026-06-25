"""
评测报告生成
"""
import os
from datetime import datetime
from config import OUTPUT_DIR, WEIGHTS


def generate_report(results, summary):
    """生成 Markdown 格式的评测报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# LLM 模型评测报告")
    lines.append(f"")
    lines.append(f"**生成时间**: {now}")
    lines.append(f"**测试用例数**: {len(set(r['case_id'] for r in results))}")
    lines.append(f"**评测模型数**: {len(summary)}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # ============ 总分对比 ============
    lines.append(f"## 一、综合评分")
    lines.append(f"")

    # 计算加权总分
    total_scores = {}
    for model, dims in summary.items():
        weighted = 0
        dim_details = []
        for dim_name, weight in WEIGHTS.items():
            if dim_name in dims:
                score = dims[dim_name]["avg_score"]
                weighted += score * weight
                dim_details.append((dim_name, score, weight))
        total_scores[model] = {"weighted": round(weighted, 1), "details": dim_details}

    # 排序
    sorted_models = sorted(total_scores.items(), key=lambda x: x[1]["weighted"], reverse=True)

    lines.append(f"| 排名 | 模型 | 加权总分 |")
    lines.append(f"|------|------|----------|")
    for rank, (model, data) in enumerate(sorted_models, 1):
        lines.append(f"| {rank} | {model} | **{data['weighted']}** |")

    lines.append(f"")
    lines.append(f"### 各维度得分明细")
    lines.append(f"")

    # 维度得分表
    header = f"| 模型 | {' | '.join(WEIGHTS.keys())} | 加权总分 |"
    sep = f"|------|{'|'.join(['---'] * len(WEIGHTS))}|----------|"
    lines.append(header)
    lines.append(sep)

    for rank, (model, data) in enumerate(sorted_models, 1):
        row = f"| {model} "
        for dim_name in WEIGHTS.keys():
            found = [d for d in data["details"] if d[0] == dim_name]
            if found:
                row += f"| {found[0][1]}"
            else:
                row += "| -"
        row += f" | **{data['weighted']}** |"
        lines.append(row)

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # ============ 各维度详评 ============
    lines.append(f"## 二、各维度表现")
    lines.append(f"")

    for dim_name in WEIGHTS.keys():
        lines.append(f"### {dim_name}（权重: {WEIGHTS[dim_name]})")
        lines.append(f"")

        dim_results = [r for r in results if r["dimension"] == dim_name]
        for r in dim_results:
            lines.append(f"- **{r['model']}**: 得分 {r['score']}/10"
                        f" | 延迟 {r['latency']}s"
                        f" | 输入 {r['input_tokens']} tokens"
                        f" | 输出 {r['output_tokens']} tokens")

            # 显示回答的前100字
            snippet = r["response"][:100].replace("\n", " ")
            if len(r["response"]) > 100:
                snippet += "..."
            lines.append(f"  > {snippet}")
            lines.append(f"")

    lines.append(f"---")
    lines.append(f"")

    # ============ 逐题记录 ============
    lines.append(f"## 三、逐题详细记录")
    lines.append(f"")

    for r in results:
        lines.append(f"### [{r['case_id']}] {r['prompt'][:60]}")
        lines.append(f"")
        lines.append(f"- **模型**: {r['model']}")
        lines.append(f"- **维度**: {r['dimension']}")
        lines.append(f"- **得分**: {r['score']}/10")
        lines.append(f"- **延迟**: {r['latency']}s")
        if r["error"]:
            lines.append(f"- **错误**: {r['error']}")
        lines.append(f"")
        lines.append(f"**回答**:")
        lines.append(f"```")
        lines.append(f"{r['response']}")
        lines.append(f"```")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    report_content = "\n".join(lines)

    # 写入文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"llm_eval_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n评测报告已保存: {os.path.abspath(filepath)}")
    return filepath
