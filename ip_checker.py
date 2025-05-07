# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import subprocess
import platform
import re
import time
from datetime import datetime

class IPChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("IP地址批量检测工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("微软雅黑", 10))
        self.style.configure("TLabel", font=("微软雅黑", 10))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # IP输入区域
        ttk.Label(main_frame, text="请输入IP地址(每行一个):").pack(anchor=tk.W, pady=(0, 5))
        
        # 创建输入文本框
        self.ip_input = scrolledtext.ScrolledText(main_frame, width=50, height=8)
        self.ip_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.ip_input.insert(tk.END, "10.147.17.4\n10.147.17.6\n10.147.17.8\n10.147.17.11\n10.147.17.12\n10.147.17.47\n10.147.17.94\n10.147.17.102")
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.check_button = ttk.Button(button_frame, text="开始检测", command=self.start_check)
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="清空结果", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪")
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # 结果区域
        ttk.Label(main_frame, text="检测结果:").pack(anchor=tk.W, pady=(5, 0))
        
        # 创建结果文本框
        self.result_text = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.result_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 添加标签显示当前时间
        self.time_label = ttk.Label(main_frame, text=self.get_current_time())
        self.time_label.pack(anchor=tk.E, pady=5)
        self.update_time()
        
        # 存储检测结果
        self.results = []
        
        # 检测是否正在运行
        self.is_running = False
    
    def update_time(self):
        """更新时间标签"""
        self.time_label.config(text=self.get_current_time())
        self.root.after(1000, self.update_time)  # 每秒更新一次
    
    def get_current_time(self):
        """获取当前时间的格式化字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def clear_results(self):
        """清空结果区域"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def start_check(self):
        """开始检测IP"""
        if self.is_running:
            messagebox.showinfo("提示", "检测正在进行中，请等待完成")
            return
        
        # 获取输入的IP地址
        ip_text = self.ip_input.get(1.0, tk.END).strip()
        if not ip_text:
            messagebox.showinfo("提示", "请输入至少一个IP地址")
            return
        
        # 解析IP地址
        ip_list = []
        for line in ip_text.split('\n'):
            line = line.strip()
            if line and self.is_valid_ip(line):
                ip_list.append(line)
        
        if not ip_list:
            messagebox.showinfo("提示", "没有找到有效的IP地址")
            return
        
        # 排序IP地址
        ip_list.sort(key=self.ip_to_int)
        
        # 清空结果
        self.clear_results()
        self.results = []
        
        # 更新UI状态
        self.is_running = True
        self.check_button.config(state=tk.DISABLED)
        self.status_label.config(text=f"正在检测 {len(ip_list)} 个IP地址...")
        self.progress_var.set(0)
        
        # 启动检测线程
        threading.Thread(target=self.check_ips, args=(ip_list,), daemon=True).start()
    
    def is_valid_ip(self, ip):
        """验证IP地址格式是否正确"""
        pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
        match = re.match(pattern, ip)
        if not match:
            return False
        for i in range(1, 5):
            if int(match.group(i)) > 255:
                return False
        return True
    
    def ip_to_int(self, ip):
        """将IP地址转换为整数用于排序"""
        try:
            return [int(x) for x in ip.split('.')]
        except:
            return [0, 0, 0, 0]
    
    def check_ips(self, ip_list):
        """检测多个IP地址"""
        total = len(ip_list)
        completed = 0
        
        # 创建线程池
        threads = []
        max_threads = min(32, total)  # 最多32个线程并行
        
        # 添加标题到结果区域
        self.update_result("IP地址         状态      延迟(ms)\n")
        self.update_result("-" * 40 + "\n")
        
        # 创建并启动线程
        for ip in ip_list:
            thread = threading.Thread(target=self.check_single_ip, args=(ip, total, completed))
            threads.append(thread)
            thread.start()
            
            # 控制并发线程数
            while sum(1 for t in threads if t.is_alive()) >= max_threads:
                time.sleep(0.1)
            
            completed += 1
            self.progress_var.set((completed / total) * 100)
            self.status_label.config(text=f"正在检测: {completed}/{total}")
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 更新UI状态
        self.progress_var.set(100)
        self.status_label.config(text=f"检测完成: {total}个IP地址")
        self.check_button.config(state=tk.NORMAL)
        self.is_running = False
        
        # 按IP排序并更新结果
        self.results.sort(key=lambda x: self.ip_to_int(x['ip']))
        
        # 添加统计信息
        online_count = sum(1 for r in self.results if r['status'] == '在线')
        offline_count = sum(1 for r in self.results if r['status'] == '离线')
        
        self.update_result("\n" + "-" * 40 + "\n")
        self.update_result(f"统计: 总计 {total} 个IP, 在线 {online_count} 个, 离线 {offline_count} 个\n")
        self.update_result(f"检测时间: {self.get_current_time()}\n")
    
    def check_single_ip(self, ip, total, completed):
        """检测单个IP地址"""
        try:
            # 根据操作系统选择不同的ping命令参数
            if platform.system().lower() == "windows":
                # Windows系统
                cmd = ["ping", "-n", "2", "-w", "1000", ip]
            else:
                # Linux/Mac系统
                cmd = ["ping", "-c", "2", "-W", "1", ip]
            
            # 执行ping命令
            start_time = time.time()
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, _ = process.communicate()
            end_time = time.time()
            
            # 解析结果
            if process.returncode == 0 and ("TTL=" in output or "ttl=" in output):
                status = "在线"
                # 提取延迟时间
                if platform.system().lower() == "windows":
                    match = re.search(r"平均 = (\d+)ms", output)
                else:
                    match = re.search(r"min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+", output)
                
                if match:
                    latency = float(match.group(1))
                else:
                    latency = round((end_time - start_time) * 1000 / 2, 1)  # 估算延迟
            else:
                status = "离线"
                latency = None
            
            # 存储结果
            result = {
                'ip': ip,
                'status': status,
                'latency': latency
            }
            self.results.append(result)
            
            # 更新UI
            status_icon = "✅" if status == "在线" else "❌"
            latency_text = f"{latency:.1f}" if latency is not None else "N/A"
            result_line = f"{ip:<15} {status_icon} {status:<6} {latency_text:<10}\n"
            
            # 使用不同颜色显示结果
            self.update_result(result_line, status == "在线")
            
        except Exception as e:
            print(f"检测IP {ip} 时出错: {str(e)}")
    
    def update_result(self, text, is_online=None):
        """更新结果文本框"""
        self.result_text.config(state=tk.NORMAL)
        
        # 获取当前文本框的末尾位置
        end_pos = self.result_text.index(tk.END)
        
        # 插入文本
        self.result_text.insert(tk.END, text)
        
        # 如果指定了状态，设置文本颜色
        if is_online is not None:
            # 计算新文本的起始位置
            start_pos = f"{float(end_pos) - 0.1}"
            end_pos = self.result_text.index(tk.END)
            
            # 设置标签
            tag_name = "online" if is_online else "offline"
            self.result_text.tag_add(tag_name, start_pos, end_pos)
            
            # 配置标签颜色
            if is_online:
                self.result_text.tag_config("online", foreground="green")
            else:
                self.result_text.tag_config("offline", foreground="red")
        
        self.result_text.config(state=tk.DISABLED)
        self.result_text.see(tk.END)  # 滚动到最新内容

if __name__ == "__main__":
    root = tk.Tk()
    app = IPChecker(root)
    root.mainloop()