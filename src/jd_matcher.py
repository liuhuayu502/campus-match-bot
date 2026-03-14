#!/usr/bin/env python3
"""
JD 匹配度计算器 - 增强版
JD Matcher - Enhanced Version

优化内容:
- 更精准的技能匹配算法
- 支持更多匹配维度
- 智能岗位筛选
- 匹配原因详细分析
"""

import re
from typing import Dict, List, Tuple, Set
from datetime import datetime


class JDMatcher:
    """JD 匹配度计算器 - 增强版"""
    
    def __init__(self):
        """初始化"""
        # 权重配置
        self.weights = {
            'skills': 0.25,       # 专业技能 25%
            'experience': 0.25,   # 项目经历 25%
            'education': 0.15,    # 教育背景 15%
            'soft_skills': 0.15, # 软技能 15%
            'location': 0.10,     # 地点偏好 10%
            'extras': 0.10       # 其他加分 10%
        }
        
        # 技能关键词库
        self.skill_library = {
            # 运营类
            '运营': ['内容运营', '用户运营', '产品运营', '活动运营', '新媒体运营', '社群运营', '电商运营', '商家运营'],
            '数据分析': ['SQL', 'Python', 'Excel', 'Tableau', 'PowerBI', 'SPSS', '数据分析', '数据可视化', 'BI'],
            '内容创作': ['文案', '写作', '内容策划', '编辑', '小红书', '抖音', '公众号', '短视频', '直播'],
            '营销': ['市场营销', '品牌营销', '数字营销', '广告投放', 'SEO', 'SEM', '增长黑客'],
            '设计': ['Photoshop', 'PS', 'AI', 'Figma', 'Sketch', 'UI', 'UX', '视觉设计', '平面设计'],
            '产品': ['产品经理', '需求分析', 'PRD', 'Axure', '原型设计', '用户体验', '竞品分析'],
            '技术': ['Java', 'Python', 'Go', 'C++', 'JavaScript', '前端', '后端', '开发', '测试', '算法'],
            '语言': ['英语', 'CET-4', 'CET-6', '托福', '雅思', '日语', '韩语'],
            '办公': ['Office', 'Word', 'Excel', 'PPT', 'PowerPoint'],
        }
        
        # 实习公司层级
        self.company_tiers = {
            'tier1': ['字节', '腾讯', '阿里', '百度', '美团', '京东'],  # 一线大厂
            'tier2': ['快手', '小红书', 'B站', '网易', '滴滴', '拼多多'],  # 头部互联网
            'tier3': ['小米', '华为', 'OPPO', 'vivo', '携程', '斗鱼'],  # 二线大厂
            'tier4': ['其他上市公司', '独角兽'],  # 其他
        }
        
        # 筛选规则
        self.filter_rules = {
            'min_score': 60,
            'exclude_keywords': ['985/211', '硕士及以上', '3 年以上经验', '博士'],
            'prefer_keywords': ['本科', '应届生', '实习', '无经验要求', '大三', '大四'],
        }
    
    def calculate_match(self, job: Dict, profile: Dict) -> Tuple[int, List[str]]:
        """
        计算匹配度
        
        Returns:
            (score, reasons): 匹配分数 (0-100) 和匹配原因列表
        """
        # 先检查是否需要过滤
        if self.should_filter(job, profile):
            return 0, ["❌ 岗位不符合基本要求，已过滤"]
        
        score = 0
        reasons = []
        
        # 1. 专业技能匹配 (25 分)
        skills_score, skills_reasons = self.match_skills(job, profile)
        score += skills_score * self.weights['skills'] * 100
        reasons.extend(skills_reasons)
        
        # 2. 项目/实习经历匹配 (25 分)
        exp_score, exp_reasons = self.match_experience(job, profile)
        score += exp_score * self.weights['experience'] * 100
        reasons.extend(exp_reasons)
        
        # 3. 教育背景匹配 (15 分)
        edu_score, edu_reasons = self.match_education(job, profile)
        score += edu_score * self.weights['education'] * 100
        reasons.extend(edu_reasons)
        
        # 4. 软技能匹配 (15 分)
        soft_score, soft_reasons = self.match_soft_skills(job, profile)
        score += soft_score * self.weights['soft_skills'] * 100
        reasons.extend(soft_reasons)
        
        # 5. 地点匹配 (10 分)
        loc_score, loc_reasons = self.match_location(job, profile)
        score += loc_score * self.weights['location'] * 100
        reasons.extend(loc_reasons)
        
        # 6. 其他加分项 (10 分)
        extras_score, extras_reasons = self.match_extras(job, profile)
        score += extras_score * self.weights['extras'] * 100
        reasons.extend(extras_reasons)
        
        # 总分取整
        final_score = min(int(score), 100)
        
        return final_score, reasons
    
    def should_filter(self, job: Dict, profile: Dict) -> bool:
        """检查是否应该过滤该岗位"""
        job_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        
        # 检查排除关键词
        for keyword in self.filter_rules['exclude_keywords']:
            if keyword in job_text:
                # 但如果是偏好关键词，优先
                if any(p in job_text for p in self.filter_rules['prefer_keywords']):
                    continue
                return True
        
        # 检查地点是否匹配
        job_location = job.get('location', '')
        user_locations = profile.get('location_preference', [])
        
        if job_location and user_locations:
            # 如果用户有偏好地点，检查是否匹配
            if not any(loc in job_location for loc in user_locations):
                # 但如果是远程或未指定，不过滤
                if '远程' not in job_location and '全国' not in job_location:
                    pass  # 暂时不过滤，给用户决定
        
        return False
    
    def match_skills(self, job: Dict, profile: Dict) -> Tuple[float, List[str]]:
        """匹配专业技能"""
        job_skills = self.extract_job_skills(job)
        user_skills = set(profile.get('skills', []))
        
        if not job_skills:
            return 1.0, ["✅ 无明确技能要求"]
        
        # 精确匹配
        exact_matches = [s for s in job_skills if s in user_skills]
        
        # 模糊匹配 (包含关系)
        fuzzy_matches = []
        for job_skill in job_skills:
            if job_skill in exact_matches:
                continue
            for user_skill in user_skills:
                if job_skill in user_skill or user_skill in job_skill:
                    fuzzy_matches.append(job_skill)
                    break
        
        all_matches = exact_matches + fuzzy_matches
        match_rate = len(all_matches) / len(job_skills) if job_skills else 1.0
        
        # 生成原因
        reasons = []
        if match_rate >= 0.7:
            reasons.append(f"✅ 技能匹配度高 ({len(all_matches)}/{len(job_skills)}): {', '.join(all_matches[:3])}")
        elif match_rate >= 0.4:
            reasons.append(f"⚠️  技能部分匹配 ({len(all_matches)}/{len(job_skills)}): {', '.join(all_matches[:2])}")
        else:
            reasons.append(f"❌ 技能匹配度低 ({len(all_matches)}/{len(job_skills)})")
        
        # 缺少的技能
        missing = [s for s in job_skills if s not in all_matches]
        if missing and match_rate < 1.0:
            reasons.append(f"💡 建议补充: {', '.join(missing[:2])}")
        
        return match_rate, reasons
    
    def match_experience(self, job: Dict, profile: Dict) -> Tuple[float, List[str]]:
        """匹配项目/实习经历"""
        internships = profile.get('internships', [])
        projects = profile.get('projects', [])
        
        job_keywords = self.extract_job_keywords(job)
        
        # 检查相关经历
        relevant_internships = []
        relevant_projects = []
        
        for internship in internships:
            title = internship.get('title', '')
            company = internship.get('company', '')
            desc = ' '.join(internship.get('description', []) + internship.get('achievements', []))
            
            if any(kw in title or kw in company or kw in desc for kw in job_keywords):
                relevant_internships.append(internship)
        
        for project in projects:
            title = project.get('title', '')
            desc = ' '.join(project.get('description', []) + project.get('achievements', []))
            
            if any(kw in title or kw in desc for kw in job_keywords):
                relevant_projects.append(project)
        
        # 计算得分
        base_score = 0.0
        
        # 实习数量加分
        if len(internships) >= 3:
            base_score += 0.3
        elif len(internships) >= 2:
            base_score += 0.2
        elif len(internships) >= 1:
            base_score += 0.1
        
        # 相关经历加分
        if len(relevant_internships) >= 2:
            base_score += 0.4
        elif len(relevant_internships) >= 1:
            base_score += 0.3
        elif len(relevant_projects) >= 2:
            base_score += 0.3
        elif len(relevant_projects) >= 1:
            base_score += 0.2
        
        # 公司层级加分 (大厂经历)
        for internship in internships:
            company = internship.get('company', '')
            for tier, companies in self.company_tiers.items():
                if any(c in company for c in companies):
                    base_score += 0.1
                    break
        
        # 量化成果加分
        for item in internships + projects:
            achievements = item.get('achievements', [])
            if any(re.search(r'\d+%', a) or re.search(r'\d+[万+]', a) for a in achievements):
                base_score += 0.05
                break
        
        score = min(base_score, 1.0)
        
        # 生成原因
        reasons = []
        if score >= 0.7:
            reasons.append(f"✅ 相关经历丰富: {len(relevant_internships)}段实习 + {len(relevant_projects)}个项目")
        elif score >= 0.4:
            reasons.append(f"⚠️  有一定相关经历: {len(relevant_internships)}段实习")
        else:
            reasons.append(f"❌ 相关经历不足")
        
        if not internships:
            reasons.append("💡 建议补充实习经历")
        
        return score, reasons
    
    def match_education(self, job: Dict, profile: Dict) -> Tuple[float, List[str]]:
        """匹配教育背景"""
        edu = profile.get('education', {})
        user_degree = edu.get('degree', '')
        user_school = edu.get('school', '')
        
        requirements = job.get('requirements', [])
        req_text = ' '.join(requirements) + ' ' + job.get('description', '')
        
        # 检查学历要求
        score = 0.5  # 基础分
        
        if '博士' in req_text:
            if user_degree == '博士':
                score = 1.0
                reasons = ["✅ 学历符合博士要求"]
            else:
                score = 0.2
                reasons = ["❌ 学历要求博士，暂不符合"]
        elif '硕士' in req_text:
            if user_degree in ['博士', '硕士']:
                score = 1.0
                reasons = ["✅ 学历符合硕士要求"]
            elif user_degree == '本科':
                score = 0.6
                reasons = ["⚠️ 学历要求硕士，本科可尝试"]
            else:
                score = 0.3
                reasons = ["❌ 学历要求硕士，暂不符合"]
        elif '本科' in req_text or '大专' in req_text:
            score = 1.0
            reasons = ["✅ 学历符合要求 (本科/大专)"]
        else:
            score = 1.0
            reasons = ["✅ 无明确学历要求"]
        
        # 学校加分
        if user_school:
            top_schools = ['清华', '北大', '复旦', '上交', '浙大', '南大', '中科大', '哈工大', '北航', '北邮']
            if any(s in user_school for s in top_schools):
                score = min(score + 0.1, 1.0)
                reasons.append("✅ 来自顶尖高校")
            elif '985' in user_school or '211' in user_school:
                score = min(score + 0.05, 1.0)
        
        return score, reasons
    
    def match_soft_skills(self, job: Dict, profile: Dict) -> Tuple[float, List[str]]:
        """匹配软技能"""
        soft_keywords = ['沟通', '团队协作', '团队合作', '领导', '管理', '抗压', '学习能力', '适应能力', '创新', '责任心', '积极主动']
        
        job_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        profile_text = ' '.join(profile.get('skills', []))
        
        job_soft_skills = [kw for kw in soft_keywords if kw in job_text]
        user_soft_skills = [kw for kw in soft_keywords if kw in profile_text]
        
        if not job_soft_skills:
            return 1.0, ["✅ 无明确软技能要求"]
        
        matched = sum(1 for kw in job_soft_skills if kw in user_soft_skills)
        score = matched / len(job_soft_skills) if job_soft_skills else 1.0
        
        if score >= 0.7:
            reasons = ["✅ 软技能匹配: " + ', '.join(user_soft_skills[:3])]
        elif score >= 0.4:
            reasons = ["⚠️  部分软技能匹配: " + ', '.join([kw for kw in job_soft_skills if kw in user_soft_skills][:2])]
        else:
            reasons = ["⚠️  软技能待提升"]
        
        return score, reasons
    
    def match_location(self, job: Dict, profile: Dict) -> Tuple[float, List[str]]:
        """匹配地点"""
        job_location = job.get('location', '')
        user_locations = profile.get('location_preference', [])
        
        if not job_location or not user_locations:
            return 1.0, ["✅ 地点无限制"]
        
        # 检查是否匹配
        if any(loc in job_location for loc in user_locations):
            return 1.0, [f"✅ 工作地点符合: {job_location}"]
        
        # 检查是否是远程
        if '远程' in job_location or '线上' in job_location:
            return 0.8, [f"⚠️ 远程岗位，可尝试"]
        
        # 检查是否是一线城市
        first_tier = ['北京', '上海', '深圳', '广州', '杭州', '新一线']
        if any(loc in job_location for loc in first_tier):
            return 0.5, [f"⚠️ 地点不符合 (期望: {', '.join(user_locations)}, 岗位: {job_location})"]
        
        return 0.3, [f"❌ 地点不符合"]
    
    def match_extras(self, job: Dict, profile: Dict) -> float:
        """匹配其他加分项"""
        score = 0
        
        # 奖项加分
        awards = profile.get('awards', [])
        if len(awards) >= 3:
            score += 0.4
        elif len(awards) >= 1:
            score += 0.2
        
        # 项目数量加分
        projects = profile.get('projects', [])
        if len(projects) >= 3:
            score += 0.3
        elif len(projects) >= 1:
            score += 0.1
        
        # 技能多样性加分
        skills = profile.get('skills', [])
        if len(skills) >= 10:
            score += 0.2
        elif len(skills) >= 5:
            score += 0.1
        
        # 实习公司知名度加分
        internships = profile.get('internships', [])
        for internship in internships:
            company = internship.get('company', '')
            for tier, companies in self.company_tiers.items():
                if any(c in company for c in companies):
                    score += 0.1
                    break
        
        return min(score, 1.0)
    
    def extract_job_skills(self, job: Dict) -> List[str]:
        """从 JD 中提取技能要求"""
        skills = []
        req_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        
        # 从技能库中匹配
        for category, keyword_list in self.skill_library.items():
            for keyword in keyword_list:
                if keyword in req_text:
                    skills.append(keyword)
        
        return list(set(skills))
    
    def extract_job_keywords(self, job: Dict) -> List[str]:
        """从 JD 中提取关键词"""
        keywords = []
        req_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        
        # 岗位相关关键词
        position_keywords = [
            '运营', '产品', '市场', '设计', '数据', '技术', '开发', '测试',
            '内容', '用户', '活动', '商家', '社群', '电商', '品牌',
            '策划', '文案', '编辑', '分析', '增长', '推广'
        ]
        
        for kw in position_keywords:
            if kw in req_text:
                keywords.append(kw)
        
        return keywords
    
    def generate_suggestions(self, job: Dict, profile: Dict, score: int) -> List[str]:
        """生成申请建议"""
        suggestions = []
        
        if score >= 80:
            suggestions.append("✅ 匹配度高，建议优先申请")
            suggestions.append("💡 突出与岗位最相关的经历")
        elif score >= 60:
            suggestions.append("⚠️  匹配度中等，可以尝试")
            suggestions.append("💡 优化简历，强调相关技能")
            suggestions.append("💡 准备作品集或项目案例")
        else:
            suggestions.append("❌ 匹配度较低，建议谨慎申请")
            suggestions.append("💡 补充相关技能或经历")
            suggestions.append("💡 考虑其他更匹配的岗位")
        
        # 针对岗位的具体建议
        job_title = job.get('position', '')
        if '运营' in job_title:
            suggestions.append("📝 建议准备运营案例展示")
        if '产品' in job_title:
            suggestions.append("📝 建议准备产品分析报告")
        if '数据' in job_title:
            suggestions.append("📝 建议准备数据分析作品")
        
        return suggestions


