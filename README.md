# 🎯 校招匹配助手 (Campus Match Bot)

智能校招岗位推荐工具，从官网获取真实岗位数据，匹配你的简历。

[English](./README_EN.md)

## ✨ 核心功能

1. **📄 简历解析** - 支持 Markdown/PDF/TXT，使用 LLM 提取能力画像
2. **🔍 官网抓取** - 从校招官网获取真实岗位信息
3. **🎯 智能匹配** - 根据用户画像与岗位 JD 计算匹配度
4. **📋 详细报告** - 输出推荐岗位，包含 JD 和申请链接

## 📦 安装

```bash
git clone https://github.com/liuhuayu502/campus-match-bot.git
cd campus-match-bot
pip install -r requirements.txt
```

## 🚀 使用方法

```bash
# 基本用法
python src/main.py --resume my-resume.md --companies bytedance --category 运营

# 指定城市和最低匹配分
python src/main.py -r resume.md -c bytedance --category 产品经理 --city 上海 --min-score 70

# 多公司同时匹配
python src/main.py --resume resume.md --companies bytedance,meituan --category 运营
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--resume, -r` | 简历文件路径 | `my-resume.md` |
| `--companies, -c` | 目标公司 | `bytedance`, `meituan` |
| `--category, -cat` | 职位类别 | `运营`, `产品经理`, `数据分析` |
| `--city` | 工作城市 | `上海`, `北京` |
| `--min-score, -m` | 最低匹配分 | `60` |
| `--output, -o` | 输出报告路径 | `report.md` |

### 职位类别

| 类别 | 说明 |
|------|------|
| `运营` | 内容运营、用户运营、活动运营 |
| `产品经理` | 产品经理、产品运营 |
| `数据分析` | 数据分析、商业分析 |
| `商业产品` | 商业产品（广告） |
| `营销策划` | 市场营销、品牌策划 |
| `广告投放` | 广告投放、增长投放 |
| `商务拓展` | BD、商务合作 |

## 📋 完整工作流程

```
用户上传简历
     ↓
LLM 解析 → 能力画像
     ↓     (教育背景/技能/实习/项目)
     ↓
校招官网抓取岗位
     ↓     (字节跳动/腾讯/美团/百度)
     ↓
匹配计算 → 匹配分数
     ↓     (技能匹配/经历匹配/学历匹配)
     ↓
输出推荐报告
     ↓
包含: 岗位名称/JD/链接/匹配分
```

## 📝 简历格式

推荐 Markdown 格式：

```markdown
# 姓名

## 教育背景
- XX大学 XX专业 本科 2022-2026
- GPA: 3.5/4.0

## 技能
- 工具: Python, SQL, Excel
- 语言: 英语CET-6

## 实习经历
### 公司名称
- 负责内容...
```

## 🏢 支持公司

| 公司 | 状态 | 官网 |
|------|------|------|
| 字节跳动 | ✅ 真实数据 | jobs.bytedance.com |
| 腾讯 | 🔜 开发中 | join.qq.com |
| 美团 | 🔜 开发中 | campus.meituan.com |
| 百度 | 🔜 开发中 | talent.baidu.com |

## 📄 报告示例

生成的报告包含：

```markdown
# 校招岗位推荐报告

## 候选人画像
- 姓名：XXX
- 学历：XX大学 XX专业
- 技能：运营、数据分析、SQL
- 实习：X段

## 推荐岗位

### 1. 字节跳动 - UGC策略运营实习生
- 匹配度：85/100
- 地点：上海
- 链接：[申请链接](https://...)
- JD：负责UGC运营业务...
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
