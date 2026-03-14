#!/bin/bash
# 📦 校招匹配助手 - 一键安装脚本

echo "🎯 正在安装校招匹配助手..."

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ 请先安装 OpenClaw: brew install openclaw"
    exit 1
fi

# 创建 skills 目录
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
mkdir -p "$SKILLS_DIR"

# 克隆或更新项目
if [ -d "$SKILLS_DIR/campus-match" ]; then
    echo "📂 更新已有安装..."
    cd "$SKILLS_DIR/campus-match"
    git pull origin main
else
    echo "📥 克隆项目..."
    git clone https://github.com/liuhuayu502/campus-match-bot.git "$SKILLS_DIR/campus-match"
fi

# 检查 skills
echo "🔍 检查 skill 状态..."
openclaw skills check

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用方式:"
echo "  1. 重启 OpenClaw"
echo "  2. 说：'爬取字节跳动实习岗位'"
echo "  3. 或者：'推荐北京运营岗'"
echo ""
echo "📄 文档: https://github.com/liuhuayu502/campus-match-bot"
