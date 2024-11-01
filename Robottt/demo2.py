import asyncio
import json
import subprocess
import time
from pathlib import Path
from khl import Bot, Message, command, EventTypes, Event, MessageTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from loguru import logger
from datetime import datetime, timedelta
import tools
import logging
from khl.requester import HTTPRequester
from tools import c1,c2,c3,c4,c5,c6,c7
import os

config_file = os.path.join(Path(os.path.abspath(os.sep)), 'config', 'robot.yaml')
press_file = os.path.join(Path(os.path.abspath(os.sep)), 'config', 'dummy.yaml')
data = tools.readYaml(config_file)
logging.basicConfig(level='INFO')

bot_xiaoliu = data['bot']['a6']
bot = Bot(bot_xiaoliu)
channel_id_a6 = data['channel']['channel_a6']
logger.add('a6.log', rotation='500MB', compression='zip')

help = {
    'temp': '发送临时消息',
    'card': '发送卡片消息',
    'single': '发送私聊消息',
}


def channel_rule(msg: Message):
    # 仅对 机器人阿6 这个频道做出响应
    logger.info(f'rule check:msg.target_id is {msg.target_id}')
    return msg.target_id in channel_id_a6


@bot.command(name='6', prefixes=['/', '.'], rules=[channel_rule])
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
    if args and 'single' in args[0].lower():
        target_user = await bot.client.fetch_user(msg.author_id)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        reply_msg = f'现在是北京时间 {current_time} , 我很想你'
        await target_user.send(reply_msg)
        return
    text = ''.join(args)
    reply_msg = f'Receive msg from {msg.author_id} is {msg.content} | Text is {text}'
    await msg.reply(reply_msg)


def miao_rule(msg: Message):
    logger.info(f'rule check:msg.content is {msg.content}')
    return msg.content.find('miao') != -1 or msg.content.find('喵') != -1


@bot.command(name='7', prefixes=['/', '.'], rules=[miao_rule])
async def contain_miao(msg: Message, *args):
    text = ''.join(args)
    await msg.reply(f'Anyone call me ? what is {text}')


@bot.command(name='now', prefixes=['/', '.'], case_sensitive=False)
async def mention_me(msg: Message, *args):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    reply_msg = f'(met){msg.author_id}(met) 现在是 {current_time}'
    await msg.reply(reply_msg)


async def exc_handlers(cmd: command.Command, exception: Exception, msg: Message):
    logger.error(f'Get exception from {msg.author_id}, type is {type(exception)}')
    await msg.reply(f'遇到错误：{type(exception)}')


@bot.command(name='presson', prefixes=['/', '.'], case_sensitive=False)
async def presson(msg: Message, nums: int, times: str):
    timestamp_seconds = int(time.time())
    report_path = f'report_{timestamp_seconds}.html'
    cmd = f'locust -f  .\createMessage4T.py --headless -u {nums} -r 1 -t {times} --html={report_path}'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await msg.reply(f'开始执行：{cmd}')
    stdout_data, stderr_data = await asyncio.gather(
        asyncio.to_thread(process.stdout.read),
        asyncio.to_thread(process.stderr.read)
    )
    output = stderr_data.decode()
    logger.info(f'生成报告：{report_path}')
    file_url = await bot.client.create_asset(f'./{report_path}')
    await msg.reply(file_url, type = MessageTypes.FILE)

@bot.command(name='update', prefixes=['/', '.'], case_sensitive=False)
async def update(msg: Message, *args):
    obj = {'channels':args}
    tools.writeYaml(press_file, obj)
    await msg.reply(f'update done')

count = 0
@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def btn_click_event(b: Bot, e: Event):
    print(f'Receive msg from {e.target_id}, body is {e.body}')
    ch = await bot.client.fetch_public_channel(channel_id_a6)
    global count
    count += 1
    ret = await ch.send(f'Moody Blues stars ++, Now is {count}')


def createCard():
    pass


if __name__ == '__main__':
    bot.run()
