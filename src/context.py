from src.common import *


class Context:

    __hashtag__ = None
    __append_timestamp__ = False
    __send_db__ = False
    __self_importing__ = False

    @staticmethod
    def append_hashtag(hashtag):
        Context.__hashtag__ = hashtag

    @staticmethod
    def append_timestamp(ll):
        Context.__append_timestamp__ = ll

    @staticmethod
    def send_me_db(ll):
        Context.__send_db__ = ll

    @staticmethod
    def solo_importing(ll):
        Context.__self_importing__ = ll
