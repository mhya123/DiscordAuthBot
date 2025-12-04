# Discord AuthBot# Discord AuthBot# Discord AuthBot



一个功能完整的 Discord 身份验证机器人，支持外部API认证、双语界面、权限管理和持久化存储。



## ✨ 主要功能一个功能完整的 Discord 身份验证机器人，支持外部API认证、双语界面、权限管理和持久化存储。一个功能完整的 Discord 身份验证机器人，支持外部API认证、双语界面、权限管理和持久化存储。



### 🔐 身份认证系统

- **外部API登录** - 通过外部认证API验证用户身份

- **安全Modal界面** - 私密输入用户名和密码，不在频道中暴露## ✨ 主要功能## ✨ 主要功能

- **自动角色分配** - 验证成功后自动授予指定角色

- **昵称同步** - 将用户昵称更新为API返回的用户名

- **防重复验证** - 已验证用户无法重复认证

### 🔐 身份认证系统### 🔐 身份认证系统

### 🌍 多语言支持

- **中英双语** - 完整的中文和英文界面- **外部API登录** - 通过外部认证API验证用户身份- **外部API登录** - 通过外部认证API验证用户身份

- **动态切换** - 用户可随时选择显示语言

- **本地化消息** - 所有用户交互均支持多语言- **安全Modal界面** - 私密输入用户名和密码，不在频道中暴露- **安全Modal界面** - 私密输入用户名和密码，不在频道中暴露



### 🛡️ 权限管理- **自动角色分配** - 验证成功后自动授予指定角色- **自动角色分配** - 验证成功后自动授予指定角色

- **智能频道控制** - 自动配置验证频道和其他频道的权限

- **角色层级管理** - 基于@everyone和Verified角色的权限模型- **昵称同步** - 将用户昵称更新为API返回的用户名- **昵称同步** - 将用户昵称更新为API返回的用户名

- **管理员命令** - 管理员可撤销用户验证状态

- **防重复验证** - 已验证用户无法重复认证- **防重复验证** - 已验证用户无法重复认证

### 💾 数据持久化

- **SQLite/MySQL** - 支持两种数据库后端，默认 SQLite

- **自动初始化** - 首次运行自动创建数据库和表

- **高效查询** - 使用索引优化查询性能### 🌍 多语言支持### 🌍 多语言支持



## 🚀 快速开始- **中英双语** - 完整的中文和英文界面- **中英双语** - 完整的中文和英文界面



### 1. 环境准备- **动态切换** - 用户可随时选择显示语言- **动态切换** - 用户可随时选择显示语言



```powershell- **本地化消息** - 所有用户交互均支持多语言- **本地化消息** - 所有用户交互均支持多语言

# 克隆项目

git clone https://github.com/mhya123/DiscordAuthBot.git

cd authbot

### 🛡️ 权限管理### 🛡️ 权限管理

# 创建并激活虚拟环境

python -m venv .venv- **智能频道控制** - 自动配置验证频道和其他频道的权限- **智能频道控制** - 自动配置验证频道和其他频道的权限

.\.venv\Scripts\Activate.ps1

- **角色层级管理** - 基于@everyone和Verified角色的权限模型- **角色层级管理** - 基于@everyone和Verified角色的权限模型

# 安装依赖

pip install -r requirements.txt- **管理员命令** - 管理员可撤销用户验证状态- **管理员命令** - 管理员可撤销用户验证状态

```



### 2. 配置环境

### 💾 数据持久化### 💾 数据持久化

复制 `.env.example` 为 `.env` 并配置以下变量：

- **JSON存储** - 验证记录和语言偏好持久化保存- **JSON存储** - 验证记录和语言偏好持久化保存

