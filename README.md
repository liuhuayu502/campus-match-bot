# 🎯 校招匹配助手 (Campus Match Bot)

智能校招岗位推荐工具，从官网获取真实岗位数据，匹配你的简历。

[English](./README_EN.md)

## ✨ 功能特点

- 📄 **智能简历解析** - 支持 Markdown/PDF/TXT 格式，可选 LLM 增强解析
- 🔍 **真实官网数据** - 从字节跳动等大厂校招官网获取真实岗位
- 🎯 **日常实习筛选** - 专门筛选日常实习岗位
- 📊 **多维度匹配** - 基于技能、经历、学历等计算匹配度
- 🔗 **岗位带链接** - 每个推荐岗位附带官方申请链接
- 📝 **详细报告** - 生成 Markdown 格式匹配报告

## 🏢 支持公司

| 公司 | 状态 | 官网 |
|------|------|------|
| 字节跳动 | ✅ 日常实习 | [jobs.bytedance.com](https://jobs.bytedance.com/campus/position) |
| 腾讯 | 🔜 即将支持 | - |
| 阿里 | 🔜 即将支持 | - |
| 美团 | 🔜 即将支持 | - |

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/liuhuayu502/campus-match-bot.git
cd campus-match-bot

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用方法

### 命令行

```bash
# 基本用法
python src/main.py --resume my-resume.md --companies bytedance

# 指定职位类别
python src/main.py --resume my-resume.md --companies bytedance --category 运营

# 指定城市和最低匹配分
python src/main.py -r resume.md -c bytedance --category 产品经理 --city 上海 --min-score 70
```

### 职位类别

| 参数值 | 说明 |
|--------|------|
| `运营` | 运营类日常实习 |
| `产品经理` | 产品经理日常实习 |
| `数据分析` | 数据分析日常实习 |
| `商业产品` | 商业产品(广告)日常实习 |
| `营销策划` | 市场营销日常实习 |
| `广告投放` | 广告投放日常实习 |
| `商务拓展` | BD商务拓展日常实习 |

### 输出示例

```
🎯 校招匹配助手 v2.0
============================================================

📄 正在解析简历：my-resume.md
✅ 简历解析完成
   姓名：张三
   学校：XX大学
   技能：5 项
   实习：2 段

🔍 正在爬取岗位信息...
   目标公司：bytedance
   职位类别：运营

[bytedance] 爬取中...
   ✅ 找到 10 个岗位

✅ 爬取完成，共 10 个岗位

🧮 正在计算匹配度...
✅ 匹配完成
   🟢 高匹配 (80+): 3 个
   🟡 中匹配 (60-79): 5 个
   🔴 已过滤：2 个

📄 正在生成报告...
✅ 报告已保存：campus-match-report-20240317.md

============================================================
✅ 全部完成！
```

## 📝 简历格式

推荐使用 Markdown 格式简历：

```markdown
# 姓名

## 教育背景
- XX大学 XX专业 本科 2020-2024

## 技能
- Python, SQL, Excel

## 实习经历
### 公司名称
- 负责内容...
```

## 🔧 进阶

### OpenClaw Skill

将此项目添加为 OpenClaw skill：

```bash
/openclaw add-skill campus-match-bot --path /path/to/campus-match-bot
```

### LLM 增强解析

如需更精准的简历解析，可以使用 LLM：

```python
from resume_parser_llm import ResumeParserLLM

parser = ResumeParserLLM()
# 在支持LLM的环境中调用
profile = parser.parse_with_llm(resume_text, llm_func=your_llm_function)
```

## 📄 报告示例

生成的报告包含：
- 匹配度统计
- 高/中匹配岗位列表（含申请链接）
- 简历优化建议
- 申请时间建议

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
