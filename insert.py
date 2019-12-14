from requests import get, post, put
from pprint import pprint as pp
from ujson import dumps


def es_create_index_template():
    """
    帮助设定Mappings和Settings, 并按照一定的规则, 自动匹配到新创建的索引上
    可以设定多个索引模板, 这些设置会被'merge'在一起
    可以指定'order'数值, 控制'merging'的过程

    当一个Index被新创建时
        应用Elasticsearch默认的settings和mappings
        应用order数值低的Index模板中的设定
        应用order数值高的Index模板中的设定, 之前的设定会被覆盖
        应用创建Index时, 用户所指定的Settings和Mappings, 并覆盖之前模板中的设定
    """

    # 定义模板的名称
    api_url = '/_template/template_default'

    data = {
        # 所有Index均采用此模板
        "index_patterns": ["*"],
        "order": 0,
        "version": 1,
        "settings": {
            # 控制副本的分区数量和副本数量
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            # 关闭 日期类型自动识别, "type"会变成"text"
            "date_detection": 'false',
            # 开启 数字类型自动识别
            "numeric_detection": 'true'
        }
    }
    resp = put(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def add_index():
    data = {
        'name': '孔祥旭'
    }

    # put需要指定id才能被索引
    # resp = put(base_url + '/hhhh/_doc/1', json=data, headers=headers).json()

    # post无需指定id
    resp = post(base_url + '/hhhh/_doc', json=data, headers=headers).json()
    pp(resp)


if __name__ == "__main__":
    headers = {
        "Content-Type": "application/json"
    }
    base_url = "http://localhost:9200"

    es_create_index_template()  # 创建Index模板

    add_index()  # 创建一条索引

    # 创建搜索模板   ---> 解耦开发
    # 索引别名   ---> 方便零停机维护
