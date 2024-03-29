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
        # 查看是如何进行打分的, 26节有讲
        "explain": 'true',
        "query": {
            "constant_score": {
                "filter": {
                    # Term是表达语意的最小单位, 搜索和利用统计语言语言模型进行自然语言处理都需要处理Term
                    # 在ES中, Term查询, 对input不做分词, 会将input作为一个整体, 在倒排索引中查找准确的词项,
                    # 并且使用相关度算分公式为每个包含该词项的文档进行相关度算分 - 例如"App Store"
                    # 通过constant_score将查询转成一个Filtering, 避免算分, 并利用缓存, 提高性能

                    # term要查询的字段, 如果是多值字段, 也会出现在结果里, 因为term的查询是包含, 而不是等于
                    # 如果是多值字段, 在索引的时候, 需要在索引的时候针对多值字段出现的次数进行计数, 且必须用bool查询的must查询多值
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


def bool_query():
    """
    Query Content会对相关性进行算分, 而Filter Content不需要算分, 可以利用Cache, 获得更好的性能

    一个bool查询, 是一个或者多个子查询子句的组合
        总共包括4种子句, 其中2种会影响算分, 2种不影响算分

    bool查询可以嵌套, 查询语句的结构, 会对相关度算分产生影响
        同一级下的竞争字段, 具有相同的权重

    匹配的子句越多, 相关性评分越高, 如果多条查询子句被合并为一条复合查询语句, 比如bool查询,
    则每个查询子句计算得出的评分会被合并到总的相关性评分中
    -------------------------------------
        must              必须匹配, 贡献算分
        should            选择性匹配, 贡献算分, 如果bool查询中没有must条件, should中必须满足一条查询
            should会对里面的语句都进行算分, 针对这里面的结果评分做一个相加, 然后做平均化的处理
        must_not          Filter Content, 查询子句, 必须不能匹配, 不贡献算分
        filter            Filter Content, 必须匹配, 不贡献算分
    """
    data = {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        # price的价格必须是30元
                        "price": 30
                    }
                },
                "filter": {
                    "term": {
                        # 过滤avaliable是true
                        "avaliable": "true"
                    }
                },
                "must_not": {
                    "range": {
                        "price": {
                            # 数值查询, 不能低于30元
                            "lte": 30
                        }
                    }
                },
                # 多选
                "should": [
                    {
                        "term": {
                            # avaliable的精确值应该是test1
                            "avaliable.keyword": "test1"
                        }
                    },
                    {
                        "term": {
                            # avaliable的精确值应该是test1
                            "avaliable.keyword": "test2"
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def boost_query():
    """
    Boosting是控制相关度的一种手段

    举个例子, 多字段有差不多相同的字段, 则优先把相关度高的放在前面

    参数boost的含义
        当 boost > 1时, 打分的相关度相对性提升
        当 0 < boost < 1时, 打分的权重相对性降低
        当 boost < 0时, 贡献负分
    """
    data = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "keyword": {
                                "query": "糖",
                                # 控制相关度
                                "boost": 3
                            }
                        }
                    },
                    {
                        "match": {
                            "keyword": {
                                "query": "糖果",
                                "boost": 1
                            }
                        }
                    }
                ]
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def low_weight_query():
    """
    低权重查询
    举个例子, 文档中有"电子apple"和"apple果汁", 想查询"电子apple", 同时又想把不相关的"苹果果汁"带上, 放到最后
    """
    data = {
        "query": {
            "boosting": {
                "positive": {
                    "match": {
                        "keyword": "apple"
                    }
                },
                "negative": {
                    "match": {
                        "keyword": "pie"
                    }
                },
                "negative_boost": 0.5
            }
        }
    }
    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def disjunction_max_query():
    """
    should会对里面的语句都进行算分, 针对这里面所有的结果评分做一个相加, 然后做平均化的处理

    此结构里, keyword和category有一定关系, 但是是属于竞争的关系, 我们不应该将分数简单叠加, 而是找到单个最佳匹配的字段的评分

    Disjunction Max Query, 同Best Fields默认类型, 不用指定
        将任何与任意查询匹配的文档作为结果返回, 采用字段上最匹配的评分最终评分返回
    """

    # data = {
    #     "query": {
    #         "bool": {
    #             "should": [
    #                 {
    #                     "match": {
    #                         "keyword": "软糖"
    #                     }
    #                 },
    #                 {
    #                     "match": {
    #                         "category": "软糖"
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    # }

    data = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "match": {
                            "keyword": "软糖"
                        }
                    },
                    {
                        "match": {
                            "category": "软糖"
                        }
                    }
                ],
                # 通过Tie Breaker参数调整
                #   1. 获得最佳匹配语句的评分_score
                #   2. 将其他匹配语句的评分与tie_breaker相乘
                #   3. 对以上评分求和并规范化
                "tie_breaker": 0.2
            }
        }
    }

    # data = {
    #     "query": {
    #         "multi_match": {
    #             "type": "best_fields",
    #             "query": "Quick pets",
    #             "fields": [
    #                 "title",
    #                 "body"
    #             ],
    #             "tie_breaker": 0.2,
    #             "minimum_should_match": "20%"
    #         }
    #     }
    # }

    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def most_fields_query():
    """
    无法做Operator操作

    此操作与disjunction_max_query方法相反, 匹配到肉眼觉得正确的词, 本质是通过增加一个子字段来累加相关度
    用广度匹配字段title包括尽可能多的文档--以提高召回率---同时又使用字段title.std作为信号将相关度更高的文档置于结果顶部

    每个字段对于最终评分的贡献可以通过自定义值boost来控制, 比如, 使title字段更为重要, 这样同时也降低了其他信号字段的作用

    """

    # data = {
    #     "mappings": {
    #         "properties": {
    #             "title": {
    #                 "type": "text",
    #                 "analyzer": "english",
    #                 # 子字段并不会对词干进行提取, 控制搜索条件的精度
    #                 "fields": {
    #                     "std": {
    #                         "type": "text",
    #                         "analyzer": "standard"
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }

    data = {
        "query": {
            "multi_match": {
                "query": "barking dogs",
                "type": "most_fields",
                "fields": [
                    # 提高权重
                    "title^10",
                    "title.std"
                ]
            }
        }
    }

    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def cross_query():
    """
    可以通过copy_to解决, 但是需要额外的存储空间, 此操作的优势是可以在搜索时为单个字段提升权重

    可以用most_fields, 但是无法使用Operator
    """

    data = {
        "query": {
            "multi_match": {
                # 这三个词
                "query": "Poland Street W1V",
                "type": "cross_fields",
                # 必须同时
                "operator": "and",
                # 出现在这三个字段当中
                "fields": [
                    "street",
                    "city",
                    "country",
                    "postcode"
                ]
            }
        }
    }

    resp = get(base_url + '/keywords/_search', headers=headers, json=data).json()
    pp(resp)


