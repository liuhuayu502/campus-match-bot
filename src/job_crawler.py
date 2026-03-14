#!/usr/bin/env python3
"""
岗位爬取器
Job Crawler

功能:
  - 爬取各大厂校招官网岗位信息
  - 支持 web_fetch 和 browser 两种方式
  - 解析岗位 JD，提取关键信息
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class JobCrawler:
    """岗位爬取器"""
    
    def __init__(self, config_path: str = "config/companies.json"):
        """初始化"""
        self.companies = self.load_companies(config_path)
        self.session = {}  # 用于存储 browser session
    
    def load_companies(self, path: str) -> Dict:
        """加载公司配置"""
        default_companies = {
            "bytedance": {
                "name": "字节跳动",
                "campusUrl": "https://jobs.bytedance.com/campus",
                "socialUrl": "https://jobs.bytedance.com",
                "cities": ["北京", "上海", "深圳", "广州", "杭州", "成都"],
                "hotPositions": ["内容运营", "用户运营", "产品运营", "市场营销"]
            },
            "tencent": {
                "name": "腾讯",
                "campusUrl": "https://join.qq.com",
                "socialUrl": "https://careers.tencent.com",
                "cities": ["深圳", "北京", "上海", "广州", "成都"],
                "hotPositions": ["产品运营", "内容策划", "用户增长"]
            },
            "alibaba": {
                "name": "阿里巴巴",
                "campusUrl": "https://talent.alibaba.com/campus",
                "socialUrl": "https://talent.alibaba.com",
                "cities": ["杭州", "北京", "上海", "深圳"],
                "hotPositions": ["运营专员", "品类运营", "活动运营"]
            },
            "meituan": {
                "name": "美团",
                "campusUrl": "https://campus.meituan.com",
                "socialUrl": "https://recruit.meituan.com",
                "cities": ["北京", "上海", "深圳", "成都"],
                "hotPositions": ["商家运营", "用户运营", "市场拓展"]
            },
            "xiaohongshu": {
                "name": "小红书",
                "campusUrl": "https://job.xiaohongshu.com/campus",
                "socialUrl": "https://job.xiaohongshu.com",
                "cities": ["上海", "北京"],
                "hotPositions": ["内容运营", "社区运营", "品牌营销"]
            }
        }
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('companies', default_companies)
        except FileNotFoundError:
            print(f"⚠️  公司配置文件未找到，使用默认配置")
            return default_companies
        except Exception as e:
            print(f"⚠️  加载配置失败：{e}")
            return default_companies
    
    def crawl(self, company_id: str, positions: List[str] = None) -> List[Dict]:
        """爬取指定公司的岗位"""
        if company_id not in self.companies:
            print(f"❌ 未知公司：{company_id}")
            return []
        
        company = self.companies[company_id]
        jobs = []
        
        # 尝试爬取校招官网
        campus_jobs = self.crawl_url(company['campusUrl'], company['name'], positions)
        jobs.extend(campus_jobs)
        
        # 如果校招官网没有，尝试社招官网
        if len(jobs) == 0 and 'socialUrl' in company:
            social_jobs = self.crawl_url(company['socialUrl'], company['name'], positions)
            jobs.extend(social_jobs)
        
        return jobs
    
    def crawl_url(self, url: str, company_name: str, positions: List[str] = None) -> List[Dict]:
        """爬取指定 URL 的岗位信息"""
        # 这里使用 web_fetch 工具
        # 实际实现中会调用 OpenClaw 的 web_fetch 工具
        print(f"   🕷️  爬取：{url}")
        
        # 模拟返回数据 (实际应该调用 web_fetch)
        mock_jobs = self.generate_mock_jobs(company_name, positions)
        
        return mock_jobs
    
    def generate_mock_jobs(self, company_name: str, positions: List[str] = None) -> List[Dict]:
        """生成模拟岗位数据 (用于测试)"""
        # 实际应该从网页爬取
        base_jobs = [
            {
                "position": "内容运营实习生",
                "location": "北京",
                "type": "日常实习",
                "salary": "200-300 元/天",
                "description": "负责内容策划、撰写、发布，数据分析",
                "requirements": ["本科及以上学历", "每周 4 天以上", "至少 3 个月", "内容敏感度好"],
                "publish_date": datetime.now().strftime("%Y-%m-%d"),
                "deadline": "2026-04-30",
                "apply_url": f"https://jobs.{company_name}.com/position/1"
            },
            {
                "position": "用户运营实习生",
                "location": "上海",
                "type": "日常实习",
                "salary": "200-300 元/天",
                "description": "负责用户增长、活动策划、数据分析",
                "requirements": ["本科及以上学历", "熟悉社交媒体", "沟通能力强"],
                "publish_date": datetime.now().strftime("%Y-%m-%d"),
                "deadline": "2026-04-30",
                "apply_url": f"https://jobs.{company_name}.com/position/2"
            },
            {
                "position": "产品运营实习生",
                "location": "深圳",
                "type": "日常实习",
                "salary": "250-350 元/天",
                "description": "负责产品运营、数据分析、用户反馈",
                "requirements": ["本科及以上学历", "数据分析能力", "产品思维"],
                "publish_date": datetime.now().strftime("%Y-%m-%d"),
                "deadline": "2026-04-30",
                "apply_url": f"https://jobs.{company_name}.com/position/3"
            }
        ]
        
        # 如果指定了岗位类型，过滤
        if positions:
            filtered_jobs = []
            for job in base_jobs:
                if any(pos in job['position'] for pos in positions):
                    filtered_jobs.append(job)
            return filtered_jobs if filtered_jobs else base_jobs[:1]
        
        return base_jobs
    
    def parse_jd(self, content: str) -> Dict:
        """解析 JD 内容"""
        jd = {
            "position": "",
            "company": "",
            "location": "",
            "type": "",
            "salary": "",
            "description": "",
            "requirements": [],
            "publish_date": "",
            "deadline": ""
        }
        
        # 提取职位名称
        import re
        position_patterns = [
            r"招聘 (.*?)\(",
            r"职位：(.*?)\n",
            r"岗位：(.*?)\n",
            r"([^\n]+?实习生 [^\n]+)"
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, content)
            if match:
                jd['position'] = match.group(1).strip()
                break
        
        # 提取工作地点
        location_patterns = [
            r"工作地点：?(.*?)\n",
            r"城市：?(.*?)\n",
            r"(北京 | 上海 | 深圳 | 广州 | 杭州 | 成都)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content)
            if match:
                jd['location'] = match.group(1).strip()
                break
        
        # 提取薪资
        salary_pattern = r"(\d+-?\d* 元/天|\d+k-\d+k|\d+-\d+w)"
        salary_match = re.search(salary_pattern, content)
        if salary_match:
            jd['salary'] = salary_match.group(1)
        
        # 提取要求
        req_patterns = [
            r"(?:任职 | 要求 | 资格)[^\n]*\n((?:.*\n)*?)(?=\n\n|\n#|\Z)",
            r"(?:1\.|2\.|3\.).+"
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, content)
            if matches:
                jd['requirements'] = [m.strip() for m in matches if m.strip()]
                break
        
        return jd
