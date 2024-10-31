import json
import time
from khl import Bot, Message, command, EventTypes, Event
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from loguru import logger
from datetime import datetime, timedelta
import tools
from khl.requester import HTTPRequester
# from tools import c1,c2,c3,c4,c5,c6,c7

data = tools.readYaml('config.yaml')

bot_xiaoliu = data['bot']['a6']
bot = Bot(bot_xiaoliu)
channel_id_a6 = data['channel']['channel_a6']
print(channel_id_a6)
logger.add('a6.log', rotation='500MB', compression='zip')

help = {
    'temp': '发送临时消息',
    'card': '发送卡片消息',
}

async def exc_handlers(cmd: command.Command, exception: Exception, msg: Message):
    print("get exception from", msg.author_id)
    print("exception type:", type(exception))

def channel_rule(msg:Message):
    # 仅对 机器人阿6 这个频道做出响应
    logger.info(f'rule check:msg.target_id is {msg.target_id}')
    return msg.target_id in channel_id_a6


@bot.command(name='6', prefixes=['/', '', '.'],rules=[channel_rule])
async def resp1(msg: Message, *args):
    logger.info(f'receive msg is {msg.content},{msg.target_id},{msg.author_id}')
    reply_msg = None

    if args and 'card' in args[0].lower():
        cm1 = CardMessage(c1, c2, c3, c4, c5)
        cm2 = CardMessage(c6)
        cm_list = [cm1, cm2]
        for cm in cm_list:
            try:
                await msg.reply(cm)
            except HTTPRequester.APIRequestFailed as e:
                logger.error(f'发送card失败：{json.dumps(cm)}')
        return

    if args and 'temp' in args[0].lower():
        reply_msg = 'temp msg only for you'
        await msg.ctx.channel.send(reply_msg, temp_target_id=msg.author.id)
        return
    if args and 'help' in args[0].lower():
        reply_msg = str(help)
        await msg.reply(reply_msg)
        return
    text = ''.join(args)
    reply_msg = f'Receive msg from {msg.author_id} is {msg.content} | Text is {text}'
    await msg.reply(reply_msg)


def miao_rule(msg:Message):
    logger.info(f'rule check:msg.content is {msg.content}')
    return msg.content.find('miao')!= -1 or msg.content.find('喵')!= -1

@bot.command(name='7', prefixes=['/', '', '.'], rules=[miao_rule])
async def mention_me(msg: Message, *args):
    text = ''.join(args)
    await msg.reply(f'Anyone call me ? what is {text}')

@bot.command(name='now', prefixes=['/', '', '.'], case_sensitive=False)
async def mention_me(msg: Message, *args):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    await msg.reply(f'Now is {current_time}')



count = 0


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def btn_click_event(b: Bot, e: Event):
    print(f'Receive msg from {e.target_id}, body is {e.body}')
    ch = await bot.client.fetch_public_channel(channel_id_a6)
    global count
    count += 1
    ret = await ch.send(f'Moody Blues stars ++, Now is {count}')


c1 = Card(
    Module.Header('这是~~标题内容~~'),
    Module.Context('这是小字'),
    Module.Section('这是正文:smile:'),
    Module.Divider(),
    color='#1f1f1f'
)
c2 = Card(
    Module.Section(
        Struct.Paragraph(
            3,
            Element.Text("**这是第一列**\n猴子", type=Types.Text.KMD),
            Element.Text("**这是第二列**\n犀牛", type=Types.Text.KMD),
            Element.Text("**这是第三列**\n熊猫", type=Types.Text.KMD),
        )
    )
)
img_src = 'https://img.kookapp.cn/attachments/2024-10/28/AHPVeUCJGN0k60si.jpeg'
c3 = Card(
    Module.Section(
        Element.Text("忧郁蓝调", type=Types.Text.KMD),
        Element.Image(src=img_src),
        mode=Types.SectionMode.RIGHT
    )
)
img2_src = 'https://img.kookapp.cn/attachments/2024-10/28/UosDrMqY4S0k60si.jpeg'
img3_src = 'https://img.kookapp.cn/attachments/2024-10/28/DPxnfvQbD60k60si.jpeg'
img4_src = 'https://img.kookapp.cn/attachments/2024-10/28/k96abDMXMH0k60si.jpeg'
c4 = Card(
    Module.ImageGroup(
        Element.Image(src=img_src),
        Element.Image(src=img2_src),
        Element.Image(src=img3_src),
        Element.Image(src=img4_src),
    )
)
c5 = Card(
    Module.Section(
        Element.Text("忧郁蓝调", type=Types.Text.KMD),
        Element.Button(
            "点赞",
            value="按钮值1",
            click=Types.Click.RETURN_VAL,
            theme=Types.Theme.INFO,
        ),
    )
)
c6 = Card(
    Module.Countdown(
        datetime.now() + timedelta(seconds=360000), mode=Types.CountdownMode.DAY
    ),
    Module.Countdown(
        datetime.now() + timedelta(seconds=3600), mode=Types.CountdownMode.HOUR
    ),
    Module.Countdown(
        datetime.now() + timedelta(seconds=3600), mode=Types.CountdownMode.SECOND
    )

)
c7 = Card(
    Module.Countdown(
        datetime.now() + timedelta(seconds=60),
        mode=Types.CountdownMode.SECOND,
        start=datetime.now() - timedelta(seconds=30),
    )
)


def createCard():
    pass


if __name__ == '__main__':
    bot.run()