def function_score_query():
    """
    可以在查询结束后, 对每一个匹配的文档进行一系列的重新算分, 根据新生成的分数进行排序
    提供了集中默认的计算分值的函数
        Weight: 为每一个文档设置一个简单而不被规范化的权重
            新的算分 = 老的算分 * 投票数(votes)
        Field Value Factor: 使用该数值来修改_score, 例如将"热度"和"点赞数"作为算分的参考因素
        Random Score: 为每一个用户使用一个不同的, 随机算分结果
        衰减函数: 以某个字段的值为标准, 距离某个值越近, 得分越高
        Script Score: 自定义脚本完全控制所需逻辑
    """

    # Weight提升权重, 在这个搜索中在继续按照投票数进行额外算分
    # data = {
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "multi_match": {
    #                     "query": "popularity",
    #                     "fields": [
    #                         "title",
    #                         "content"
    #                     ]
    #                 }
    #             },
    #             "field_value_factor": {
    #                 "field": "votes"
    #             }
    #         }
    #     }
    # }

    # 如果投票数有些是0, 有些是100000, 这样_score悬殊就大了, 通过log让数字平滑处理
    # data = {
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "multi_match": {
    #                     "query": "popularity",
    #                     "fields": [
    #                         "title",
    #                         "content"
    #                     ]
    #                 }
    #             },
    #             "field_value_factor": {
    #                 "field": "votes",
    #                 # 通过api进行平滑处理
    #                 "modifier": "log1p"
    #             }
    #         }
    #     }
    # }

    # 引入Factor, 新的算分 * log(1 + factor * 投票数)
    # data = {
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "multi_match": {
    #                     "query": "popularity",
    #                     "fields": [
    #                         "title",
    #                         "content"
    #                     ]
    #                 }
    #             },
    #             "field_value_factor": {
    #                 "field": "votes",
    #                 "modifier": "log1p",
    #                 "factor": 0.1
    #             }
    #         }
    #     }
    # }

    # 还可以采用不同的Boost Mode来计算新的算分, 默认值是Multiply(算分与函数值的成绩)
    #   Sum: 算分与函数的和
    #   Min / Max: 算分与函数取 最小/最大值
    #   Replace: 使用函数值取代算分
    # data = {
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "multi_match": {
    #                     "query": "popularity",
    #                     "fields": [
    #                         "title",
    #                         "content"
    #                     ]
    #                 }
    #             },
    #             "field_value_factor": {
    #                 "field": "votes",
    #                 "modifier": "log1p",
    #                 "factor": 0.1
    #             },
    #             # 使用Boost Mode
    #             "boost_mode": "sum"
    #         }
    #     }
    # }

    # 可以用MAX Boost将算分控制在一个最大值
    data = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": "popularity",
                        "fields": [
                            "title",
                            "content"
                        ]
                    }
                },
                "field_value_factor": {
                    "field": "votes",
                    "modifier": "log1p",
                    "factor": 0.1
                },
                "boost_mode": "sum",
                # 使用Max Boost将算分控制在一个最大值
                "max_boost": 3
            }
        }
    }

    # 一致性随机函数, 同一个seed下得分是一样, 不同seed不同得分
    data = {
        "query": {
            "function_score": {
                "random_score": {
                    "seed": 314159265359
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
    """
    Query Content会对相关性进行算分, 而Filter Content不需要算分, 可以利用Cache, 获得更好的性能
    """
    # difficult_query()  # term查询, 复合型查询 Constant Score转为Filter, 去掉相关性算分
    # bool_query()  # 布尔查询, 可以多条件查询
    # boost_query()  # 控制相关度查询
    # low_weight_query()  # 低权重查询
    # disjunction_max_query()  # 单字符串多字段查询
    # cross_query()  # 跨字段搜索
    function_score_query()  # 查询之后重新算分在进行排序

    # range_query()  # 数值范围查询, 不进行打分
    # date_query()  # 日期范围查询, 不进行打分
    # exist_query()  # 查询包含某字段的文档, 同时不进行打分

    # es_phrase_match()  # 短语搜索, 词必须是按照先后顺序出现, 中间允许有几个字符串介入
