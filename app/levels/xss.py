from flask import Blueprint, request, render_template, make_response
from db import get_db
import html
import re

xss_bp = Blueprint('xss', __name__, template_folder='../templates')


def level_info(num, title, desc, hint):
    return {
        'category': 'xss',
        'level': num,
        'title': title,
        'desc': desc,
        'hint': hint,
    }


# ── Lv1: 反射型 XSS（无过滤） ──────────────────────────────────────
@xss_bp.route('/1', methods=['GET'])
def level1():
    info = level_info(1, '反射型 XSS（无过滤）',
                      '搜索框直接显示输入内容，没有任何过滤。弹个窗试试。',
                      '尝试: <script>alert(1)</script>')
    search = request.args.get('q', '')
    return render_template('xss_reflected.html', info=info,
                           search=search,
                           sanitized=False)


# ── Lv2: 反射型 XSS（标签过滤绕过） ────────────────────────────────
@xss_bp.route('/2', methods=['GET'])
def level2():
    info = level_info(2, '反射型 XSS（标签过滤绕过）',
                      '<script> 被过滤了，但你还可以用其他标签。',
                      '尝试: <img src=x onerror=alert(1)>  或  <body onload=alert(1)>')
    search = request.args.get('q', '')
    # 过滤 script 标签（大小写不敏感），不处理其他标签
    sanitized = re.sub(r'(?i)<script[^>]*>.*?</script>', '', search)
    sanitized = re.sub(r'(?i)<script[^>]*>', '', sanitized)
    return render_template('xss_reflected.html', info=info,
                           search=sanitized,
                           sanitized=False)


# ── Lv3: 存储型 XSS（留言板） ──────────────────────────────────────
@xss_bp.route('/3', methods=['GET', 'POST'])
def level3():
    info = level_info(3, '存储型 XSS（留言板）',
                      '评论内容存储在数据库中，每次访问页面都会加载。所有访客都能看到你的 XSS。',
                      '尝试在名字或内容中插入: <script>alert(document.cookie)</script>')
    message = ''

    if request.method == 'POST':
        name = request.form.get('name', '')
        content = request.form.get('content', '')
        conn = get_db()
        conn.execute(
            "INSERT INTO comments (name, content) VALUES (?,?)",
            (name, content)
        )
        conn.commit()
        conn.close()
        message = '评论已提交！'

    conn = get_db()
    comments = [dict(r) for r in conn.execute(
        'SELECT id, name, content, created_at FROM comments ORDER BY id DESC'
    ).fetchall()]
    conn.close()

    return render_template('xss_stored.html', info=info,
                           comments=comments, message=message)


# ── Lv4: DOM 型 XSS ──────────────────────────────────────────────
@xss_bp.route('/4')
def level4():
    info = level_info(4, 'DOM 型 XSS',
                      '输入的内容通过 JavaScript 直接写入页面 DOM，不经过服务端渲染。',
                      '查看源码，找到 JavaScript 中操作 innerHTML 的部分。尝试: <img src=x onerror=alert(1)>')
    return render_template('xss_dom.html', info=info)


# ── Lv5: 存储型 XSS（CSP 绕过） ──────────────────────────────────
@xss_bp.route('/5', methods=['GET', 'POST'])
def level5():
    info = level_info(5, '存储型 XSS + CSP 绕过',
                      '页面开启了 CSP 限制，不允许执行内联脚本和 eval。但仍有办法——注意到 CSP 允许加载同源资源。',
                      'CSP 策略: default-src \'self\'; 尝试寻找同源可控资源注入点，或在 HTML 标签的事件属性中执行 JS。')
    message = ''

    if request.method == 'POST':
        name = request.form.get('name', '')
        content = request.form.get('content', '')
        # 过滤 script 标签但不过滤事件处理器
        sanitized = re.sub(r'(?i)<script[^>]*>.*?</script>', '', content)
        sanitized = re.sub(r'(?i)<script[^>]*>', '', sanitized)
        conn = get_db()
        conn.execute(
            "INSERT INTO comments (name, content) VALUES (?,?)",
            (name, sanitized)
        )
        conn.commit()
        conn.close()
        message = '评论已提交！'

    conn = get_db()
    comments = [dict(r) for r in conn.execute(
        'SELECT id, name, content, created_at FROM comments ORDER BY id DESC'
    ).fetchall()]
    conn.close()

    response = make_response(
        render_template('xss_stored_csp.html', info=info,
                        comments=comments, message=message)
    )
    # CSP: 只允许加载同源资源，禁止内联脚本
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'"
    )
    return response
