# Discord AuthBot

一个功能完整的 Discord 身份验证机器人，支持外部API认证、双语界面、权限管理和持久化存储。

## ✨ 主要功能

### 🔐 身份认证系统
- **外部API登录** - 通过外部认证API验证用户身份
- **安全Modal界面** - 私密输入用户名和密码，不在频道中暴露
- **自动角色分配** - 验证成功后自动授予指定角色
- **昵称同步** - 将用户昵称更新为API返回的用户名
- **防重复验证** - 已验证用户无法重复认证

### 🌍 多语言支持
- **中英双语** - 完整的中文和英文界面
- **动态切换** - 用户可随时选择显示语言
- **本地化消息** - 所有用户交互均支持多语言

### 🛡️ 权限管理
- **智能频道控制** - 自动配置验证频道和其他频道的权限
- **角色层级管理** - 基于@everyone和Verified角色的权限模型
- **管理员命令** - 管理员可撤销用户验证状态

### 💾 数据持久化
- **JSON存储** - 验证记录和语言偏好持久化保存
- **原子写入** - 防止数据损坏的安全写入机制
- **自动初始化** - 首次运行自动创建数据文件

### 🎯 基础命令
- `/basic ping` - 测试机器人响应
- `/basic echo <text>` - 回显用户输入
- `/basic help` - 显示帮助信息

## 🚀 快速开始

### 1. 环境准备

```powershell
# 克隆项目
git clone <repository-url>
cd authbot

# 创建并激活虚拟环境
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制 `.env.example` 为 `.env` 并配置以下变量：

```bash
# Discord Bot Token (必需)
DISCORD_TOKEN=your_bot_token_here

# 认证API配置
AUTH_API_BASE=https://auth.hvhbbs.cc

# 可选配置
GUILD_ID=123456789012345678          # 特定服务器ID，留空则全局同步
AUTH_SUCCESS_ROLE=Verified           # 验证成功角色名
AUTH_CHANNEL_NAME=auth-verify        # 验证频道名
AUTH_LOGIN_CHANNEL_ONLY=true         # 是否限制登录命令只能在验证频道使用
AUTH_HIDE_OTHER_CHANNELS=true        # 是否对未验证用户隐藏其他频道
LOG_LEVEL=INFO                       # 日志等级
AUTH_DATA_FILE=./data.json          # 数据文件路径
```

### 3. 运行机器人

```powershell
# 推荐方式：直接运行
python .\run.py

# 或者模块方式运行
$env:PYTHONPATH = "$PWD/src"
python -m authbot
```

> 首次运行 Slash 命令可能需要数分钟在服务器中同步，请在 Discord 客户端中等待命令出现或尝试重新输入。

## 📋 命令详解

### 管理员命令

#### `/auth setup`
- **功能**: 初始化认证系统
- **权限**: 需要管理员权限
- **效果**: 
  - 创建Verified角色
  - 创建或更新auth-verify频道
  - 配置频道权限（未验证用户只能看到验证频道）
  - 发送语言选择消息

#### `/auth revoke <member>`
- **功能**: 撤销用户验证状态
- **权限**: 需要管理员权限
- **效果**:
  - 移除用户的Verified角色
  - 清除数据库中的验证记录
  - 可选择添加Unverified角色

### 用户命令

#### `/auth login`
- **功能**: 打开登录验证界面
- **限制**: 
  - 默认只能在验证频道使用
  - 已验证用户无法重复使用
- **流程**:
  1. 弹出安全登录Modal
  2. 用户输入用户名/邮箱和密码
  3. 调用外部API验证
  4. 验证成功后分配角色和更新昵称

## 🔧 技术架构

### 项目结构
```
authbot/
├── src/authbot/
│   ├── __init__.py          # 包初始化
│   ├── __main__.py          # 模块入口点
│   ├── main.py              # 主程序逻辑
│   ├── commands.py          # 基础命令
│   ├── auth_commands.py     # 认证命令
│   ├── auth_api.py          # 外部API客户端
│   ├── i18n.py             # 国际化支持
│   ├── prefs.py            # 用户偏好管理
│   └── storage.py          # 数据持久化
├── requirements.txt         # Python依赖
├── run.py                  # 启动脚本
├── .env.example           # 环境变量模板
└── README.md              # 项目文档
```

### 依赖库
- **discord.py** (2.x) - Discord API 封装
- **python-dotenv** (1.x) - 环境变量管理
- **httpx** (0.27) - 异步HTTP客户端

### 核心组件

#### AuthAPI (`auth_api.py`)
- 处理外部认证API调用
- 支持POST请求到 `{base}/?action=login`
- 返回包含状态码的JSON响应
- 自动处理各种HTTP错误情况

#### 国际化系统 (`i18n.py`)
- 基于字典的多语言支持
- 支持占位符和参数化消息
- 自动降级到默认语言

#### 权限模型
- **@everyone**: 只能看到验证频道
- **Verified角色**: 可以访问所有频道并发言
- **频道权限**: 自动配置分类和频道的查看/发言权限

## 🛠️ 开发指南

### 添加新命令
在 `commands.py` 或 `auth_commands.py` 中添加新的 `app_commands`:

```python
@app_commands.command(name="example", description="示例命令")
async def example(self, interaction: Interaction):
    await interaction.response.send_message("示例响应", ephemeral=True)
```

### 添加多语言文本
在 `i18n.py` 的 `_messages` 字典中添加新键值对：

```python
"new_message": {
    "zh": "中文消息",
    "en": "English message",
},
```

### 日志记录
使用模块级别的logger：

```python
import logging
log = logging.getLogger("authbot.module_name")
log.info("信息日志")
log.warning("警告日志")
```

## 🔍 故障排除

### 常见问题

**Q: 机器人启动后看不到斜杠命令？**
A: 
- 确保机器人有 `applications.commands` 权限
- 首次同步可能需要几分钟，请耐心等待
- 检查 `GUILD_ID` 设置是否正确

**Q: 认证API调用失败？**
A:
- 检查 `AUTH_API_BASE` 是否正确配置
- 确认API端点支持 POST 请求到 `/?action=login`
- 查看日志中的详细错误信息

**Q: 无法分配角色或修改昵称？**
A:
- 确保机器人角色在服务器角色列表中位置足够高
- 检查机器人是否有 `Manage Roles` 和 `Manage Nicknames` 权限

**Q: 权限设置不生效？**
A:
- 确认机器人有 `Manage Channels` 权限
- 检查频道权限是否被其他设置覆盖
- 查看控制台日志中的权限设置警告

### 调试模式
设置 `LOG_LEVEL=DEBUG` 获取详细的调试信息：

```bash
LOG_LEVEL=DEBUG
```

## 📄 许可证

本项目使用 MIT 许可证。详情请参见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如需帮助，请：
1. 查看本README文档
2. 检查日志输出中的错误信息
3. 在GitHub上提交Issue

```bash
来自 WWW.HVHBBS.CC | MhYa123
```