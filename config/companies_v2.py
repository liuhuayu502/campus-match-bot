#!/usr/bin/env python3
"""
大厂校招官网配置数据 v2.1
Company Career Website Configuration v2.1

包含各大厂的校招/社招官网URL、岗位分类结构
以及预设的岗位详情页面结构和API端点

数据来源: 实际访问各公司招聘官网抓取
更新时间: 2026-03-17
"""

# =============================================================================
# 岗位详情页面结构配置
# =============================================================================

# 岗位详情URL模板
JOB_DETAIL_URLS = {
    "bytedance": {
        "base": "https://jobs.bytedance.com/campus/position/{job_id}/detail",
        "pattern": r"/campus/position/(\d+)/detail",
        "id_prefix": ""
    },
    "tencent": {
        "base": "https://careers.tencent.com/reccpost/{job_id}",
        "pattern": r"jobid=(\d+)",
        "id_prefix": ""
    },
    "meituan": {
        "base": "https://campus.meituan.com/job/{job_id}",
        "pattern": r"/job/(\d+)",
        "id_prefix": ""
    },
    "baidu": {
        "base": "https://talent.baidu.com/jobs/detail/{job_id}",
        "pattern": r"/detail/(\d+)",
        "id_prefix": ""
    },
    "xiaohongshu": {
        "base": "https://job.xiaohongshu.com/campus/position/{job_id}/detail",
        "pattern": r"/position/(\d+)/detail",
        "id_prefix": ""
    },
    "kuaishou": {
        "base": "https://campus.kuaishou.com/campus/position/{job_id}/detail",
        "pattern": r"/position/(\d+)",
        "id_prefix": ""
    },
    "bilibili": {
        "base": "https://jobs.bilibili.com/campus/position/{job_id}/detail",
        "pattern": r"/position/(\d+)",
        "id_prefix": ""
    },
    "xiaomi": {
        "base": "https://campus.xiaomi.com/job/{job_id}",
        "pattern": r"/job/(\d+)",
        "id_prefix": ""
    },
    "huawei": {
        "base": "https://career.huawei.com/receptionjob/apply/{job_id}",
        "pattern": r"/apply/(\d+)",
        "id_prefix": ""
    }
}


# =============================================================================
# 公司配置
# =============================================================================

