# SKILL.md - Campus Match Bot

## 简介

校招匹配助手 - 智能校招岗位推荐工具

**核心流程：**
1. 📄 用户上传简历
2. 🤖 LLM解析能力画像
3. 🔍 Browser抓取官网实时岗位
4. 🎯 匹配计算（含语言过滤）
5. 📋 输出推荐报告（含JD和链接）

## 使用方法

```bash
# 匹配字节跳动运营岗
/openclaw run campus-match-bot --resume ~/简历.md --companies bytedance --category 运营

# 匹配美团+指定城市
/openclaw run campus-match-bot -r 简历.md -c bytedance --category 运营 --city 上海
```

### 参数

| 参数 | 说明 |
|------|------|
| `--resume` | 简历路径 |
| `--companies` | 目标公司 |
| `--category` | 职位类别 |
| `--city` | 工作城市 |
| `--min-score` | 最低匹配分 |

## 核心功能

1. **Browser抓取** - 每次从校招官网实时抓取岗位
2. **语言过滤** - 自动检测小语种要求，标记风险
3. **实时JD** - 输出完整岗位描述和链接

## 报告输出

- 候选人画像
- 推荐岗位（含JD和链接）
- 匹配分数
- 风险提示
- 申请建议
