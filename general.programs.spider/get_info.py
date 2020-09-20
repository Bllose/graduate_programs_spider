import time
from urllib import request, parse


# 获取当前页面(顶层)
def get_top_page(yjxkdm_, xxfs_, page_):
    data = bytes(parse.urlencode({'yjxkdm': yjxkdm_, 'xxfs': xxfs_, 'pageno': page_}), encoding='utf-8')
    return request.urlopen("https://yz.chsi.com.cn/zsml/queryAction.do", data=data)


def get_program_table(url):
    try:
        return request.urlopen(url, timeout=5)
    except:
        print("[", url, "]调用超时，尝试重新调用 ...")
        time.sleep(2)
        return get_program_table(url)


def get(url):
    try:
        return request.urlopen(url, timeout=5)
    except:
        print(url, "请求超时, 准备发起第二次请求")
        time.sleep(2)
        try:
            return request.urlopen(url, timeout=5)
        except:
            print(url, "第二次请求超时，跳过此url")
    return None