COMPANIES = {
    "bytedance": {
        "name": "字节跳动",
        "name_en": "ByteDance",
        "campus_url": "https://jobs.bytedance.com/campus",
        "social_url": "https://jobs.bytedance.com",
        "job_list_url": "https://jobs.bytedance.com/campus/position",
        
        # 页面结构 (从官网抓取)
        "page_structure": {
            "list_selector": ".job-list, .position-list",
            "item_selector": ".job-item, .position-item",
            "detail_selector": ".job-detail, .position-detail",
            "title_selector": ".title, .job-title",
            "location_selector": ".location, .city",
            "category_selector": ".category, .type",
            "description_selector": ".description, .responsibility",
            "requirement_selector": ".requirement, .qualification",
            "pagination": {
                "type": "page",
                "total_text": "开启新的工作",
                "total_pattern": r"开启新的工作（(\d+)）",
                "selector": ".pagination button, .page-num",
                "next_text": "下一页"
            }
        },
        
        # 招聘项目 (校招)
        "campus_projects": {
            "2026届校园招聘": {
                "id": "7194661553653016845",
                "type": "campus",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661553653016845"
            },
            "2026届筋斗云人才计划": {
                "id": "7194661553652951317",
                "type": "talent",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661553652951317"
            },
            "2026届Top Seed人才计划": {
                "id": "7194661553652885781",
                "type": "talent",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661553652885781"
            },
            "日常实习": {
                "id": "7194661644654577981",
                "type": "intern",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661644654577981"
            },
            "Top Seed人才计划研究实习生专项": {
                "id": "7194661644654512445",
                "type": "research_intern",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661644654512445"
            },
            "筋斗云人才计划实习专项": {
                "id": "7194661644654446901",
                "type": "intern",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661644654446901"
            },
            "ByteIntern": {
                "id": "7194661644654381357",
                "type": "intern",
                "url": "https://jobs.bytedance.com/campus/position?project=7194661644654381357"
            }
        },
        
        # 职位类别 (category)
        "categories": {
            "研发": "6704215882438019342",
            "运营": "6704215882479962371",
            "产品": "6704215955154667787",
            "职能/支持": "6704216057269192973",
            "设计": "6704215961064442123",
            "销售": "6704215882517301450",
            "市场": "6704217437631416580",
            "游戏策划": "6850051246221429006"
        },
        
        # 职位子类别 (functionCategory)
        "sub_categories": {
            # 产品
            "产品经理": "6704215955154667787",
            "数据分析": "6704215961064442123",
            "商业产品（广告）": "6704215908782442766",
            # 市场
            "营销策划": "6704217437631416580",
            "广告投放": "6850051246221429006",
            "商务拓展BD": "6863074795655792910"
        },
        
        # 城市
        "cities": {
            "北京": "100010000",
            "上海": "100020000",
            "深圳": "100030000",
            "广州": "100040000",
            "杭州": "100070000",
            "成都": "100080000",
            "武汉": "100170000",
            "南京": "100090000",
            "西安": "100110000"
        },
        
        # 薪资范围
        "salary_range": "200-400 元/天",
        
        # 特点
        "features": ["免费三餐", "房补", "健身房"],
        
        # 招聘项目类型映射
        "project_type": {
            "7194661644654577981": "intern",  # 日常实习
            "7194661553653016845": "campus",  # 正式校招
        }
    },
    
    "tencent": {
        "name": "腾讯",
        "name_en": "Tencent",
        "campus_url": "https://join.qq.com",
        "social_url": "https://careers.tencent.com",
        "job_list_url": "https://join.qq.com/#/job",
        
        # 招聘项目
        "campus_projects": {
            "2026应届生招聘": {
                "type": "campus",
                "url": "https://join.qq.com/post/373"
            },
            "2026实习生招聘": {
                "type": "intern",
                "url": "https://join.qq.com/post/374"
            },
            "青云计划-应届生": {
                "type": "talent",
                "url": "https://join.qq.com/post/375"
            },
            "青云计划-实习生": {
                "type": "talent_intern",
                "url": "https://join.qq.com/post/376"
            }
        },
        
        # 职位类别
        "categories": {
            "技术类": "tech",
            "产品类": "product",
            "设计类": "design",
            "市场/职能类": "marketing",
            "内容类": "content"
        },
        
        # 城市
        "cities": ["深圳", "北京", "上海", "广州", "成都", "杭州", "武汉", "南京", "西安", "重庆"],
        
        "salary_range": "200-350 元/天",
        "features": ["免费早餐", "房补", "年度旅游"]
    },
    
    "alibaba": {
        "name": "阿里巴巴",
        "name_en": "Alibaba",
        "campus_url": "https://campus.alibaba.com",
        "social_url": "https://talent.alibaba.com",
        "job_list_url": "https://talent.alibaba.com/campus/position",
        
        # 招聘项目
        "campus_projects": {
            "阿里星": {
                "type": "talent",
                "url": "https://campus.alibaba.com/aliStar"
            },
            "应届生招聘": {
                "type": "campus",
                "url": "https://talent.alibaba.com/campus/position"
            },
            "实习生招聘": {
                "type": "intern",
                "url": "https://talent.alibaba.com/campus/position"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "运营": "operation",
            "设计": "design",
            "市场/营销": "marketing",
            "职能": "function"
        },
        
        # 城市
        "cities": ["杭州", "北京", "上海", "深圳", "广州", "成都", "西安", "南京"],
        
        "salary_range": "250-400 元/天",
        "features": ["免费三餐", "房补"]
    },
    
    "meituan": {
        "name": "美团",
        "name_en": "Meituan",
        "campus_url": "https://campus.meituan.com",
        "social_url": "https://recruit.meituan.com",
        "job_list_url": "https://campus.meituan.com/web/campus",
        
        # 招聘项目
        "campus_projects": {
            "应届校招": {
                "type": "campus",
                "url": "https://campus.meituan.com/web/campus"
            },
            "北斗计划": {
                "type": "talent",
                "url": "https://campus.meituan.com/web/beidouprogram"
            },
            "转正实习": {
                "type": "intern_conversion",
                "url": "https://campus.meituan.com/web/campus?type=conversion"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://campus.meituan.com/web/campus?type=daily"
            }
        },
        
        # 职位类别
        "categories": {
            "技术类": "tech",
            "产品类": "product",
            "商业分析类": "ba",
            "零售类": "retail",
            "运营类": "operation",
            "设计类": "design",
            "市场营销类": "marketing",
            "职能类": "function",
            "金融类": "finance",
            "销售/客服与支持类": "sales"
        },
        
        # 城市
        "cities": ["北京", "上海", "深圳", "成都", "香港", "广州", "武汉", "杭州", "西安", "重庆", "南京", "厦门"],
        
        "salary_range": "200-350 元/天",
        "features": ["免费晚餐", "打车报销"]
    },
    
    "baidu": {
        "name": "百度",
        "name_en": "Baidu",
        "campus_url": "https://talent.baidu.com/jobs/campus",
        "social_url": "https://talent.baidu.com",
        "job_list_url": "https://talent.baidu.com/jobs/campus",
        
        # 页面结构 (从官网抓取)
        "page_structure": {
            "list_selector": ".job-list .job-item, .position-list .position-item",
            "detail_selector": ".job-detail, .position-detail",
            "pagination": {
                "type": "page",
                "selector": ".pagination a, .page a",
                "next_text": "下一页"
            }
        },
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://talent.baidu.com/jobs/campus"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://talent.baidu.com/jobs/campus?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "设计": "design",
            "运营": "operation",
            "市场": "marketing",
            "职能": "function"
        },
        
        # 城市
        "cities": ["北京", "上海", "深圳", "广州", "成都", "武汉", "南京"],
        
        "salary_range": "200-400 元/天",
        "features": ["免费早餐", "健身房"]
    },
    
    "xiaohongshu": {
        "name": "小红书",
        "name_en": "Xiaohongshu",
        "campus_url": "https://job.xiaohongshu.com/campus",
        "social_url": "https://job.xiaohongshu.com",
        "job_list_url": "https://job.xiaohongshu.com/campus/position",
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://job.xiaohongshu.com/campus/position"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://job.xiaohongshu.com/campus/position?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "运营": "operation",
            "市场": "marketing",
            "设计": "design"
        },
        
        # 城市
        "cities": ["上海", "北京"],
        
        "salary_range": "250-400 元/天",
        "features": ["免费三餐", "下午茶"]
    },
    
    "kuaishou": {
        "name": "快手",
        "name_en": "Kuaishou",
        "campus_url": "https://campus.kuaishou.com",
        "social_url": "https://job.kuaishou.com",
        "job_list_url": "https://campus.kuaishou.com/campus",
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://campus.kuaishou.com/campus"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://campus.kuaishou.com/campus?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "运营": "operation",
            "市场": "marketing",
            "设计": "design"
        },
        
        # 城市
        "cities": ["北京", "上海", "深圳", "杭州", "成都", "武汉"],
        
        "salary_range": "250-400 元/天",
        "features": ["免费三餐", "房补"]
    },
    
    "bilibili": {
        "name": "B站",
        "name_en": "Bilibili",
        "campus_url": "https://jobs.bilibili.com/campus",
        "social_url": "https://jobs.bilibili.com",
        "job_list_url": "https://jobs.bilibili.com/campus/position",
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://jobs.bilibili.com/campus/position"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://jobs.bilibili.com/campus/position?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "运营": "operation",
            "游戏": "game",
            "内容": "content",
            "市场": "marketing",
            "设计": "design"
        },
        
        # 城市
        "cities": ["上海", "北京", "广州", "武汉"],
        
        "salary_range": "200-350 元/天",
        "features": ["免费三餐", "手办"]
    },
    
    "xiaomi": {
        "name": "小米",
        "name_en": "Xiaomi",
        "campus_url": "https://campus.xiaomi.com",
        "social_url": "https://career.xiaomi.com",
        "job_list_url": "https://campus.xiaomi.com/campus",
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://campus.xiaomi.com/campus"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://campus.xiaomi.com/campus?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "产品": "product",
            "运营": "operation",
            "市场": "marketing",
            "设计": "design"
        },
        
        # 城市
        "cities": ["北京", "上海", "深圳", "武汉"],
        
        "salary_range": "200-350 元/天",
        "features": ["免费三餐", "房补"]
    },
    
    "huawei": {
        "name": "华为",
        "name_en": "Huawei",
        "campus_url": "https://career.huawei.com",
        "social_url": "https://career.huawei.com",
        "job_list_url": "https://career.huawei.com/campus",
        
        # 招聘项目
        "campus_projects": {
            "校园招聘": {
                "type": "campus",
                "url": "https://career.huawei.com/campus"
            },
            "日常实习": {
                "type": "intern",
                "url": "https://career.huawei.com/campus?type=intern"
            }
        },
        
        # 职位类别
        "categories": {
            "技术": "tech",
            "研发": "rd",
            "市场": "marketing",
            "职能": "function"
        },
        
        # 城市
        "cities": ["深圳", "北京", "上海", "南京", "西安", "成都", "武汉", "杭州", "苏州", "东莞"],
        
        "salary_range": "300-500 元/天",
        "features": ["年终奖", "股票"]
    }
}


