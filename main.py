# -*-coding:utf-8-*-
import asyncio
import os
import platform
import sys
import time

try:
    from httpx import AsyncClient
except ImportError:
    print("请先安装 httpx 库")
    sys.exit(1)
try:
    from prettytable import PrettyTable
except ImportError:
    print("请先安装 prettytable 库")
    sys.exit(1)

# 请修改以下设置
cookie = "COOKIE"  # Cookie, 以 hfs-session-id= 开头
refresh_time = "60"  # 刷新时间, 单位秒
# 配置结束, 请勿修改以下内容


headers = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": cookie
}


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


async def main():
    while True:
        try:
            async with AsyncClient() as client:
                url_exam_list = "https://hfs-be.yunxiao.com/v3/exam/list"
                req = await client.get(url=url_exam_list, headers=headers)
                exam_id = str(req.json()["data"]["list"][0]["examId"])
                exam_name = str(req.json()["data"]["list"][0]["name"])
                exam_score_full = str(req.json()["data"]["list"][0]["manfen"])
                exam_score = str(req.json()["data"]["list"][0]["score"])
                exam_rank_class = str(req.json()["data"]["list"][0]["classRank"])
                url_exam_info = f"https://hfs-be.yunxiao.com/v3/exam/{exam_id}/same-group-analysis"
                req = await client.get(url=url_exam_info, headers=headers)
                exam_score_avg_class = str(req.json()["data"]["classAvg"])
                exam_score_avg_grade = str(req.json()["data"]["gradeAvg"])
                url_exam_detail = f"https://hfs-be.yunxiao.com/v3/exam/{exam_id}/papers-analysis"
                req = await client.get(url=url_exam_detail, headers=headers)
                exam_papers = req.json()["data"]["papers"]
                length_exam_papers = len(exam_papers)
                result = (
                        "以下是最近一次考试的信息:\n\n" +
                        exam_name + " | 刷新时间: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n" +
                        "个人总分: " + f"\033[32m{exam_score}\033[0m" + "/" + exam_score_full + " 班级平均分: " +
                        exam_score_avg_class + " 年级平均分: " + exam_score_avg_grade + " 班级排名: " +
                        exam_rank_class + "\n\n" + "各科成绩:"
                )
                table = PrettyTable(
                    ["科目", "成绩", "班级平均分", "年级平均分", "班级最高分", "年级最高分", "班级排名", "年级排名"])
                for i in range(length_exam_papers):
                    exam_paper_id = str(exam_papers[i]["paperId"])
                    exam_subject = str(exam_papers[i]["subject"])
                    exam_subject_score = str(exam_papers[i]["score"])
                    exam_subject_score_full = str(exam_papers[i]["manfen"])
                    exam_subject_score_avg_class = str(exam_papers[i]["classAvg"])
                    exam_subject_score_avg_grade = str(exam_papers[i]["gradeAvg"])
                    url_exam_subject_rank = f"https://hfs-be.yunxiao.com/v3/exam/" \
                                            f"{exam_id}/papers/{exam_paper_id}/rank-info"
                    req = await client.get(url=url_exam_subject_rank, headers=headers)
                    exam_subject_highest_class = str(req.json()["data"]["highest"]["class"])
                    exam_subject_highest_grade = str(req.json()["data"]["highest"]["grade"])
                    exam_subject_rank_class = str(req.json()["data"]["rank"]["class"])
                    exam_subject_rank_grade = str(req.json()["data"]["rank"]["grade"])
                    table.add_row([exam_subject, f"\033[32m{exam_subject_score}\033[0m/{exam_subject_score_full}",
                                   exam_subject_score_avg_class, exam_subject_score_avg_grade,
                                   exam_subject_highest_class, exam_subject_highest_grade, exam_subject_rank_class,
                                   exam_subject_rank_grade])
                clear()
                print(result)
                print(table)
        except BaseException as e:
            print("获取失败: Error: ", e, "  Time: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        await asyncio.sleep(float(refresh_time))


if __name__ == '__main__':
    tasks = [main() for _ in range(1)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
