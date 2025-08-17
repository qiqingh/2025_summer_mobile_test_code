#!/usr/bin/env python3
"""
日志错误检查脚本
用于遍历指定路径下的mac_sch开头的文件夹，检查日志文件中的错误信息
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 硬编码的根路径 - 请根据您的实际路径修改
ROOT_PATH = "/home/qiqingh/Desktop/2025_mobile_testing/mobile_test/single_field_results/oneplus13"  # 修改为您的实际路径

# 错误关键词
ERROR_KEYWORDS = ["fatal error", "beginning of crash", "fatal signal"]

# 连接成功标识
CONNECTION_SUCCESS = "1/2 UE connected to eNB/gNB"

# 输出文件
OUTPUT_FILE = "./reproduce_onePlus13_single_field_payloads.txt"


def find_log_file(folder_path):
    """在文件夹中查找.log文件"""
    for file in os.listdir(folder_path):
        if file.endswith('.log'):
            return os.path.join(folder_path, file)
    return None


def check_log_for_errors(log_file_path):
    """检查日志文件中是否包含错误关键词"""
    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            for keyword in ERROR_KEYWORDS:
                if keyword.lower() in content:
                    return True
    except Exception as e:
        print(f"读取日志文件时出错 {log_file_path}: {e}")
    return False


def check_events_file(folder_path):
    """检查docker_logs/events.1.txt文件中是否包含连接成功信息"""
    events_file = os.path.join(folder_path, "docker_logs", "events.1.txt")
    
    if not os.path.exists(events_file):
        return False
    
    try:
        with open(events_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if CONNECTION_SUCCESS in content:
                return True
    except Exception as e:
        print(f"读取events文件时出错 {events_file}: {e}")
    
    return False


def process_folders():
    """主处理函数"""
    results = []
    processed_count = 0
    error_found_count = 0
    
    print(f"开始扫描路径: {ROOT_PATH}")
    print(f"查找以'mac_sch'开头的文件夹...")
    print("-" * 60)
    
    # 遍历所有子文件夹
    for root, dirs, files in os.walk(ROOT_PATH):
        for dir_name in dirs:
            if dir_name.startswith("mac_sch"):
                folder_path = os.path.join(root, dir_name)
                processed_count += 1
                
                # 查找log文件
                log_file = find_log_file(folder_path)
                if not log_file:
                    print(f"警告: 在 {folder_path} 中未找到.log文件")
                    continue
                
                # 检查log文件是否包含错误
                if check_log_for_errors(log_file):
                    error_found_count += 1
                    print(f"发现错误日志: {log_file}")
                    
                    # 检查events.1.txt文件
                    has_connection = check_events_file(folder_path)
                    
                    if not has_connection:
                        # 符合条件，记录结果
                        results.append({
                            'folder_name': dir_name,
                            'folder_path': folder_path,
                            'log_file': os.path.basename(log_file)
                        })
                        print(f"  → 记录: {dir_name} (无UE连接)")
                    else:
                        print(f"  → 跳过: {dir_name} (已有UE连接)")
    
    print("-" * 60)
    print(f"扫描完成!")
    print(f"总共处理文件夹: {processed_count}")
    print(f"发现错误日志: {error_found_count}")
    print(f"需要记录的文件夹: {len(results)}")
    
    # 写入结果文件
    if results:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# 扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 扫描路径: {ROOT_PATH}\n")
            f.write(f"# 找到 {len(results)} 个需要重现的payload\n")
            f.write("#" * 60 + "\n\n")
            
            for result in results:
                f.write(f"文件夹名称: {result['folder_name']}\n")
                f.write(f"完整路径: {result['folder_path']}\n")
                f.write(f"日志文件: {result['log_file']}\n")
                f.write("-" * 40 + "\n")
        
        print(f"\n结果已保存到: {OUTPUT_FILE}")
    else:
        print("\n没有找到符合条件的文件夹")


def main():
    """主函数"""
    # 检查根路径是否存在
    if not os.path.exists(ROOT_PATH):
        print(f"错误: 根路径不存在: {ROOT_PATH}")
        print("请修改脚本中的ROOT_PATH变量为您的实际路径")
        return
    
    # 执行处理
    try:
        process_folders()
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
    except Exception as e:
        print(f"\n执行过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()