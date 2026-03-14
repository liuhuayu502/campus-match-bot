#!/usr/bin/env python3
"""
JD 匹配度计算器
JD Matcher

功能:
  - 计算简历与 JD 的匹配度
  - 多维度评分 (专业技能、项目经历、教育背景、软技能、其他)
  - 生成匹配原因和建议
"""

import re
from typing import Dict, List, Tuple


class JDMatcher:
    """JD 匹配度计算器"""
    
    def __init__(self):
        """初始化"""
        self.weights = {
            'skills': 0.30,      # 专业技能 30%
            'experience': 0.25,  # 项目经历 25%
            'education': 0.20,   # 教育背景 20%
            'soft_skills': 0.15, # 软技能 15%
            'extras': 0.10       # 其他加分 10%
        }
    
    def calculate_match(self, job: Dict, profile: Dict) -> Tuple[int, List[str]]:
        """
        计算匹配度
        
        Returns:
            (score, reasons): 匹配分数 (0-100) 和匹配原因列表
        """
        score = 0
        reasons = []
        
        # 1. 专业技能匹配 (30 分)
        skills_score = self.match_skills(job, profile)
        score += skills_score * self.weights['skills'] * 100
        
        if skills_score >= 0.7:
            reasons.append(f"✅ 专业技能匹配度高 ({int(skills_score*100)}%)")
        elif skills_score >= 0.4:
            reasons.append(f"⚠️  专业技能部分匹配 ({int(skills_score*100)}%)")
        else:
            reasons.append(f"❌ 专业技能匹配度低 ({int(skills_score*100)}%)")
        
        # 2. 项目/实习经历匹配 (25 分)
        experience_score = self.match_experience(job, profile)
        score += experience_score * self.weights['experience'] * 100
        
        if experience_score >= 0.7:
            reasons.append(f"✅ 相关经历丰富 ({int(experience_score*100)}%)")
        elif experience_score >= 0.4:
            reasons.append(f"⚠️  有一定相关经历 ({int(experience_score*100)}%)")
        else:
            reasons.append(f"❌ 相关经历不足 ({int(experience_score*100)}%)")
        
        # 3. 教育背景匹配 (20 分)
        education_score = self.match_education(job, profile)
        score += education_score * self.weights['education'] * 100
        
        if education_score >= 0.8:
            reasons.append(f"✅ 教育背景符合要求")
        elif education_score >= 0.5:
            reasons.append(f"⚠️  教育背景基本符合")
        else:
            reasons.append(f"❌ 教育背景有差距")
        
        # 4. 软技能匹配 (15 分)
        soft_score = self.match_soft_skills(job, profile)
        score += soft_score * self.weights['soft_skills'] * 100
        
        if soft_score >= 0.7:
            reasons.append(f"✅ 软技能匹配")
        else:
            reasons.append(f"⚠️  软技能待提升")
        
        # 5. 其他加分项 (10 分)
        extras_score = self.match_extras(job, profile)
        score += extras_score * self.weights['extras'] * 100
        
        if extras_score > 0:
            reasons.append(f"✅ 有额外加分项")
        
        # 总分取整
        final_score = min(int(score), 100)
        
        return final_score, reasons
    
    def match_skills(self, job: Dict, profile: Dict) -> float:
        """匹配专业技能"""
        job_skills = self.extract_job_skills(job)
        user_skills = set(profile.get('skills', []))
        
        if not job_skills:
            return 1.0  # JD 没有明确要求，默认匹配
        
        matched = sum(1 for skill in job_skills if any(skill in s or s in skill for s in user_skills))
        return matched / len(job_skills) if job_skills else 1.0
    
    def match_experience(self, job: Dict, profile: Dict) -> float:
        """匹配项目/实习经历"""
        internships = profile.get('internships', [])
        projects = profile.get('projects', [])
        
        # 检查是否有相关经历
        has_relevant = False
        job_keywords = self.extract_job_keywords(job)
        
        for internship in internships:
            title = internship.get('title', '')
            company = internship.get('company', '')
            desc = ' '.join(internship.get('description', []))
            
            if any(kw in title or kw in company or kw in desc for kw in job_keywords):
                has_relevant = True
                break
        
        for project in projects:
            title = project.get('title', '')
            desc = ' '.join(project.get('description', []))
            
            if any(kw in title or kw in desc for kw in job_keywords):
                has_relevant = True
                break
        
        # 评分
        if len(internships) >= 2 and has_relevant:
            return 1.0
        elif len(internships) >= 1 and has_relevant:
            return 0.7
        elif has_relevant:
            return 0.5
        elif len(internships) >= 1:
            return 0.3
        else:
            return 0.1
    
    def match_education(self, job: Dict, profile: Dict) -> float:
        """匹配教育背景"""
        edu = profile.get('education', {})
        user_degree = edu.get('degree', '')
        user_school = edu.get('school', '')
        
        requirements = job.get('requirements', [])
        req_text = ' '.join(requirements) + ' ' + job.get('description', '')
        
        # 检查学历要求
        if '博士' in req_text:
            if user_degree == '博士':
                degree_score = 1.0
            else:
                degree_score = 0.3
        elif '硕士' in req_text:
            if user_degree in ['博士', '硕士']:
                degree_score = 1.0
            else:
                degree_score = 0.5
        elif '本科' in req_text or '大专' in req_text:
            degree_score = 1.0
        else:
            degree_score = 1.0  # 无明确要求
        
        # 检查学校要求 (简化版)
        school_score = 1.0
        if '985' in req_text or '211' in req_text:
            # 简化处理，假设用户符合
            school_score = 0.8
        
        return (degree_score * 0.7 + school_score * 0.3)
    
    def match_soft_skills(self, job: Dict, profile: Dict) -> float:
        """匹配软技能"""
        soft_keywords = ['沟通', '团队协作', '领导', '抗压', '学习', '创新', '责任']
        
        job_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        profile_text = ' '.join(profile.get('skills', []))
        
        job_soft_skills = [kw for kw in soft_keywords if kw in job_text]
        user_soft_skills = [kw for kw in soft_keywords if kw in profile_text]
        
        if not job_soft_skills:
            return 1.0
        
        matched = sum(1 for kw in job_soft_skills if kw in user_soft_skills)
        return matched / len(job_soft_skills) if job_soft_skills else 1.0
    
    def match_extras(self, job: Dict, profile: Dict) -> float:
        """匹配其他加分项"""
        score = 0
        
        # 奖项加分
        if profile.get('awards'):
            score += 0.3
        
        # 项目数量加分
        if len(profile.get('projects', [])) >= 3:
            score += 0.3
        
        # 技能多样性加分
        if len(profile.get('skills', [])) >= 10:
            score += 0.2
        
        # 实习公司知名度加分 (简化)
        internships = profile.get('internships', [])
        if any('大厂' in i.get('company', '') or len(i.get('company', '')) > 4 for i in internships):
            score += 0.2
        
        return min(score, 1.0)
    
    def extract_job_skills(self, job: Dict) -> List[str]:
        """从 JD 中提取技能要求"""
        skills = []
        req_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        
        skill_keywords = [
            'Office', 'Excel', 'PPT', 'Word',
            'Python', 'SQL', '数据分析',
            'Photoshop', '设计',
            '运营', '策划', '文案',
            '沟通', '团队协作'
        ]
        
        for skill in skill_keywords:
            if skill in req_text:
                skills.append(skill)
        
        return skills
    
    def extract_job_keywords(self, job: Dict) -> List[str]:
        """从 JD 中提取关键词"""
        keywords = []
        req_text = ' '.join(job.get('requirements', [])) + ' ' + job.get('description', '')
        
        # 岗位相关关键词
        position_keywords = ['运营', '产品', '市场', '设计', '数据', '技术', '开发', '测试']
        
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
        
        return suggestions