# 测试代码
if __name__ == "__main__":
    # 创建匹配器
    matcher = JDMatcher()
    
    # 测试数据
    test_job = {
        "position": "内容运营实习生",
        "location": "北京",
        "requirements": ["本科及以上", "熟悉社交媒体", "有运营经验优先", "每周4天"],
        "description": "负责小红书、抖音内容运营，数据分析，活动策划"
    }
    
    test_profile = {
        "skills": ["内容运营", "小红书", "抖音", "文案", "数据分析", "Excel", "沟通"],
        "internships": [{"title": "内容运营实习", "company": "字节跳动", "description": ["负责内容发布"], "achievements": ["粉丝增长30%"]}],
        "projects": [{"title": "自媒体运营", "description": ["运营个人公众号"], "achievements": ["阅读量10万+"]}],
        "education": {"school": "北京大学", "degree": "本科"},
        "awards": ["奖学金"],
        "location_preference": ["北京", "上海"]
    }
    
    # 计算匹配度
    score, reasons = matcher.calculate_match(test_job, test_profile)
    
    print("=" * 60)
    print("📊 匹配度分析报告")
    print("=" * 60)
    print(f"岗位：{test_job['position']}")
    print(f"地点：{test_job['location']}")
    print(f"匹配度：{score}/100")
    print()
    print("📋 匹配原因:")
    for reason in reasons:
        print(f"  {reason}")
    print("=" * 60)
