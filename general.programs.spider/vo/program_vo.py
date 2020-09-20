class program:
    # 学校名称
    college_name = ''
    # 院系所
    department = ''
    # 专业
    domain = ''
    # 研究方向
    research = ''
    # 拟招人数
    invite_amount = ''
    # 学习方式
    learing_style = ''
    # 考试方式
    examination_means = ''
    # 指导老师
    adviser = ''
    # 专业课程一
    subject_1 = ''
    # 专业课程二
    subject_2 = ''
    # 英语科目
    english = ''
    # 考试范围详情地址
    url_detail = ''

    # 专业课程一
    subject_1_2 = ''
    # 专业课程二
    subject_2_2 = ''
    # 英语科目
    english_2 = ''


    def toString(self):
        if self.english_2 != '':
            print(self.college_name, self.department, self.domain, self.research, self.invite_amount,
                  self.learing_style, self.examination_means, self.adviser, self.subject_1,
                  self.subject_2, self.english, self.url_detail,
                  self.subject_1_2, self.subject_2_2, self.english_2)
        else:
            print(self.college_name, self.department, self.domain, self.research, self.invite_amount,
              self.learing_style, self.examination_means, self.adviser, self.subject_1,
              self.subject_2, self.english, self.url_detail)

    def outputString(self):
        result = f'{self.college_name}\t{self.department}\t{self.domain}\t{self.research}\t{self.invite_amount}\t{self.learing_style}\t{self.examination_means}\t{self.adviser}\t{self.subject_1}\t{self.subject_2}\t{self.english}\t{self.url_detail}\t{self.subject_1_2}\t{self.subject_2_2}\t{self.english_2}'
        print(result)
        return result
