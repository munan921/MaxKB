import hashlib
import hmac
import time
from functools import wraps

from django.http import JsonResponse

from maxkb.const import CONFIG


def mcp_token_required(view_func):
    """MCP内部令牌验证装饰器"""

    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # 1. 验证IP白名单
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip not in ['127.0.0.1', '::1']:
            return JsonResponse({'code': 403, 'message': 'Access denied'}, status=403)

        # 2. 验证MCP令牌
        mcp_token = request.headers.get('X-MCP-Token')
        timestamp = request.headers.get('X-MCP-Timestamp')

        # 允许无令牌请求通过
        if not mcp_token or not timestamp:
            return view_func(self, request, *args, **kwargs)

        # 3. 验证时间戳(防止重放攻击,5分钟有效期)
        try:
            ts = int(timestamp)
            if abs(time.time() - ts) > 300:  # 5分钟
                return JsonResponse({'code': 401, 'message': 'Token expired'}, status=401)
        except ValueError:
            return JsonResponse({'code': 401, 'message': 'Invalid timestamp'}, status=401)

        # 4. 验证令牌签名
        secret = CONFIG.get('MCP_INTERNAL_SECRET', 'your-secret-key')

        # 从Authorization获取API Key
        auth_header = request.headers.get('Authorization', '')
        api_key = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else ''

        # 重新计算签名
        token_data = f"{api_key}:{timestamp}"
        expected_token = hmac.new(
            secret.encode(),
            token_data.encode(),
            hashlib.sha256
        ).hexdigest()

        # print(expected_token, mcp_token)

        if not hmac.compare_digest(mcp_token, expected_token):
            return JsonResponse({'code': 401, 'message': 'Invalid MCP token'}, status=401)

        return view_func(self, request, *args, **kwargs)

    return wrapper
