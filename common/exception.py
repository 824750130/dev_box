from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

error_log = logging.getLogger('')


def custom_exception_handler(exc, context):
    '''重定义异常(使异常返回值符合规范)'''
    # 先让drf内部做处理
    response = exception_handler(exc, context)
    # drf处理过得异常 可以按照自己的规范来返回
    if response:
        '''drf内部错误'''
        detail = response.data.get('detail')
        if detail:
            # error_log.warning('err_type:%s, err_detail:%s' % (detail.code, detail))
            if detail.code == 'authentication_failed':
                return Response({"code": 1001, "msg": detail})
            else:
                return Response({"code": 1001, "msg": detail})
        return response
    # 没有经过drf处理的异常比如代码报错 我们可以捕捉下来写入日志
    else:
        '''异常写入日志'''
        error_views = context['view']
        error_info = repr(exc)
        error_line = []
        trace = exc.__traceback__
        while trace:
            error = '"%s"  line %s' % (trace.tb_frame.f_code.co_filename, trace.tb_lineno)
            error_line.append(error)
            trace = trace.tb_next
        # error_log.error(f'error_views:{error_views} | error_info:{error_info} | error_line:{error_line[::-1]}')
        error = '服务器内部错误'

        return Response({"code": 1001, "msg": error}, status=500)