```bash

# Discord Bot Token (必需)- **原子写入** - 防止数据损坏的安全写入机制- **原子写入** - 防止数据损坏的安全写入机制

DISCORD_TOKEN=your_bot_token_here

- **自动初始化** - 首次运行自动创建数据文件- **自动初始化** - 首次运行自动创建数据文件

# 认证API配置

AUTH_API_BASE=https://auth.hvhbbs.cc



# 可选配置## 🚀 快速开始### 🎯 基础命令

GUILD_ID=123456789012345678          # 特定服务器ID，留空则全局同步

AUTH_SUCCESS_ROLE=Verified           # 验证成功角色名- `/basic ping` - 测试机器人响应

AUTH_CHANNEL_NAME=auth-verify        # 验证频道名

AUTH_LOGIN_CHANNEL_ONLY=true         # 是否限制登录命令只能在验证频道使用### 1. 环境准备- `/basic echo <text>` - 回显用户输入

AUTH_HIDE_OTHER_CHANNELS=true        # 是否对未验证用户隐藏其他频道

LOG_LEVEL=INFO                       # 日志等级- `/basic help` - 显示帮助信息



# ========== 数据库配置 ==========```powershell

# 数据库类型: sqlite (默认) 或 mysql

DB_TYPE=sqlite# 克隆项目## 🚀 快速开始



# SQLite 配置git clone https://github.com/mhya123/DiscordAuthBot.git

DB_PATH=./data.db                    # SQLite 数据库文件路径

cd authbot### 1. 环境准备

# MySQL 配置 (仅当 DB_TYPE=mysql 时需要)

DB_HOST=localhost

DB_PORT=3306

DB_USER=root# 创建并激活虚拟环境```powershell

DB_PASSWORD=your_password

DB_NAME=authbotpython -m venv .venv# 克隆项目

```

.\.venv\Scripts\Activate.ps1https://github.com/mhya123/DiscordAuthBot.git

### 3. 运行机器人

cd authbot

```powershell

# 推荐方式：直接运行# 安装依赖

python .\run.py

pip install -r requirements.txt# 创建并激活虚拟环境

# 或者模块方式运行

$env:PYTHONPATH = "$PWD/src"```python -m venv .venv

python -m authbot

```.\.venv\Scripts\Activate.ps1



> 首次运行 Slash 命令可能需要数分钟在服务器中同步，请在 Discord 客户端中等待命令出现或尝试重新输入。### 2. 配置环境



## 📋 命令详解# 安装依赖



### 👤 用户命令（常用）复制 `.env.example` 为 `.env` 并配置以下变量：pip install -r requirements.txt



| 命令 | 描述 | 备注 |```

|------|------|------|

| `/login` | 🔐 登录验证账号 | 打开安全登录窗口 |```bash

| `/status` | 📊 查看验证状态 | 显示当前认证状态和账号信息 |

| `/lang` | 🌐 切换显示语言 | 支持中文和英文 |# Discord Bot Token (必需)### 2. 配置环境

| `/help` | ❓ 显示帮助信息 | 查看所有可用命令 |

DISCORD_TOKEN=your_bot_token_here

### 🛡️ 管理员命令

复制 `.env.example` 为 `.env` 并配置以下变量：

| 命令 | 描述 | 权限要求 |

|------|------|----------|# 认证API配置

| `/auth setup` | 🔧 初始化认证系统 | 管理员 |

| `/auth revoke <成员>` | 🚫 撤销用户验证 | 管理员 |AUTH_API_BASE=https://auth.hvhbbs.cc```bash

| `/auth list` | 📋 查看已验证用户列表 | 管理员 |

# Discord Bot Token (必需)

### 命令使用流程

# 可选配置DISCORD_TOKEN=your_bot_token_here

#### 首次设置（管理员）

```GUILD_ID=123456789012345678          # 特定服务器ID，留空则全局同步

1. 使用 /auth setup 初始化系统

2. 系统会自动创建 Verified 角色和 #auth-verify 频道AUTH_SUCCESS_ROLE=Verified           # 验证成功角色名# 认证API配置

3. 验证频道中会发送带有快捷按钮的欢迎消息

```AUTH_CHANNEL_NAME=auth-verify        # 验证频道名AUTH_API_BASE=https://auth.hvhbbs.cc



