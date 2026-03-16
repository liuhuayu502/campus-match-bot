#!/usr/bin/env python3
"""
FluxA API 集成模块
用于调用 FluxA Monetize 的付费 API

支持的 API:
- google-jobs: Google Job Scrapper ($0.01/次)
- web-crawler: Web Content Crawler ($0.10/次)
- qwen-llm: Qwen AI Chat (免费)
"""

import os
import json
import requests
from typing import Dict, List, Optional

# FluxA API 配置
FLUXA_API_BASE = "https://api.fluxapay.xyz/v1"

# 从环境变量获取 API Key
FLUXA_API_KEY = os.environ.get("FLUXA_API_KEY", "")


class FluxAClient:
    """FluxA API 客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or FLUXA_API_KEY
        self.base_url = FLUXA_API_BASE
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """发送 API 请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.request(method, url, headers=headers, json=data)
        
        if response.status_code == 402:
            # 需要支付
            return {"error": "PAYMENT_REQUIRED", "message": "需要支付"}
        
        return response.json()
    
    def search_google_jobs(self, query: str, location: str = None) -> List[Dict]:
        """
        使用 Google Job Scrapper API 搜索职位
        
        Args:
            query: 搜索关键词，如 "字节跳动 运营 实习"
            location: 工作地点
        
        Returns:
            职位列表
        """
        # 尝试直接调用（如果有 x402 支持的 MCP）
        endpoint = "/google-jobs"
        
        # 构建搜索查询
        search_query = query
        if location:
            search_query += f" {location}"
        
        # 模拟 API 调用结构（实际需要通过 FluxA MCP）
        payload = {
            "query": search_query,
            "num_results": 20
        }
        
        # 这里返回模拟数据，实际使用时请配置 FluxA MCP Server
        # 真实调用会通过 x402 自动处理支付
        return self._request("POST", endpoint, payload)
    
    def crawl_website(self, url: str) -> Dict:
        """
        使用 Web Content Crawler 深度抓取网页
        
        Args:
            url: 目标网址
        
        Returns:
            网页内容
        """
        endpoint = "/crawl"
        
        payload = {
            "url": url,
            "max_depth": 2,
            "extract_text": True
        }
        
        return self._request("POST", endpoint, payload)
    
    def chat_with_qwen(self, prompt: str, system_prompt: str = None) -> str:
        """
        使用 Qwen AI Chat 进行对话（免费）
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示（可选）
        
        Returns:
            AI 回复
        """
        endpoint = "/llm"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "qwen2.5",
            "messages": messages,
            "temperature": 0.7
        }
        
        result = self._request("POST", endpoint, payload)
        
        if "error" in result:
            # 如果 API 不可用，返回本地处理
            return None
        
        return result.get("choices", [{}])[0].get("message", {}).get("content")


# 全局客户端实例
fluxa_client = FluxAClient()


def get_job_listings_via_api(query: str, location: str = None) -> List[Dict]:
    """
    通过 FluxA API 获取职位列表
    
    这是一个高级功能，需要:
    1. 在 FluxA Monetize 注册 MCP Server
    2. 配置 x402 支付
    3. 设置价格
    
    当前版本返回空列表，实际使用时启用
    """
    try:
        jobs = fluxa_client.search_google_jobs(query, location)
        return jobs if isinstance(jobs, list) else []
    except Exception as e:
        print(f"⚠️  API 调用失败: {e}")
        return []


def analyze_resume_with_ai(resume_text: str) -> Dict:
    """
    使用 Qwen AI 分析简历（免费）
    
    Args:
        resume_text: 简历文本
    
    Returns:
        解析后的能力画像
    """
    prompt = f"""请分析以下简历，提取关键信息：

{resume_text}

请按以下 JSON 格式返回：
{{
    "name": "姓名",
    "skills": ["技能1", "技能2"],
    "experience": ["经历1", "经历2"],
    "education": "学校",
    "languages": ["语言能力"]
}}"""
    
    try:
        result = fluxa_client.chat_with_qwen(prompt)
        if result:
            import re
            # 尝试提取 JSON
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except:
        pass
    
    # 如果 API 不可用，返回 None 让本地解析器处理
    return None


def analyze_jd_with_ai(jd_text: str) -> Dict:
    """
    使用 Qwen AI 分析职位描述（免费）
    
    Args:
        jd_text: 职位描述文本
    
    Returns:
        解析后的岗位要求
    """
    prompt = f"""请分析以下职位描述，提取关键要求：

{jd_text}

请按以下 JSON 格式返回：
{{
    "required_skills": ["必备技能1", "必备技能2"],
    "preferred_skills": ["加分技能1", "加分技能2"],
    "experience": "经验要求",
    "education": "学历要求",
    "key_responsibilities": ["职责1", "职责2"]
}}"""
    
    try:
        result = fluxa_client.chat_with_qwen(prompt)
        if result:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except:
        pass
    
    return None


if __name__ == "__main__":
    # 测试
    client = FluxAClient()
    
    print("🔧 FluxA API 客户端测试")
    print("-" * 40)
    
    # 测试 Qwen AI（免费）
    print("\n📝 测试 Qwen AI (免费)...")
    result = client.chat_with_qwen("你好，请用一句话介绍你自己")
    if result:
        print(f"✅ Qwen AI 响应: {result[:100]}...")
    else:
        print("⚠️  Qwen AI 暂不可用，将使用本地解析")
    
    print("\n✅ 测试完成!")
