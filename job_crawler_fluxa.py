#!/usr/bin/env python3
"""
岗位爬取器 - FluxA API 集成版 v3.0
Job Crawler - FluxA API Integration

功能:
  - 集成 FluxA 付费 API (Google Jobs, Web Crawler)
  - 支持 x402 自动支付
  - 保留本地备用方案

使用方式:
  from job_crawler_fluxa import JobCrawlerFluxA
  
  crawler = JobCrawlerFluxA(use_fluxa=True)
  jobs = crawler.crawl("bytedance", category="运营", city="北京")
"""

from job_crawler import JobCrawler
from fluxa_api import fluxa_client, analyze_jd_with_ai

import json
from typing import Dict, List, Optional


class JobCrawlerFluxA(JobCrawler):
    """集成 FluxA API 的岗位爬取器"""
    
    def __init__(self, config_path: str = "config/companies.json", use_fluxa: bool = True):
        super().__init__(config_path)
        self.use_fluxa = use_fluxa
        self.use_count = 0  # API 调用计数
    
    def crawl(self, company_id: str, positions: List[str] = None, 
              category: str = None, city: str = None, use_real_data: bool = True) -> List[Dict]:
        """
        爬取指定公司的岗位（支持 FluxA API）
        """
        if company_id not in self.company_info:
            print(f"❌ 未知公司：{company_id}")
            return []
        
        # 如果启用 FluxA，优先使用 API
        if self.use_fluxa and use_real_data:
            jobs = self._crawl_with_fluxa(company_id, category, city)
            if jobs:
                print(f"✅ 通过 FluxA API 获取 {len(jobs)} 个岗位")
                return jobs
        
        # 回退到本地方案
        return super().crawl(company_id, positions, category, city, use_real_data)
    
    def _crawl_with_fluxa(self, company_id: str, category: str = None, city: str = None) -> List[Dict]:
        """
        使用 FluxA API 爬取岗位
        
        这需要:
        1. 在 FluxA Monetize 开通 Google Jobs API
        2. 设置 x402 支付
        3. 用户调用时自动扣费
        """
        company = self.company_info.get(company_id, {})
        company_name = company.get("name", company_id)
        
        # 构建搜索查询
        query = f"{company_name} 实习"
        if category:
            query += f" {category}"
        if city:
            query += f" {city}"
        
        # 调用 FluxA API
        try:
            # 尝试使用 Google Jobs API ($0.01/次)
            results = fluxa_client.search_google_jobs(query, city)
            self.use_count += 1
            
            if results and isinstance(results, list):
                return self._parse_fluxa_results(results, company_id)
        except Exception as e:
            print(f"⚠️  FluxA API 调用失败: {e}")
            print("   回退到本地数据...")
        
        return None
    
    def _parse_fluxa_results(self, results: List[Dict], company_id: str) -> List[Dict]:
        """解析 FluxA API 返回的结果"""
        jobs = []
        
        for item in results:
            job = {
                "job_id": item.get("job_id", ""),
                "position": item.get("title", ""),
                "company": item.get("company", ""),
                "company_id": company_id,
                "location": item.get("location", ""),
                "category": item.get("category", ""),
                "job_type": "实习",
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "requirements": item.get("requirements", []),
                "salary": item.get("salary", ""),
                "source": "fluxa_api",  # 标记数据来源
                "price_paid": 0.01  # 支付金额
            }
            jobs.append(job)
        
        return jobs
    
    def enrich_job_details(self, job: Dict) -> Dict:
        """
        使用 FluxA API 丰富岗位详情
        
        调用 Web Content Crawler ($0.10/次) 获取完整 JD
        """
        url = job.get("url")
        if not url:
            return job
        
        try:
            # 获取完整职位描述
            content = fluxa_client.crawl_website(url)
            self.use_count += 1
            
            if content:
                # 使用 AI 分析 JD
                jd_analysis = analyze_jd_with_ai(content.get("text", ""))
                
                if jd_analysis:
                    job["jd_analysis"] = jd_analysis
                    job["enriched"] = True
                    job["enrichment_cost"] = 0.10
        except Exception as e:
            print(f"⚠️  丰富岗位详情失败: {e}")
        
        return job
    
    def get_usage_stats(self) -> Dict:
        """获取 API 使用统计"""
        return {
            "total_calls": self.use_count,
            "estimated_cost": self.use_count * 0.01,  # 假设平均 $0.01/次
            "revenue_potential": self.use_count * 0.05  # 假设定价 $0.05/次
        }


# 便捷函数
def create_crawler(use_fluxa: bool = True) -> JobCrawlerFluxA:
    """创建爬虫实例"""
    return JobCrawlerFluxA(use_fluxa=use_fluxa)


if __name__ == "__main__":
    # 测试
    print("🔧 FluxA 岗位爬取器测试")
    print("-" * 40)
    
    crawler = JobCrawlerFluxA(use_fluxa=True)
    
    # 尝试爬取字节跳动岗位
    print("\n🔍 爬取字节跳动运营岗位...")
    jobs = crawler.crawl("bytedance", category="运营", city="北京")
    
    if jobs:
        print(f"\n✅ 获取到 {len(jobs)} 个岗位:")
        for job in jobs[:3]:
            print(f"  - {job.get('position')} @ {job.get('location')}")
    else:
        print("⚠️  使用本地数据（FluxA API 未配置）")
        # 使用本地数据
        jobs = crawler.crawl("bytedance", category="运营", city="北京", use_real_data=False)
        print(f"✅ 获取到 {len(jobs)} 个本地岗位")
    
    # 显示统计
    stats = crawler.get_usage_stats()
    print(f"\n📊 使用统计:")
    print(f"   API 调用次数: {stats['total_calls']}")
    print(f"   预估成本: ${stats['estimated_cost']:.2f}")
    print(f"   营收潜力: ${stats['revenue_potential']:.2f}")