#### 用户验证流程AUTH_LOGIN_CHANNEL_ONLY=true         # 是否限制登录命令只能在验证频道使用

```

1. 进入 #auth-verify 频道AUTH_HIDE_OTHER_CHANNELS=true        # 是否对未验证用户隐藏其他频道# 可选配置

2. 点击「登录验证」按钮 或使用 /login 命令

3. 在弹出的窗口中输入账号密码LOG_LEVEL=INFO                       # 日志等级GUILD_ID=123456789012345678          # 特定服务器ID，留空则全局同步

4. 验证成功后自动获得角色并更新昵称

5. 可使用 /status 查看验证状态AUTH_DATA_FILE=./data.json          # 数据文件路径AUTH_SUCCESS_ROLE=Verified           # 验证成功角色名

```

```AUTH_CHANNEL_NAME=auth-verify        # 验证频道名

## 🗄️ 数据库配置

AUTH_LOGIN_CHANNEL_ONLY=true         # 是否限制登录命令只能在验证频道使用

### SQLite（默认）

### 3. 运行机器人AUTH_HIDE_OTHER_CHANNELS=true        # 是否对未验证用户隐藏其他频道

无需额外配置，数据存储在本地 `data.db` 文件中：

LOG_LEVEL=INFO                       # 日志等级

```bash

DB_TYPE=sqlite```powershellAUTH_DATA_FILE=./data.json          # 数据文件路径

DB_PATH=./data.db

```# 推荐方式：直接运行```



### MySQLpython .\run.py



如需使用 MySQL，配置以下变量：### 3. 运行机器人



```bash# 或者模块方式运行

DB_TYPE=mysql

DB_HOST=localhost$env:PYTHONPATH = "$PWD/src"```powershell

DB_PORT=3306

DB_USER=rootpython -m authbot# 推荐方式：直接运行

DB_PASSWORD=your_password

DB_NAME=authbot```python .\run.py

```



**注意**：使用 MySQL 需要安装 `pymysql`：

```bash> 首次运行 Slash 命令可能需要数分钟在服务器中同步，请在 Discord 客户端中等待命令出现或尝试重新输入。# 或者模块方式运行

pip install pymysql

```$env:PYTHONPATH = "$PWD/src"



### 数据库表结构## 📋 命令详解python -m authbot



| 表名 | 描述 |```

|------|------|

| `verified_users` | 存储已验证用户信息 |### 👤 用户命令（常用）

| `user_prefs` | 存储用户偏好（如语言设置） |

> 首次运行 Slash 命令可能需要数分钟在服务器中同步，请在 Discord 客户端中等待命令出现或尝试重新输入。

## 🔧 技术架构

| 命令 | 描述 | 备注 |

### 项目结构

```|------|------|------|## 📋 命令详解

authbot/

├── src/authbot/| `/login` | 🔐 登录验证账号 | 打开安全登录窗口 |

│   ├── __init__.py          # 包初始化

│   ├── __main__.py          # 模块入口点| `/status` | 📊 查看验证状态 | 显示当前认证状态和账号信息 |### 管理员命令

│   ├── main.py              # 主程序逻辑

│   ├── auth_commands.py     # 认证命令和用户命令| `/lang` | 🌐 切换显示语言 | 支持中文和英文 |

│   ├── auth_api.py          # 外部API客户端

│   ├── i18n.py              # 国际化支持| `/help` | ❓ 显示帮助信息 | 查看所有可用命令 |#### `/auth setup`

│   ├── prefs.py             # 用户偏好管理

│   └── storage.py           # 数据库存储（SQLite/MySQL）- **功能**: 初始化认证系统

