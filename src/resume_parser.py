#!/usr/bin/env python3
"""
简历解析器 - 增强版
Resume Parser - Enhanced Version

优化内容:
- 更精准的信息提取
- 支持更多简历格式
- 自动识别技能标签
- 生成完整能力画像
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


class ResumeParser:
    """简历解析器 - 增强版"""
    
    def __init__(self):
        """初始化"""
        # 技能库
        self.skill_library = {
            # 编程语言
            "Python": ["Python", "python", "PyTorch", "TensorFlow", "Django", "Flask"],
            "Java": ["Java", "java", "Spring", "SpringBoot", "Maven"],
            "JavaScript": ["JavaScript", "JS", "Node.js", "Vue", "React", "React Native"],
            "C++": ["C++", "c++", "C语言"],
            "Go": ["Go", "golang"],
            "SQL": ["SQL", "MySQL", "PostgreSQL", "Oracle", "Redis"],
            
            # 数据分析
            "数据分析": ["数据分析", "数据分析工具", "数据挖掘", "BI"],
            "Excel": ["Excel", "excel", "VLOOKUP", "数据透视表"],
            "SPSS": ["SPSS", "spss"],
            "Tableau": ["Tableau", "tableau"],
            
            # 设计工具
            "Photoshop": ["Photoshop", "PS", "Adobe Photoshop"],
            "Figma": ["Figma", "figma", "Sketch", "Axure", "XD"],
            "视频剪辑": ["Pr", "Premiere", "剪映", "Final Cut", "AE", "After Effects"],
            
            # 运营工具
            "运营": ["内容运营", "用户运营", "产品运营", "活动运营", "新媒体运营", "社群运营", "电商运营"],
            "社交媒体": ["小红书", "抖音", "快手", "B站", "公众号", "微博", "知乎", "豆瓣"],
            
            # 产品工具
            "产品经理": ["产品经理", "PRD", "Axure", "原型设计", "需求分析", "竞品分析"],
            
            # 办公软件
            "Office": ["Office", "Word", "PowerPoint", "PPT", "Excel"],
            
            # 语言能力
            "英语": ["英语", "CET-4", "CET-6", "托福", "雅思", "TOEFL", "IELTS"],
            "日语": ["日语", "N1", "N2", "JLPT"],
        }
        
        # 教育背景关键词
        self.edu_keywords = {
            "degree": ["博士", "硕士", "本科", "大专", "高中", "中专"],
            "grade": ["大一", "大二", "大三", "大四", "研一", "研二", "研三"],
            "honor": ["奖学金", "一等奖", "二等奖", "三等奖", "优秀", "三好学生", "保研"],
        }
        
        # 实习公司识别
        self.company_patterns = [
            r'([^\s]+公司)', r'([^\s]+科技)', r'([^\s]+互联网)', 
            r'([^\s]+网络)', r'([^\s]+信息)', r'([^\s]+软件)'
        ]
        
        # 时间表达式
        self.time_patterns = [
            r'(\d{4})\.(\d{1,2})?-(\d{4})\.(\d{1,2})?',  # 2023.9-2024.6
            r'(\d{4})/(\d{1,2})?-(\d{4})/(\d{1,2})?',    # 2023/9-2024/6
            r'(\d{4})年(\d{1,2})?-(\d{4})年(\d{1,2})?', # 2023年9月-2024年6月
            r'(\d{4})\.(\d{1,2})',  # 2023.9
        ]
    
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
            "name": "",
            "gender": "",
            "age": "",
            "contact": {
                "email": "",
                "phone": "",
                "wechat": "",
                "location": ""
            },
            "education": {
                "school": "",
                "major": "",
                "degree": "",
                "gpa": "",
                "ranking": "",
                "graduation": "",
                "courses": []
            },
            "skills": [],
            "skill_tags": {},  # 按类别分组的技能
            "internships": [],
            "projects": [],
            "awards": [],
            "certificates": [],
            "languages": [],
            "self_assessment": "",
            "summary": "",
            "target": {
                "positions": [],
                "cities": [],
                "salary": ""
            }
        }
        
        # 提取各项信息
        profile["name"] = self.extract_name(content)
        profile["contact"] = self.extract_contact(content)
        profile["education"] = self.extract_education(content)
        profile["skills"], profile["skill_tags"] = self.extract_skills(content)
        profile["internships"] = self.extract_experiences(content, "internship")
        profile["projects"] = self.extract_experiences(content, "project")
        profile["awards"] = self.extract_awards(content)
        profile["certificates"] = self.extract_certificates(content)
        profile["languages"] = self.extract_languages(content)
        profile["self_assessment"] = self.extract_self_assessment(content)
        profile["target"] = self.extract_target(content)
        
        # 生成摘要
        profile["summary"] = self.generate_summary(profile)
        
        return profile
    
    def extract_name(self, content: str) -> str:
        """提取姓名"""
        # 方式1: # 姓名
        patterns = [
            r'^#\s*(.+?)(?:\s*简历)?\s*$',
            r'姓名[：:]\s*([^\n]+)',
            r'名字[：:]\s*([^\n]+)',
            r'^([^\n]+?)\s*(?:男|女|199|200|\d{4})',  # 姓名后跟性别或年份
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                name = match.group(1).strip()
                # 过滤掉常见非姓名词汇
                if name and len(name) <= 10 and not any(kw in name for kw in ["简历", "个人", "求职", "应聘"]):
                    return name
        
        return ""
    
    def extract_contact(self, content: str) -> Dict:
        """提取联系方式"""
        contact = {"email": "", "phone": "", "wechat": "", "location": ""}
        
        # 邮箱
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        email_match = re.search(email_pattern, content)
        if email_match:
            contact["email"] = email_match.group(1)
        
        # 电话
        phone_pattern = r'(1[3-9]\d{9})'
        phone_match = re.search(phone_pattern, content)
        if phone_match:
            contact["phone"] = phone_match.group(1)
        
        # 微信
        wechat_patterns = [
            r'微信[：:]\s*([^\n\s]+)',
            r'WeChat[：:]\s*([^\n\s]+)',
        ]
        for pattern in wechat_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                contact["wechat"] = match.group(1).strip()
                break
        
        # 所在地
        location_patterns = [
            r'所在地[：:]\s*([^\n]+)',
            r'现居[地:]\s*([^\n]+)',
            r'居住地[：:]\s*([^\n]+)',
            r'(北京|上海|深圳|广州|杭州|成都|武汉|南京|西安|苏州|天津)\s*(?:市|人)?',
        ]
        for pattern in location_patterns:
            match = re.search(pattern, content)
            if match:
                contact["location"] = match.group(1).strip()
                break
        
        return contact
    
    def extract_education(self, content: str) -> Dict:
        """提取教育背景"""
        edu = {
            "school": "",
            "major": "",
            "degree": "",
            "gpa": "",
            "ranking": "",
            "graduation": "",
            "courses": []
        }
        
        # 学校
        school_patterns = [
            r'(?:学校|院校|毕业院校)[：:]\s*([^\n]+)',
            r'([^\s]+?(?:大学|学院|学校))[^\n]*',
        ]
        for pattern in school_patterns:
            match = re.search(pattern, content)
            if match:
                school = match.group(1).strip()
                # 过滤常见非学校词汇
                if school and not any(kw in school for kw in ["简历", "个人", "求职"]):
                    edu["school"] = school
                    break
        
        # 专业
        major_patterns = [
            r'(?:专业|所学专业)[：:]\s*([^\n]+)',
            r'([^\n]+?(?:专业|系))[^\n]*',
        ]
        for pattern in major_patterns:
            match = re.search(pattern, content)
            if match:
                major = match.group(1).strip()
                # 过滤学校名称
                if major and "大学" not in major and "学院" not in major:
                    edu["major"] = major
                    break
        
        # 学历
        for degree in ["博士", "硕士", "本科", "大专", "高中", "中专"]:
            if degree in content:
                edu["degree"] = degree
                break
        
        # GPA
        gpa_patterns = [
            r'GPA[:\s]*(\d+\.?\d*)/?(\d+\.?\d*)',
            r'绩点[:\s]*(\d+\.?\d*)/?(\d+\.?\d*)',
        ]
        for pattern in gpa_patterns:
            match = re.search(pattern, content)
            if match:
                if match.group(2):
                    edu["gpa"] = f"{match.group(1)}/{match.group(2)}"
                else:
                    edu["gpa"] = match.group(1)
                break
        
        # 排名
        ranking_patterns = [
            r'排名[:\s]*(\d+)/?(\d+)',
            r'(?:前|top)[:\s]*(\d+)%',
        ]
        for pattern in ranking_patterns:
            match = re.search(pattern, content)
            if match:
                if match.group(2):
                    edu["ranking"] = f"{match.group(1)}/{match.group(2)}"
                else:
                    edu["ranking"] = f"前{match.group(1)}%"
                break
        
        # 毕业时间
        year_patterns = [
            r'(?:毕业时间|预计毕业)[:\s]*(\d{4})年?(\d{1,2})?月?',
            r'(\d{4})\.(\d{1,2})?(?:\s*[-~]\s*)?(?:\d{4})?\.?(\d{1,2})?',
        ]
        for pattern in year_patterns:
            match = re.search(pattern, content)
            if match:
                year = match.group(1)
                month = match.group(2) if match.group(2) else "06"
                edu["graduation"] = f"{year}.{month}"
                break
        
        return edu
    
    def extract_skills(self, content: str) -> tuple:
        """提取技能"""
        skills = []
        skill_tags = {}
        
        # 从技能库匹配
        for category, keywords in self.skill_library.items():
            matched = []
            for keyword in keywords:
                if keyword in content:
                    # 避免重复匹配
                    if keyword not in skills:
                        matched.append(keyword)
            
            if matched:
                skills.extend(matched)
                skill_tags[category] = matched
        
        # 去重
        skills = list(set(skills))
        
        return skills, skill_tags
    
    def extract_experiences(self, content: str, exp_type: str) -> List[Dict]:
        """提取经历 (实习/项目)"""
        experiences = []
        
        # 查找经历章节
        if exp_type == "internship":
            keywords = ["实习", "工作经历", "实践经验"]
        else:
            keywords = ["项目", "项目经历", "课题"]
        
        for keyword in keywords:
            # 查找章节
            pattern = rf'#+\s*.*{keyword}.*'
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            
            for match in matches:
                start = match.end()
                
                # 找到下一个章节
                next_match = re.search(r'\n#+\s', content[start:])
                if next_match:
                    end = start + next_match.start()
                else:
                    end = len(content)
                
                section = content[start:end].strip()
                
                # 解析每段经历
                # 按行分割，识别每个经历块
                lines = section.split('\n')
                current_exp = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查是否是新的经历块 (有公司名或项目名)
                    is_new_exp = False
                    
                    # 公司/项目名模式
                    if exp_type == "internship":
                        company_patterns = [
                            r'([^\s]+公司)',
                            r'([^\s]+科技)',
                            r'([^\s]+互联网)',
                        ]
                        for p in company_patterns:
                            if re.search(p, line) and ("有限公司" in line or "科技" in line or "互联网" in line or "字节" in line or "腾讯" in line or "阿里" in line):
                                is_new_exp = True
                                break
                    else:
                        if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                            if len(line) > 5:
                                is_new_exp = True
                    
                    if is_new_exp:
                        # 保存上一个经历
                        if current_exp and (current_exp.get("title") or current_exp.get("company")):
                            experiences.append(current_exp)
                        
                        # 新建经历
                        current_exp = {
                            "title": "",
                            "company": "",
                            "duration": "",
                            "description": [],
                            "achievements": []
                        }
                        
                        # 提取公司/项目名
                        if exp_type == "internship":
                            for p in [r'([^\s]+公司)', r'([^\s]+科技)']:
                                m = re.search(p, line)
                                if m:
                                    current_exp["company"] = m.group(1)
                                    break
                        else:
                            current_exp["title"] = line.lstrip('-*•').strip()
                        
                        # 提取时间
                        for tp in self.time_patterns:
                            m = re.search(tp, line)
                            if m:
                                current_exp["duration"] = m.group(0)
                                break
                    
                    elif current_exp is not None:
                        # 添加描述
                        line = line.lstrip('-*•').strip()
                        if line:
                            # 检查是否是成果 (包含数字)
                            if re.search(r'\d+%', line) or re.search(r'\d+[万+]', line) or re.search(r'\d+x', line):
                                current_exp["achievements"].append(line)
                            else:
                                current_exp["description"].append(line)
                
                # 保存最后一个经历
                if current_exp and (current_exp.get("title") or current_exp.get("company")):
                    experiences.append(current_exp)
        
        return experiences
    
    def extract_awards(self, content: str) -> List[Dict]:
        """提取奖项"""
        awards = []
        
        # 查找奖项章节
        keywords = ["奖项", "荣誉", "奖学金", "竞赛"]
        
        for keyword in keywords:
            pattern = rf'#+\s*.*{keyword}.*'
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            
            for match in matches:
                start = match.end()
                next_match = re.search(r'\n#+\s', content[start:])
                end = start + next_match.start() if next_match else len(content)
                
                section = content[start:end].strip()
                
                # 解析奖项
                for line in section.split('\n'):
                    line = line.strip().lstrip('-*•')
                    if line and len(line) > 2:
                        # 提取时间
                        year_match = re.search(r'(\d{4})', line)
                        year = year_match.group(1) if year_match else ""
                        
                        awards.append({
                            "name": line,
                            "year": year
                        })
        
        return awards
    
    def extract_certificates(self, content: str) -> List[str]:
        """提取证书"""
        certificates = []
        
        cert_keywords = ["证书", "资质", "认证"]
        
        for keyword in cert_keywords:
            pattern = rf'#+\s*.*{keyword}.*'
            match = re.search(pattern, content, re.MULTILINE)
            
            if match:
                start = match.end()
                next_match = re.search(r'\n#+\s', content[start:])
                end = start + next_match.start() if next_match else len(content)
                
                section = content[start:end].strip()
                
                for line in section.split('\n'):
                    line = line.strip().lstrip('-*•')
                    if line and len(line) > 2:
                        certificates.append(line)
        
        return certificates
    
    def extract_languages(self, content: str) -> List[Dict]:
        """提取语言能力"""
        languages = []
        
        # 英语
        english_patterns = [
            r'英语[:\s]*(CET-4|CET-6|四级|六级|雅思|托福|TOEFL|IELTS)',
            r'(CET-4|CET-6|四级|六级)[:\s]*(\d+)',
        ]
        
        for pattern in english_patterns:
            match = re.search(pattern, content)
            if match:
                languages.append({
                    "language": "英语",
                    "level": match.group(1),
                    "score": match.group(2) if match.group(2) else ""
                })
        
        # 日语
        japanese_patterns = [
            r'日语[:\s]*(N1|N2|N3|N4|N5|JLPT)',
        ]
        
        for pattern in japanese_patterns:
            match = re.search(pattern, content)
            if match:
                languages.append({
                    "language": "日语",
                    "level": match.group(1),
                    "score": ""
                })
        
        return languages
    
    def extract_self_assessment(self, content: str) -> str:
        """提取自我评价"""
        keywords = ["自我评价", "个人评价", "自我介绍", "关于我"]
        
        for keyword in keywords:
            pattern = rf'#+\s*.*{keyword}.*'
            match = re.search(pattern, content, re.MULTILINE)
            
            if match:
                start = match.end()
                next_match = re.search(r'\n#+\s', content[start:])
                end = start + next_match.start() if next_match else min(start + 500, len(content))
                
                assessment = content[start:end].strip()
                return assessment[:500]  # 限制长度
        
        return ""
    
    def extract_target(self, content: str) -> Dict:
        """提取求职意向"""
        target = {
            "positions": [],
            "cities": [],
            "salary": ""
        }
        
        keywords = ["求职意向", "期望岗位", "目标岗位"]
        
        for keyword in keywords:
            pattern = rf'#+\s*.*{keyword}.*'
            match = re.search(pattern, content, re.MULTILINE)
            
            if match:
                start = match.end()
                next_match = re.search(r'\n#+\s', content[start:])
                end = start + next_match.start() if next_match else min(start + 300, len(content))
                
                section = content[start:end]
                
                # 提取岗位
                position_keywords = ["运营", "产品", "市场", "设计", "技术", "开发", "测试", "HR", "人力"]
                for kw in position_keywords:
                    if kw in section:
                        target["positions"].append(kw)
                
                # 提取城市
                city_keywords = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "南京", "西安"]
                for city in city_keywords:
                    if city in section:
                        target["cities"].append(city)
                
                # 提取薪资
                salary_match = re.search(r'(\d+)[-到](\d+)[k千]/[月年]?', section)
                if salary_match:
                    target["salary"] = f"{salary_match.group(1)}-{salary_match.group(2)}k/月"
        
        return target
    
    def generate_summary(self, profile: Dict) -> str:
        """生成能力摘要"""
        summary_parts = []
        
        # 基本信息
        if profile["name"]:
            summary_parts.append(f"{profile['name']}")
        
        # 教育背景
        edu = profile["education"]
        if edu["school"] or edu["major"]:
            edu_str = f"{edu.get('degree', '')}{edu.get('major', '')}{edu.get('school', '')}"
            summary_parts.append(edu_str.strip())
        
        # 技能数量
        if profile["skills"]:
            summary_parts.append(f"掌握 {len(profile['skills'])} 项技能")
        
        # 经历数量
        if profile["internships"]:
            summary_parts.append(f"{len(profile['internships'])} 段实习经历")
        
        if profile["projects"]:
            summary_parts.append(f"{len(profile['projects'])} 个项目经历")
        
        # 奖项数量
        if profile["awards"]:
            summary_parts.append(f"{len(profile['awards'])} 项奖项")
        
        return '，'.join(summary_parts)


# 测试代码
if __name__ == "__main__":
    parser = ResumeParser()
    
    # 测试简历内容
    test_resume = """
