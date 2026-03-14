# 🎯 校招匹配助手 (Campus Match Bot)

**版本:** 1.1.0  
**作者:** 求职助手团队  
**许可证:** MIT

---

## 🚀 快速开始 (安装方式)

### 方式 1: 一键安装 (推荐)

```bash
# 克隆项目
git clone https://github.com/liuhuayu502/campus-match-bot.git

# 进入目录
cd campus-match-bot

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 方式 2: 手动安装

```bash
# 1. 克隆项目到 OpenClaw skills 目录
git clone https://github.com/liuhuayu502/campus-match-bot.git ~/.openclaw/workspace/skills/campus-match

# 2. 安装依赖
cd ~/.openclaw/workspace/skills/campus-match
pip install -r requirements.txt

# 3. 重启 OpenClaw
openclaw restart
```

### 方式 3: 仅 Python 使用

```bash
# 克隆项目
git clone https://github.com/liuhuayu502/campus-match-bot.git
cd campus-match-bot

# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py --resume my-resume.md --companies bytedance,tencent
```

---

**校招匹配助手** 是一个智能校招岗位匹配工具，可以帮助你：

1. **解析简历** - 从用户上传的简历中提取关键能力
2. **爬取岗位** - 自动进入各大厂校招官网爬取岗位信息
3. **智能匹配** - 根据简历能力与 JD 要求进行匹配度计算
4. **筛选推荐** - 自动过滤低匹配岗位，只推荐高匹配机会
5. **生成报告** - 输出详细的岗位推荐报告（含链接和发布时间）

---

## ✨ 核心功能

### 1️⃣ 简历解析

- 📄 支持 Markdown/PDF/TXT 格式简历
- 🔍 提取关键信息：教育背景、技能、实习经历、项目经验
- 📊 生成能力画像：技术栈、软技能、行业偏好

### 2️⃣ 岗位爬取

- 🏢 支持 10+ 大厂：字节、腾讯、阿里、美团、百度、小红书、快手、B 站、小米、华为
- 🌐 数据源：官方校招官网、社招官网、招聘平台
- 📋 抓取内容：岗位名称、地点、JD、薪资、截止时间、申请链接

### 3️⃣ 智能匹配

- 🧮 多维度匹配算法（5 大维度，12 个子项）
- 📈 匹配度评分（0-100 分）
- 🎯 分级推荐：高匹配 (80%+)、中匹配 (60-79%)、低匹配 (<60%)

### 4️⃣ 智能筛选

- ❌ 自动过滤：低匹配岗位、门槛过高岗位、不符合期望岗位
- ✅ 优先推荐：高匹配岗位、转正机会、日常实习

### 5️⃣ 报告生成

- 📊 详细岗位信息表
- 🔗 一键申请链接
- 📅 发布时间与截止时间
- 💡 申请建议与优化方向

---

## 🚀 快速开始

### 前置要求

- OpenClaw 运行环境
- Python 3.8+
- MiniMax API Key 或 阿里云百炼 API Key

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/campus-match-bot.git
cd campus-match-bot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp config/api.example.json config/api.json
# 编辑 config/api.json，填入你的 API Key

# 4. 填写简历
cp examples/user-resume.example.md my-resume.md
# 编辑 my-resume.md，填入你的真实简历
```

### 使用

```bash
# 方式 1: 命令行运行
python src/main.py --resume my-resume.md --companies bytedance,tencent --output report.md

# 方式 2: OpenClaw 技能调用
/openclaw run campus-match-bot --resume my-resume.md

# 方式 3: 交互式
python src/main.py --interactive
```

---

## 📋 命令接口

### 基本命令

```bash
# 爬取指定公司岗位
爬取 字节跳动 实习岗位

# 分析 JD 匹配度
分析这个 JD 的匹配度：[粘贴 JD 文本]

# 推荐岗位
推荐 北京 运营岗 实习

# 生成完整报告
生成校招匹配报告 --公司 字节，腾讯，阿里 --城市 北京，上海
```

### 高级命令

