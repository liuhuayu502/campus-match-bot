#!/usr/bin/env python3
"""
岗位爬取器 - 增强版
Job Crawler - Enhanced Version

优化内容:
- 支持更多大厂校招官网
- 优化爬取逻辑
- 支持更多岗位类型
- 添加薪资解析
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class JobCrawler:
    """岗位爬取器 - 增强版"""
    
    def __init__(self, config_path: str = "config/companies.json"):
        """初始化"""
        self.companies = self.load_companies(config_path)
        self.session = {}
        
        # 公司信息库 (扩展版)
        self.company_info = {
            "bytedance": {
                "name": "字节跳动",
                "alias": ["抖音", "TikTok", "飞书"],
                "campusUrl": "https://jobs.bytedance.com/campus",
                "socialUrl": "https://jobs.bytedance.com",
                "cities": ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "南京", "西安"],
                "hotPositions": ["内容运营", "用户运营", "产品运营", "市场营销", "数据分析", "HR"],
                "salaryRange": "200-400 元/天",
                "features": ["免费三餐", "房补", "健身房"]
            },
            "tencent": {
                "name": "腾讯",
                "alias": ["微信", "QQ"],
                "campusUrl": "https://join.qq.com",
                "socialUrl": "https://careers.tencent.com",
                "cities": ["深圳", "北京", "上海", "广州", "成都", "杭州", "武汉"],
                "hotPositions": ["产品策划", "运营", "游戏策划", "市场", "HR"],
                "salaryRange": "200-350 元/天",
                "features": ["免费早餐", "房补", "年度旅游"]
            },
            "alibaba": {
                "name": "阿里巴巴",
                "alias": ["阿里", "淘宝", "天猫", "支付宝"],
                "campusUrl": "https://talent.alibaba.com/campus",
                "socialUrl": "https://talent.alibaba.com",
                "cities": ["杭州", "北京", "上海", "深圳", "广州", "成都", "西安"],
                "hotPositions": ["运营专员", "品类运营", "活动运营", "商家运营", "产品经理"],
                "salaryRange": "250-400 元/天",
                "features": ["免费三餐", "房补", "健身"]
            },
            "meituan": {
                "name": "美团",
                "alias": ["大众点评", "美团外卖"],
                "campusUrl": "https://campus.meituan.com",
                "socialUrl": "https://recruit.meituan.com",
                "cities": ["北京", "上海", "深圳", "成都", "杭州", "武汉", "西安"],
                "hotPositions": ["商家运营", "用户运营", "产品经理", "数据分析", "市场推广"],
                "salaryRange": "200-350 元/天",
                "features": ["免费晚餐", "打车报销"]
            },
            "baidu": {
                "name": "百度",
                "alias": ["Apollo", "文心一言"],
                "campusUrl": "https://talent.baidu.com/campus",
                "socialUrl": "https://talent.baidu.com",
                "cities": ["北京", "上海", "深圳", "广州", "成都", "武汉"],
                "hotPositions": ["产品经理", "运营", "算法工程师", "数据分析", "市场营销"],
                "salaryRange": "200-400 元/天",
                "features": ["免费早餐", "健身房"]
            },
            "xiaohongshu": {
                "name": "小红书",
                "alias": ["笔记"],
                "campusUrl": "https://job.xiaohongshu.com/campus",
                "socialUrl": "https://job.xiaohongshu.com",
                "cities": ["上海", "北京"],
                "hotPositions": ["内容运营", "社区运营", "品牌营销", "产品经理", "用户运营"],
                "salaryRange": "250-400 元/天",
                "features": ["免费三餐", "下午茶"]
            },
            "kuaishou": {
                "name": "快手",
                "alias": ["快聘", "电商"],
                "campusUrl": "https://campus.kuaishou.com",
                "socialUrl": "https://job.kuaishou.com",
                "cities": ["北京", "上海", "深圳", "杭州", "成都", "武汉"],
                "hotPositions": ["内容运营", "直播运营", "用户增长", "产品经理", "数据分析"],
                "salaryRange": "250-400 元/天",
                "features": ["免费三餐", "房补"]
            },
            "bilibili": {
                "name": "B站",
                "alias": ["哔哩哔哩", "B站"],
                "campusUrl": "https://jobs.bilibili.com/campus",
                "socialUrl": "https://jobs.bilibili.com",
                "cities": ["上海", "北京", "广州", "杭州", "武汉"],
                "hotPositions": ["内容运营", "社区运营", "游戏运营", "产品经理", "市场"],
                "salaryRange": "200-350 元/天",
                "features": ["免费三餐", "手办", "年会"]
            },
            "xiaomi": {
                "name": "小米",
                "alias": ["MIUI", "米家"],
                "campusUrl": "https://hr.xiaomi.com/campus",
                "socialUrl": "https://hr.xiaomi.com",
                "cities": ["北京", "上海", "深圳", "武汉", "南京", "西安"],
                "hotPositions": ["产品经理", "运营", "市场营销", "设计", "HR"],
                "salaryRange": "200-350 元/天",
                "features": ["免费三餐", "房补"]
            },
            "huawei": {
                "name": "华为",
                "alias": ["华为云", "鸿蒙"],
                "campusUrl": "https://career.huawei.com/reccampportal",
                "socialUrl": "https://career.huawei.com",
                "cities": ["深圳", "北京", "上海", "杭州", "成都", "武汉", "南京", "西安"],
                "hotPositions": ["产品营销", "解决方案", "运营管理", "客户经理", "HR"],
                "salaryRange": "300-500 元/天",
                "features": ["年终奖", "股票", "深圳户口"]
            },
            "jd": {
                "name": "京东",
                "alias": ["京东物流", "京东科技"],
                "campusUrl": "https://campus.jd.com",
                "socialUrl": "https://job.jd.com",
                "cities": ["北京", "上海", "深圳", "广州", "武汉", "西安", "成都"],
                "hotPositions": ["产品经理", "运营", "供应链", "市场营销", "数据分析"],
                "salaryRange": "200-350 元/天",
                "features": ["免费班车", "房补"]
            },
            "netease": {
                "name": "网易",
                "alias": ["云音乐", "游戏"],
                "campusUrl": "https://campus.163.com",
                "socialUrl": "https://hr.163.com",
                "cities": ["杭州", "北京", "上海", "广州", "深圳"],
                "hotPositions": ["游戏运营", "产品经理", "内容运营", "市场营销", "HR"],
                "salaryRange": "200-350 元/天",
                "features": ["免费三餐", "健身房"]
            },
            "didi": {
                "name": "滴滴",
                "alias": ["滴滴出行", "青桔"],
                "campusUrl": "https://campus.didiglobal.com",
                "socialUrl": "https://career.didiglobal.com",
                "cities": ["北京", "上海", "杭州", "深圳", "广州", "成都"],
                "hotPositions": ["产品经理", "运营", "数据分析", "算法", "市场营销"],
                "salaryRange": "250-400 元/天",
                "features": ["免费晚餐", "打车券"]
            },
            "pinduoduo": {
                "name": "拼多多",
                "alias": ["多多买菜", "TEMU"],
                "campusUrl": "https://career.pinduoduo.com/campus",
                "socialUrl": "https://career.pinduoduo.com",
                "cities": ["上海", "深圳", "北京", "广州", "杭州"],
                "hotPositions": ["产品经理", "运营", "招商", "数据分析", "HR"],
                "salaryRange": "300-500 元/天",
                "features": ["免费三餐", "房补"]
            },
            "shein": {
                "name": "希音",
                "alias": ["SHEIN", "跨境电商"],
                "campusUrl": "https://career.sheincorp.cn/campus",
                "socialUrl": "https://career.sheincorp.cn",
                "cities": ["广州", "深圳", "杭州", "南京", "武汉"],
                "hotPositions": ["产品经理", "运营", "供应链", "市场营销", "设计"],
                "salaryRange": "250-400 元/天",
                "features": ["免费三餐", "房补"]
            }
        }
    
    def load_companies(self, path: str) -> Dict:
        """加载公司配置"""
        default_companies = list(self.company_info.keys())
        
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
        if company_id not in self.company_info:
            print(f"❌ 未知公司：{company_id}")
            return []
        
        company = self.company_info[company_id]
        
        # 构建搜索 URL (实际应该根据官网结构构建)
        # 这里使用模拟数据
        jobs = self.generate_jobs(company_id, company, positions)
        
        return jobs
    
    def crawl_multiple(self, company_ids: List[str], positions: List[str] = None) -> List[Dict]:
        """爬取多个公司的岗位"""
        all_jobs = []
        
        for company_id in company_ids:
            jobs = self.crawl(company_id, positions)
            all_jobs.extend(jobs)
        
        return all_jobs
    
    def generate_jobs(self, company_id: str, company: Dict, positions: List[str] = None) -> List[Dict]:
        """生成岗位数据 (模拟，实际应该从官网爬取)"""
        
        # 岗位模板
        job_templates = [
            {
                "position_type": "运营类",
                "templates": [
                    {"title": "{company}内容运营实习生", "desc": "负责内容策划、撰写、发布，数据分析", "req": ["本科及以上", "每周4天", "至少3个月", "内容敏感度好"]},
                    {"title": "{company}用户运营实习生", "desc": "负责用户增长、活动策划、数据分析", "req": ["本科及以上", "熟悉社交媒体", "沟通能力强"]},
                    {"title": "{company}产品运营实习生", "desc": "负责产品运营、数据分析、用户反馈", "req": ["本科及以上", "数据分析能力", "产品思维"]},
                    {"title": "{company}活动运营实习生", "desc": "负责活动策划、执行、复盘", "req": ["本科及以上", "创意能力", "执行力强"]},
                ]
            },
            {
                "position_type": "产品类",
                "templates": [
                    {"title": "{company}产品经理实习生", "desc": "负责需求分析、产品设计、项目跟进", "req": ["本科及以上", "逻辑清晰", "沟通能力好"]},
                    {"title": "{company}产品实习生", "desc": "协助产品经理完成产品工作", "req": ["本科及以上", "学习能力强"]},
                ]
            },
            {
                "position_type": "市场类",
                "templates": [
                    {"title": "{company}市场营销实习生", "desc": "负责市场推广、品牌宣传、活动策划", "req": ["本科及以上", "营销敏感", "创意能力"]},
                    {"title": "{company}商务实习生", "desc": "负责商务合作、客户对接", "req": ["本科及以上", "沟通能力强", "外向"]},
                ]
            },
            {
                "position_type": "数据类",
                "templates": [
                    {"title": "{company}数据分析实习生", "desc": "负责数据分析、报告产出、指标监控", "req": ["本科及以上", "SQL", "Python", "Excel"]},
                    {"title": "{company}商业分析实习生", "desc": "负责商业分析、竞品研究、行业研究", "req": ["本科及以上", "分析能力", "PPT"]},
                ]
            }
        ]
        
        jobs = []
        company_name = company["name"]
        
        # 生成岗位
        for category in job_templates:
            for template in category["templates"]:
                # 如果指定了岗位类型过滤
                if positions:
                    if not any(pos in template["title"] for pos in positions):
                        continue
                
                # 随机选择城市
                import random
                city = random.choice(company["cities"])
                
                # 解析薪资
                salary_range = company.get("salaryRange", "200-300 元/天")
                
                job = {
                    "company_id": company_id,
                    "company": company_name,
                    "position": template["title"].format(company=company_name),
                    "position_type": category["position_type"],
                    "location": city,
                    "type": "日常实习",
                    "salary": salary_range,
                    "description": template["desc"],
                    "requirements": template["req"],
                    "publish_date": datetime.now().strftime("%Y-%m-%d"),
                    "deadline": "2026-04-30",
                    "apply_url": f"https://jobs.{company_id}.com/position/{random.randint(1000,9999)}",
                    "features": company.get("features", []),
                    "hot": company_name in company.get("hotPositions", [])
                }
                
                jobs.append(job)
        
        return jobs
    
    def parse_salary(self, salary_text: str) -> Dict:
        """解析薪资文本"""
        # 解析日薪
        daily_pattern = r'(\d+)-(\d+)\s*元/天'
        daily_match = re.search(daily_pattern, salary_text)
        
        if daily_match:
            return {
                "type": "daily",
                "min": int(daily_match.group(1)),
                "max": int(daily_match.group(2)),
                "unit": "元/天"
            }
        
        # 解析月薪
        monthly_pattern = r'(\d+)-(\d+)k'
        monthly_match = re.search(monthly_pattern, salary_text, re.IGNORECASE)
        
        if monthly_match:
            return {
                "type": "monthly",
                "min": int(monthly_match.group(1)) * 1000,
                "max": int(monthly_match.group(2)) * 1000,
                "unit": "元/月"
            }
        
        # 解析年薪
        yearly_pattern = r'(\d+)-(\d+)w'
        yearly_match = re.search(yearly_pattern, salary_text, re.IGNORECASE)
        
        if yearly_match:
            return {
                "type": "yearly",
                "min": int(yearly_match.group(1)) * 10000,
                "max": int(yearly_match.group(2)) * 10000,
                "unit": "元/年"
            }
        
        return {"type": "unknown", "text": salary_text}
    
    def search_jobs(self, keyword: str, location: str = None, company: str = None) -> List[Dict]:
        """搜索岗位"""
        results = []
        
        # 遍历所有公司
        for company_id, company_info in self.company_info.items():
            # 公司过滤
            if company and company_id not in company:
                continue
            
            # 爬取岗位
            jobs = self.crawl(company_id)
            
            # 关键词过滤
            for job in jobs:
                if keyword in job["position"] or keyword in job["description"]:
                    # 地点过滤
                    if location:
                        if location in job["location"]:
                            results.append(job)
                    else:
                        results.append(job)
        
        return results
    
    def get_company_info(self, company_id: str) -> Optional[Dict]:
        """获取公司信息"""
        return self.company_info.get(company_id)
    
    def list_companies(self) -> List[Dict]:
        """列出所有支持的公司"""
        return [
            {
                "id": company_id,
                "name": info["name"],
                "cities": info["cities"][:5],  # 只显示前5个城市
                "hot_positions": info["hotPositions"][:3],  # 只显示前3个热门岗位
                "salary_range": info.get("salaryRange", "未知")
            }
            for company_id, info in self.company_info.items()
        ]


# 测试代码
if __name__ == "__main__":
    crawler = JobCrawler()
    
    # 列出所有公司
    print("📋 支持的公司:")
    for company in crawler.list_companies():
        print(f"  {company['id']}: {company['name']} ({company['salary_range']})")
    
    print("\n" + "=" * 60)
    
    # 爬取字节跳动岗位
    print("\n🔍 爬取字节跳动实习岗位:")
    jobs = crawler.crawl("bytedance", ["运营"])
    
    for job in jobs[:3]:
        print(f"\n📌 {job['position']}")
        print(f"   地点: {job['location']}")
        print(f"   薪资: {job['salary']}")
        print(f"   要求: {', '.join(job['requirements'])}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
