import re


def get_value(href):
    pattern = 'dwmc=([^&]+)'
    matchObj = re.search(pattern, href, re.M | re.I)
    # print(matchObj.group(1))
    return matchObj.group(1)


# \r\n      （101）思想政治理论\r\n      见招生简章
# （204）英语二\r\n      见招生简章
# (923)操作系统原理\r\n    详见北京
def get_project(text):
    matchObj = re.match("(\r\n\s+)?([^\r]+)\r\n.+", text, re.M | re.I)
    # print("[", matchObj.group(2), "]")
    return matchObj.group(2)


# target = "\r\n      （101）思想政治理论\r\n      见招生简章"
# target = "（204）英语二\r\n      见招生简章"
# target = "(923)操作系统原理\r\n    详见北京"
# get_project(target)