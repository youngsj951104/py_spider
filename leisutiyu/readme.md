#爬取数据块字段说明

##match

###数据类型

array

###成员参数

####away:客队信息

|字段名称|字段类型|对应含义|
|  ----  |---| ----  |
|name|string|球队名称|
|name_en|string|球队英文名称|
|score|array|得分详情，细节见得分详情|

#####score详情

|||
|  ----  |---|
|score[0]|本场得分|
|score[1]|半场得分|
|score[2]|红牌数|
|score[3]|黄牌数|
|score[4]|角球数|

####com_info：联赛信息

|字段名称|字段类型|对应含义|
|  ----  |---| ----  |
|name|string|联赛名称|

####home:主队信息

|字段名称|字段类型|对应含义|
|  ----  |---| ----  |
|name|string|球队名称|
|name_en|string|球队英文名称|
|score|array|得分详情,细节同客队得分详情|

####id:比赛编号

####matchtime:比赛时间

####round_num：轮次
