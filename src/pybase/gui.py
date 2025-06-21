#!/usr/bin/env python3
"""
GUI 模块示例
使用 PyQt5 创建图形用户界面
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QSlider,
    QProgressBar, QMessageBox, QFileDialog, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon

class PyBaseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('PyBase GUI 示例')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(tab_widget)
        
        # 添加不同的标签页
        tab_widget.addTab(self.create_basic_tab(), "基础功能")
        tab_widget.addTab(self.create_calculator_tab(), "计算器")
        tab_widget.addTab(self.create_file_tab(), "文件操作")
        tab_widget.addTab(self.create_progress_tab(), "进度演示")
        
    def create_basic_tab(self):
        """创建基础功能标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("PyBase GUI 欢迎界面")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_label = QLabel("输入你的名字:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入你的名字")
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.name_input)
        layout.addLayout(input_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        greet_btn = QPushButton("问候")
        greet_btn.clicked.connect(self.show_greeting)
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_input)
        button_layout.addWidget(greet_btn)
        button_layout.addWidget(clear_btn)
        layout.addLayout(button_layout)
        
        # 显示区域
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setMaximumHeight(200)
        layout.addWidget(self.display_text)
        
        # 选择器
        combo_layout = QHBoxLayout()
        combo_label = QLabel("选择主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["默认", "深色", "浅色", "高对比度"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.theme_combo)
        layout.addLayout(combo_layout)
        
        layout.addStretch()
        return widget
    
    def create_calculator_tab(self):
        """创建计算器标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("简单计算器")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 输入区域
        input_layout = QHBoxLayout()
        self.num1_input = QLineEdit()
        self.num1_input.setPlaceholderText("第一个数字")
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["+", "-", "*", "/"])
        self.num2_input = QLineEdit()
        self.num2_input.setPlaceholderText("第二个数字")
        input_layout.addWidget(self.num1_input)
        input_layout.addWidget(self.operator_combo)
        input_layout.addWidget(self.num2_input)
        layout.addLayout(input_layout)
        
        # 计算按钮
        calc_btn = QPushButton("计算")
        calc_btn.clicked.connect(self.calculate)
        layout.addWidget(calc_btn)
        
        # 结果显示
        self.result_label = QLabel("结果: ")
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        return widget
    
    def create_file_tab(self):
        """创建文件操作标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("文件操作")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 文件选择
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("未选择文件")
        select_file_btn = QPushButton("选择文件")
        select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(select_file_btn)
        layout.addLayout(file_layout)
        
        # 文件内容显示
        self.file_content = QTextEdit()
        self.file_content.setPlaceholderText("文件内容将显示在这里...")
        layout.addWidget(self.file_content)
        
        # 保存按钮
        save_btn = QPushButton("保存内容")
        save_btn.clicked.connect(self.save_content)
        layout.addWidget(save_btn)
        
        return widget
    
    def create_progress_tab(self):
        """创建进度演示标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("进度演示")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 进度条
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # 滑块
        slider_layout = QHBoxLayout()
        slider_label = QLabel("速度:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.speed_slider)
        layout.addLayout(slider_layout)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始")
        self.start_btn.clicked.connect(self.start_progress)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_progress)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # 设置定时器
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        
        return widget
    
    def show_greeting(self):
        """显示问候信息"""
        name = self.name_input.text().strip()
        if name:
            greeting = f"你好，{name}！欢迎使用 PyBase GUI 应用！\n"
            greeting += f"当前时间: {QApplication.instance().applicationName()}\n"
            self.display_text.append(greeting)
        else:
            QMessageBox.warning(self, "警告", "请输入你的名字！")
    
    def clear_input(self):
        """清空输入"""
        self.name_input.clear()
        self.display_text.clear()
    
    def change_theme(self, theme):
        """改变主题"""
        self.display_text.append(f"主题已切换到: {theme}")
    
    def calculate(self):
        """执行计算"""
        try:
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())
            operator = self.operator_combo.currentText()
            
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 == 0:
                    QMessageBox.error(self, "错误", "除数不能为零！")
                    return
                result = num1 / num2
            
            self.result_label.setText(f"结果: {num1} {operator} {num2} = {result}")
        except ValueError:
            QMessageBox.error(self, "错误", "请输入有效的数字！")
    
    def select_file(self):
        """选择文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            self.file_path_label.setText(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.file_content.setText(content)
            except Exception as e:
                QMessageBox.error(self, "错误", f"无法读取文件: {str(e)}")
    
    def save_content(self):
        """保存内容"""
        content = self.file_content.toPlainText()
        if not content:
            QMessageBox.warning(self, "警告", "没有内容可保存！")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(self, "成功", "文件保存成功！")
            except Exception as e:
                QMessageBox.error(self, "错误", f"保存文件失败: {str(e)}")
    
    def start_progress(self):
        """开始进度"""
        self.progress_bar.setValue(0)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("运行中...")
        self.progress_timer.start(1000 // self.speed_slider.value())
    
    def stop_progress(self):
        """停止进度"""
        self.progress_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("已停止")
    
    def update_progress(self):
        """更新进度"""
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 1)
        else:
            self.stop_progress()
            self.status_label.setText("完成！")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("PyBase GUI")
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = PyBaseGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 