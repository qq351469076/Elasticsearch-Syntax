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


def single_agg():
    """
    按照目的地进行Bucket统计
    """
    data = {
        # 做聚合不应返回结果, 所以此处应该是0
        "size": 0,
        # 聚合函数
        "aggs": {
            # 自定义聚合之后的名字
            "flight_dest": {
                # term不会做分词
                # terms将input作为一个整体, 不进行任何分词, 而Index会对每个文档做索引, 索引的词和input匹配不上
                # 所以有可能会匹配不到, 需要对字段.keyword进行精确匹配, 如本次的DestCountry.keyword
                "terms": {
                    # 对DestCountry字段进行分桶聚合
                    "field": "DestCountry"
                }
            }
        }
    }
    resp = get(base_url + '/kibana_sample_data_flights/_search', headers=headers, json=data).json()
    pp(resp)


def many_agg():
    """
    多字段聚合
    """
    data = {
        "size": 0,
        "aggs": {
            "flight_dest": {
                "terms": {
                    "field": "DestCountry"
                },
                "aggs": {
                    "avg_price": {
                        # Metric方法, 求平均
                        "avg": {
                            "field": "AvgTicketPrice"
                        }
                    },
                    "max_price": {
                        # 求最大
                        "max": {
                            "field": "AvgTicketPrice"
                        }
                    },
                    "min_price": {
                        # 求最小
                        "min": {
                            "field": "AvgTicketPrice"
                        }
                    }
                }
            }
        }
    }
    resp = get(base_url + '/kibana_sample_data_flights/_search', headers=headers, json=data).json()
    pp(resp)


def agg_and_status():
    data = {
        "size": 0,
        "aggs": {
            "flight_dest": {
                "terms": {
                    "field": "DestCountry"
                },
                "aggs": {
                    "start_price": {
                        # stats方法
                        "stats": {
                            # 对AvgTicketPrice字段进行count, sum, avg, max, min
                            "field": "AvgTicketPrice"
                        }
                    },
                    "weather": {
                        "terms": {
                            # 对DestWeather字段聚合, 比如大雪天有多少天, 雾天有多少天
                            "field": "DestWeather",
                            # 聚合后的结果显示多少条, 如果有6条, 只显示前5条
                            "size": 5
                        }
                    }
                }
            }
        }
    }
    resp = get(base_url + '/kibana_sample_data_flights/_search', headers=headers, json=data).json()
    pp(resp)


def difficult_query():
    """
    将Query转成Filter, 忽略TF-IDF计算, 避免相关性算分的开销
    Filter可以有效利用缓存
    """
    data = {
        "explain": 'true',
        "query": {
            "constant_score": {
                "filter": {
                    # Term是表达语意的最小单位, 搜索和利用统计语言语言模型进行自然语言处理都需要处理Tem
                    # 在ES中, Term查询, 对input不做分词, 会将input作为一个整体, 在倒排索引中查找准确的词项,
                    # 并且使用相关度算分公式为每个包含该词项的文档进行相关度算分 - 例如"App Store"
                    # 通过constant_score将查询转成一个Filtering, 避免算分, 并利用缓存, 提高性能
                    # term要查询的字段, 如果是多值字段, 也会出现在结果里, 因为term的查询是包含, 而不是等于
                    "term": {
                        # 词 必须要 精准 才能准确命中, 同时对字段.keyword进行精确取值
                        "keyword.keyword": "糖"
                    }
                }
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def range_query():
    data = {
        "query": {
            "constant_score": {
                "filter": {
                    # 数字范围查询, 不进行打分
                    "range": {
                        "searchavg7days": {
                            "gte": 1000,
                            "lte": 2000
                        }
                    }
                }
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def date_query():
    data = {
        "query": {
            "constant_score": {
                "filter": {
                    # 数字范围查询, 不进行打分
                    "range": {
                        # 对date字段进行日期查询
                        "date": {
                            # 时间必须大于一年以前
                            # y 年      M 月        d 天
                            # w 周      H/h 小时     m 分钟     s 秒
                            "gte": 'now-1y'
                        }
                    }
                }
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def exist_query():
    data = {
        "query": {
            "constant_score": {
                "filter": {
                    "exists": {
                        # 查询包含keyword字段的文档
                        "field": "keyword"
                    }
                }
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
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

    # single_agg()  # 单字段桶聚合
    # many_agg()  # 多字段聚合
    # agg_and_status()  # 求agg和status方法

    # es_select()  # match查询, 指定一个字段查询, 字段=值
    # es_select_and()  # match查询, 指定一个字段查询, 两个字段查询一个结果, 同上面的另外一种写法
    # es_use_fileds_selcet()  # match查询, 指定一个字段查询, 同上上的另外一种写法
    # simple_query_string_query()  # match查询, 简单查询语法, 用得少
    # es_use_many_fileds_selcet()  # match查询, 指定多个字段查询, 查询相同的结果
    # find_many_field()  # match查询, 查询不同字段的不同值
    difficult_query()  # term查询, 复合型查询 Constant Score转为Filter, 去掉相关性算分
    # range_query()  # 数值范围查询, 不进行打分
    # date_query()  # 日期范围查询, 不进行打分
    # exist_query()  # 查询包含某字段的文档, 同时不进行打分

    # es_phrase_match()  # 短语搜索, 词必须是按照先后顺序出现, 中间允许有几个字符串介入