├── requirements.txt          # Python依赖

├── run.py                   # 启动脚本### 🛡️ 管理员命令- **权限**: 需要管理员权限

├── .env.example             # 环境变量模板

└── README.md                # 项目文档- **效果**: 

```

| 命令 | 描述 | 权限要求 |  - 创建Verified角色

### 依赖库

- **discord.py** (2.x) - Discord API 封装|------|------|----------|  - 创建或更新auth-verify频道

- **python-dotenv** (1.x) - 环境变量管理

- **httpx** (0.27) - 异步HTTP客户端| `/auth setup` | 🔧 初始化认证系统 | 管理员 |  - 配置频道权限（未验证用户只能看到验证频道）

- **pymysql** (1.x) - MySQL 连接器（可选）

| `/auth revoke <成员>` | 🚫 撤销用户验证 | 管理员 |  - 发送语言选择消息

### 核心组件

| `/auth list` | 📋 查看已验证用户列表 | 管理员 |

#### 存储后端 (`storage.py`)

- 抽象数据库接口，支持 SQLite 和 MySQL#### `/auth revoke <member>`

- 自动创建数据库和表

- 提供统一的 API 进行数据操作### 命令使用流程- **功能**: 撤销用户验证状态



#### AuthAPI (`auth_api.py`)- **权限**: 需要管理员权限

- 处理外部认证API调用

- 支持POST请求到 `{base}/?action=login`#### 首次设置（管理员）- **效果**:

- 返回包含状态码的JSON响应

```  - 移除用户的Verified角色

#### 国际化系统 (`i18n.py`)

- 基于字典的多语言支持1. 使用 /auth setup 初始化系统  - 清除数据库中的验证记录

- 支持占位符和参数化消息

- 自动降级到默认语言2. 系统会自动创建 Verified 角色和 #auth-verify 频道  - 可选择添加Unverified角色



## 🛠️ 开发指南3. 验证频道中会发送带有快捷按钮的欢迎消息



### 添加新命令```### 用户命令



在 `auth_commands.py` 中添加新的顶级命令：



```python#### 用户验证流程#### `/auth login`

@app_commands.command(name="example", description="示例命令")

async def example_command(interaction: Interaction):```- **功能**: 打开登录验证界面

    await interaction.response.send_message("示例响应", ephemeral=True)

```1. 进入 #auth-verify 频道- **限制**: 



然后在 `register_commands` 函数中注册：2. 点击「登录验证」按钮 或使用 /login 命令  - 默认只能在验证频道使用



```python3. 在弹出的窗口中输入账号密码  - 已验证用户无法重复使用

def register_commands(bot: commands.Bot) -> None:

    bot.tree.add_command(example_command)4. 验证成功后自动获得角色并更新昵称- **流程**:

```

5. 可使用 /status 查看验证状态  1. 弹出安全登录Modal

### 添加多语言文本

```  2. 用户输入用户名/邮箱和密码

在 `i18n.py` 的 `_messages` 字典中添加新键值对：

  3. 调用外部API验证

```python

"new_message": {## 🔧 技术架构  4. 验证成功后分配角色和更新昵称

    "zh": "中文消息",

    "en": "English message",

},

```### 项目结构## 🔧 技术架构



### 日志记录```



使用模块级别的logger：authbot/### 项目结构



```python├── src/authbot/```

import logging

log = logging.getLogger("authbot.module_name")│   ├── __init__.py          # 包初始化authbot/

log.info("信息日志")

log.warning("警告日志")│   ├── __main__.py          # 模块入口点├── src/authbot/

