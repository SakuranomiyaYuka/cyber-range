# 🏴‍☠️ Cyber Range

> v1.0.0

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-本地存储-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![难度](https://img.shields.io/badge/关卡-15-blueviolet)
![License](https://img.shields.io/badge/License-MIT-blue)

> Web 安全训练靶场，从零基础到实战技巧，15 个原创关卡循序渐进。
> Docker Compose 一键部署，专为安全学习者设计。

涵盖 **SQL 注入、XSS 跨站脚本、文件上传** 三大经典漏洞类型，每个关卡只教一个知识点，配有明确提示。

## 快速体验（30 秒上手）

```bash
git clone https://github.com/SakuranomiyaYuka/cyber-range.git && cd cyber-range
docker compose up -d

# 浏览器打开 http://localhost:5000
# 开始闯关！
```

## 适用场景

- 🎓 Web 安全初学者，想动手实践 SQL 注入 / XSS / 文件上传
- 🏫 安全培训讲师，需要一个开箱即用的教学靶场
- 🏁 CTF 选手赛前热身，练习基础漏洞利用技巧
- 🔬 安全研究者，快速验证 payload 和绕过思路

## 为什么选择 Cyber Range？

| 对比维度 | Cyber Range | DVWA | WebGoat | PortSwigger Lab |
|---------|-------------|------|---------|-----------------|
| 部署方式 | ✅ Docker Compose 一行命令 | ✅ Docker | ❌ 需 Java 环境 | ❌ 需公网访问 |
| 关卡数量 | 15 关，3 个系列 | 12 关 | ~30 关 | 无限（在线） |
| 设计理念 | 一关一个知识点，提示明确 | 难度跳跃大 | 偏理论 | 高质量但需联网 |
| 中文支持 | ✅ 全中文界面和提示 | ❌ 英文 | ❌ 英文 | ❌ 英文 |
| 离线可用 | ✅ 完全离线，零依赖 | ✅ 离线 | ✅ 离线 | ❌ 需在线环境 |
| 文件体积 | ~50MB | ~300MB | ~1GB | N/A |
| 原创性 | 全部原创关卡 | 经典复现 | 经典复现 | 官方出品 |

## 特性

- **3 大系列 15 关** — SQL 注入 5 关、XSS 5 关、文件上传 5 关，难度递增
- **Docker Compose 一键部署** — 无需配置环境，一条命令启动
- **轻量级** — Flask + SQLite，低配机器也能跑
- **每关明确提示** — 不翻答案也能学
- **免 Docker 可运行** — 直接 `python app.py` 也能启动
- **预设 Flag** — 每关都有明确的目标
- **通关参考** — 前几关附解题示例

---

## 关卡列表

### SQL 注入系列（5关）

| 关卡 | 类型 | 难度 | 攻击面 | 核心技巧 |
|------|------|:----:|--------|----------|
| Lv1 | GET 注入 | ★☆☆ | URL 参数 `?id=` | 单引号闭合，`OR 1=1` 爆出全部数据 |
| Lv2 | POST 登录绕过 | ★☆☆ | 登录表单 | 注释符 `--` 绕过密码验证 |
| Lv3 | 布尔盲注 | ★★☆ | URL 参数 `?id=` | 页面仅返回存在/不存在，逐位猜解 |
| Lv4 | 时间盲注 | ★★★ | URL 参数 `?id=` | 通过 `SLEEP()` 延时判断真伪 |
| Lv5 | UPDATE 注入 | ★★★ | 修改密码表单 | 在 UPDATE 语句中嵌入子查询读取 secrets 表 |

### XSS 跨站脚本系列（5关）

| 关卡 | 类型 | 难度 | 攻击面 | 核心技巧 |
|------|------|:----:|--------|----------|
| Lv1 | 反射型（无过滤） | ★☆☆ | 搜索框 | 直接输出 `<script>alert(1)</script>` |
| Lv2 | 反射型（标签绕过） | ★☆☆ | 搜索框 | `<script>` 被过滤，用 `<img src=x onerror=alert(1)>` 绕过 |
| Lv3 | 存储型（留言板） | ★★☆ | 评论表单 | 内容存入数据库，每次刷新都触发 |
| Lv4 | DOM 型 | ★★☆ | URL hash | 前端 `innerHTML` 直接插入，不经服务端渲染 |
| Lv5 | 存储型 + CSP 绕过 | ★★★ | 留言板 | CSP 限制内联脚本，需上传 `.js` 文件并引用 |

### 文件上传系列（5关）

| 关卡 | 类型 | 难度 | 攻击面 | 核心技巧 |
|------|------|:----:|--------|----------|
| Lv1 | 无过滤 | ★☆☆ | 文件选择 | 直接上传任意后缀文件 |
| Lv2 | 后缀黑名单 | ★☆☆ | 文件名 | 黑名单不全，改 `.php5` / `.phtml` / 大小写绕过 |
| Lv3 | MIME 类型检查 | ★★☆ | Content-Type | 仅检查 Content-Type，改 `image/jpeg` |
| Lv4 | 文件头检查 | ★★★ | 文件内容 | 检查幻数，在文件头加 `GIF89a` 后再放 payload |
| Lv5 | 多重过滤 | ★★★ | 组合检查 | 同时检查后缀、MIME、幻数，需组合多种技巧 |

---

## 项目结构

```
cyber-range/
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml     # Docker Compose 配置
├── LICENSE                # MIT 协议
├── README.md              # 本文件
└── app/
    ├── app.py             # Flask 入口
    ├── db.py              # 数据库初始化
    ├── levels/            # 关卡逻辑
    │   ├── sqli.py        # SQL 注入系列
    │   ├── xss.py         # XSS 系列
    │   └── upload.py      # 文件上传系列
    └── templates/         # Jinja2 模板
```

## 快速启动

### Docker Compose（推荐）

```bash
git clone https://github.com/SakuranomiyaYuka/cyber-range.git
cd cyber-range
docker compose up -d
```

启动后访问 http://localhost:5000

停止：`docker compose down`

### 直接运行（无需 Docker）

```bash
cd cyber-range/app
pip install flask gunicorn
python app.py
```

访问 http://localhost:5000

## 通关参考

### SQLi Lv1 — 基础 GET 注入

传入 `?id=1 OR 1=1`，底层 SQL 变为：

```sql
SELECT id, username, email, role FROM users WHERE id = 1 OR 1=1
```

`OR 1=1` 使条件恒成立，返回全部记录。

### XSS Lv1 — 反射型 XSS

在搜索框输入 `<script>alert('XSS')</script>`，页面弹出对话框。

### Upload Lv2 — 后缀黑名单绕过

将 `.php` 改为 `.php5` / `.phtml` / `.Php` 即可绕过。

上传后访问 `http://localhost:5000/upload/uploads/shell.php5`。

## 数据库结构

SQLite 数据库 `app/data.db`，包含三张表：

```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, role TEXT DEFAULT 'user');
CREATE TABLE comments (id INTEGER PRIMARY KEY, name TEXT, content TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE secrets (id INTEGER PRIMARY KEY, name TEXT, value TEXT);
```

secrets 表预置两个 flag：

| name | value |
|------|-------|
| flag_sqli_level5 | flag{f1rst_0rd3r_upd4t3_1nj3ct10n} |
| flag_xss_level5 | flag{st0r3d_xss_w1th_csp_byp4ss} |

## 常见问题

**Q: 启动后 5000 端口无响应？** 检查 `docker compose logs -f`

**Q: 数据库报错？** `rm app/data.db && docker compose restart`

**Q: Docker 下载慢？** 配置国内镜像加速

## License

[MIT](LICENSE) — Copyright © 2026 [SakuranomiyaYuka](https://github.com/SakuranomiyaYuka)
