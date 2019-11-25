from requests import get, post, put
from pprint import pprint as pp
from ujson import dumps


def es_concat():
    """
    在某个字段上做操作, 类似MySQL的一些方法
    我测试了一下, 中文字符串不可以
    数字型 可以   拼接字符串, 可以加减乘除
    """
    api_url = '/keywords/_search'

    data = {
        "script_fields": {
            "new_field": {
                "script": {
                    "lang": "painless",
                    "source": "doc['竞争指数'].value*5"
                }
            }
        },
        "query": {
            "match_all": {}
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_update_dynamic():
    """
    dynamic自动检测类型

                     'true'      'false'     'strict'
    文档可被索引      yes         yes         no
    字段可别索引      yes         no          no
    Mapping别更新      yes         no          no

    当dynamic被设置成false时候, 存在新增字段的数据写入, 该数据可以被索引, 但是新增字段会被丢弃
    当设置成Strict模式时候, 数据直接写入出错
    """
    api_url = '/keywords/_mapping'

    data = {
        'dynamic': 'true'
    }

    resp = put(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_update_mapping():
    """
    mapping有点类似mysql的表定义概念, 但还不是意义上的表概念, 稍微有点区别
    """
    api_url = '/keywords'

    data = {
        "mappings": {
            'properties': {
                '关键词': {
                    'type': 'text',
                    # 'index': 'false'
                },
                '竞争指数': {
                    'type': 'text',

                    # 控制当前字段是否被索引, 默认为true, 如果设置成false 该字段不可被索引
                    # 比如不希望手机号被人搜索到
                    # 不能被索引, 也会节省许多开销, 倒排索引就不会被创建
                    # 'index': 'false',

                    # 四种不同级别的配置, 可以控制倒排索引记录的内容
                    #   docs - 记录doc id
                    #   freqs - 记录doc id和term frequencies
                    #   positions - 记录doc id / term frequencies / term position
                    #   offsets - 记录doc id / term frequencies / term position / character offsets
                    # Text类型的默认记录positions, 其他默认为docs
                    # 记录的内容越多 占用空间存储越大
                    'index_options': 'positions'  # 有此选项, index用不了
                }
            }
        }
    }

    resp = put(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_update_null_value():
    """
    需要对Null值进行搜索
    插入某些文档字段的值为Null, 后续还要针对Null值进行搜索

    查询的时候value应该被设置成'NULL'才可以被索引
    """
    api_url = '/keywords'

    data = {
        "mappings": {
            'properties': {
                '关键词': {
                    'type': 'keyword',
                    'null_value': 'NULL'
                }
            }
        }
    }

    resp = put(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_copy_to():
    """
    只需要对fullName查询, 即包括了关键词和竞争指数查询
    不会出现在_source找那个
    满足特定的搜索需求
    """
    api_url = '/keywords'

    data = {
        "mappings": {
            'properties': {
                '关键词': {
                    'type': 'keyword',
                    'copy_to': 'fullName'
                },
                '测试字段': {
                    'type': 'keyword',
                    'copy_to': 'fullName'
                }
            }
        }
    }

    resp = put(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_anaylizer_delete_html():
    """
    分词, 去掉html标签
    """
    api_url = '/_analyze'

    data = {
        'tokenizer': 'keyword',
        'char_filter': ['html_strip'],
        'text': '<b>hello world</b>'
    }

    resp = post(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_anaylizer_replace_str():
    """
    分词, 把 "-" 替换成 "_"
    """
    api_url = '/_analyze'

    data = {
        'tokenizer': 'standard',
        'char_filter': [
            {
                'type': 'mapping',
                'mappings': ['- => _', ':) => happy']
            }
        ],
        # 替换表情符号
        'text': '123-456, I-test! test-990 650-555-1234! i am very :)'
    }

    resp = post(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_anaylizer_re():
    """
    分词, 正则匹配
    """
    api_url = '/_analyze'

    data = {
        'tokenizer': 'standard',
        'char_filter': [
            {
                'type': 'pattern_replace',
                'pattern': 'http://(.*)',
                'replacement': '$1'
            }
        ],
        'text': 'http://elastic.co'
    }

    resp = post(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_anaylizer_path():
    """
    分词, 区分目录
    """
    api_url = '/_analyze'

    data = {
        'tokenizer': 'path_hierarchy',
        'text': '/user/ymruan/a/b/c/d/e'
    }

    resp = post(base_url + api_url, headers=headers, data=dumps(data)).json()
    pp(resp)


def es_anaylizer_whitespace():
    """
    分词, 切分空格, 过滤stop停用词
    """
    api_url = '/_analyze'

    data = {
        'tokenizer': 'whitespace',
        'filter': ['lowercase', 'stop'],
        'text': ['The rain in Spain falls mainly on the plain.']
    }

    resp = get(base_url + api_url, headers=headers, data=dumps(data)).json()
    # 大写的The不会过滤, 因为没有转换成小写
    # 先转换成小写, 在过滤停用词
    pp(resp)


if __name__ == '__main__':
    headers = {
        "Content-Type": "application/json"
    }
    base_url = 'http://localhost:9200'

    # 类似sql方法, 对字段进行操作
    # es_concat()
    # 更新mapping dynamic
    # es_update_dynamic()
    # 修改mapping
    # es_update_mapping()
    # 修改null值, 为后续查找做准备
    # es_update_null_value()
    # 查询多个字段, 在7.0版本之前是all
    # es_copy_to()
    # 分词, 去除html标签
    # es_anaylizer_delete_html()
    # 分词, 进行替换
    # es_anaylizer_replace_str()
    # 分词, 正则匹配
    # es_anaylizer_re()
    # 分词, 区分路径
    # es_anaylizer_path()
    # 分词, 切分空格,过滤停用词
    es_anaylizer_whitespace()
