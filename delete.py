from requests import get, post, delete
from pprint import pprint as pp


def es_delete_index():
    """
    删除索引
    """
    api_url = '/keywords'

    resp = delete(base_url + api_url).json()
    pp(resp)


if __name__ == '__main__':
    headers = {
        "Content-Type": "application/json"
    }
    base_url = 'http://localhost:9200'

    # 删除索引
    es_delete_index()
