import scrapy
import re
from scrapy.http import HtmlResponse
import json
import os
from dotenv import load_dotenv
from copy import deepcopy
from instaparser.items import InstaparserItem
load_dotenv()
USERNAME = os.environ.get("USERNAME_INST", None)
PASSWORD = os.environ.get("PASSWORD", None)


class SubscriptionsInstaSpider(scrapy.Spider):
    name = 'subscriptions_insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = USERNAME
    inst_pswd = PASSWORD
    parse_users = ['artificialintelligencefacts', 'drikis.ru', 'welcome.ai']
    query_hash_posts = '8c2a529969ee035a5063f2fc8602a0fd'
    api_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_url,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pswd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        for parse_user in self.parse_users:

            j_data = response.json()
            if j_data['authenticated']:
                yield response.follow(
                    f'/{parse_user}',
                    callback=self.parse_subscriptions_data,
                    cb_kwargs={'username': parse_user}
                )

    def parse_subscriptions_data(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        max_id = None
        url_posts = f'{self.api_url}{user_id}/following/?count=12'

        yield response.follow(url_posts,
                              callback=self.subscriptions_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'max_id': max_id
                                         },
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

    def subscriptions_parse(self, response: HtmlResponse, username, user_id, max_id):
        j_data = response.json()

        page_max_id = j_data.get("next_max_id")
        if j_data.get("next_max_id"):
            max_id = page_max_id

        url_posts = f'{self.api_url}{user_id}/following/?count=12&max_id={max_id}'
        yield response.follow(url_posts,
                              callback=self.subscriptions_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'max_id': deepcopy(max_id)
                                         },
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

        subscriptions = j_data.get('users')
        for i in subscriptions:
            if i['pk'] and i['username']:
                subscriptions_id = i.get('pk')
                subscriptions_username = i.get('username')
                subscriptions_photo = i.get('profile_pic_url')
                item = InstaparserItem(
                    username=username,
                    user_id=user_id,
                    friendships_id=subscriptions_id,
                    friendships_username=subscriptions_username,
                    friendships_photo=subscriptions_photo
                )
                yield item


        # Получаем токен для авторизации

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

        # Получаем id желаемого пользователя

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')