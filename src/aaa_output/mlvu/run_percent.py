import json

# 定义输入文件
input_json_file = './aaa_output/mlvu/result.json' 
output_report_file = './aaa_output/mlvu/analysis_report.txt' # 这是新增加的输出文件名

# 初始化计数器
total_questions = 0
response_correct_count = 0
malmm_correct_count = 0

print(f"--- 开始分析文件: {input_json_file} ---")

try:
    with open(input_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确保数据是一个列表
    if not isinstance(data, list):
        print(f"错误: {input_json_file} 的内容不是一个列表。")
    else:
        # --- (这部分的逻辑和之前完全一样) ---
        for item in data:
            if not isinstance(item, dict):
                continue

            ground_truth = item.get('answer')
            if not ground_truth:
                continue 
            
            ground_truth = ground_truth.strip().upper()
            total_questions += 1 

            response_ans = item.get('response')
            if response_ans:
                response_ans_clean = response_ans.strip()
                if response_ans_clean: 
                    response_pred_letter = response_ans_clean[0].upper()
                    if response_pred_letter == ground_truth:
                        response_correct_count += 1

            malmm_ans = item.get('malmm_ans')
            if malmm_ans:
                malmm_ans_clean = malmm_ans.strip()
                if malmm_ans_clean: 
                    malmm_pred_letter = malmm_ans_clean[0].upper()
                    if malmm_pred_letter == ground_truth:
                        malmm_correct_count += 1
        
        # --- 循环结束，计算并写入文件 ---
        
        if total_questions > 0:
            # 计算百分比
            response_percent = (response_correct_count / total_questions) * 100
            malmm_percent = (malmm_correct_count / total_questions) * 100
            
            print(f"分析完成。正在将结果写入到: {output_report_file}")

            # --- 核心改动：打开一个新文件来写入结果 ---
            with open(output_report_file, 'w', encoding='utf-8') as f_out:
                f_out.write("--- 分析结果 ---\n")
                f_out.write(f"总题数: {total_questions}\n")
                
                f_out.write("\n--- 'response' (首字母比较) ---\n")
                f_out.write(f"答对题数: {response_correct_count}\n")
                f_out.write(f"正确率: {response_percent:.2f}%\n")
                
                f_out.write("\n--- 'malmm_ans' (首字母比较) ---\n")
                f_out.write(f"答对题数: {malmm_correct_count}\n")
                f_out.write(f"正确率: {malmm_percent:.2f}%\n")
            
            print(f"成功！结果已保存到 {output_report_file}")

        else:
            message = "文件中没有找到有效数据（或没有找到 'answer' 字段）。"
            print(message)
            # 也把这个消息写入文件
            with open(output_report_file, 'w', encoding='utf-8') as f_out:
                f_out.write(message + "\n")

except FileNotFoundError:
    print(f"错误: 文件 {input_json_file} 未找到。")
except json.JSONDecodeError:
    print(f"错误: 文件 {input_json_file} 不是一个有效的JSON。")
except Exception as e:
    print(f"发生了一个未知错误: {e}")