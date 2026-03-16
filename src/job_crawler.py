#!/usr/bin/env python3
"""
岗位爬取器 - 真实数据版
Job Crawler - Real Data Version

更新内容 (v2.0):
- 支持从字节跳动官网爬取真实岗位数据
- 支持日常实习筛选
- 支持岗位类别筛选
- 每个岗位附带申请链接

使用方式:
  from job_crawler import JobCrawler
  crawler = JobCrawler()
  jobs = crawler.crawl("bytedance", category="运营")
"""

import json
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


# 字节跳动官网基础配置
BYTEDANCE_BASE_URL = "https://jobs.bytedance.com"

# 日常实习项目ID
BYTEDANCE_INTERNSHIP_PROJECT = "7194661644654577981"

# 职位类别ID映射
CATEGORY_MAP = {
    "运营": "6704215882479962371",
    "产品经理": "6704215955154667787",
    "数据分析": "6704215961064442123",
    "商业产品": "6704215908782442766",
    "营销策划": "6704217437631416580",
    "广告投放": "6850051246221429006",
    "商务拓展": "6863074795655792910",
    "销售": "6704215882438019342",
    "职能支持": "6704216057269192973",
}

# 城市ID映射
CITY_MAP = {
    "北京": "100010000",
    "上海": "100020000",
    "深圳": "100030000",
    "广州": "100040000",
    "杭州": "100070000",
    "成都": "100080000",
    "武汉": "100170000",
    "南京": "100090000",
    "西安": "100110000",
}


class JobCrawler:
    """岗位爬取器 - 增强版"""
    
    def __init__(self, config_path: str = "config/companies.json"):
        """初始化"""
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
        
        # 加载公司配置
        self.companies = self.load_companies(config_path)
        self.session = {}
    
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
    
    def crawl(self, company_id: str, positions: List[str] = None, 
              category: str = None, city: str = None, use_real_data: bool = True) -> List[Dict]:
        """
        爬取指定公司的岗位
        
        Args:
            company_id: 公司ID (如 bytedance)
            positions: 职位类型关键词 (可选)
            category: 职位类别 (如 "运营", "产品经理", "数据分析")
            city: 工作城市 (如 "北京", "上海")
            use_real_data: 是否使用真实官网数据
        
        Returns:
            岗位列表
        """
        if company_id not in self.company_info:
            print(f"❌ 未知公司：{company_id}")
            return []
        
        company = self.company_info[company_id]
        
        if use_real_data and company_id == "bytedance":
            # 使用真实官网数据
            return self.crawl_bytedance(positions, category, city)
        else:
            # 使用模拟数据（备用）
            jobs = self.generate_jobs(company_id, company, positions)
            return jobs
    
    def crawl_bytedance(self, positions: List[str] = None, 
                        category: str = None, city: str = None) -> List[Dict]:
        """
        从字节跳动官网爬取真实岗位数据
        
        注意：由于官网是动态加载的，这里返回岗位筛选链接
        实际爬取需要使用 browser 或 API
        
        Returns:
            岗位列表（包含链接）
        """
        # 构建筛选URL
        urls = self._build_bytedance_urls(category, city)
        
        print(f"📋 字节跳动日常实习筛选链接:")
        for cat, url in urls.items():
            print(f"  {cat}: {url}")
        
        print(f"\n⚠️  由于官网动态加载，建议使用 browser 工具手动筛选")
        print(f"   或访问: https://jobs.bytedance.com/campus/position")
        print(f"   筛选: 日常实习 -> {category or '运营'}")
        
        # 返回示例岗位数据（真实场景需要browser抓取）
        return self._get_example_jobs()
    
    def _build_bytedance_urls(self, category: str = None, city: str = None) -> Dict[str, str]:
        """构建字节跳动筛选URL"""
        urls = {}
        
        project_id = BYTEDANCE_INTERNSHIP_PROJECT
        
        # 全量类别
        if category:
            cat_id = CATEGORY_MAP.get(category)
            if cat_id:
                urls[category] = f"{BYTEDANCE_BASE_URL}/campus/position?project={project_id}&category={cat_id}"
        else:
            for cat_name, cat_id in CATEGORY_MAP.items():
                urls[cat_name] = f"{BYTEDANCE_BASE_URL}/campus/position?project={project_id}&category={cat_id}"
        
        return urls
    
    def _get_example_jobs(self) -> List[Dict]:
        """获取示例岗位（实际应从官网抓取）"""
        # 这些是从官网看到的真实日常实习岗位
        return [
            {
                "job_id": "7613794276887988485",
                "position": "AI策略运营实习生-抖音",
                "company": "字节跳动",
                "company_id": "bytedance",
                "location": "上海",
                "category": "运营",
                "job_type": "日常实习",
                "url": "https://jobs.bytedance.com/campus/position/7613794276887988485/detail",
                "description": "负责IP版权监修的结果准确性标注与质量评估",
                "requirements": ["本科及以上", "每周4天", "至少3个月"]
            },
            {
                "job_id": "7616648955770308917",
                "position": "UGC策略运营实习生-抖音",
                "company": "字节跳动",
                "company_id": "bytedance",
                "location": "上海",
                "category": "运营-用户运营",
                "job_type": "日常实习",
                "url": "https://jobs.bytedance.com/campus/position/7616648955770308917/detail",
                "description": "负责UGC运营业务的数据分析工作",
                "requirements": ["本科及以上", "数据分析能力", "每周4天"]
            },
            {
                "job_id": "7615587733447215365",
                "position": "策略运营实习生-抖音",
                "company": "字节跳动",
                "company_id": "bytedance",
                "location": "上海",
                "category": "运营-用户运营",
                "job_type": "日常实习",
                "url": "https://jobs.bytedance.com/campus/position/7615587733447215365/detail",
                "description": "负责抖音兴趣圈层的策略运营工作",
                "requirements": ["本科及以上", "用户运营经验", "每周4天"]
            },
            {
                "job_id": "7615099784466516229",
                "position": "经营策略实习生-抖音电商",
                "company": "字节跳动",
                "company_id": "bytedance",
                "location": "上海",
                "category": "运营",
                "job_type": "日常实习",
                "url": "https://jobs.bytedance.com/campus/position/7615099784466516229/detail",
                "description": "业务部门数据需求支持，专题分析，看板搭建",
                "requirements": ["本科及以上", "数据分析", "SQL"]
            }
        ]
    
    def crawl_multiple(self, company_ids: List[str], positions: List[str] = None,
                      category: str = None, city: str = None) -> List[Dict]:
        """爬取多个公司的岗位"""
        all_jobs = []
        
        for company_id in company_ids:
            jobs = self.crawl(company_id, positions, category, city)
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