```

│   ├── main.py              # 主程序逻辑│   ├── __init__.py          # 包初始化

## 🔍 故障排除

│   ├── auth_commands.py     # 认证命令和用户命令│   ├── __main__.py          # 模块入口点

### 常见问题

│   ├── auth_api.py          # 外部API客户端│   ├── main.py              # 主程序逻辑

**Q: 机器人启动后看不到斜杠命令？**

A: │   ├── i18n.py             # 国际化支持│   ├── commands.py          # 基础命令

- 确保机器人有 `applications.commands` 权限

- 首次同步可能需要几分钟，请耐心等待│   ├── prefs.py            # 用户偏好管理│   ├── auth_commands.py     # 认证命令

- 检查 `GUILD_ID` 设置是否正确

│   └── storage.py          # 数据持久化│   ├── auth_api.py          # 外部API客户端

**Q: 认证API调用失败？**

A:├── requirements.txt         # Python依赖│   ├── i18n.py             # 国际化支持

- 检查 `AUTH_API_BASE` 是否正确配置

- 确认API端点支持 POST 请求到 `/?action=login`├── run.py                  # 启动脚本│   ├── prefs.py            # 用户偏好管理

- 查看日志中的详细错误信息

├── .env.example           # 环境变量模板│   └── storage.py          # 数据持久化

**Q: 无法分配角色或修改昵称？**

A:└── README.md              # 项目文档├── requirements.txt         # Python依赖

- 确保机器人角色在服务器角色列表中位置足够高

- 检查机器人是否有 `Manage Roles` 和 `Manage Nicknames` 权限```├── run.py                  # 启动脚本



**Q: 数据库连接失败？**├── .env.example           # 环境变量模板

A:

- SQLite：检查 `DB_PATH` 路径是否有写入权限### 依赖库└── README.md              # 项目文档

- MySQL：确认 MySQL 服务正在运行，检查连接参数

- **discord.py** (2.x) - Discord API 封装```

### 调试模式

- **python-dotenv** (1.x) - 环境变量管理

设置 `LOG_LEVEL=DEBUG` 获取详细的调试信息：

- **httpx** (0.27) - 异步HTTP客户端### 依赖库

```bash

LOG_LEVEL=DEBUG- **discord.py** (2.x) - Discord API 封装

```

### 核心组件- **python-dotenv** (1.x) - 环境变量管理

## 📄 许可证

- **httpx** (0.27) - 异步HTTP客户端

本项目使用 MIT 许可证。详情请参见 LICENSE 文件。

#### AuthAPI (`auth_api.py`)

## 🤝 贡献

- 处理外部认证API调用### 核心组件

欢迎提交 Issue 和 Pull Request！

- 支持POST请求到 `{base}/?action=login`

## 📞 支持

- 返回包含状态码的JSON响应#### AuthAPI (`auth_api.py`)

如需帮助，请：

1. 查看本README文档- 自动处理各种HTTP错误情况- 处理外部认证API调用

2. 检查日志输出中的错误信息

3. 在GitHub上提交Issue- 支持POST请求到 `{base}/?action=login`



---#### 国际化系统 (`i18n.py`)- 返回包含状态码的JSON响应

来自 WWW.HVHBBS.CC | MhYa123

- 基于字典的多语言支持- 自动处理各种HTTP错误情况

- 支持占位符和参数化消息

- 自动降级到默认语言#### 国际化系统 (`i18n.py`)

- 基于字典的多语言支持

#### 权限模型- 支持占位符和参数化消息

- **@everyone**: 只能看到验证频道- 自动降级到默认语言

- **Verified角色**: 可以访问所有频道并发言

- **频道权限**: 自动配置分类和频道的查看/发言权限#### 权限模型

- **@everyone**: 只能看到验证频道

## 🛠️ 开发指南- **Verified角色**: 可以访问所有频道并发言

- **频道权限**: 自动配置分类和频道的查看/发言权限

### 添加新命令

## 🛠️ 开发指南

在 `auth_commands.py` 中添加新的顶级命令：

### 添加新命令

```python在 `commands.py` 或 `auth_commands.py` 中添加新的 `app_commands`:

@app_commands.command(name="example", description="示例命令")

