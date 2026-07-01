import os
import re
import hashlib
from flask import Blueprint, request, render_template, send_from_directory, abort

upload_bp = Blueprint('upload', __name__, template_folder='../templates')

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_KINDS = ['image/png', 'image/jpeg', 'image/gif', 'text/plain', 'application/x-php', 'text/x-php']

os.makedirs(UPLOAD_DIR, exist_ok=True)


def level_info(num, title, desc, hint):
    return {
        'category': 'upload',
        'level': num,
        'title': title,
        'desc': desc,
        'hint': hint,
    }


def save_file(f):
    if not f or f.filename == '':
        return None, '未选择文件'
    safe_name = f.filename.replace('..', '').replace('/', '').replace('\\', '')
    path = os.path.join(UPLOAD_DIR, safe_name)
    f.save(path)
    return safe_name, None


# ── Lv1: 无过滤 ──────────────────────────────────────────────────
@upload_bp.route('/1', methods=['GET', 'POST'])
def level1():
    info = level_info(1, '无过滤直接上传',
                      '没有任何检查，上传什么文件都行。',
                      '上传一个 PHP webshell，访问 /uploads/你的文件名 即可执行。')
    result = None
    filename = None

    if request.method == 'POST':
        f = request.files.get('file')
        filename, err = save_file(f)
        if err:
            result = {'error': err}
        else:
            result = {'success': f'上传成功！访问路径: /uploads/{filename}'}

    return render_template('upload_level.html', info=info,
                           result=result, filename=filename, level=1)


# ── Lv2: 后缀黑名单绕过 ────────────────────────────────────────────
@upload_bp.route('/2', methods=['GET', 'POST'])
def level2():
    info = level_info(2, '后缀黑名单绕过',
                      '禁止了 .php 后缀，但还有 .phtml .php5 .php7 .Php 等变体，以及 .php. 点绕过。',
                      '尝试: shell.phtml  shell.php5  shell.Php  shell.php.  shell.php%00.png')
    result = None
    BLACKLIST = ['.php', '.php3', '.php4']

    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            ext = os.path.splitext(f.filename)[1].lower()
            if ext in BLACKLIST:
                result = {'error': f'不允许上传 {ext} 文件'}
            else:
                filename, err = save_file(f)
                if err:
                    result = {'error': err}
                else:
                    result = {'success': f'上传成功！路径: /uploads/{filename}'}
        else:
            result = {'error': '未选择文件'}

    return render_template('upload_level.html', info=info,
                           result=result, level=2)


# ── Lv3: MIME 类型检查 ──────────────────────────────────────────
@upload_bp.route('/3', methods=['GET', 'POST'])
def level3():
    info = level_info(3, 'MIME 类型检查绕过',
                      '服务端检查了 Content-Type，只允许图片 MIME。但客户端可控，改一下就行了。',
                      '使用 Burp Suite 或浏览器 DevTools 修改请求的 Content-Type 为 image/jpeg。')
    result = None

    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            # 检查 Content-Type
            content_type = f.content_type or ''
            if 'image/' not in content_type:
                result = {'error': f'只允许上传图片，当前 MIME: {content_type}'}
            else:
                filename, err = save_file(f)
                if err:
                    result = {'error': err}
                else:
                    result = {'success': f'图片上传成功！路径: /uploads/{filename}'}
        else:
            result = {'error': '未选择文件'}

    return render_template('upload_level.html', info=info,
                           result=result, level=3)


# ── Lv4: 文件头内容检查绕过 ──────────────────────────────────────
@upload_bp.route('/4', methods=['GET', 'POST'])
def level4():
    info = level_info(4, '文件头内容检查绕过',
                      '服务端读取文件头部字节判断是否为图片（幻数检查）。可以在 PHP 文件内容前加上图片头。',
                      '准备一个包含 GIF89a 头部 + PHP 代码的文件: GIF89a<?php system($_GET["cmd"]); ?>')
    result = None

    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            head = f.read(6)
            f.seek(0)

            # 检查常见图片幻数
            magic_bytes = {
                b'\x89PNG\r\n': 'PNG',
                b'\xff\xd8\xff': 'JPEG',
                b'GIF89a': 'GIF',
                b'GIF87a': 'GIF',
            }

            detected = None
            for magic, fmt in magic_bytes.items():
                if head.startswith(magic):
                    detected = fmt
                    break

            if not detected:
                result = {'error': '文件头不匹配，只允许图片上传'}
            else:
                filename, err = save_file(f)
                if err:
                    result = {'error': err}
                else:
                    result = {'success': f'{detected} 图片上传成功！路径: /uploads/{filename}'}
        else:
            result = {'error': '未选择文件'}

    return render_template('upload_level.html', info=info,
                           result=result, level=4)


# ── Lv5: 多重过滤综合绕过 ──────────────────────────────────────────
@upload_bp.route('/5', methods=['GET', 'POST'])
def level5():
    info = level_info(5, '多重过滤综合绕过',
                      '综合了后缀黑名单、MIME 检查、文件头检查。需要组合前面的所有技巧。',
                      '文件头 + MIME 修改 + 大小写/双重后缀（如 .php.jpg 或 .pHp 等）')
    result = None
    BLACKLIST_EXT = ['.php', '.php3', '.php4', '.php5', '.phtml', '.pht']

    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            # 1. 后缀检查
            ext = os.path.splitext(f.filename)[1].lower()
            if ext in BLACKLIST_EXT:
                result = {'error': '不允许上传此文件类型'}
                return render_template('upload_level.html', info=info, result=result, level=5)

            # 2. MIME 检查
            if f.content_type and 'image/' not in f.content_type:
                result = {'error': 'MIME 类型不匹配'}
                return render_template('upload_level.html', info=info, result=result, level=5)

            # 3. 文件头检查
            head = f.read(6)
            f.seek(0)
            is_image = any(
                head.startswith(m)
                for m in [b'\x89PNG\r\n', b'\xff\xd8\xff', b'GIF89a', b'GIF87a']
            )
            if not is_image:
                result = {'error': '文件头不是图片格式'}
                return render_template('upload_level.html', info=info, result=result, level=5)

            # 全部通过
            filename, err = save_file(f)
            if err:
                result = {'error': err}
            else:
                result = {'success': f'上传成功！路径: /uploads/{filename}'}
        else:
            result = {'error': '未选择文件'}

    return render_template('upload_level.html', info=info,
                           result=result, level=5)


# ── 资源文件访问 ──────────────────────────────────────────────────
@upload_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_from_directory(UPLOAD_DIR, filename)
