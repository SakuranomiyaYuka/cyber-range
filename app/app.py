import os
import sys
from flask import Flask, render_template

sys.path.insert(0, os.path.dirname(__file__))

from levels.sqli import sqli_bp
from levels.xss import xss_bp
from levels.upload import upload_bp

app = Flask(__name__)
app.secret_key = 'cyber-range-secret-key-change-in-production'

app.register_blueprint(sqli_bp,  url_prefix='/sqli')
app.register_blueprint(xss_bp,   url_prefix='/xss')
app.register_blueprint(upload_bp, url_prefix='/upload')

LEVELS = {
    'SQL 注入': [
        ('/sqli/1',  'Lv1 — 基础 GET 注入（单引号闭合）'),
        ('/sqli/2',  'Lv2 — 基础 POST 登录绕过'),
        ('/sqli/3',  'Lv3 — 布尔盲注'),
        ('/sqli/4',  'Lv4 — 时间盲注'),
        ('/sqli/5',  'Lv5 — UPDATE 注入'),
    ],
    'XSS 跨站脚本': [
        ('/xss/1',  'Lv1 — 反射型 XSS（无过滤）'),
        ('/xss/2',  'Lv2 — 反射型 XSS（标签过滤绕过）'),
        ('/xss/3',  'Lv3 — 存储型 XSS（留言板）'),
        ('/xss/4',  'Lv4 — DOM 型 XSS'),
        ('/xss/5',  'Lv5 — 存储型 XSS + 简单 CSP 绕过'),
    ],
    '文件上传': [
        ('/upload/1',  'Lv1 — 无过滤直接上传'),
        ('/upload/2',  'Lv2 — 后缀黑名单绕过'),
        ('/upload/3',  'Lv3 — MIME 类型绕过'),
        ('/upload/4',  'Lv4 — 文件头内容检查绕过'),
        ('/upload/5',  'Lv5 — 多重过滤综合绕过'),
    ],
}


@app.route('/')
def index():
    return render_template('index.html', levels=LEVELS, info=None)


if __name__ == '__main__':
    from db import init_db
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
