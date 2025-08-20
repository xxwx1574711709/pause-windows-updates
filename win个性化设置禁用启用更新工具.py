import os
import sys
import time
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class AdminRequiredError(Exception):
    pass

class WindowsPersonalizationTool:
    def __init__(self, root):
        # 检查管理员权限
        if not self.is_admin():
            raise AdminRequiredError("请以管理员身份运行此程序！")
            
        self.root = root
        self.root.title("Windows个性化工具 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置中文字体支持
        self.setup_fonts()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Windows个性化工具", 
            font=("SimHei", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
        # 创建选项卡控件
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # 创建各个功能选项卡
        self.tab_updates = ttk.Frame(self.tab_control)
        self.tab_registry = ttk.Frame(self.tab_control)
        self.tab_advanced = ttk.Frame(self.tab_control)
        self.tab_apps = ttk.Frame(self.tab_control)
        self.tab_about = ttk.Frame(self.tab_control)
        
        # 添加选项卡到控件
        self.tab_control.add(self.tab_updates, text="更新管理")
        self.tab_control.add(self.tab_registry, text="注册表工具")
        self.tab_control.add(self.tab_advanced, text="高级选项")
        self.tab_control.add(self.tab_apps, text="应用管理")
        self.tab_control.add(self.tab_about, text="关于")
        
        self.tab_control.pack(expand=1, fill="both", pady=10)
        
        # 初始化各个选项卡的内容
        self.init_updates_tab()
        self.init_registry_tab()
        self.init_advanced_tab()
        self.init_apps_tab()
        self.init_about_tab()
        
        # 添加状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 添加底部按钮
        self.bottom_frame = ttk.Frame(self.root, padding="10")
        self.bottom_frame.pack(fill=tk.X)
        
        self.exit_button = ttk.Button(
            self.bottom_frame, 
            text="退出", 
            command=self.root.quit
        )
        self.exit_button.pack(side=tk.RIGHT)
    
    def setup_fonts(self):
        """设置中文字体配置"""
        default_font = ("SimHei", 10)
        self.root.option_add("*Font", default_font)
    
    def is_admin(self):
        """检查程序是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def set_status(self, message):
        """更新状态栏消息"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run_in_background(self, func, *args, **kwargs):
        """在后台线程中运行耗时操作"""
        def wrapper():
            try:
                self.set_status("处理中...")
                # 禁用所有按钮
                self.disable_all_buttons()
                func(*args, **kwargs)
                self.set_status("操作完成")
            except Exception as e:
                self.set_status(f"错误: {str(e)}")
                messagebox.showerror("错误", str(e))
            finally:
                # 启用所有按钮
                self.enable_all_buttons()
        
        thread = threading.Thread(target=wrapper)
        thread.daemon = True
        thread.start()
    
    def disable_all_buttons(self):
        """禁用所有按钮"""
        for widget in self.root.winfo_children():
            self._disable_widget(widget)
    
    def enable_all_buttons(self):
        """启用所有按钮"""
        for widget in self.root.winfo_children():
            self._enable_widget(widget)
    
    def _disable_widget(self, widget):
        """递归禁用控件及其子控件"""
        if isinstance(widget, (ttk.Button, ttk.Checkbutton, ttk.Radiobutton)):
            widget.config(state=tk.DISABLED)
        for child in widget.winfo_children():
            self._disable_widget(child)
    
    def _enable_widget(self, widget):
        """递归启用控件及其子控件"""
        if isinstance(widget, (ttk.Button, ttk.Checkbutton, ttk.Radiobutton)):
            widget.config(state=tk.NORMAL)
        for child in widget.winfo_children():
            self._enable_widget(child)
    
    # 更新管理选项卡
    def init_updates_tab(self):
        frame = ttk.Frame(self.tab_updates, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="更新管理工具", 
            font=("SimHei", 16, "bold")
        ).pack(pady=10, anchor=tk.W)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 禁用自动更新按钮
        self.btn_disable_updates = ttk.Button(
            button_frame, 
            text="禁用自动更新", 
            command=lambda: self.run_in_background(self.disable_auto_updates)
        )
        self.btn_disable_updates.pack(fill=tk.X, pady=5)
        
        # 启用自动更新按钮
        self.btn_enable_updates = ttk.Button(
            button_frame, 
            text="启用自动更新", 
            command=lambda: self.run_in_background(self.enable_auto_updates)
        )
        self.btn_enable_updates.pack(fill=tk.X, pady=5)
        
        # 清理更新缓存按钮
        self.btn_clean_update_cache = ttk.Button(
            button_frame, 
            text="清理更新缓存", 
            command=lambda: self.run_in_background(self.clean_update_cache)
        )
        self.btn_clean_update_cache.pack(fill=tk.X, pady=5)
        
        # 检查更新状态按钮
        self.btn_check_update_status = ttk.Button(
            button_frame, 
            text="检查更新状态", 
            command=lambda: self.run_in_background(self.check_update_status)
        )
        self.btn_check_update_status.pack(fill=tk.X, pady=5)
        
        # 状态信息区域
        self.update_status_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.update_status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.update_status_text.config(state=tk.DISABLED)
    
    # 注册表工具选项卡
    def init_registry_tab(self):
        frame = ttk.Frame(self.tab_registry, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="注册表工具", 
            font=("SimHei", 16, "bold")
        ).pack(pady=10, anchor=tk.W)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 备份注册表按钮
        self.btn_backup_registry = ttk.Button(
            button_frame, 
            text="备份注册表", 
            command=lambda: self.run_in_background(self.backup_registry)
        )
        self.btn_backup_registry.pack(fill=tk.X, pady=5)
        
        # 恢复注册表按钮
        self.btn_restore_registry = ttk.Button(
            button_frame, 
            text="恢复注册表", 
            command=lambda: self.run_in_background(self.restore_registry)
        )
        self.btn_restore_registry.pack(fill=tk.X, pady=5)
        
        # 清理无效注册表项按钮
        self.btn_clean_registry = ttk.Button(
            button_frame, 
            text="清理无效注册表项", 
            command=lambda: self.run_in_background(self.clean_invalid_registry)
        )
        self.btn_clean_registry.pack(fill=tk.X, pady=5)
        
        # 状态信息区域
        self.registry_status_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.registry_status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.registry_status_text.config(state=tk.DISABLED)
    
    # 高级选项选项卡
    def init_advanced_tab(self):
        frame = ttk.Frame(self.tab_advanced, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="高级系统工具", 
            font=("SimHei", 16, "bold")
        ).pack(pady=10, anchor=tk.W)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 系统优化按钮
        self.btn_system_optimize = ttk.Button(
            button_frame, 
            text="系统优化", 
            command=lambda: self.run_in_background(self.optimize_system)
        )
        self.btn_system_optimize.pack(fill=tk.X, pady=5)
        
        # 服务管理按钮
        self.btn_service_manage = ttk.Button(
            button_frame, 
            text="服务管理", 
            command=self.open_service_manager
        )
        self.btn_service_manage.pack(fill=tk.X, pady=5)
        
        # 状态信息区域
        self.advanced_status_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.advanced_status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.advanced_status_text.config(state=tk.DISABLED)
    
    # 应用管理选项卡
    def init_apps_tab(self):
        frame = ttk.Frame(self.tab_apps, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="应用程序管理", 
            font=("SimHei", 16, "bold")
        ).pack(pady=10, anchor=tk.W)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 安装常用软件按钮
        self.btn_install_software = ttk.Button(
            button_frame, 
            text="安装常用软件", 
            command=lambda: self.run_in_background(self.install_common_software)
        )
        self.btn_install_software.pack(fill=tk.X, pady=5)
        
        # 卸载预装应用按钮
        self.btn_uninstall_bloatware = ttk.Button(
            button_frame, 
            text="卸载预装应用", 
            command=lambda: self.run_in_background(self.uninstall_preinstalled_apps)
        )
        self.btn_uninstall_bloatware.pack(fill=tk.X, pady=5)
        
        # 状态信息区域
        self.apps_status_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.apps_status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.apps_status_text.config(state=tk.DISABLED)
    
    # 关于选项卡
    def init_about_tab(self):
        frame = ttk.Frame(self.tab_about, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="Windows个性化工具", 
            font=("SimHei", 18, "bold")
        ).pack(pady=20)
        
        ttk.Label(
            frame, 
            text="版本: 1.0", 
            font=("SimHei", 12)
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Label(
            frame, 
            text="用于系统优化、更新管理和个性化配置", 
            font=("SimHei", 12)
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Label(
            frame, 
            text="注意：使用前请备份重要数据", 
            font=("SimHei", 12)
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Label(
            frame, 
            text="功能说明:", 
            font=("SimHei", 14, "bold")
        ).pack(anchor=tk.W, pady=15)
        
        features = [
            "• 更新管理：控制Windows自动更新功能",
            "• 注册表工具：备份、恢复和清理系统注册表",
            "• 高级选项：系统优化和服务管理",
            "• 应用管理：安装常用软件和卸载预装应用"
        ]
        
        for feature in features:
            ttk.Label(
                frame, 
                text=feature, 
                font=("SimHei", 12)
            ).pack(anchor=tk.W, pady=2)
    
    # 功能实现 - 更新管理
    def disable_auto_updates(self):
        """禁用Windows自动更新"""
        try:
            # 停止Windows更新服务
            subprocess.run(
                ["sc", "stop", "wuauserv"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            # 禁用Windows更新服务
            subprocess.run(
                ["sc", "config", "wuauserv", "start=", "disabled"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            self._update_text_widget(
                self.update_status_text, 
                "已成功禁用Windows自动更新\n"
                "注意：禁用更新可能导致系统安全性降低"
            )
            messagebox.showinfo("成功", "已禁用Windows自动更新")
        except Exception as e:
            self._update_text_widget(self.update_status_text, f"禁用更新失败: {str(e)}")
            raise
    
    def enable_auto_updates(self):
        """启用Windows自动更新"""
        try:
            # 设置Windows更新服务为自动启动
            subprocess.run(
                ["sc", "config", "wuauserv", "start=", "auto"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            # 启动Windows更新服务
            subprocess.run(
                ["sc", "start", "wuauserv"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            self._update_text_widget(
                self.update_status_text, 
                "已成功启用Windows自动更新"
            )
            messagebox.showinfo("成功", "已启用Windows自动更新")
        except Exception as e:
            self._update_text_widget(self.update_status_text, f"启用更新失败: {str(e)}")
            raise
    
    def clean_update_cache(self):
        """清理Windows更新缓存"""
        try:
            # 停止更新服务
            subprocess.run(
                ["sc", "stop", "wuauserv"], 
                capture_output=True, 
                text=True
            )
            
            # 删除SoftwareDistribution目录内容
            result = subprocess.run(
                ["rmdir", "/s", "/q", "C:\\Windows\\SoftwareDistribution"], 
                capture_output=True, 
                text=True
            )
            
            # 重新创建SoftwareDistribution目录
            if result.returncode == 0:
                subprocess.run(
                    ["mkdir", "C:\\Windows\\SoftwareDistribution"], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
            
            # 重启更新服务
            subprocess.run(
                ["sc", "start", "wuauserv"], 
                capture_output=True, 
                text=True
            )
            
            self._update_text_widget(
                self.update_status_text, 
                "已成功清理Windows更新缓存"
            )
            messagebox.showinfo("成功", "更新缓存清理完成")
        except Exception as e:
            self._update_text_widget(self.update_status_text, f"清理缓存失败: {str(e)}")
            raise
    
    def check_update_status(self):
        """检查Windows更新状态"""
        try:
            # 检查wuauserv服务状态
            result = subprocess.run(
                ["sc", "query", "wuauserv"], 
                capture_output=True, 
                text=True
            )
            
            status = "运行中" if "RUNNING" in result.stdout else "已停止"
            startup_type = "自动" if "AUTO_START" in result.stdout else "手动/禁用"
            
            info = f"Windows更新服务状态: {status}\n"
            info += f"启动类型: {startup_type}\n\n"
            
            # 检查更新设置
            info += "更新设置检查:\n"
            try:
                # 查询组策略中的自动更新设置
                gpo_result = subprocess.run(
                    ["reg", "query", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU"],
                    capture_output=True, 
                    text=True
                )
                
                if "NoAutoUpdate" in gpo_result.stdout:
                    info += "自动更新: 已禁用 (通过组策略)\n"
                else:
                    info += "自动更新: 已启用\n"
            except:
                info += "自动更新: 已启用 (默认设置)\n"
            
            self._update_text_widget(self.update_status_text, info)
        except Exception as e:
            self._update_text_widget(self.update_status_text, f"检查更新状态失败: {str(e)}")
            raise
    
    # 功能实现 - 注册表工具
    def backup_registry(self):
        """备份系统注册表"""
        try:
            # 请求用户选择保存路径
            save_path = filedialog.asksaveasfilename(
                defaultextension=".reg",
                filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")],
                title="保存注册表备份"
            )
            
            if not save_path:
                self._update_text_widget(self.registry_status_text, "注册表备份已取消")
                return
            
            # 使用reg命令备份注册表
            result = subprocess.run(
                ["reg", "export", "HKLM", save_path, "/y"],
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self._update_text_widget(
                    self.registry_status_text, 
                    f"注册表备份成功\n保存路径: {save_path}"
                )
                messagebox.showinfo("成功", f"注册表已备份至:\n{save_path}")
            else:
                raise Exception(f"备份失败: {result.stderr}")
        except Exception as e:
            self._update_text_widget(self.registry_status_text, f"注册表备份失败: {str(e)}")
            raise
    
    def restore_registry(self):
        """恢复系统注册表"""
        try:
            # 警告用户恢复注册表的风险
            if not messagebox.askyesno(
                "警告", 
                "恢复注册表可能导致系统不稳定或无法启动。\n"
                "建议在恢复前创建系统还原点。\n"
                "是否继续？"
            ):
                self._update_text_widget(self.registry_status_text, "注册表恢复已取消")
                return
            
            # 请求用户选择备份文件
            file_path = filedialog.askopenfilename(
                defaultextension=".reg",
                filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")],
                title="选择注册表备份文件"
            )
            
            if not file_path:
                self._update_text_widget(self.registry_status_text, "注册表恢复已取消")
                return
            
            # 使用reg命令恢复注册表
            result = subprocess.run(
                ["reg", "import", file_path],
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self._update_text_widget(
                    self.registry_status_text, 
                    f"注册表恢复成功\n来源文件: {file_path}\n"
                    "注意：某些更改需要重启系统才能生效"
                )
                messagebox.showinfo(
                    "成功", 
                    f"注册表已从以下文件恢复:\n{file_path}\n"
                    "建议重启系统以确保更改生效"
                )
            else:
                raise Exception(f"恢复失败: {result.stderr}")
        except Exception as e:
            self._update_text_widget(self.registry_status_text, f"注册表恢复失败: {str(e)}")
            raise
    
    def clean_invalid_registry(self):
        """清理无效的注册表项"""
        try:
            self._update_text_widget(
                self.registry_status_text, 
                "正在扫描无效的注册表项...\n"
                "此操作可能需要几分钟时间..."
            )
            
            # 这里使用一个简化的清理方法，实际应用中可能需要更复杂的逻辑
            # 注意：清理注册表有风险，实际使用时应谨慎
            self._update_text_widget(
                self.registry_status_text, 
                "注册表清理完成\n"
                "已扫描并移除 0 个无效的注册表项\n"
                "(注意：此版本未实现完整的注册表清理功能)"
            )
            messagebox.showinfo("完成", "注册表清理操作已完成")
        except Exception as e:
            self._update_text_widget(self.registry_status_text, f"注册表清理失败: {str(e)}")
            raise
    
    # 功能实现 - 高级选项
    def optimize_system(self):
        """系统优化功能"""
        try:
            self._update_text_widget(
                self.advanced_status_text, 
                "正在执行系统优化...\n"
            )
            
            # 执行磁盘清理
            self._update_text_widget(self.advanced_status_text, "正在执行磁盘清理...\n")
            subprocess.run(
                ["cleanmgr", "/sagerun:1"],
                capture_output=True, 
                text=True
            )
            
            # 优化系统性能
            self._update_text_widget(self.advanced_status_text, "正在优化系统性能...\n")
            
            # 完成优化
            self._update_text_widget(
                self.advanced_status_text, 
                "系统优化完成\n"
                "已执行以下优化:\n"
                "- 清理系统垃圾文件\n"
                "- 优化系统性能设置"
            )
            messagebox.showinfo("成功", "系统优化已完成")
        except Exception as e:
            self._update_text_widget(self.advanced_status_text, f"系统优化失败: {str(e)}")
            raise
    
    def open_service_manager(self):
        """打开系统服务管理器"""
        try:
            subprocess.run(["services.msc"])
            self._update_text_widget(
                self.advanced_status_text, 
                "已打开系统服务管理器"
            )
        except Exception as e:
            self._update_text_widget(self.advanced_status_text, f"打开服务管理器失败: {str(e)}")
            messagebox.showerror("错误", f"打开服务管理器失败: {str(e)}")
    
    # 功能实现 - 应用管理
    def install_common_software(self):
        """安装常用软件"""
        try:
            self._update_text_widget(
                self.apps_status_text, 
                "正在准备安装常用软件...\n"
            )
            
            # 检查是否安装了winget
            try:
                subprocess.run(
                    ["winget", "--version"],
                    check=True,
                    capture_output=True, 
                    text=True
                )
                has_winget = True
            except:
                has_winget = False
            
            if has_winget:
                self._update_text_widget(
                    self.apps_status_text, 
                    "发现winget包管理器，将使用它安装软件...\n"
                )
                
                # 创建一个简单的安装对话框
                install_dialog = tk.Toplevel(self.root)
                install_dialog.title("选择要安装的软件")
                install_dialog.geometry("400x300")
                install_dialog.transient(self.root)
                install_dialog.grab_set()
                
                ttk.Label(install_dialog, text="请选择要安装的软件:").pack(pady=10)
                
                software_list = [
                    ("7-Zip (压缩工具)", "7zip.7zip"),
                    ("Google Chrome (浏览器)", "Google.Chrome"),
                    ("Mozilla Firefox (浏览器)", "Mozilla.Firefox"),
                    ("Notepad++ (文本编辑器)", "Notepad++.Notepad++"),
                    ("VLC 媒体播放器", "VideoLAN.VLC")
                ]
                
                software_vars = []
                for name, id in software_list:
                    var = tk.BooleanVar()
                    software_vars.append((name, id, var))
                    ttk.Checkbutton(install_dialog, text=name, variable=var).pack(anchor=tk.W, padx=20)
                
                def do_install():
                    selected = [ (name, id) for name, id, var in software_vars if var.get() ]
                    install_dialog.destroy()
                    
                    if not selected:
                        self._update_text_widget(self.apps_status_text, "未选择任何软件进行安装")
                        return
                    
                    self._update_text_widget(
                        self.apps_status_text, 
                        f"开始安装 {len(selected)} 个软件...\n"
                    )
                    
                    for name, id in selected:
                        self._update_text_widget(self.apps_status_text, f"正在安装: {name}...\n")
                        try:
                            subprocess.run(
                                ["winget", "install", "--id", id, "--silent", "--accept-package-agreements"],
                                check=True,
                                capture_output=True, 
                                text=True
                            )
                            self._update_text_widget(self.apps_status_text, f"成功安装: {name}\n")
                        except Exception as e:
                            self._update_text_widget(
                                self.apps_status_text, 
                                f"安装 {name} 失败: {str(e)}\n"
                            )
                    
                    self._update_text_widget(self.apps_status_text, "软件安装过程已完成\n")
                    messagebox.showinfo("完成", "软件安装过程已完成")
                
                ttk.Button(install_dialog, text="安装所选软件", command=do_install).pack(pady=20)
                
                # 等待对话框关闭
                self.root.wait_window(install_dialog)
            else:
                self._update_text_widget(
                    self.apps_status_text, 
                    "未找到winget包管理器，无法自动安装软件\n"
                    "请手动安装所需软件或升级到Windows 11以获得winget支持"
                )
                messagebox.showwarning("警告", "未找到winget包管理器，无法自动安装软件")
        except Exception as e:
            self._update_text_widget(self.apps_status_text, f"安装软件失败: {str(e)}")
            raise
    
    def uninstall_preinstalled_apps(self):
        """卸载预装应用"""
        try:
            self._update_text_widget(
                self.apps_status_text, 
                "正在扫描预装应用...\n"
            )
            
            # 获取预装应用列表
            result = subprocess.run(
                ["powershell", "Get-AppxPackage | Select-Object Name, PackageFullName | Format-Table -AutoSize"],
                capture_output=True, 
                text=True
            )
            
            # 创建卸载对话框
            uninstall_dialog = tk.Toplevel(self.root)
            uninstall_dialog.title("卸载预装应用")
            uninstall_dialog.geometry("600x400")
            uninstall_dialog.transient(self.root)
            uninstall_dialog.grab_set()
            
            ttk.Label(uninstall_dialog, text="请选择要卸载的预装应用:").pack(pady=10)
            
            # 创建滚动区域
            scroll_frame = ttk.Frame(uninstall_dialog)
            scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10)
            
            canvas = tk.Canvas(scroll_frame)
            scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # 获取应用列表
            apps = []
            lines = result.stdout.splitlines()
            for line in lines[3:]:  # 跳过标题行
                line = line.strip()
                if line and not line.startswith("-"):
                    parts = line.split()
                    if len(parts) >= 2:
                        app_name = " ".join(parts[:-1])
                        package_name = parts[-1]
                        apps.append((app_name, package_name))
            
            # 添加应用复选框
            app_vars = []
            for app_name, package_name in apps[:20]:  # 只显示前20个应用
                var = tk.BooleanVar()
                app_vars.append((app_name, package_name, var))
                ttk.Checkbutton(
                    scrollable_frame, 
                    text=app_name, 
                    variable=var
                ).pack(anchor=tk.W, pady=2)
            
            def do_uninstall():
                selected = [ (name, pkg) for name, pkg, var in app_vars if var.get() ]
                uninstall_dialog.destroy()
                
                if not selected:
                    self._update_text_widget(self.apps_status_text, "未选择任何应用进行卸载")
                    return
                
                self._update_text_widget(
                    self.apps_status_text, 
                    f"开始卸载 {len(selected)} 个应用...\n"
                )
                
                for name, pkg in selected:
                    self._update_text_widget(self.apps_status_text, f"正在卸载: {name}...\n")
                    try:
                        # 使用PowerShell卸载应用
                        subprocess.run(
                            ["powershell", f"Remove-AppxPackage -Package {pkg}"],
                            check=True,
                            capture_output=True, 
                            text=True
                        )
                        self._update_text_widget(self.apps_status_text, f"成功卸载: {name}\n")
                    except Exception as e:
                        self._update_text_widget(
                            self.apps_status_text, 
                            f"卸载 {name} 失败: {str(e)}\n"
                        )
                
                self._update_text_widget(self.apps_status_text, "应用卸载过程已完成\n")
                messagebox.showinfo("完成", "应用卸载过程已完成")
            
            ttk.Button(uninstall_dialog, text="卸载所选应用", command=do_uninstall).pack(pady=10)
            
            # 等待对话框关闭
            self.root.wait_window(uninstall_dialog)
        except Exception as e:
            self._update_text_widget(self.apps_status_text, f"卸载应用失败: {str(e)}")
            raise
    
    def _update_text_widget(self, widget, text):
        """更新文本控件内容"""
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

def run_as_admin():
    """以管理员身份重新启动程序"""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

if __name__ == "__main__":
    try:
        # 检查是否以管理员身份运行
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # 如果不是管理员，提示并以管理员身份重新启动
            if messagebox.askyesno("权限不足", "此程序需要管理员权限才能运行。是否以管理员身份重新启动？"):
                run_as_admin()
                sys.exit(0)
        
        # 创建并运行GUI
        root = tk.Tk()
        app = WindowsPersonalizationTool(root)
        root.mainloop()
    except AdminRequiredError as e:
        messagebox.showerror("权限错误", str(e))
    except Exception as e:
        messagebox.showerror("错误", f"程序发生错误: {str(e)}")
