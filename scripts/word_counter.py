#!/usr/bin/env python3
"""
创客星球CGHub文章字数统计器
功能：
1. 统计文章总字数（不含广告推荐、代码块、引用格式）
2. 统计中文字数、英文字数、标点符号数
3. 排除广告推荐部分（如"推荐阅读"、"广告"等标记的内容）
4. 支持Markdown和纯文本格式
5. 批量统计多个文件
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class WordCounter:
    """字数统计器"""
    
    # 广告关键词（这些部分的内容不计入字数）
    AD_KEYWORDS = [
        "推荐阅读", "推荐阅读:", "广告", "广告:", "赞助", "赞助:", 
        "相关阅读", "相关阅读:", "推广", "推广:", "商业合作", "商业合作:",
        "点击购买", "购买链接", "购买链接:", "优惠券", "优惠券代码:",
        "限时优惠", "限时优惠:", "折扣", "折扣:", "特价", "特价:"
    ]
    
    # 引用标记（这些部分的内容不计入字数）
    QUOTE_MARKERS = [
        "> ", "```", "`", "---", "***", "====", "####"
    ]
    
    def __init__(self):
        self.total_words = 0
        self.chinese_chars = 0
        self.english_words = 0
        self.punctuation = 0
        self.excluded_sections = 0
        
    def count_file(self, file_path: str) -> Dict[str, int]:
        """
        统计单个文件的字数
        
        Args:
            file_path: 文件路径
            
        Returns:
            字数统计字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.count_content(content, file_path)
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return {}
    
    def count_content(self, content: str, source_name: str = "内容") -> Dict[str, int]:
        """
        统计文本内容的字数
        
        Args:
            content: 文本内容
            source_name: 内容来源名称（用于显示）
            
        Returns:
            字数统计字典
        """
        # 重置计数器
        self.total_words = 0
        self.chinese_chars = 0
        self.english_words = 0
        self.punctuation = 0
        self.excluded_sections = 0
        
        # 预处理内容
        processed_content = self._preprocess_content(content)
        
        # 统计字数
        self._count_characters(processed_content)
        
        # 输出统计结果
        self._print_statistics(source_name)
        
        return {
            "total_words": self.total_words,
            "chinese_chars": self.chinese_chars,
            "english_words": self.english_words,
            "punctuation": self.punctuation,
            "excluded_sections": self.excluded_sections
        }
    
    def _preprocess_content(self, content: str) -> str:
        """
        预处理内容：移除广告、代码块、引用等
        
        Args:
            content: 原始内容
            
        Returns:
            处理后的内容
        """
        lines = content.split('\n')
        processed_lines = []
        in_excluded_section = False
        exclude_reason = ""
        
        for line in lines:
            # 检查是否进入排除区域
            if self._should_exclude_line(line):
                if not in_excluded_section:
                    in_excluded_section = True
                    exclude_reason = self._get_exclude_reason(line)
                    self.excluded_sections += 1
                    print(f"  [排除] {exclude_reason}")
                continue
            
            # 检查是否退出排除区域
            if in_excluded_section and self._is_end_of_excluded_section(line):
                in_excluded_section = False
                continue
            
            # 如果不在排除区域，保留该行
            if not in_excluded_section:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _should_exclude_line(self, line: str) -> bool:
        """检查是否应该排除该行"""
        line_stripped = line.strip()
        
        # 检查广告关键词
        for keyword in self.AD_KEYWORDS:
            if keyword in line_stripped:
                return True
        
        # 检查引用标记
        for marker in self.QUOTE_MARKERS:
            if line_stripped.startswith(marker):
                return True
        
        # 检查代码块开始
        if line_stripped.startswith("```") or line_stripped.startswith("~~~"):
            return True
        
        # 检查HTML注释
        if line_stripped.startswith("<!--") and "广告" in line_stripped:
            return True
        
        return False
    
    def _get_exclude_reason(self, line: str) -> str:
        """获取排除原因"""
        line_lower = line.lower()
        
        if any(keyword in line for keyword in ["推荐阅读", "相关阅读"]):
            return "推荐/相关阅读部分"
        elif "广告" in line or "推广" in line or "赞助" in line:
            return "广告/推广内容"
        elif line.strip().startswith("```") or line.strip().startswith("~~~"):
            return "代码块"
        elif line.strip().startswith(">"):
            return "引用块"
        elif line.strip().startswith("`"):
            return "行内代码"
        else:
            return "其他排除内容"
    
    def _is_end_of_excluded_section(self, line: str) -> bool:
        """检查是否到达排除区域的结束"""
        # 对于代码块，检查结束标记
        if line.strip() == "```" or line.strip() == "~~~":
            return True
        
        # 对于引用块，检查是否不再是引用
        if line.strip() and not line.strip().startswith(">"):
            return True
        
        return False
    
    def _count_characters(self, content: str):
        """统计字符数"""
        # 移除空白字符
        content = re.sub(r'\s+', '', content)
        
        for char in content:
            # 中文字符
            if '\u4e00' <= char <= '\u9fff':
                self.chinese_chars += 1
                self.total_words += 1
            # 英文字母
            elif 'a' <= char.lower() <= 'z':
                self.english_words += 1
                self.total_words += 1
            # 数字
            elif '0' <= char <= '9':
                self.total_words += 1
            # 标点符号
            elif char in '，。！？；："\'（）《》【】、':
                self.punctuation += 1
    
    def _print_statistics(self, source_name: str):
        """打印统计结果"""
        print(f"\n{'='*50}")
        print(f"字数统计报告 - {source_name}")
        print(f"{'='*50}")
        print(f"总字数: {self.total_words}")
        print(f"中文字数: {self.chinese_chars}")
        print(f"英文单词数: {self.english_words}")
        print(f"标点符号数: {self.punctuation}")
        print(f"排除部分数: {self.excluded_sections}")
        
        # 计算阅读时间（按中文字符计算，约300字/分钟）
        if self.chinese_chars > 0:
            reading_time = self.chinese_chars / 300
            print(f"预计阅读时间: {reading_time:.1f} 分钟")
        
        print(f"{'='*50}")


