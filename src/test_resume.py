#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import glob

def get_processed_questions(dataset):
    """获取已经处理过的问题列表"""
    output_dir = f"./outputs_web/{dataset}"
    processed_questions = set()
    
    if not os.path.exists(output_dir):
        return processed_questions
    
    batch_files = glob.glob(f"{output_dir}/web_agent_output_batch_*.json")
    
    for batch_file in batch_files:
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
            
            for item in batch_data:
                if 'question' in item and 'results' in item:
                    question = item['question']
                    results = item['results']
                    
                    # 检查是否成功获取到足够的结果（至少10个有效结果）
                    valid_results = 0
                    for result in results:
                        if 'detail' in result and result['detail'] and not result['detail'].startswith('无法获取网页内容'):
                            valid_results += 1
                    
                    # 如果获取到足够的结果，标记为已处理
                    if valid_results >= 10:
                        processed_questions.add(question)
                        print(f"✓ Processed: {question[:50]}... ({valid_results} valid results)")
                        
        except Exception as e:
            print(f"Error reading {batch_file}: {str(e)}")
            continue
    
    return processed_questions

def get_all_questions(dataset):
    """获取所有问题"""
    questions = []
    dataset_dir = f"./output_videomind/{dataset}_test"
    
    if not os.path.exists(dataset_dir):
        print(f"Dataset directory not found: {dataset_dir}")
        return questions
    
    # 获取所有JSON文件
    json_files = glob.glob(f"{dataset_dir}/*.json")
    print(f"Found {len(json_files)} JSON files in {dataset_dir}")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 如果data是列表，遍历每个元素
            if isinstance(data, list):
                for item in data:
                    if 'question' in item:
                        questions.append(item['question'])
            # 如果data是字典，直接获取question
            elif isinstance(data, dict) and 'question' in data:
                questions.append(data['question'])
                
        except Exception as e:
            print(f"Error reading {json_file}: {str(e)}")
    
    return questions

if __name__ == "__main__":
    dataset = "nextgqa"
    
    print(f"Checking progress for dataset: {dataset}")
    
    # 获取所有问题
    all_questions = get_all_questions(dataset)
    print(f"Total questions: {len(all_questions)}")
    
    # 获取已处理的问题
    processed_questions = get_processed_questions(dataset)
    print(f"Processed questions: {len(processed_questions)}")
    
    # 计算剩余问题
    remaining_questions = [q for q in all_questions if q not in processed_questions]
    print(f"Remaining questions: {len(remaining_questions)}")
    
    if remaining_questions:
        print("\nFirst 5 remaining questions:")
        for i, q in enumerate(remaining_questions[:5]):
            print(f"  {i+1}. {q[:100]}...")
    else:
        print("\nAll questions have been processed!")


