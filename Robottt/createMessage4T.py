import sys

from locust import HttpUser,task,between
from locust import run_single_user
import os
import tools
from pathlib import Path
from loguru import logger

# channels = ['9097247795165471', '7055894740364371', '2854923845314999', '5127108435170752']
# channels = ['7055894740364371','2854923845314999']
# uids = ['18800010001','18800010002','18800010003','18800010004']
# host = "https://tttt-www.dev.chuanyuapp.com"

config_file = os.path.join(Path(os.path.abspath(os.sep)),'config','dummy-4t.yaml')
data = tools.readYaml(config_file)
logger.info(f'dummy.yaml is {data}')

channels = data['channels']
print(channels)
uids = data['uids']
host = data['host']
invitecode = data['invitecode']
role = data['role']

user_index = 0
auths = []

class UserBahavior(HttpUser):

    wait_time = between(2, 5)
    host = host
    url='/api/v3/message/create'
    index=0
    current_auth = None
    task_executed = False
    uid = None
    auth = None


    def on_start(self) -> None:
        global user_index
        user_current = user_index % len(uids)

        path = '/api/v2/auth/login'
        full_url = self.host + path
        header = {}
        contentType = 'application/json; charset=utf-8'
        header['content-type'] = contentType

        # if uids:
        #     self.uid = uids.pop()
        self.uid = uids[user_current]
        print(f'current user is {self.uid}')

        body = f'{{"mobile":"{self.uid}","password":"kk123456","mobile_prefix":"86","remember":true}}'
        response = self.client.post(full_url,headers=header,data=body)
        if response.status_code == 200:
            auth_data = response.json()['token']
            logger.info(f'{self.uid} 当前的auth：{auth_data}')
            auths.append(auth_data)
        else:
            logger.error(f"Login failed with status code: {response.content}")
            sys.exit(1)
        user_index += 1

        path_join = '/api/v2/guilds/join'
        full_url_join = self.host + path_join

        if auths:
            self.auth = auths.pop()
        header['authorization'] = self.auth
        body = '{"code":"g8oDDl"}'
        response = self.client.post(full_url_join, headers=header, data=body)
        logger.info(f'join 结果：{response.content}')
        result = response.json()['joined']
        assert result == True

    def on_stop(self):
        print("---stop---")

    @task(1)
    def task(self):
        # self.current_auth=self.auths[user_index]
        self.current_auth = self.auth
        print(f'current auth is {self.current_auth}')
        header={}
        authorization=self.current_auth
        contentType='application/json; charset=utf-8'
        header['authorization']=authorization
        header['content-type']=contentType
        content = role +str(self.index) if (self.index)%3 == 0 else str(self.index)
        for channel in channels:
            body = f'{{"type":9,"content":"{content}","nonce":"","target_id":"{channel}"}}'
            print(f'content is {content}')
            if not self.task_executed:
                res=self.client.post(headers=header,data=body,url=self.url)
    #            self.task_executed = True
                logger.info(f'消息发送结果： {res.json()}')
        self.index += 1


if __name__ == '__main__':
    # 单用户模式
    run_single_user(UserBahavior)

