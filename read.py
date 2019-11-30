from requests import get, post, put
from pprint import pprint as pp


def es_select_mapping():
    """
    查看集群安装了哪些插件
    """
    api_url = "/keywords/_mapping"

    resp = get(base_url + api_url).json()
    pp(resp)


def es_select_plugins():
    """
    查看集群安装了哪些插件
    """
    api_url = "/_cat/plugins"

    resp = get(base_url + api_url)
    print(resp.text)


def get_cluster_health():
    resp = get(base_url + '/_cluster/health').json()
    pp(resp)


def sort_index_docs():
    resp = get(base_url + '/_cat/indices?v&s=docs.count:desc')
    print(resp.text)


def get_current_node_info():
    resp = get(base_url).json()
    pp(resp)


def search_index():
    # 查看    包括****  的所有Index
    resp = get(base_url + '/_cat/indices/kibana*?v&s=index')

    # 查看所有Index
    # resp = get(base_url + '/_cat/indices?v&s=index')

    # 查看所有Index状态是绿色的
    # resp = get(base_url + '/_cat/indices?v&health=green')

    print(resp.text)


def get_all_node_info():
    resp = get(base_url + '/_cat/nodes?v')
    print(resp.text)


def get_shard_info():
    resp = get(base_url + '/_cat/shards?&v')
    print(resp.text)


def get_custom_field_index():
    resp = get(base_url + '/_cat/indices/kibana*?pri&v&h=health,index,pri,rep,docs,count,mt')
    print(resp.text)


def get_index_info():
    resp = get(base_url + '/keywords').json()
    pp(resp)


def es_count():
    """
    类似sql的length
    """
    api_url = "/keywords/_count"
    data = {
        "query": {
            "match_all": {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def get_document_info():
    resp = get(base_url + '/keywords/_doc/1').json()
    pp(resp)


def es_sort():
    """
    最好在"数字型"与"日期型"字段上进行排序
    因为对于多值类型或分析过的字段, 系统会选取一个值, 无法得知该值
    """

    api_url = "/keywords/_search"
    data = {
        "sort": [
            {"searchavg7days": "desc"}
        ],
        "query": {
            "match_all": {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_count_limit():
    """
    获取靠后的结果, 成本较高, 默认返回10个结果
    """
    api_url = "/keywords/_search"
    data = {
        "from": 0,
        "size": 3,
        "query": {
            "match_all": {}
        }
    }
    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_filter():
    """
    类似select 返回指定字段
    """
    api_url = "/kibana_sample_data_ecommerce/_search"

    data = {
        "_source": ["category"],
        "query": {
            "match_all": {}
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_select():
    """
    查找, 默认是or关系, 要么是糖, 要么是果
    """
    api_url = "/keywords/_search"

    data = {
        "query": {
            "match": {
                "keyword": '糖 批发'
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_select_and():
    """
    查找, and关系, 也就是同时出现
    """
    api_url = "/keywords/_search"

    data = {
        "query": {
            "match": {
                "keyword": {
                    "query": "糖 果",
                    "operator": "AND"
                }
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def find_many_field():
    params = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "keyword": '糖'
                        }
                    },
                    {
                        "match": {
                            "category": '软糖'
                        }
                    }
                ]
            }
        }
    }
    resp = get(base_url + '/keywords/_search', json=params, headers=headers).json()
    pp(resp)


def es_phrase_match():
    """
    短语查询, 在query里出现的这些term必须是按照顺序出现的
    slop代表每个term中间可以允许有n个字符介入
    """
    api_url = "/keywords/_search"

    data = {
        "query": {
            "match_phrase": {
                "关键词": {
                    "query": "糖 果",
                    "slop": 1
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
    api_url = "/keywords/_search"

    data = {
        "query": {
            "query_string": {
                "default_field": "关键词",
                "query": "糖 AND 果"
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def es_use_many_fileds_selcet():
    """
    指定多字段查询
    """
    api_url = "/keywords/_search"

    data = {
        "query": {
            "query_string": {
                "fields": ["关键词", "推荐理由"],
                "query": "(糖 AND 果) OR (糖)"
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
    api_url = "/keywords/_search"

    data = {
        "query": {
            "simple_query_string": {
                "query": "糖 AND 果",
                "fields": ["关键词"]
            }
        }
    }

    resp = post(base_url + api_url, headers=headers, json=data).json()
    pp(resp)


def get_index_template():
    resp = get(base_url + '/_template').json()
    pp(resp)


def get_index_settings():
    resp = get(base_url + '/_settings').json()
    pp(resp)


if __name__ == "__main__":
    headers = {
        "Content-Type": "application/json"
    }
    base_url = "http://localhost:9200"

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

    # es_select_mapping()  # 查看指定Index的mapping
    # get_index_settings()  # 查看指定Index的Settings
    # get_index_info()    # 查看指定Index的Mapping和Settings
    # es_select_plugins()  # 查看集群安装了哪些插件
    # get_current_node_info()  # 查看当前节点信息
    # get_all_node_info()  # 查看集群内所有节点信息
    # get_index_template()  # 查看Index模板
    # get_cluster_health()  # 查看集群健康程度
    # get_document_info()  # 查看指定Index里的具体一个文档
    # search_index()  # 查看 目前已有的Index,  里面有各种方法
    # sort_index_docs()  # 查看所有Index, 根据文档数量进行排序
    # get_custom_field_index()  # 查看所有Index, 只获取某些列
    # get_shard_info()  # 查看分区的信息

    # es_count()  # 查看Index文档数量
    # es_sort()  # 对某字段进行排序
    # es_count_limit()  # 分页
    # es_filter()  # 返回指定字段, 过滤没用字段

    # es_select()  # 指定一个字段查询, 字段=值
    # es_select_and()  # 指定一个字段查询, 两个字段查询一个结果, 同上面的另外一种写法
    # es_use_fileds_selcet()  # 指定一个字段查询, 同上上的另外一种写法
    # simple_query_string_query()  # 简单查询语法, 用得少
    # es_use_many_fileds_selcet()  # 指定多个字段查询, 查询相同的结果
    # find_many_field()  # 查询不同字段的不同值

    # es_phrase_match()  # 短语搜索, 词必须是按照先后顺序出现, 中间允许有几个字符串介入
