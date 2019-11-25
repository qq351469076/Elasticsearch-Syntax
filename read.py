from requests import get, post
from pprint import pprint as pp


def es_select_mapping():
    """
    查看集群安装了哪些插件
    """
    api_url = '/keywords/_mapping'

    resp = get(base_url + api_url).json()
    pp(resp)


def es_select_plugins():
    """
    查看集群安装了哪些插件
    """
    api_url = '/_cat/plugins'

    resp = get(base_url + api_url)
    print(resp.text)


def es_count():
    """
    类似sql的length
    """
    api_url = '/keywords/_count'
    data = {
        'query': {
            'match_all': {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_sort():
    """
    最好在"数字型"与"日期型"字段上进行排序
    因为对于多值类型或分析过的字段, 系统会选取一个值, 无法得知该值
    """
    api_url = '/keywords/_search'
    data = {
        'sort': [
            {'竞争指数': 'desc'}
        ],
        'query': {
            'match_all': {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_count_limit():
    """
    获取靠后的结果, 成本较高, 默认返回10个结果
    """
    api_url = '/keywords/_search'
    data = {
        'from': 0,
        'size': 3,
        'query': {
            'match_all': {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_filter():
    """
    类似select 指定字段返回结果
    """
    api_url = '/kibana_sample_data_ecommerce/_search'

    data = {
        '_source': ['category'],
        'from': 0,
        'size': 1,
        'query': {
            'match_all': {}
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_select():
    """
    查找, or关系, 要么是糖, 要么是果
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'match': {
                '竞争指数': 3000
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_select_and():
    """
    查找, and关系, 也就是同时出现
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'match': {
                '关键词': {
                    'query': '糖 果',
                    'operator': 'AND'
                }
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_phrase_match():
    """
    短语查询, 在query里出现的这些term必须是按照顺序出现的
    slop代表每个term中间可以允许有n个字符介入
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'match_phrase': {
                '关键词': {
                    'query': '糖 果',
                    'slop': 1
                }
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_use_fileds_selcet():
    """
    指定字段查询
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'query_string': {
                'default_field': '关键词',
                'query': '糖 AND 果'
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_use_many_fileds_selcet():
    """
    指定多字段查询
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'query_string': {
                'fields': ['关键词', '推荐理由'],
                'query': '(糖 AND 果) OR (糖)'
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def simple_query_string_query():
    """
    类似Query String, 但是会忽略错误的语法, 同时只支持部分查询语法
    不支持 AND OR NOT, 会被当做字符串处理
    TREM之间的默认关系是OR, 可以指定operator
    支持部分逻辑
        + 代替 AND
        | 代替 OR
        - 代替 NOT
    """
    api_url = '/keywords/_search'

    data = {
        'query': {
            'simple_query_string': {
                'query': '糖 AND 果',
                'fields': ['关键词']
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


if __name__ == '__main__':
    headers = {
        "Content-Type": "application/json"
    }
    base_url = 'http://localhost:9200'

    """
    本文核心观点：
        1：查询分URI查询和DSL查询两大类。
            用DSL查询比较多，DSL查询有分term query，match query和一些复合查询。

        2：三种查询的区别
            query 功能强大易出错
            query_string 功能简单灵活性低
            simple_query_string 功能简单灵活性低

        3：老师对于API学习的建议，先广后深
            本节api里面填写的是URI query里的语法。你可以查lucene query syntax。也就是字段名冒号➕数值。
            另外需要了解分组等概念。在我的learning path中，我建议大家先对每一个概念有一个广度优先的了解，都大概使用一下。
    """

    # 查看索引mapping定义
    # es_select_mapping()
    # 查看集群安装了哪些插件
    # es_select_plugins()
    # 查看index数量
    # es_count()
    # 排序
    # es_sort()
    # 分页
    # es_count_limit()
    # 过滤
    # es_filter()
    # 查找, or关系, 要么是糖, 要么是果
    es_select()
    # 查找, and关系, 又有糖又有果
    # es_select_and()
    # 短语搜索
    # es_phrase_match()
    # 指定字段查询
    # es_use_fileds_selcet()
    # 指定多字段查询
    # es_use_many_fileds_selcet()
    # 简单查询语法
    # simple_query_string_query()
