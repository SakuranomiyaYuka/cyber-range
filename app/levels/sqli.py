from flask import Blueprint, request, render_template
from db import get_db

sqli_bp = Blueprint('sqli', __name__, template_folder='../templates')


def level_info(num, title, desc, hint):
    return {
        'category': 'sqli',
        'level': num,
        'title': title,
        'desc': desc,
        'hint': hint,
    }


# ── Lv1: GET 注入（单引号闭合） ──────────────────────────────────────
@sqli_bp.route('/1', methods=['GET'])
def level1():
    info = level_info(1, '基础 GET 注入', 'URL 参数 id 存在注入，尝试闭合查询获取所有用户数据。', '尝试输入: id=1 OR 1=1')
    result = None
    query = ''
    uid = request.args.get('id', '')

    if uid:
        conn = get_db()
        # 漏洞：直接拼接 SQL
        query = f"SELECT id, username, email, role FROM users WHERE id = {uid}"
        try:
            rows = conn.execute(query).fetchall()
            result = [dict(r) for r in rows]
        except Exception as e:
            result = {'error': str(e)}
        conn.close()

    return render_template('level.html', info=info, result=result, query=query, input=uid)


# ── Lv2: POST 登录绕过 ──────────────────────────────────────────────
@sqli_bp.route('/2', methods=['GET', 'POST'])
def level2():
    info = level_info(2, 'POST 登录绕过', '登录表单存在注入，尝试绕过身份验证以 admin 身份登录。', '尝试用户名: admin\' --')
    result = None
    query = ''

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = get_db()
        # 漏洞：直接拼接 SQL
        query = f"SELECT id, username, email, role FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            rows = conn.execute(query).fetchall()
            result = [dict(r) for r in rows]
        except Exception as e:
            result = {'error': str(e)}
        conn.close()

    return render_template('level_login.html', info=info, result=result, query=query)


# ── Lv3: 布尔盲注 ────────────────────────────────────────────────────
@sqli_bp.route('/3', methods=['GET'])
def level3():
    info = level_info(3, '布尔盲注', '页面不返回数据内容，仅通过"存在/不存在"的布尔状态来判断注入是否成功。', '尝试: id=1\' AND 1=1 --  和  id=1\' AND 1=2 --  观察页面差异')
    result = None
    query = ''
    uid = request.args.get('id', '')

    if uid:
        conn = get_db()
        query = f"SELECT username FROM users WHERE id = {uid}"
        try:
            row = conn.execute(query).fetchone()
            if row:
                result = {'status': 'ok', 'message': f'用户存在: {row["username"]}'}
            else:
                result = {'status': 'not_found', 'message': '用户不存在'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
        conn.close()

    return render_template('level_blind.html', info=info, result=result, query=query, input=uid)


# ── Lv4: 时间盲注 ────────────────────────────────────────────────────
@sqli_bp.route('/4', methods=['GET'])
def level4():
    info = level_info(4, '时间盲注', '页面不显示任何差异，只能通过响应时间长短来判断注入。注意：sleep 时间设得很短，耐心观察。', '尝试: id=1\' OR IF(1=1, SLEEP(2), 0) --')
    result = None
    query = ''
    uid = request.args.get('id', '')

    if uid:
        conn = get_db()
        query = f"SELECT username FROM users WHERE id = {uid}"
        try:
            import time
            start = time.time()
            row = conn.execute(query).fetchone()
            elapsed = round(time.time() - start, 2)
            if row:
                result = {'status': 'ok', 'message': f'查询完成，耗时 {elapsed}s'}
            else:
                result = {'status': 'not_found', 'message': f'查询完成，耗时 {elapsed}s'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
        conn.close()

    return render_template('level_time.html', info=info, result=result, query=query, input=uid)


# ── Lv5: UPDATE 注入 ──────────────────────────────────────────────
@sqli_bp.route('/5', methods=['GET', 'POST'])
def level5():
    info = level_info(5, 'UPDATE 注入', '更新用户信息的接口存在注入。不只是 SELECT 才能注入，UPDATE 也可以。尝试读取 secrets 表中的数据。', '尝试构造子查询更新自己的 email: email=test@a.com, password=123, 在某个字段注入子查询')
    result = None
    query = ''

    if request.method == 'POST':
        uid = request.form.get('id', '1')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        conn = get_db()
        # 漏洞：password 参数直接拼接
        query = f"UPDATE users SET email = '{email}' WHERE id = {uid} AND password = '{password}'"
        try:
            conn.execute(query)
            conn.commit()
            result = {'status': 'ok', 'message': '更新成功！如果修改了当前用户的邮箱，返回上一页刷新即可看到变化。'}
        except Exception as e:
            result = {'error': str(e)}
        conn.close()

    return render_template('level_update.html', info=info, result=result, query=query)
