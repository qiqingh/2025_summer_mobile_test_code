#!/usr/bin/env python3
"""
统一文件清理工具
包含以下功能：
1. 删除 .pcapng 文件
2. 删除空的 .txt 文件
3. 清理不包含特定内容的文件夹
"""

import os
import glob
import shutil
from pathlib import Path


class FileCleanupTool:
    def __init__(self):
        self.default_path = "/Volumes/Sharge/2025_mobile_testing/mobile_test/multiple_field_results"
        
    def delete_pcapng_files(self, directory_path, auto_confirm=False):
        """删除所有.pcapng文件"""
        if not os.path.exists(directory_path):
            print(f"错误：路径 '{directory_path}' 不存在")
            return
        
        pcapng_pattern = os.path.join(directory_path, "**", "*.pcapng")
        pcapng_files = glob.glob(pcapng_pattern, recursive=True)
        
        if not pcapng_files:
            print("没有找到任何.pcapng文件")
            return
        
        print(f"找到 {len(pcapng_files)} 个.pcapng文件:")
        for file_path in pcapng_files[:10]:  # 只显示前10个文件
            print(f"  - {file_path}")
        if len(pcapng_files) > 10:
            print(f"  ... 还有 {len(pcapng_files) - 10} 个文件")
        
        if not auto_confirm:
            confirm = input(f"\n确定要删除这 {len(pcapng_files)} 个文件吗？(y/N): ")
            if confirm.lower() not in ['y', 'yes', '是']:
                print("操作已取消")
                return
        
        deleted_count = 0
        failed_count = 0
        
        for file_path in pcapng_files:
            try:
                os.remove(file_path)
                if deleted_count < 5:  # 只显示前5个删除的文件
                    print(f"已删除: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"删除失败 {file_path}: {e}")
                failed_count += 1
        
        print(f"\n删除完成！成功删除 {deleted_count} 个文件，失败 {failed_count} 个文件")
    
    def delete_empty_txt_files(self, root_path):
        """删除空的txt文件"""
        root_path = Path(root_path)
        
        if not root_path.exists():
            print(f"错误：路径 '{root_path}' 不存在")
            return
        
        if not root_path.is_dir():
            print(f"错误：'{root_path}' 不是一个目录")
            return
        
        deleted_count = 0
        checked_count = 0
        
        print(f"开始扫描路径: {root_path}")
        print("-" * 50)
        
        for txt_file in root_path.rglob("*.txt"):
            checked_count += 1
            
            try:
                file_size = txt_file.stat().st_size
                
                if file_size == 0:
                    if deleted_count < 5:  # 只显示前5个删除的文件
                        print(f"删除空文件: {txt_file}")
                    txt_file.unlink()
                    deleted_count += 1
                else:
                    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if not content.strip():
                            if deleted_count < 5:
                                print(f"删除只含空白字符的文件: {txt_file}")
                            txt_file.unlink()
                            deleted_count += 1
                            
            except PermissionError:
                print(f"警告：没有权限访问文件 {txt_file}")
            except Exception as e:
                print(f"处理文件 {txt_file} 时出错: {e}")
        
        print("-" * 50)
        print(f"扫描完成！")
        print(f"检查了 {checked_count} 个txt文件")
        print(f"删除了 {deleted_count} 个空文件")
    
    def check_and_clean_folders(self, base_path, target_string="[M] TX --> RRC Setup"):
        """检查并清理不包含特定内容的文件夹"""
        base_path = Path(base_path)
        
        if not base_path.exists():
            print(f"错误：路径 {base_path} 不存在")
            return
        
        folders_to_delete = set()
        
        print(f"查找目标字符串: {target_string}")
        print("-" * 50)
        
        for top_level_folder in base_path.iterdir():
            if not top_level_folder.is_dir():
                continue
                
            events_files = list(top_level_folder.rglob("events.1.txt"))
            
            if not events_files:
                print(f"文件夹 {top_level_folder.name} 中没有找到 events.1.txt 文件")
                continue
            
            contains_target = False
            
            for events_file in events_files:
                try:
                    with open(events_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if target_string in content:
                            contains_target = True
                            print(f"✓ 找到目标字符串在: {events_file.relative_to(base_path)}")
                            break
                except Exception as e:
                    print(f"读取文件 {events_file} 时出错: {e}")
            
            if not contains_target:
                folders_to_delete.add(top_level_folder)
                print(f"✗ 文件夹 {top_level_folder.name} 中的events.1.txt不包含目标字符串")
        
        if folders_to_delete:
            print(f"\n找到 {len(folders_to_delete)} 个需要删除的文件夹:")
            for folder in folders_to_delete:
                print(f"  - {folder.name}")
            
            confirm = input(f"\n确定要删除这些文件夹吗？(y/N): ")
            if confirm.lower() in ['y', 'yes', '是']:
                for folder in folders_to_delete:
                    try:
                        shutil.rmtree(folder)
                        print(f"已删除: {folder.name}")
                    except Exception as e:
                        print(f"删除文件夹 {folder} 时出错: {e}")
            else:
                print("操作已取消")
        else:
            print("\n没有需要删除的文件夹")
        
        print("\n处理完成！")
    
    def show_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "="*60)
            print("文件清理工具 - 主菜单")
            print("="*60)
            print("1. 删除 .pcapng 文件")
            print("2. 删除空的 .txt 文件")
            print("3. 清理不包含特定内容的文件夹")
            print("4. 执行所有清理操作")
            print("5. 设置默认路径")
            print("0. 退出")
            print("-"*60)
            print(f"当前默认路径: {self.default_path}")
            print("="*60)
            
            choice = input("\n请选择操作 (0-5): ")
            
            if choice == '0':
                print("感谢使用，再见！")
                break
            elif choice == '1':
                self.handle_pcapng_cleanup()
            elif choice == '2':
                self.handle_txt_cleanup()
            elif choice == '3':
                self.handle_folder_cleanup()
            elif choice == '4':
                self.handle_all_cleanup()
            elif choice == '5':
                self.set_default_path()
            else:
                print("无效的选择，请重试")
    
    def get_path_input(self, prompt_text):
        """获取路径输入"""
        print(f"\n{prompt_text}")
        print(f"1. 使用默认路径: {self.default_path}")
        print("2. 输入自定义路径")
        
        choice = input("选择 (1/2): ")
        if choice == '1':
            return self.default_path
        elif choice == '2':
            path = input("请输入路径: ").strip()
            return path if path else self.default_path
        else:
            return self.default_path
    
    def handle_pcapng_cleanup(self):
        """处理 pcapng 文件清理"""
        path = self.get_path_input("选择要清理 .pcapng 文件的路径")
        print(f"\n开始清理路径: {path}")
        self.delete_pcapng_files(path)
        input("\n按回车键返回主菜单...")
    
    def handle_txt_cleanup(self):
        """处理空 txt 文件清理"""
        path = self.get_path_input("选择要清理空 .txt 文件的路径")
        print(f"\n开始清理路径: {path}")
        self.delete_empty_txt_files(path)
        input("\n按回车键返回主菜单...")
    
    def handle_folder_cleanup(self):
        """处理文件夹清理"""
        path = self.get_path_input("选择要检查并清理文件夹的路径")
        print(f"\n开始处理路径: {path}")
        self.check_and_clean_folders(path)
        input("\n按回车键返回主菜单...")
    
    def handle_all_cleanup(self):
        """执行所有清理操作"""
        path = self.get_path_input("选择要执行所有清理操作的路径")
        
        print("\n" + "="*60)
        print("开始执行所有清理操作")
        print("="*60)
        
        print("\n[1/3] 清理 .pcapng 文件...")
        self.delete_pcapng_files(path, auto_confirm=True)
        
        print("\n[2/3] 清理空的 .txt 文件...")
        self.delete_empty_txt_files(path)
        
        print("\n[3/3] 清理不包含特定内容的文件夹...")
        self.check_and_clean_folders(path)
        
        print("\n所有清理操作已完成！")
        input("\n按回车键返回主菜单...")
    
    def set_default_path(self):
        """设置默认路径"""
        print(f"\n当前默认路径: {self.default_path}")
        new_path = input("请输入新的默认路径 (直接回车保持不变): ").strip()
        
        if new_path:
            if os.path.exists(new_path):
                self.default_path = new_path
                print(f"默认路径已更新为: {self.default_path}")
            else:
                print(f"错误：路径 '{new_path}' 不存在，保持原路径不变")
        else:
            print("默认路径未更改")
        
        input("\n按回车键返回主菜单...")


def main():
    """主函数"""
    tool = FileCleanupTool()
    
    # 可以通过命令行参数设置默认路径
    import sys
    if len(sys.argv) > 1:
        tool.default_path = sys.argv[1]
    
    tool.show_menu()


if __name__ == "__main__":
    main()