from . import BaseAPI


class DoubanAPI(BaseAPI):
    @classmethod
    def read(cls, key_word, num=5):
        """
        从豆瓣读取电影信息，并且更新数据库缓存
        :param key_word:
        :param num:
        :return: list(dict)
        """
        pass

    @classmethod
    def read_all(cls, key_word):
        """

        :param key_word:
        :return: list(dict)
        """
        pass