# 张三的简历

## 基本信息
- 姓名：张三
- 邮箱：zhangsan@example.com
- 电话：13812345678
- 所在地：北京

## 教育背景
- 学校：北京大学
- 专业：市场营销
- 学历：本科
- GPA：3.8/4.0
- 毕业时间：2025.06

## 技能清单
- Python、SQL、数据分析
- Excel、PowerPoint
- 内容运营、用户运营
- 小红书、抖音、公众号
- 英语CET-6

## 实习经历

### 字节跳动 | 内容运营实习生 | 2024.6-2024.9
- 负责小红书账号运营，3个月粉丝从0增长到5000+
- 策划3场线上活动，参与人数1w+
- 撰写20+篇推文，平均阅读量3000+

### 腾讯 | 产品运营实习生 | 2024.3-2024.6
- 负责用户增长活动，数据分析
- 优化产品功能，提升DAU 15%

## 项目经历

### 自媒体账号运营 | 2023.9-2024.3
- 运营个人公众号，粉丝1万+
- 单篇最高阅读量10万+

## 奖项
- 一等奖学金 (2023)
- 三好学生 (2022)

## 求职意向
- 岗位：内容运营、用户运营
- 城市：北京、上海
- 薪资：8k-15k/月
"""
    
    # 解析
    profile = parser.parse_content(test_resume)
    
    print("=" * 60)
    print("📋 简历解析结果")
    print("=" * 60)
    print(f"姓名: {profile['name']}")
    print(f"学校: {profile['education']['school']}")
    print(f"专业: {profile['education']['major']}")
    print(f"学历: {profile['education']['degree']}")
    print(f"GPA: {profile['education']['gpa']}")
    print(f"\n技能: {', '.join(profile['skills'])}")
    print(f"\n实习: {len(profile['internships'])} 段")
    for exp in profile['internships']:
        print(f"  - {exp.get('company', '')} {exp.get('title', '')}")
    print(f"\n项目: {len(profile['projects'])} 个")
    print(f"\n奖项: {len(profile['awards'])} 项")
    print(f"\n📝 摘要: {profile['summary']}")
    print("=" * 60)