async def example_command(interaction: Interaction):```python

    await interaction.response.send_message("示例响应", ephemeral=True)@app_commands.command(name="example", description="示例命令")

```async def example(self, interaction: Interaction):

    await interaction.response.send_message("示例响应", ephemeral=True)

然后在 `register_commands` 函数中注册：```



```python### 添加多语言文本

def register_commands(bot: commands.Bot) -> None:在 `i18n.py` 的 `_messages` 字典中添加新键值对：

    bot.tree.add_command(example_command)

``````python

"new_message": {

### 添加多语言文本    "zh": "中文消息",

    "en": "English message",

在 `i18n.py` 的 `_messages` 字典中添加新键值对：},

```

```python

"new_message": {### 日志记录

    "zh": "中文消息",使用模块级别的logger：

    "en": "English message",

},```python

```import logging

log = logging.getLogger("authbot.module_name")

### 日志记录log.info("信息日志")

log.warning("警告日志")

使用模块级别的logger：```



```python## 🔍 故障排除

import logging

log = logging.getLogger("authbot.module_name")### 常见问题

log.info("信息日志")

log.warning("警告日志")**Q: 机器人启动后看不到斜杠命令？**

```A: 

- 确保机器人有 `applications.commands` 权限

## 🔍 故障排除- 首次同步可能需要几分钟，请耐心等待

- 检查 `GUILD_ID` 设置是否正确

### 常见问题

**Q: 认证API调用失败？**

**Q: 机器人启动后看不到斜杠命令？**A:

A: - 检查 `AUTH_API_BASE` 是否正确配置

- 确保机器人有 `applications.commands` 权限- 确认API端点支持 POST 请求到 `/?action=login`

- 首次同步可能需要几分钟，请耐心等待- 查看日志中的详细错误信息

- 检查 `GUILD_ID` 设置是否正确

**Q: 无法分配角色或修改昵称？**

**Q: 认证API调用失败？**A:

A:- 确保机器人角色在服务器角色列表中位置足够高

- 检查 `AUTH_API_BASE` 是否正确配置- 检查机器人是否有 `Manage Roles` 和 `Manage Nicknames` 权限

- 确认API端点支持 POST 请求到 `/?action=login`

- 查看日志中的详细错误信息**Q: 权限设置不生效？**

A:

**Q: 无法分配角色或修改昵称？**- 确认机器人有 `Manage Channels` 权限

A:- 检查频道权限是否被其他设置覆盖

- 确保机器人角色在服务器角色列表中位置足够高- 查看控制台日志中的权限设置警告

- 检查机器人是否有 `Manage Roles` 和 `Manage Nicknames` 权限

### 调试模式

**Q: 权限设置不生效？**设置 `LOG_LEVEL=DEBUG` 获取详细的调试信息：

A:

- 确认机器人有 `Manage Channels` 权限```bash

- 检查频道权限是否被其他设置覆盖LOG_LEVEL=DEBUG

- 查看控制台日志中的权限设置警告```



### 调试模式## 📄 许可证



设置 `LOG_LEVEL=DEBUG` 获取详细的调试信息：本项目使用 MIT 许可证。详情请参见 LICENSE 文件。



```bash## 🤝 贡献

LOG_LEVEL=DEBUG

```欢迎提交 Issue 和 Pull Request！



## 📄 许可证## 📞 支持



本项目使用 MIT 许可证。详情请参见 LICENSE 文件。如需帮助，请：

1. 查看本README文档

## 🤝 贡献2. 检查日志输出中的错误信息

3. 在GitHub上提交Issue

欢迎提交 Issue 和 Pull Request！

```bash

## 📞 支持来自 WWW.HVHBBS.CC | MhYa123

```
如需帮助，请：
1. 查看本README文档
2. 检查日志输出中的错误信息
3. 在GitHub上提交Issue

---
来自 WWW.HVHBBS.CC | MhYa123
