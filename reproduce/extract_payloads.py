#!/usr/bin/env python3
"""
从reproduce_onePlus13_single_field_payloads.txt文件中提取payload名字
并保存到reproduce_payload_name.txt文件中
"""

import re
import os

def extract_payload_names(input_file, output_file):
    """
    从输入文件中提取payload名字并保存到输出文件
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    payload_names = []
    
    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: 找不到输入文件 '{input_file}'")
        return
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 遍历每一行，查找文件夹名称行
    for line in lines:
        line = line.strip()
        if line.startswith("文件夹名称:"):
            # 提取文件夹名称
            folder_name = line.replace("文件夹名称:", "").strip()
            
            # 使用正则表达式匹配并去除时间戳
            # 时间戳格式为 _YYYYMMDD_HHMMSS
            match = re.match(r'^(.+?)_\d{8}_\d{6}$', folder_name)
            
            if match:
                payload_name = match.group(1)
                payload_names.append(payload_name)
                print(f"提取: {folder_name} -> {payload_name}")
            else:
                print(f"警告: 无法解析文件夹名称 '{folder_name}'")
    
    # 去重并排序
    unique_payload_names = sorted(list(set(payload_names)))
    
    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in unique_payload_names:
                f.write(name + '\n')
        
        print(f"\n成功提取 {len(unique_payload_names)} 个唯一的payload名字")
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"写入文件时出错: {e}")

def main():
    """主函数"""
    # 设置输入输出文件路径
    input_file = "reproduce_onePlus13_single_field_payloads.txt"
    output_file = "./reproduce_onePlus13_payload_name.txt"
    
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print("-" * 50)
    
    # 执行提取
    extract_payload_names(input_file, output_file)

if __name__ == "__main__":
    main()