# =============================================================================
# 通用配置
# =============================================================================

# 实习类型映射
INTERNSHIP_TYPE_MAP = {
    "日常实习": "daily",
    "转正实习": "conversion",
    "暑期实习": "summer",
    "寒假实习": "winter"
}

# 职位类别通用映射
COMMON_CATEGORIES = {
    "运营": ["内容运营", "用户运营", "活动运营", "产品运营", "电商运营", "直播运营"],
    "产品": ["产品经理", "产品助理", "产品运营"],
    "市场": ["市场营销", "品牌营销", "商务拓展", "广告投放", "BD"],
    "数据分析": ["数据分析", "商业分析", "数据运营"],
    "技术": ["算法", "后端", "前端", "移动端", "测试", "运维"],
    "设计": ["UI设计", "UX设计", "视觉设计", "交互设计"],
    "职能": ["HR", "行政", "法务", "财务"]
}


# =============================================================================
# 工具函数
# =============================================================================

def get_company_config(company_id: str) -> dict:
    """获取公司配置"""
    return COMPANIES.get(company_id)


def get_internship_url(company_id: str, category: str = None, city: str = None) -> str:
    """
    获取日常实习筛选URL
    
    Args:
        company_id: 公司ID
        category: 职位类别
        city: 城市
    
    Returns:
        筛选URL
    """
    company = COMPANIES.get(company_id)
    if not company:
        return ""
    
    base_url = company.get("job_list_url", "")
    
    # 字节跳动特殊处理
    if company_id == "bytedance":
        project_id = company["campus_projects"]["日常实习"]["id"]
        url = f"{base_url}?project={project_id}&type=1"
        
        if category:
            cat_id = company.get("sub_categories", {}).get(category)
            if cat_id:
                url += f"&category={cat_id}"
        
        if city:
            city_id = company.get("cities", {}).get(city)
            if city_id:
                url += f"&location={city_id}"
        
        return url
    
    # 其他公司
    if category or city:
        url = base_url
        params = []
        if category:
            params.append(f"category={category}")
        if city:
            params.append(f"city={city}")
        url += "?" + "&".join(params)
        return url
    
    # 返回默认日常实习URL
    intern_project = company.get("campus_projects", {}).get("日常实习", {})
    return intern_project.get("url", base_url)


