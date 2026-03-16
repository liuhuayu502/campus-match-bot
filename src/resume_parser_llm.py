#!/usr/bin/env python3
"""
简历解析器 - LLM增强版
Resume Parser - LLM Enhanced Version

功能:
- 使用LLM解析简历（推荐）
- 提取关键信息：教育背景、实习经历、技能、项目经验
- 支持Markdown和PDF格式

使用方式:
  1. 直接调用: ResumeParserLLM().parse_with_llm(resume_text)
  2. 在OpenClaw中: 使用内置LLM能力解析
"""

import re
import json
from typing import Dict, Optional


class ResumeParserLLM:
    """LLM简历解析器"""
    
    def __init__(self):
        pass
    
    def create_prompt(self, resume_text: str) -> str:
        """创建LLM解析提示词"""
        prompt = f"""请解析以下简历，提取关键信息并以JSON格式输出。

要求输出格式（必须是合法的JSON）:
{{
    "name": "姓名",
    "phone": "手机号",
    "email": "邮箱",
    "education": {{
        "school": "学校名称",
        "major": "专业",
        "degree": "学历(本科/硕士/博士)",
        "graduation_year": "毕业年份",
        "gpa": "GPA(可选)",
        "awards": ["奖项1", "奖项2"]
    }},
    "skills": {{
        "tools": ["工具技能1", "工具技能2"],
        "languages": ["语言能力1", "语言能力2"],
        "other": ["其他技能"]
    }},
    "internships": [
        {{
            "company": "公司名称",
            "position": "岗位名称",
            "duration": "时间(如2024.6-2024.9)",
            "location": "地点",
            "highlights": ["工作亮点1", "工作亮点2"]
        }}
    ],
    "projects": [
        {{
            "name": "项目名称",
            "role": "角色/职责",
            "description": "项目描述",
            "achievements": ["成果/成就"]
        }}
    ],
    "awards": ["奖项列表"],
    "other_highlights": ["其他亮点"]
}}

简历内容:
{resume_text}

请直接输出JSON，不要其他内容。"""
        return prompt
    
    def parse_with_llm(self, resume_text: str, llm_func=None) -> Dict:
        """
        使用LLM解析简历
        
        Args:
            resume_text: 简历文本内容
            llm_func: LLM调用函数(可选)
        
        Returns:
            解析后的简历信息字典
        """
        prompt = self.create_prompt(resume_text)
        
        # 如果没有提供LLM函数，返回提示让用户在OpenClaw中调用LLM
        if llm_func is None:
            return {
                "raw_text": resume_text,
                "needs_llm": True,
                "prompt": prompt
            }
        
        # 调用LLM
        try:
            result = llm_func(prompt)
            return json.loads(result)
        except json.JSONDecodeError:
            # 尝试提取JSON
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"raw_text": resume_text, "error": "解析失败"}
    
    def parse_markdown(self, md_text: str) -> Dict:
        """解析Markdown格式简历（备用方法）"""
        lines = md_text.strip().split('\n')
        
        profile = {
            "name": "",
            "phone": "",
            "email": "",
            "education": {},
            "skills": {"tools": [], "languages": [], "other": []},
            "internships": [],
            "projects": [],
            "awards": [],
            "other_highlights": []
        }
        
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测章节标题
            if line.startswith('#'):
                current_section = line.strip('#').strip()
                continue
            
            # 解析各部分
            if current_section == "技能工具" or current_section == "技能":
                profile["skills"]["tools"].extend([s.strip() for s in line.split(',') if s.strip()])
            
            elif current_section == "语言能力":
                profile["skills"]["languages"].extend([s.strip() for s in line.split(',') if s.strip()])
            
            elif "实习" in current_section:
                if line.startswith('###'):
                    profile["internships"].append({
                        "company": line.strip('#').strip(),
                        "position": "",
                        "duration": "",
                        "highlights": []
                    })
                elif profile["internships"] and line.startswith('-'):
                    profile["internships"][-1]["highlights"].append(line.strip('- '))
            
            elif "项目" in current_section:
                if line.startswith('###'):
                    profile["projects"].append({
                        "name": line.strip('#').strip(),
                        "achievements": []
                    })
                elif profile["projects"] and line.startswith('-'):
                    profile["projects"][-1]["achievements"].append(line.strip('- '))
        
        return profile


def format_resume_for_matching(profile: Dict) -> str:
    """将解析后的简历格式化为匹配用的文本"""
    text_parts = []
    
    if profile.get("name"):
        text_parts.append(f"姓名: {profile['name']}")
    
    # 教育背景
    edu = profile.get("education", {})
    if edu.get("school"):
        text_parts.append(f"学校: {edu['school']} {edu.get('major', '')} {edu.get('degree', '')}")
    
    # 技能
    skills = profile.get("skills", {})
    all_skills = []
    all_skills.extend(skills.get("tools", []))
    all_skills.extend(skills.get("languages", []))
    all_skills.extend(skills.get("other", []))
    if all_skills:
        text_parts.append(f"技能: {', '.join(all_skills)}")
    
    # 实习
    for intern in profile.get("internships", []):
        text_parts.append(f"实习: {intern.get('company', '')} {intern.get('position', '')}")
        for h in intern.get("highlights", [])[:2]:
            text_parts.append(f"  - {h[:50]}")
    
    # 项目
    for proj in profile.get("projects", []):
        text_parts.append(f"项目: {proj.get('name', '')}")
        for a in proj.get("achievements", [])[:2]:
            text_parts.append(f"  - {a[:50]}")
    
    return "\n".join(text_parts)


# 测试
if __name__ == "__main__":
    # 测试Markdown解析
    test_resume = """# 刘华宇
    
## 技能工具
- MS Office、Keynote、FCPX、AIGC Tools、SQL

## 实习经历

### 联想中国
- Campaign策划
- Social/PR支持
"""
    
    parser = ResumeParserLLM()
    result = parser.parse_markdown(test_resume)
    print(json.dumps(result, ensure_ascii=False, indent=2))
