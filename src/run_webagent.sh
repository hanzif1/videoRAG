#!/bin/bash

# 设置默认数据集参数
default_dataset="nextgqa"

# 获取命令行参数，如果没有提供则使用默认值
dataset="${1:-$default_dataset}"

# 执行 webagent，传递数据集参数
python web_agent.py "${dataset}"

echo "WebAgent execution completed for dataset: ${dataset}"
echo "Results saved to: ./outputs_web/${dataset}/web_agent_output.json"
