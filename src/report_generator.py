#!/usr/bin/env python3
"""
报告生成器
Report Generator

功能:
  - 生成 Markdown 格式的校招匹配报告
  - 包含岗位详情、匹配度、申请链接
  - 支持导出为 PDF (可选)
"""

from datetime import datetime
from typing import Dict, List
from pathlib import Path


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        """初始化"""
        self.template = self.load_template()
    
    def load_template(self) -> str:
        """加载报告模板"""
        return """# 🎯 校招匹配报告

**生成时间:** {timestamp}
**简历:** {resume}
**匹配公司:** {companies}
**最低匹配分:** {min_score}

---

## 📊 汇总统计

| 等级 | 数量 | 说明 |
|------|------|------|
| 🟢 高匹配 | {high_count} | 80 分 +，强烈推荐 |
| 🟡 中匹配 | {mid_count} | 60-79 分，可以尝试 |
| 🔴 已过滤 | {filtered_count} | <60 分，暂不推荐 |

---

## 🟢 高匹配岗位 (80%+)

{high_match_jobs}

---

## 🟡 中匹配岗位 (60-79%)

{mid_match_jobs}

---

## 💡 申请建议

{ suggestions}

---

**报告生成工具:** 校招匹配助手 v{version}
"""
    
    def generate(self, matched_jobs: List[Dict], profile: Dict, 
                 output_path: str, format: str = "markdown") -> str:
        """生成报告"""
        # 分类岗位
        high_match = [j for j in matched_jobs if j['match_score'] >= 80]
        mid_match = [j for j in matched_jobs if 60 <= j['match_score'] < 80]
        filtered_count = len(matched_jobs) - len(high_match) - len(mid_match)
        
        # 生成岗位列表
        high_match_text = self.format_jobs(high_match) if high_match else "暂无高匹配岗位"
        mid_match_text = self.format_jobs(mid_match) if mid_match else "暂无中匹配岗位"
        
        # 生成建议
        suggestions = self.generate_suggestions(profile, high_match, mid_match)
        
        # 填充模板
        report = self.template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            resume=profile.get('name', '未填写') + '的简历',
            companies=', '.join(set(j['company'] for j in matched_jobs)),
            min_score=60,
            high_count=len(high_match),
            mid_count=len(mid_match),
            filtered_count=filtered_count,
            high_match_jobs=high_match_text,
            mid_match_jobs=mid_match_text,
            suggestions='\n'.join(suggestions),
            version='1.0.0'
        )
        
        # 保存报告
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(output_file)
    
    def format_jobs(self, jobs: List[Dict]) -> str:
        """格式化岗位列表"""
        formatted = []
        
        for i, job in enumerate(jobs, 1):
            job_text = f"""### {i}. {job['company']} - {job['position']}

- **匹配度:** {job['match_score']}/100
- **地点:** {job.get('location', '未指定')}
- **薪资:** {job.get('salary', '面议')}
- **类型:** {job.get('type', '未指定')}
- **发布时间:** {job.get('publish_date', '未指定')}
- **截止时间:** {job.get('deadline', '未指定')}
- **申请链接:** [{job.get('apply_url', '点击申请')}]({job.get('apply_url', '#')})
- **匹配原因:**
{self.format_reasons(job.get('match_reasons', []))}
- **申请建议:** {job.get('suggestion', '尽早申请，突出相关经历')}
"""
            formatted.append(job_text)
        
        return '\n'.join(formatted)
    
    def format_reasons(self, reasons: List[str]) -> str:
        """格式化匹配原因"""
        if not reasons:
            return "  暂无详细原因"
        
        return '\n'.join(f"  {reason}" for reason in reasons)
    
    def generate_suggestions(self, profile: Dict, high_match: List[Dict], 
                            mid_match: List[Dict]) -> List[str]:
        """生成申请建议"""
        suggestions = []
        
        # 总体建议
        if len(high_match) >= 5:
            suggestions.append("✅ 你的简历匹配度很高，建议优先申请高匹配岗位")
        elif len(high_match) >= 1:
            suggestions.append("✅ 有部分高匹配岗位，建议重点准备这些岗位的申请")
        else:
            suggestions.append("⚠️  高匹配岗位较少，建议优化简历或扩大申请范围")
        
        # 简历优化建议
        if not profile.get('internships'):
            suggestions.append("💡 建议补充实习经历，提升竞争力")
        
        if len(profile.get('skills', [])) < 5:
            suggestions.append("💡 建议补充技能描述，突出与岗位相关的技能")
        
        if not profile.get('projects'):
            suggestions.append("💡 建议补充项目经历，展示实际能力")
        
        # 申请策略建议
        suggestions.append("💡 建议按匹配度从高到低依次申请")
        suggestions.append("💡 每个岗位定制简历，突出相关经历")
        suggestions.append("💡 尽早申请，避免错过截止时间")
        
        return suggestions
    
    def export_pdf(self, markdown_path: str, pdf_path: str = None):
        """导出为 PDF (可选功能)"""
        # 需要安装 markdown 转 PDF 工具
        # 如：mdpdf, pandoc 等
        pass
