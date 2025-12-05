import json

# 用来存放所有不重复的属性名
all_keys = set()

file_name = 'tmp/output_malmm/nextgqa_test/output_with_malmm_answers_0.json'

try:
    with open(file_name, 'r', encoding='utf-8') as f:
        # 加载JSON文件
        data = json.load(f)
        
        # 确保数据是一个列表 (list)
        if isinstance(data, list):
            # 遍历列表中的每一个单元（对象）
            for item in data:
                # 确保这个单元是一个字典 (dict)
                if isinstance(item, dict):
                    # 将这个单元的所有属性名（键）添加到set中
                    all_keys.update(item.keys())
        
    # 打印结果
    if all_keys:
        print(f"在文件 '{file_name}' 中找到的所有不重复的属性（共 {len(all_keys)} 个）:")
        # 排序后打印，更清晰
        for key in list(all_keys):
            print(f"- {key}")
    else:
        print(f"在 {file_name} 中没有找到列表数据或数据格式不正确。")

except FileNotFoundError:
    print(f"错误: 文件 {file_name} 未找到。")
except json.JSONDecodeError:
    print(f"错误: 文件 {file_name} 不是一个有效的JSON。")
except Exception as e:
    print(f"发生了一个错误: {e}")