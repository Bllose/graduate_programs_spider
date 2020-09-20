import get_info
import analy_info
import sys
import socket
import time
from vo.program_vo import program

# 进入最顶层页面
yjxkdm = '0854'
xxfs = 2
print("一级学科代码:", yjxkdm, " 学习方式", xxfs)
response = get_info.get_top_page(yjxkdm, xxfs, None)
amount_page = analy_info.get_page_info(response)

# 拿到所有学校与学校的专业列表地址
all_university = {}
cur_page = 1
while cur_page <= amount_page:
    print("当前处理第", cur_page, "页数据")
    response = get_info.get_top_page(yjxkdm, xxfs, cur_page)
    print("获取当前桌面上的学院信息 ...")
    cur_table = analy_info.get_college_on_the_table(response)
    if cur_table is not None:
        all_university.update(cur_table)
        cur_page += 1
    else:
        print("当前桌面没有任何学院信息... 结束此段逻辑")
        break
# print(all_university)

# counter = 0

# 通过专业列表地址获取每一栏专业的细节信息地址
all_program_detail_urls = []
for college in all_university:
    url = all_university[college]
    print("当前查询", college, "下所有符合条件的专业目录")

    response = get_info.get_program_table(url)
    amount_page = analy_info.get_page_info(response)

    if amount_page == 1:
        response = get_info.get_program_table(url)
        all_program_detail_urls.append(analy_info.get_programs_dict(response))
    else:
        cur_page = 2
        response = get_info.get_program_table(url)
        all_program_detail_urls.append(analy_info.get_programs_dict(response))
        while cur_page <= amount_page:
            response = get_info.get_program_table(url+"&pageno="+str(cur_page))
            all_program_detail_urls.append(analy_info.get_programs_dict(response))
            cur_page += 1
    # counter += 1
    # if counter == 3:
    #     break

total = len(all_program_detail_urls)
cur = 0
print("一共获取专业信息URL", total, "组")

file_ = "D:/save_programs_detail.txt"
file = open(file_, mode='a+', encoding='utf-8')

# 最终通过细节信息地址获取详细信息
programs_detail = []


def recorder(programs_detail):
    for detail in programs_detail:
        file.write(detail.outputString())
        file.write("\r\n")


for url_list in all_program_detail_urls:
    cur += 1
    print("当前开始分析第", cur, "组专业信息URL")
    for url in url_list:
        print("当前获取地址", url)
        response = get_info.get(url)
        if response is None:
            continue
        try:
            response_string = response.read().decode("utf-8")
        except socket.timeout:
            print("获取反馈报文超时,再次尝试获取 ...")
            time.sleep(2)
            try:
                response_string = response.read().decode("utf-8")
            except:
                print("再次尝试获取返回报文失败,跳过此内容 ...")
                detail = program()
                detail.url_detail = url
                programs_detail.append(detail)
                continue
        except:
            print("Unexception error:", sys.exc_info()[0])
            continue

        detail = analy_info.get_program_detail(response_string)
        detail.url_detail = url
        programs_detail.append(detail)

        if len(programs_detail) >= 100:
            print("100条数据写入文件:", file_)
            recorder(programs_detail)
            programs_detail.clear()

# total = len(programs_detail)
# print("一共获得专业详情", total, "条")

if len(programs_detail) != 0:
    print("剩余数据", str(len(programs_detail)), "将写入文件", file_)
    recorder(programs_detail)


