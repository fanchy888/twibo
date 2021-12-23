import json

from flask import request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):

    code = 400
    msg = 'sorry，internal error'
    error_code = 999
    data = ''

    def __init__(self, msg=None, code=None, error_code=None, data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        if data:
            self.data = data
        super().__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            msg=self.msg,
        )
        # sort_keys 取消排序规则，ensure_ascii 中文显示
        text = json.dumps(body, sort_keys=False, ensure_ascii=False)
        return text

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_parm():
        full_path = str(request.path)
        return full_path


class ParameterError(APIException):
    def __init__(self, code, msg):
        super().__init__(msg=msg)
        self.code = code
