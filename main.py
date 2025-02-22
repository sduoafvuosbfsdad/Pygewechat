from Pygewechat import *
import GPUtil
import ollama

client = GeWechatClient(
    base_url = 'http://127.0.0.1:2531/v2/api',
    app_id = 'wx__QJH_UXoV_pqQFrGisM2q',
    uuid = 'geKLOqmg-LzEtbT1FOIr',
    skip_init = True
)

verified = {
    'wxid_yeh2c6fejbtq22':'zsh',
    'wxid_grxdzlt00mq622':'yx',
    'wxid_4nrc6twf7yjk22':'yls'
}

@client.event('on_message')
def on_message(message: Objects.TextMessage):
    print(f'{message.sender.id} -> {message.recipient.id}: {message.content}')
    if message.sender.id in verified:
        if message.content.startswith('[憨笑]'):
            command = message.content.replace('[憨笑]', '')
            if command == '显卡占用' or command == 'GPUStatus':
                response = ''
                for i in GPUtil.getGPUs():
                    response += f'GPU名称：{i.name} 显存占用：{i.memoryUsed:.2f}/{i.memoryTotal:.2f} GPU占用：{i.load * 100:2f}% 温度：{i.temperature}°C\n'
                client.send_message(message.sender, response)
                return

            elif command == '搜索' or command == 'Search':
                pass

        else:
            response = ollama.chat(
                model = 'deepseek-r1:8b',
                messages = [
                    {
                        'role': 'user',
                        'content': message.content
                    }
                ]
            )
            client.send_message(message.sender, response.message.content)

print(client.app_id)

client.mainloop()