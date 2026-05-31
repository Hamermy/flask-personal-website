# app.py
import json
import os
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

# 创建 Flask 应用（这里用回了标准的 app 命名，方便后续扩展）
app = Flask(__name__)

# ==================== 配置区域（在这里修改你的个人信息） ====================
CONFIG = {
    # ---------- 基本信息（已同步你的修改） ----------
    "name": "小樱同学",  # 替换成你的名字/昵称
    "school": "北京体育大学",  # 你的学校
    "major": "运动康复",  # 你的专业
    "motto": "用温暖的双手，帮助每一位需要康复的人 ✨",
    "avatar": "/static/preview.jpg",
    # ---------- 社交链接（🌟 记得改成你自己的真实链接！） ----------
    "github_url": "https://github.com/你的用户名",  # ← 改成你的 GitHub 主页
    "bilibili_url": "https://space.bilibili.com/你的UID",  # ← 改成你的 B站主页
    "email": "your@email.com",  # ← 改成你的邮箱
    "wechat_id": "your_wechat_id",  # ← 改成你的微信号

    # ---------- 留言板背景图 ----------
    # 方式1: 使用本地图片（把图片放到 static/images/ 目录下）
    "message_bg": "/static/images/bg_message.jpg",
    # 方式2: 使用网络图片（直接填URL，比如动漫壁纸链接）
    # "message_bg": "https://example.com/your-anime-wallpaper.jpg",

    # ---------- 爱好标签（已同步你的修改） ----------
    "hobbies": ["二次元", "编程", "运动康复研究", "追番"],

    # ---------- 技能树（已同步你的修改） ----------
    "skills": [
        {"name": "运动康复", "level": 40},
        {"name": "心理学", "level": 30},
        {"name": "统计学", "level": 20},
        {"name": "Python编程", "level": 10},
        {"name": "投资技能", "level": 10},
    ],

    # ---------- 成长时间线（已同步你的修改） ----------
    "timeline": [
        {"year": "2025", "event": "🎓 进入大学，开启康复之路"},
        {"year": "2026", "event": "📚 逐步了解心理学与统计学"},
        {"year": "2026", "event": "🏥 开始学习投资啦"},
        {"year": "2026", "event": "💻 开始学python"},
    ]
}

# ==================== 留言板数据存储 ====================
MESSAGE_FILE = "messages.json"


def load_messages():
    """从 JSON 文件读取所有留言"""
    if not os.path.exists(MESSAGE_FILE):
        return []
    with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_message(name, content, avatar_color):
    """保存一条新留言到 JSON 文件"""
    messages = load_messages()
    new_message = {
        "id": len(messages) + 1,
        "name": name,
        "content": content,
        "avatar_color": avatar_color,  # 随机头像颜色
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "likes": 0
    }
    messages.insert(0, new_message)  # 新留言插到最前面
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    return new_message


def like_message(message_id):
    """给留言点赞"""
    messages = load_messages()
    for msg in messages:
        if msg["id"] == message_id:
            msg["likes"] = msg.get("likes", 0) + 1
            break
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


# ==================== 路由 ====================

@app.route("/")
def home():
    """首页 - 显示所有内容和留言"""
    messages = load_messages()
    # 模拟一个基础访客数（你可以后续改成真实的计数）
    visitor_count = len(messages) + 1024
    return render_template(
        "index1.html",  # 注意这里对应你的 index1.html
        info=CONFIG,
        messages=messages,
        visitor_count=visitor_count
    )


@app.route("/post_message", methods=["POST"])
def post_message():
    """处理留言提交"""
    name = request.form.get("name", "").strip()
    content = request.form.get("content", "").strip()

    # 简单的输入验证
    if not name or not content:
        return redirect(url_for("home"))

    # 限制长度，防止恶意输入
    name = name[:20]  # 名字最多20字
    content = content[:500]  # 内容最多500字

    # 随机生成一个柔和的头像背景色
    colors = ["#ff85a2", "#b388eb", "#7ec8e3", "#ffb347", "#87ceeb", "#dda0dd", "#98fb98"]
    avatar_color = random.choice(colors)

    save_message(name, content, avatar_color)
    return redirect(url_for("home"))


@app.route("/like/<int:message_id>", methods=["POST"])
def like(message_id):
    """点赞接口（前端 AJAX 调用）"""
    like_message(message_id)
    return jsonify({"status": "ok"})


# ==================== 启动 ====================
if __name__ == "__main__":
    # 确保图片目录存在
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

    print("=" * 50)
    print("🌸 网站已启动！")
    print("📌 打开浏览器访问: http://localhost:5000")
    print("📌 留言板背景图请放到: static/images/bg_message.jpg")
    print("=" * 50)

    # debug=True 表示修改代码后自动重启，方便开发
    app.run(debug=True, port=5000)