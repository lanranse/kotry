import yaml
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from datetime import datetime, timedelta

def readYaml(file):
    with open(file, 'r', encoding='utf-8') as fr:
        return yaml.load(fr, Loader=yaml.SafeLoader)

c1 = Card(
    Module.Header('这是~~标题内容~~'),
    Module.Context('这是小字'),
    Module.Section('这是正文:smile:'),
    Module.Divider(),
    color = '#1f1f1f'
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




if __name__ == '__main__':
    data = readYaml('config.yaml')
    bot_xiaoliu = data['bot']['a6']
    channel_id_a6 = data['channel']['channel_a6']
    print(bot_xiaoliu)
    print(channel_id_a6)
