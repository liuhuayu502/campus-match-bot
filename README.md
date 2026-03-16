# 🚀 校招匹配助手 - FluxA 付费版 v3.0

## 💰 赚钱模式

**每次使用收费：$1.00 USDC** 🎉

这个版本集成了 **FluxA 付费 API**，用户每次使用付费 $1，你获得营收！

| 功能 | 成本 | 定价 |
|------|------|------|
| 基础岗位查询 | $0 (本地数据) | - |
| AI 简历解析 | $0 (Qwen 免费) | - |
| AI JD 分析 | $0 (Qwen 免费) | - |
| 高级岗位爬取 | $0.01 (Google Jobs) | - |

**收费：$1.00 USDC/次** 💰

## 📦 文件结构

```
fluxa-api-integration/
├── fluxa_api.py           # FluxA API 客户端
├── job_crawler_fluxa.py   # 集成 API 的爬虫
├── main_fluxa.py          # 主程序 (付费版)
├── README.md              # 本文件
└── config/                # 配置文件
```

## 🔧 配置步骤

### 1. 在 FluxA Monetize 注册 MCP Server

```bash
# 1. 访问 https://monetize.fluxapay.xyz/studio/servers
# 2. 点击 "Add Server"
# 3. 选择 "MCP Server"
# 4. 填写信息:
#    - Name: campus-match-api
#    - Endpoint: 你的服务器 URL
#    - Tools: google_jobs, crawl_website, qwen_chat
# 5. 设置每个工具的价格
```

### 2. 配置 API Key

```bash
# 在环境变量中设置
export FLUXA_API_KEY="your_api_key_here"
```

### 3. 发布技能

```bash
# 访问 https://monetize.fluxapay.xyz/studio/skills
# 创建新技能，选择刚才的 MCP Server
# 设置价格: $0.05/次
```

## 🧪 测试

```bash
# 测试 API 客户端
python fluxa_api.py

# 测试爬虫
python job_crawler_fluxa.py

# 运行完整流程
python main_fluxa.py --resume my-resume.md --companies bytedance --category 运营 --price 0.05
```

## 💡 优化建议

1. **增加更多 API**：集成 LinkedIn Jobs、BOSS直聘等
2. **添加增值服务**：简历优化、面试辅导
3. **设置套餐**：基础版/高级版
4. **推广**：在龙虾派等平台分享，吸引用户

## 📝 更新日志

- v3.0 (2026-03-17): 集成 FluxA 付费 API，支持 x402 自动支付，定价 $1/次
- v2.0: 支持真实官网数据
- v1.0: 基础版本
