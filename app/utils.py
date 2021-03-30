from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for
import os
import uuid
from PIL import Image


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def random_filename(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# 图片压缩
def compress_image(fp, after=1500000, step=6, quality=90):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param after: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = os.path.getsize(fp)
    if o_size <= after:
        return
    while o_size > after:
        im = Image.open(fp)
        im.save(fp, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = os.path.getsize(fp)
