import time
from get_data import *
import pypresence


async def on_invite_received(args):
    print(args)
    print(f"Получено событие ACTIVITY_JOIN!")


async def ready_funcs(args):
    print(args)
    print("Получено событие ACTIVITY_JOIN_REQUEST!")


async def set_discord_activity(rpc_data, client, is_active):
    try:

        if not rpc_data:
            try:
                await client.clear_activity()
                return None
            except Exception as e:
                return None

        if client is None:
            client = pypresence.AioClient(RPC_CLIENT_ID)
            await client.start()
            await client.register_event("ACTIVITY_JOIN", on_invite_received)
            await client.register_event("ACTIVITY_JOIN_REQUEST", ready_funcs)
            print('Connect to discord')
            print('Ивенты зарегистрированы')

        if is_active:
            start = int(time.time())
            rpc_data['start'] = start
            await client.set_activity(**rpc_data)
            print("Активность установили")

        else:
            await client.clear_activity()
            print("Активность отчистили")

        return client
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        os._exit(0)