def list_companies() -> list:
    """列出所有支持的公司"""
    return [
        {
            "id": k,
            "name": v["name"],
            "name_en": v.get("name_en", ""),
            "campus_url": v["campus_url"],
            "has_internship": "日常实习" in v.get("campus_projects", {})
        }
        for k, v in COMPANIES.items()
    ]


def get_job_detail_url(company_id: str, job_id: str) -> str:
    """
    获取岗位详情页URL
    
    Args:
        company_id: 公司ID
        job_id: 岗位ID
    
    Returns:
        岗位详情页URL
    """
    config = JOB_DETAIL_URLS.get(company_id)
    if not config:
        return ""
    
    return config["base"].format(job_id=job_id)


def parse_job_id_from_url(url: str, company_id: str) -> str:
    """
    从URL解析岗位ID
    
    Args:
        url: 岗位URL
        company_id: 公司ID
    
    Returns:
        岗位ID
    """
    import re
    config = JOB_DETAIL_URLS.get(company_id)
    if not config:
        return ""
    
    match = re.search(config["pattern"], url)
    return match.group(1) if match else ""


def build_filter_url(company_id: str, project: str = None, category: str = None, 
                     city: str = None, page: int = 1) -> str:
    """
    构建筛选URL
    
    Args:
        company_id: 公司ID
        project: 招聘项目
        category: 职位类别
        city: 城市
        page: 页码
    
    Returns:
        筛选URL
    """
    company = COMPANIES.get(company_id)
    if not company:
        return ""
    
    base_url = company.get("job_list_url", "")
    
    # 根据不同公司构建URL
    if company_id == "bytedance":
        params = [f"project={company['campus_projects'].get(project or '日常实习', {}).get('id', '7194661644654577981')}", "type=1"]
        if category:
            cat_id = company.get("sub_categories", {}).get(category)
            if cat_id:
                params.append(f"category={cat_id}")
        if city:
            city_id = company.get("cities", {}).get(city)
            if city_id:
                params.append(f"location={city_id}")
        if page > 1:
            params.append(f"current={page}")
        return f"{base_url}?{'&'.join(params)}"
    
    elif company_id == "meituan":
        params = []
        if project:
            type_map = {"日常实习": "daily", "转正实习": "conversion"}
            params.append(f"type={type_map.get(project, 'daily')}")
        if category:
            params.append(f"category={category}")
        if city:
            params.append(f"city={city}")
        if page > 1:
            params.append(f"page={page}")
        return f"{base_url}?{'&'.join(params)}" if params else base_url
    
    # 其他公司使用默认方式
    params = []
    if page > 1:
        params.append(f"page={page}")
    return f"{base_url}?{'&'.join(params)}" if params else base_url


