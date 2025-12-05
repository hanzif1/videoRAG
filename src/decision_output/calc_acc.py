import json
import re
import sys

dataset="mvbench"

def extract_answer_key(text):
    """
    从文本中提取第一个出现的选项字母 (A-E)。
    处理如 "C) Lay on floor", "E. Crawl", "Answer: B" 等格式。
    """
    if not text:
        return None
    text = str(text).strip()
    # 正则匹配字符串开头或非单词字符后的 A-E
    match = re.search(r'(?:^|[\s\.\)\:\,])([A-E])(?:$|[\s\.\)\:\,])', text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    # 备用策略：直接取第一个字符（如果格式非常规范）
    return text[0].upper() if text else None

if len(sys.argv) > 1:
    dataset = sys.argv[1]
# 如果你是读取本地文件，请取消下面两行的注释：
with open(f'decision_{dataset}_details.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 初始化计数器
stats = {
    "videomind": 0,
    "malmm": 0,
    "answer_w_vmw_10": 0
}

total = len(data)

print(f"{'ID':<5} {'GT':<5} {'VM':<5} {'MM':<5} {'VMW10':<5} | 判定情况")
print("-" * 50)

for item in data:
    ground_truth = extract_answer_key(item.get('answer'))
    
    # 提取各模型的预测结果
    pred_vm = extract_answer_key(item.get('videomind'))
    pred_mm = extract_answer_key(item.get('malmm'))
    pred_vmw10 = extract_answer_key(item.get('answer_w_vmw_10'))
    
    # 只有在成功提取到 Ground Truth 时才进行比对
    if ground_truth:
        if pred_vm == ground_truth:
            stats["videomind"] += 1
        if pred_mm == ground_truth:
            stats["malmm"] += 1
        if pred_vmw10 == ground_truth:
            stats["answer_w_vmw_10"] += 1
            
        # (可选) 打印每一行的比对详情用于调试
        # print(f"{item['id']:<5} {ground_truth:<5} {pred_vm:<5} {pred_mm:<5} {pred_vmw10:<5}")

# 计算并打印最终结果
print("\n=== 最终准确率统计 (Total: {}) ===".format(total))
for model, correct_count in stats.items():
    accuracy = (correct_count / total) * 100
    print(f"{model}: {accuracy:.2f}% ({correct_count}/{total})")