import json
import logging
import os
import sys

import uuid_utils.compat as uuid
from asgiref.sync import sync_to_async
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING)
logging.getLogger("mcp").setLevel(logging.ERROR)
logging.getLogger("mcp.server").setLevel(logging.ERROR)


def app_mcp_init(base_dir: str, application_id: str, name: str, description: str):
    import django

    sys.path.insert(0, base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maxkb.settings")

    django.setup()
    mcp = FastMCP()

    @sync_to_async
    def _get_chat_id():
        from application.models import ChatUserType
        from chat.serializers.chat import OpenChatSerializers
        from common.init import init_template

        init_template.run()

        return OpenChatSerializers(data={
            'application_id': application_id,
            'chat_user_id': str(uuid.uuid7()),
            'chat_user_type': ChatUserType.ANONYMOUS_USER,
            'debug': False
        }).open()

    @sync_to_async
    def _chat_with_ai(chat_id: str, message: str) -> str:
        from application.models import ChatUserType
        from chat.serializers.chat import ChatSerializers

        payload = {
            'message': message,
            'stream': False,
            're_chat': False
        }
        resp = ChatSerializers(data={
            'chat_id': chat_id,
            'chat_user_id': str(uuid.uuid7()),
            'chat_user_type': ChatUserType.ANONYMOUS_USER,
            'application_id': application_id,
            'debug': False,
        }).chat(payload)
        data = json.loads(str(resp.text))
        return str(data.get("data", {}).get("content") or data.get("response"))

    @mcp.tool(description=f'{name} {description}')
    async def ai_chat(message: str) -> str:
        chat_id = await _get_chat_id()
        reply = await _chat_with_ai(chat_id, message)

        return reply or "AI 未能生成回复"

    mcp.run(transport='stdio')


app_mcp_init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
