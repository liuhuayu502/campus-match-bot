#!/usr/bin/env python3
"""
简历解析器
Resume Parser

功能:
  - 解析 Markdown 格式简历
  - 提取关键信息：基本信息、教育背景、技能、实习经历、项目经历
  - 生成用户能力画像
"""

import re
from pathlib import Path
from typing import Dict, List, Optional


class ResumeParser:
    """简历解析器"""
    
    def __init__(self):
        """初始化"""
        self.sections = {
            'basic': r'(?:基本信|个|姓|名|邮|电|学|专).*?(?=\n\n|\n#|\Z)',
            'education': r'(?:教育背|学|校).*?(?=\n\n|\n#|\Z)',
            'skills': r'(?:技|掌|熟).*?(?=\n\n|\n#|\Z)',
            'internships': r'(?:实习|工作|经).*?(?=\n\n|\n#|\Z)',
            'projects': r'(?:项目|课).*?(?=\n\n|\n#|\Z)',
            'awards': r'(?:奖项|荣|竞).*?(?=\n\n|\n#|\Z)'
        }
    
    def parse(self, resume_path: str) -> Optional[Dict]:
        """解析简历文件"""
        try:
            with open(resume_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ 文件未找到：{resume_path}")
            return None
        except Exception as e:
            print(f"❌ 读取失败：{e}")
            return None
        
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Dict:
        """解析简历内容"""
        profile = {
            'name': '',
            'contact': {
                'email': '',
                'phone': '',
                'location': ''
            },
            'education': {
                'school': '',
                'major': '',
                'degree': '',
                'gpa': '',
                'graduation': ''
            },
            'skills': [],
            'internships': [],
            'projects': [],
            'awards': [],
            'summary': ''
        }
        
        # 提取姓名
        name_patterns = [
            r'(?:姓名 | 名字 | 姓\s*名)[:：\s]*([^\n]+)',
            r'^#\s*(.+?)(?:\s*的)?(?:简历)?\s*$',
            r'^([^\n]+?)\s*\n[-=]+'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                profile['name'] = match.group(1).strip()
                break
        
        # 提取邮箱
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        email_match = re.search(email_pattern, content)
        if email_match:
            profile['contact']['email'] = email_match.group(1)
        
        # 提取电话
        phone_pattern = r'(1[3-9]\d{9})'
        phone_match = re.search(phone_pattern, content)
        if phone_match:
            profile['contact']['phone'] = phone_match.group(1)
        
        # 提取学校
        school_patterns = [
            r'(?:学校 | 院校 | 毕业)[:：\s]*([^\n]+)',
            r'([^\n]+?(?:大学 | 学院|学校))[^\n]*'
        ]
        for pattern in school_patterns:
            match = re.search(pattern, content)
            if match:
                profile['education']['school'] = match.group(1).strip()
                break
        
        # 提取专业
        major_patterns = [
            r'(?:专业 | 系)[:：\s]*([^\n]+)',
            r'([^\n]+?(?:专业 | 方向))[^\n]*'
        ]
        for pattern in major_patterns:
            match = re.search(pattern, content)
            if match:
                profile['education']['major'] = match.group(1).strip()
                break
        
        # 提取学历
        degree_keywords = ['博士', '硕士', '本科', '大专', '高中']
        for degree in degree_keywords:
            if degree in content:
                profile['education']['degree'] = degree
                break
        
        # 提取技能
        skills = self.extract_skills(content)
        profile['skills'] = skills
        
        # 提取实习经历
        internships = self.extract_sections(content, ['实习', '工作', '经历'])
        profile['internships'] = internships
        
        # 提取项目经历
        projects = self.extract_sections(content, ['项目', '课题', '设计'])
        profile['projects'] = projects
        
        # 提取奖项
        awards = self.extract_sections(content, ['奖项', '荣誉', '竞赛', '奖学金'])
        profile['awards'] = awards
        
        # 生成摘要
        profile['summary'] = self.generate_summary(profile)
        
        return profile
    
    def extract_skills(self, content: str) -> List[str]:
        """提取技能列表"""
        skills = []
        
        # 常见技能关键词
        skill_keywords = [
            # 办公软件
            'Office', 'Word', 'Excel', 'PowerPoint', 'PPT',
            # 设计工具
            'Photoshop', 'PS', 'Illustrator', 'AI', 'Figma', 'Sketch', 'Canva',
            # 数据分析
            'Python', 'SQL', 'R', 'SPSS', 'Tableau', 'Excel',
            # 编程语言
            'Java', 'C++', 'JavaScript', 'Go', 'C', 'HTML', 'CSS',
            # 运营相关
            '内容运营', '用户运营', '产品运营', '活动运营', '新媒体运营',
            '社交媒体', '小红书', '抖音', '公众号', '微博',
            # 软技能
            '沟通', '团队协作', '领导力', '抗压', '学习', '创新'
        ]
        
        for skill in skill_keywords:
            if skill in content:
                skills.append(skill)
        
        return list(set(skills))  # 去重
    
    def extract_sections(self, content: str, keywords: List[str]) -> List[Dict]:
        """提取经历章节"""
        sections = []
        
        for keyword in keywords:
            # 查找章节标题
            pattern = rf'(?:^|\n)#+\s*.*?{keyword}.*?(?=\n)'
            matches = re.finditer(pattern, content, re.MULTILINE)
            
            for match in matches:
                start = match.end()
                # 找到下一个章节标题
                next_section = re.search(r'\n#+\s', content[start:])
                if next_section:
                    end = start + next_section.start()
                else:
                    end = len(content)
                
                section_content = content[start:end].strip()
                
                # 解析经历详情
                experience = self.parse_experience(section_content)
                if experience:
                    sections.append(experience)
        
        return sections
    
    def parse_experience(self, content: str) -> Optional[Dict]:
        """解析单段经历"""
        experience = {
            'title': '',
            'company': '',
            'duration': '',
            'description': [],
            'achievements': []
        }
        
        # 提取标题/公司
        lines = content.split('\n')
        for line in lines[:3]:
            line = line.strip()
            if not line:
                continue
            
            # 公司名
            if any(kw in line for kw in ['公司', '企业', '组织', '|', '｜']):
                parts = re.split(r'[|｜]', line)
                if len(parts) >= 2:
                    experience['company'] = parts[0].strip()
                    experience['title'] = parts[1].strip()
                else:
                    experience['company'] = line
            else:
                experience['title'] = line
            
            # 时间
            time_pattern = r'(\d{4}[\.-]\d{2}|\d{4} 年 [\.-]?\d{2}?[月年]?)'
            time_match = re.search(time_pattern, line)
            if time_match:
                experience['duration'] = time_match.group(1)
        
        # 提取描述和成就
        for line in lines[3:]:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 成就通常包含数字
            if re.search(r'\d+%', line) or re.search(r'\d+[万 +]', line):
                experience['achievements'].append(line)
            else:
                experience['description'].append(line)
        
        return experience if experience['title'] or experience['company'] else None
    
    def generate_summary(self, profile: Dict) -> str:
        """生成能力摘要"""
        summary_parts = []
        
        # 基本信息
        if profile['name']:
            summary_parts.append(f"{profile['name']}")
        
        # 教育背景
        edu = profile['education']
        if edu['school'] or edu['major']:
            edu_str = f"{edu.get('degree', '')}{edu.get('major', '')}{edu.get('school', '')}"
            summary_parts.append(edu_str.strip())
        
        # 技能数量
        if profile['skills']:
            summary_parts.append(f"掌握 {len(profile['skills'])} 项技能")
        
        # 经历数量
        if profile['internships']:
            summary_parts.append(f"{len(profile['internships'])} 段实习经历")
        
        if profile['projects']:
            summary_parts.append(f"{len(profile['projects'])} 个项目经历")
        
        return '，'.join(summary_parts)
