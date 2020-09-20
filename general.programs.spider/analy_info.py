from bs4 import BeautifulSoup
from urllib import parse
import reject_regex
from vo.program_vo import program


# 判断当前对象是否为一个数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 获取当前页面表格的页面的数量，最小为1
def get_page_info(response):
    page_num = 0

    # 通过第三方库bs，将获取的页面数据转化为页面对象
    print("开始解析当前页面 ...")
    soup = BeautifulSoup(response.read().decode("utf-8"), 'html.parser')
    # print(type(soup))
    # print(soup)
    # 分析页面，获取页面数据，为后序批量操作做好准备
    print("获取总的页面数量 ...")
    pages = soup.find('div', class_='zsml-page-box')
    each_page = pages.find_all('li', class_='lip')

    for curPage in each_page:
        # print(type(curPage))
        # print(curPage)
        link = curPage.find('a')
        if link is None:
            continue
        elif is_number(link.text):
            page_num += 1

    if page_num == 0:
        page_num = 1

    print("当前表格一共", page_num, "页")
    return page_num


def get_college_on_the_table(response):
    curPageSoup = BeautifulSoup(response.read().decode("utf-8"), 'html.parser')
    return cur_table_handler(curPageSoup)


url_prefix = "https://yz.chsi.com.cn/"


# 解析当前招生单位信息
def cur_table_handler(curPageSoup):
    all_university_this_table = {}

    ch_table = curPageSoup.find('table', class_='ch-table')
    tbody = ch_table.find('tbody')
    trs = tbody.find_all('tr')
    for curTrs in trs:
        a_ = curTrs.find('a')
        # postfix = parse_dwmc(a_['href'].lstrip('/'))
        target_url = url_prefix + a_['href'].lstrip('/')
        # print(a_.text, target_url)
        cur_university = {a_.text: target_url}
        all_university_this_table.update(cur_university)
    return all_university_this_table


# 将urlEncode过的单位名称还原成中文
def parse_dwmc(href):
    urlEncoded_name = reject_regex.get_value(href)
    original_name = parse.unquote(urlEncoded_name)
    href = href.replace(urlEncoded_name, original_name)
    return href


url_list = []


def get_programs_dict(response):
    soup = BeautifulSoup(response.read().decode("utf-8"), 'html.parser')
    # print(soup)
    ch_table = soup.find('table', class_='ch-table')
    t_body = ch_table.find('tbody')
    rows = t_body.find_all('tr')
    for row in rows:
        urls = row.find_all('a', target='_blank')
        for url in urls:
            if url.text == '查看':
                the_url = url_prefix + url['href'].lstrip('/')
                url_list.append(the_url)
    return url_list


def get_program_detail(response_string):
    soup = BeautifulSoup(response_string, 'html.parser')

    detail_table = soup.find('div', class_='zsml-wrapper')

    zsml_condition = detail_table.find('table', class_='zsml-condition')
    zsml_result = detail_table.find('div', class_='zsml-result')

    tr_list = zsml_condition.find_all('tr') # 招生信息详情
    td_list = zsml_result.find_all('td')    # 考试范围

    trList = []
    for tr in tr_list:
        eachLineList = []
        for td in tr.find_all('td', class_='zsml-summary'):
            # print(td.text)
            eachLineList.append(td.text)
        trList += eachLineList

    tdList = []
    for td in td_list:
        if td.text.__contains__("或"):
            continue
        curProgram = reject_regex.get_project(td.text)
        tdList.append(curProgram)

    cur_vo = program()
    cur_vo.college_name = trList[0]
    cur_vo.department = trList[2]
    cur_vo.domain = trList[4]
    cur_vo.invite_amount = trList[8]
    cur_vo.adviser = trList[7]
    cur_vo.learing_style = trList[5]
    cur_vo.research = trList[6]

    cur_vo.subject_1 = tdList[2]
    cur_vo.subject_2 = tdList[3]
    cur_vo.english = tdList[1]

    if len(tdList) > 5:
        cur_vo.english_2 = tdList[5]
        cur_vo.subject_1_2 = tdList[6]
        cur_vo.subject_2_2 = tdList[7]

    return cur_vo