def batch_count_files(directory: str, pattern: str = "*.md"):
    """
    批量统计目录中的文件
    
    Args:
        directory: 目录路径
        pattern: 文件匹配模式
    """
    counter = WordCounter()
    total_stats = {
        "total_words": 0,
        "chinese_chars": 0,
        "english_words": 0,
        "files_counted": 0
    }
    
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"目录不存在: {directory}")
        return
    
    files = list(directory_path.glob(pattern))
    if not files:
        print(f"未找到匹配 {pattern} 的文件")
        return
    
    print(f"开始批量统计 {len(files)} 个文件...")
    
    for file_path in files:
        print(f"\n处理文件: {file_path.name}")
        stats = counter.count_file(str(file_path))
        
        if stats:
            total_stats["total_words"] += stats["total_words"]
            total_stats["chinese_chars"] += stats["chinese_chars"]
            total_stats["english_words"] += stats["english_words"]
            total_stats["files_counted"] += 1
    
    # 打印汇总统计
    print(f"\n{'='*50}")
    print("批量统计汇总")
    print(f"{'='*50}")
    print(f"统计文件数: {total_stats['files_counted']}")
    print(f"总字数: {total_stats['total_words']}")
    print(f"总中文字数: {total_stats['chinese_chars']}")
    print(f"总英文单词数: {total_stats['english_words']}")
    
    if total_stats['files_counted'] > 0:
        avg_words = total_stats['total_words'] / total_stats['files_counted']
        print(f"平均每篇文章字数: {avg_words:.0f}")
    
    print(f"{'='*50}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='创客星球CGHub文章字数统计器')
    parser.add_argument('input', nargs='?', help='输入文件路径或目录')
    parser.add_argument('-d', '--directory', help='批量统计目录')
    parser.add_argument('-p', '--pattern', default='*.md', 
                       help='文件匹配模式（默认: *.md）')
    parser.add_argument('-c', '--content', help='直接统计文本内容')
    
    args = parser.parse_args()
    
    counter = WordCounter()
    
    if args.content:
        # 直接统计文本内容
        counter.count_content(args.content, "直接输入内容")
    elif args.directory:
        # 批量统计目录
        batch_count_files(args.directory, args.pattern)
    elif args.input:
        # 统计单个文件
        if os.path.isdir(args.input):
            batch_count_files(args.input, args.pattern)
        else:
            counter.count_file(args.input)
    else:
        # 交互模式
        print("创客星球CGHub字数统计器")
        print("输入文本内容（输入空行结束）：")
        
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                break
        
        content = '\n'.join(lines)
        if content.strip():
            counter.count_content(content, "交互输入内容")
        else:
            print("未输入内容")


if __name__ == "__main__":
    main()