```bash
# 自定义匹配阈值
生成报告 --min-score 70

# 排除特定岗位类型
生成报告 --exclude 技术，数据

# 定时监控新岗位
监控 字节跳动 --interval 24h --notify
```

---

## 📁 项目结构

```
campus-match-bot/
├── README.md                 # 项目说明
├── SKILL.md                  # OpenClaw 技能定义
├── requirements.txt          # Python 依赖
├── config/
│   ├── api.json             # API 配置
│   └── companies.json       # 公司官网配置
├── src/
│   ├── main.py              # 主入口
│   ├── resume_parser.py     # 简历解析
│   ├── job_crawler.py       # 岗位爬取
│   ├── jd_matcher.py        # 匹配度计算
│   └── report_generator.py  # 报告生成
├── examples/
│   ├── user-resume.example.md  # 简历模板
│   └── sample-report.md     # 报告示例
└── docs/
    ├── API.md               # API 文档
    └── CONFIG.md            # 配置指南
```

---

## 🎯 匹配算法

### 匹配维度

| 维度 | 权重 | 子项 |
|------|------|------|
| **专业技能** | 30% | 技术栈匹配、工具熟练度、语言能力 |
| **项目经历** | 25% | 相关项目、实习经历、成果量化 |
| **教育背景** | 20% | 学校层次、专业匹配、GPA |
| **软技能** | 15% | 沟通、团队协作、领导力 |
| **其他加分项** | 10% | 竞赛、开源、证书、特殊技能 |

### 匹配度分级

| 等级 | 分数 | 建议 |
|------|------|------|
| 🟢 高匹配 | 80-100 | 强烈推荐，优先申请 |
| 🟡 中匹配 | 60-79 | 可以尝试，需优化简历 |
| 🔴 低匹配 | 0-59 | 暂不推荐或作为保底 |

---

## 📊 输出示例

### 报告格式

```markdown
# 校招匹配报告

**生成时间:** 2026-03-14 15:00
**简历:** my-resume.md
**匹配公司:** 字节跳动、腾讯、阿里

---

## 🟢 高匹配岗位 (80%+)

### 1. 字节跳动 - 内容运营实习生
- **匹配度:** 85/100
- **地点:** 北京
- **薪资:** 200-300 元/天
- **发布时间:** 2026-03-10
- **截止时间:** 2026-04-30
- **申请链接:** https://jobs.bytedance.com/...
- **匹配原因:**
  ✅ 有 2 段运营实习经验
  ✅ 熟悉小红书、抖音平台
  ✅ 内容创作能力强
- **申请建议:** 突出内容创作成果，准备作品集

### 2. 腾讯 - 产品运营实习生
- **匹配度:** 82/100
...

---

## 🟡 中匹配岗位 (60-79%)
...
```

---

## 🔧 配置指南

### API 配置

```json
{
  "minimax": {
    "apiKey": "sk-xxx",
    "model": "MiniMax-M2.5"
  },
  "bailian": {
    "apiKey": "xxx",
    "model": "qwen3.5-plus"
  }
}
```

### 公司配置

```json
{
  "bytedance": {
    "name": "字节跳动",
    "campusUrl": "https://jobs.bytedance.com/campus",
    "socialUrl": "https://jobs.bytedance.com",
    "cities": ["北京", "上海", "深圳"]
  }
}
```

---

## 🛠️ 开发指南

### 添加新公司

1. 在 `config/companies.json` 中添加公司配置
2. 在 `src/job_crawler.py` 中实现爬取逻辑
3. 测试爬取功能

### 优化匹配算法

1. 修改 `src/jd_matcher.py` 中的权重配置
2. 添加新的匹配维度
3. 使用测试数据集验证

---

## 📝 更新日志

### v1.0.0 (2026-03-14)

- ✅ 初始版本发布
- ✅ 支持 10+ 大厂校招官网爬取
- ✅ 简历解析与能力提取
- ✅ 智能匹配算法（5 维度）
- ✅ 报告生成与导出

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系方式

- **作者:** 求职助手团队
- **邮箱:** job-hunter@example.com
- **问题反馈:** [GitHub Issues](https://github.com/YOUR_USERNAME/campus-match-bot/issues)

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**
