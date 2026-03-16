# SKILL.md - Campus Match Bot

## 简介

校招匹配助手 - 智能校招岗位推荐工具，从官网获取真实岗位数据，匹配你的简历。

## 功能

- 📄 智能简历解析（支持 Markdown/PDF/TXT）
- 🔍 从字节跳动官网获取真实日常实习岗位
- 🎯 多维度匹配（技能、经历、学历）
- 📝 生成详细匹配报告（含申请链接）

## 使用方法

### 基本命令

```bash
# 爬取字节跳动运营类日常实习
/openclaw run campus-match-bot --resume <简历路径> --companies bytedance --category 运营

# 指定城市
/openclaw run campus-match-bot --resume my-resume.md --companies bytedance --category 产品经理 --city 上海
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--resume, -r` | 简历文件路径 | `my-resume.md` |
| `--companies, -c` | 目标公司 | `bytedance` |
| `--category, -cat` | 职位类别 | `运营`、`产品经理`、`数据分析`、`商业产品`、`营销策划`、`广告投放`、`商务拓展` |
| `--city` | 工作城市 | `北京`、`上海`、`深圳` |
| `--min-score, -m` | 最低匹配分 | `60` |
| `--output, -o` | 输出报告路径 | `report.md` |

## 职位类别

- `运营` - 内容运营、用户运营、活动运营等
- `产品经理` - 产品经理实习生
- `数据分析` - 数据分析、商业分析等
- `商业产品` - 商业产品（广告）实习生
- `营销策划` - 市场营销、策划等
- `广告投放` - 广告投放实习生
- `商务拓展` - BD、商务合作实习生

## 简历格式

推荐 Markdown 格式，包含：
- 基本信息（姓名、联系方式）
- 教育背景
- 技能列表
- 实习经历
- 项目经验

## 示例

```
/openclaw run campus-match-bot --resume ~/Desktop/简历.md --companies bytedance --category 运营
```

## 注意事项

1. 目前仅支持字节跳动日常实习的真实数据
2. 其他公司使用模拟数据
3. 简历建议使用 Markdown 格式以获得最佳解析效果
