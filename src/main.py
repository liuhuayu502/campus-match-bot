#!/usr/bin/env python3
"""
校招匹配助手 - 主入口
Campus Match Bot - Main Entry Point

功能:
  1. 解析用户简历，提取关键能力
  2. 爬取大厂校招官网岗位信息
  3. 计算简历与 JD 的匹配度
  4. 筛选并推荐高匹配岗位
  5. 生成详细报告

使用方式:
  python main.py --resume <简历文件> --companies <公司列表> --output <输出文件>
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from resume_parser import ResumeParser
from job_crawler import JobCrawler
from jd_matcher import JDMatcher
from report_generator import ReportGenerator


class CampusMatchBot:
    """校招匹配助手主类"""
    
    def __init__(self, config_path: str = "config/api.json"):
        """初始化"""
        self.config = self.load_config(config_path)
        self.resume_parser = ResumeParser()
        self.job_crawler = JobCrawler()
        self.jd_matcher = JDMatcher()
        self.report_generator = ReportGenerator()
        self.user_profile = {}
        self.jobs = []
        self.matched_jobs = []
    
    def load_config(self, path: str) -> dict:
        """加载配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  配置文件未找到：{path}")
            print("使用默认配置")
            return {
                "default_model": "minimax/MiniMax-M2.5",
                "filter_rules": {
                    "min_match_score": 60,
                    "exclude_keywords": ["985/211", "硕士及以上", "3 年以上经验"],
                    "min_salary": 150
                }
            }
    
    def load_resume(self, resume_path: str):
        """加载并解析简历"""
        print(f"📄 正在解析简历：{resume_path}")
        self.user_profile = self.resume_parser.parse(resume_path)
        
        if not self.user_profile:
            print("❌ 简历解析失败，请检查文件格式")
            sys.exit(1)
        
        print(f"✅ 简历解析完成")
        print(f"   姓名：{self.user_profile.get('name', '未填写')}")
        print(f"   学校：{self.user_profile.get('education', {}).get('school', '未填写')}")
        print(f"   技能：{len(self.user_profile.get('skills', []))} 项")
        print(f"   实习：{len(self.user_profile.get('internships', []))} 段")
    
    def crawl_jobs(self, companies: list, positions: list = None):
        """爬取岗位信息"""
        print(f"\n🔍 正在爬取岗位信息...")
        print(f"   目标公司：{', '.join(companies)}")
        
        for company in companies:
            print(f"\n[{company}] 爬取中...")
            company_jobs = self.job_crawler.crawl(company, positions)
            self.jobs.extend(company_jobs)
            print(f"   ✅ 找到 {len(company_jobs)} 个岗位")
        
        print(f"\n✅ 爬取完成，共 {len(self.jobs)} 个岗位")
    
    def match_jobs(self, min_score: int = 60):
        """匹配岗位并筛选"""
        print(f"\n🧮 正在计算匹配度...")
        
        for job in self.jobs:
            score, reasons = self.jd_matcher.calculate_match(
                job, 
                self.user_profile
            )
            job['match_score'] = score
            job['match_reasons'] = reasons
            
            # 筛选
            if score >= min_score:
                self.matched_jobs.append(job)
        
        # 按匹配度排序
        self.matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        # 统计
        high_match = len([j for j in self.matched_jobs if j['match_score'] >= 80])
        mid_match = len([j for j in self.matched_jobs if 60 <= j['match_score'] < 80])
        filtered = len(self.jobs) - len(self.matched_jobs)
        
        print(f"✅ 匹配完成")
        print(f"   🟢 高匹配 (80+): {high_match} 个")
        print(f"   🟡 中匹配 (60-79): {mid_match} 个")
        print(f"   🔴 已过滤：{filtered} 个")
    
    def generate_report(self, output_path: str, format: str = "markdown"):
        """生成报告"""
        print(f"\n📄 正在生成报告...")
        
        report = self.report_generator.generate(
            self.matched_jobs,
            self.user_profile,
            output_path,
            format
        )
        
        print(f"✅ 报告已保存：{output_path}")
        return report
    
    def run(self, args):
        """主运行流程"""
        print("=" * 60)
        print("🎯 校招匹配助手 v1.0.0")
        print("=" * 60)
        
        # 1. 解析简历
        self.load_resume(args.resume)
        
        # 2. 爬取岗位
        companies = args.companies.split(',') if args.companies else ['bytedance']
        positions = args.positions.split(',') if args.positions else None
        self.crawl_jobs(companies, positions)
        
        # 3. 匹配筛选
        min_score = args.min_score if args.min_score else 60
        self.match_jobs(min_score)
        
        # 4. 生成报告
        output = args.output if args.output else f"campus-match-report-{datetime.now().strftime('%Y%m%d')}.md"
        self.generate_report(output)
        
        print("\n" + "=" * 60)
        print("✅ 全部完成！")
        print("=" * 60)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='🎯 校招匹配助手 - 智能校招岗位推荐工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --resume my-resume.md --companies bytedance,tencent
  python main.py --resume resume.md --output report.md --min-score 70
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        '--resume', '-r',
        type=str,
        required=True,
        help='简历文件路径 (Markdown 格式)'
    )
    
    parser.add_argument(
        '--companies', '-c',
        type=str,
        default='bytedance',
        help='目标公司列表，逗号分隔 (默认：bytedance)'
    )
    
    parser.add_argument(
        '--positions', '-p',
        type=str,
        default=None,
        help='目标岗位类型，逗号分隔 (默认：全部)'
    )
    
    parser.add_argument(
        '--min-score', '-m',
        type=int,
        default=60,
        help='最低匹配分数 (默认：60)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='输出报告文件路径 (默认：campus-match-report-YYYYMMDD.md)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='交互式模式'
    )
    
    args = parser.parse_args()
    
    # 创建机器人实例并运行
    bot = CampusMatchBot()
    bot.run(args)


if __name__ == "__main__":
    main()
