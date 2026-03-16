#!/usr/bin/env python3
"""
校招匹配助手 - FluxA 付费版 v3.0
Campus Match Bot - FluxA Monetized Version

功能:
  - 集成 FluxA 付费 API
  - 支持 x402 自动支付
  - 每次使用可赚钱

使用方式:
  python main_fluxa.py --resume my-resume.md --companies bytedance --category 运营 --price 0.05
  
参数:
  --price: 每次调用收费 (默认 0.05 USDC)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from resume_parser import ResumeParser
from resume_parser_llm import ResumeParserLLM
from job_crawler_fluxa import JobCrawlerFluxA
from jd_matcher import JDMatcher
from report_generator import ReportGenerator
from fluxa_api import analyze_resume_with_ai


class CampusMatchBotFluxA:
    """FluxA 付费版校招匹配助手"""
    
    def __init__(self, config_path: str = "config/api.json", price: float = 0.05):
        self.config = self.load_config(config_path)
        self.price = price
        self.revenue = 0.0
        self.api_calls = 0
        
        # 初始化组件
        self.resume_parser = ResumeParser()
        self.resume_parser_llm = ResumeParserLLM()
        self.job_crawler = JobCrawlerFluxA(use_fluxa=True)  # 启用 FluxA
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
            return {
                "default_model": "minimax/MiniMax-M2.5",
                "filter_rules": {
                    "min_match_score": 60,
                    "exclude_keywords": ["985/211", "硕士及以上", "3 年以上经验"],
                    "min_salary": 150
                }
            }
    
    def load_resume(self, resume_path: str):
        """加载并解析简历（优先使用 AI）"""
        print(f"📄 正在解析简历：{resume_path}")
        
        # 尝试使用 FluxA AI 分析（免费）
        try:
            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            
            ai_result = analyze_resume_with_ai(resume_text)
            if ai_result:
                self.user_profile = {
                    "name": ai_result.get("name", ""),
                    "skills": ai_result.get("skills", []),
                    "experience": ai_result.get("experience", []),
                    "education": ai_result.get("education", ""),
                    "languages": ai_result.get("languages", []),
                    "parsing_method": "fluxa_ai"
                }
                self.api_calls += 1
                print(f"✅ AI 解析完成 (FluxA Qwen API)")
                return
        except Exception as e:
            print(f"⚠️  AI 解析失败，使用本地: {e}")
        
        # 回退到本地解析
        self.user_profile = self.resume_parser.parse(resume_path)
        
        if not self.user_profile:
            print("❌ 简历解析失败，请检查文件格式")
            sys.exit(1)
        
        print(f"✅ 本地解析完成")
        print(f"   姓名：{self.user_profile.get('name', '未填写')}")
        print(f"   学校：{self.user_profile.get('education', {}).get('school', '未填写')}")
        print(f"   技能：{len(self.user_profile.get('skills', []))} 项")
    
    def crawl_jobs(self, companies: list, positions: list = None, category: str = None, city: str = None):
        """爬取岗位信息"""
        print(f"\n🔍 正在爬取岗位信息 (FluxA API)...")
        print(f"   目标公司：{', '.join(companies)}")
        if category:
            print(f"   职位类别：{category}")
        if city:
            print(f"   工作城市：{city}")
        
        for company in companies:
            print(f"\n[{company}] 爬取中...")
            company_jobs = self.job_crawler.crawl(company, positions, category, city)
            self.jobs.extend(company_jobs)
            print(f"   ✅ 找到 {len(company_jobs)} 个岗位")
        
        # 记录 API 调用
        stats = self.job_crawler.get_usage_stats()
        self.api_calls += stats['total_calls']
        
        print(f"\n✅ 爬取完成，共 {len(self.jobs)} 个岗位")
        print(f"   API 调用：{stats['total_calls']} 次")
    
    def match_jobs(self, min_score: int = 60):
        """匹配岗位并筛选"""
        print(f"\n🧮 正在计算匹配度...")
        
        for job in self.jobs:
            score, reasons = self.jd_matcher.calculate_match(job, self.user_profile)
            job['match_score'] = score
            job['match_reasons'] = reasons
            
            if score >= min_score:
                self.matched_jobs.append(job)
        
        self.matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        high_match = len([j for j in self.matched_jobs if j['match_score'] >= 80])
        mid_match = len([j for j in self.matched_jobs if 60 <= j['match_score'] < 80])
        
        print(f"✅ 匹配完成")
        print(f"   🟢 高匹配 (80+): {high_match} 个")
        print(f"   🟡 中匹配 (60-79): {mid_match} 个")
    
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
    
    def calculate_revenue(self) -> dict:
        """计算营收"""
        return {
            "price": self.price,
            "api_calls": self.api_calls,
            "estimated_revenue": self.price,  # 简化模型：每次调用收固定费用
            "api_cost": self.api_calls * 0.01  # 预估 API 成本
        }
    
    def run(self, args):
        """主运行流程"""
        print("=" * 60)
        print("🎯 校招匹配助手 v3.0 (FluxA 付费版)")
        print(f"   定价: ${args.price:.2f} USDC/次 (专业版)")
        print("=" * 60)
        
        # 1. 解析简历
        self.load_resume(args.resume)
        
        # 2. 爬取岗位
        companies = args.companies.split(',') if args.companies else ['bytedance']
        positions = args.positions.split(',') if args.positions else None
        self.crawl_jobs(companies, positions, args.category, args.city)
        
        # 3. 匹配筛选
        min_score = args.min_score if args.min_score else 60
        self.match_jobs(min_score)
        
        # 4. 生成报告
        output = args.output if args.output else f"campus-match-report-{datetime.now().strftime('%Y%m%d')}.md"
        self.generate_report(output)
        
        # 5. 显示营收
        revenue = self.calculate_revenue()
        print(f"\n💰 营收统计:")
        print(f"   本次收费: ${revenue['price']:.2f} USDC")
        print(f"   API 调用: {revenue['api_calls']} 次")
        
        print("\n" + "=" * 60)
        print("✅ 全部完成！")
        print("=" * 60)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='🎯 校招匹配助手 v3.0 - FluxA 付费版',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--resume', '-r', type=str, required=True,
                       help='简历文件路径')
    
    parser.add_argument('--companies', '-c', type=str, default='bytedance',
                       help='目标公司列表')
    
    parser.add_argument('--positions', '-p', type=str, default=None,
                       help='目标岗位类型关键词')
    
    parser.add_argument('--category', '-cat', type=str, default=None,
                       help='职位类别')
    
    parser.add_argument('--city', type=str, default=None,
                       help='工作城市')
    
    parser.add_argument('--min-score', '-m', type=int, default=60,
                       help='最低匹配分数')
    
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='输出报告文件路径')
    
    parser.add_argument('--price', '-p', type=float, default=1.00,
                       help='每次调用收费 (USDC, 默认 1.00)')
    
    args = parser.parse_args()
    
    bot = CampusMatchBotFluxA(price=args.price)
    bot.run(args)


if __name__ == "__main__":
    main()
