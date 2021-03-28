# meet_love_web
一个好玩的婚恋交友网站程序

## flask-uploads.py 需要修改
26 from werkzeug.utils import secure_filename

27 from werkzeug.datastructures import  FileStorage

## wtfform 版本过高会导致 email 验证缺失， 降低版本即可 2.2.1