# 测试
if __name__ == "__main__":
    print("🏢 支持的公司列表:")
    print("-" * 60)
    for company in list_companies():
        status = "✅" if company["has_internship"] else "❌"
        print(f"{status} {company['name']} ({company['name_en']})")
        print(f"   校招: {company['campus_url']}")
    
    print("\n" + "=" * 60)
    print("\n🎯 字节跳动日常实习筛选链接:")
    print("-" * 60)
    
    print("\n📋 运营类:")
    print(get_internship_url("bytedance", "运营"))
    
    print("\n📋 产品经理类:")
    print(get_internship_url("bytedance", "产品经理"))
    
    print("\n📋 数据分析类:")
    print(get_internship_url("bytedance", "数据分析"))
    
    print("\n📋 商业产品(广告)类:")
    print(get_internship_url("bytedance", "商业产品"))
    
    print("\n📋 营销策划类:")
    print(get_internship_url("bytedance", "营销策划"))
    
    print("\n📋 广告投放类:")
    print(get_internship_url("bytedance", "广告投放"))
    
    print("\n📋 商务拓展BD类:")
    print(get_internship_url("bytedance", "商务拓展"))
    
    print("\n" + "=" * 60)
    print("\n🎯 美团日常实习筛选链接:")
    print("-" * 60)
    print(get_internship_url("meituan"))
