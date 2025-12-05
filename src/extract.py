import json
import os # 导入os模块来处理文件路径和创建文件夹

# 定义输入文件的基本路径和文件名列表
dataset="videomme"
input_base_dir = f'tmp/output_malmm/{dataset}_test/'
input_file_names = [
    'output_with_malmm_answers_0.json',
    'output_with_malmm_answers_1.json',
    'output_with_malmm_answers_2.json',
    'output_with_malmm_answers_3.json'
]

# 定义统一的输出文件名
output_file_name = f'./aaa_output/{dataset}/result.json'

# 用来存放 *所有* 文件提取后的数据
all_extracted_data = []

print("--- 开始批量处理 ---")

# --- 检查并创建输出目录 ---
# os.path.dirname(output_file_name) 会获取文件所在的目录路径 (例如 './aaa_output/nextgqa')
output_dir = os.path.dirname(output_file_name)

# 如果目录路径不为空 并且 该目录不存在
if output_dir and not os.path.exists(output_dir):
    try:
        # 创建所有必需的中间目录
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    except Exception as e:
        print(f"创建目录 {output_dir} 失败: {e}")
        # 如果目录创建失败，后续写入也会失败，不如直接退出
        exit() # 退出脚本

# --- 循环处理每个输入文件 ---
for file_name in input_file_names:
    # 组合出完整的文件路径
    full_input_path = os.path.join(input_base_dir, file_name)
    
    print(f"\n正在尝试读取文件: {full_input_path}")
    
    try:
        # 打开并读取当前的JSON文件
        with open(full_input_path, 'r', encoding='utf-8') as f_in:
            data = json.load(f_in)
            
            # 确保顶层数据是一个列表
            if isinstance(data, list):
                count_before = len(all_extracted_data) # 记录处理前的数据量
                
                # 遍历列表中的每一个单元（item）
                for item in data:
                    # 确保单元是一个字典
                    if isinstance(item, dict):
                        # 创建新字典，逻辑不变
                        new_item = {
                            'question': item.get('question'),
                            'options': item.get('options'),
                            'answer': item.get('ans'),
                            'response': item.get('response'),
                            'malmm_ans': item.get('malmm_ans')
                        }
                        # 将这个新字典添加到 *总的* 结果列表中
                        all_extracted_data.append(new_item)
                
                count_after = len(all_extracted_data)
                print(f"处理完成: 从 {file_name} 提取了 {count_after - count_before} 条数据。")
                
            else:
                print(f"警告: 文件 {full_input_path} 的内容不是一个列表 (list)，已跳过。")

    except FileNotFoundError:
        print(f"错误: 输入文件 {full_input_path} 未找到。请检查路径是否正确。(已跳过此文件)")
    except json.JSONDecodeError:
        print(f"错误: 输入文件 {full_input_path} 不是一个有效的JSON。(已跳过此文件)")
    except Exception as e:
        print(f"处理 {full_input_path} 时发生了一个未知错误: {e} (已跳过此文件)")

# --- 所有文件都处理完毕后，统一写入 ---
print("\n--- 所有文件处理完毕 ---")

if all_extracted_data:
    print(f"总共提取了 {len(all_extracted_data)} 条数据。")
    print(f"正在写入到合并后的文件: {output_file_name}")
    
    try:
        # 打开输出文件 (用 'w' 模式，如果文件已存在则覆盖)
        with open(output_file_name, 'w', encoding='utf-8') as f_out:
            # 将 *所有* 数据一次性写入
            json.dump(all_extracted_data, f_out, ensure_ascii=False, indent=2)
        
        print(f"成功！所有提取的数据已合并保存到 {output_file_name}")
    
    except Exception as e:
        print(f"写入到 {output_file_name} 时发生错误: {e}")
else:
    print("没有从任何文件中提取到数据。")