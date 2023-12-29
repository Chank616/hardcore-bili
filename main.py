import requests
from gpt import send_msg

if __name__ == '__main__':
    DedeUserID = ""
    SESSDATA = ""
    bili_jct = ""
    csrf = bili_jct
    headers = {
        "Cookie": f"SESSDATA={SESSDATA};bili_jct={bili_jct};DedeUserID={DedeUserID};",
        "Accept": "application/json, text/plain, */*",
    }

    resp = requests.get(url="https://api.bilibili.com/x/senior/v1/captcha",
                        params={
                            "csrf": csrf
                        },
                        headers=headers).json()
    print(f"获取验证码{resp}")
    with open("code.jpg", "wb") as f:
        f.write(requests.get(url=resp["data"]["url"]).content)
    bili_code = input("输入验证码：")
    bili_token = resp["data"]["token"]
    resp = requests.post(url="https://api.bilibili.com/x/senior/v1/captcha/submit",
                         params={
                             "bili_code": bili_code,
                             "bili_token": bili_token,
                             "csrf": csrf,
                             "type": "bilibili",
                             "gt_seccode": "",
                             "gt_challenge": "",
                             "gt_validate": "",
                             "ids": "2"
                         },
                         headers=headers).json()
    print(f"验证码结果{resp}")

    resp = requests.get(url="https://api.bilibili.com/x/senior/v1/answer/result",
                        params={
                            "csrf": csrf
                        },
                        headers=headers).json()
    total = resp['data']['scores'][0]["total"]
    for total in range(total, 100):
        example = requests.get(url="https://api.bilibili.com/x/senior/v1/question",
                               params={
                                   "csrf": csrf
                               },
                               headers=headers).json()
        print(f"第{total + 1}个题")
        question_id = example["data"]["id"]
        question = example["data"]["question"]
        answers = example["data"]["answers"]
        a = answers[0]["ans_text"]
        b = answers[1]["ans_text"]
        c = answers[2]["ans_text"]
        d = answers[3]["ans_text"]
        question_text = f"{question}A.{a} B.{b} C.{c} D.{d} \n注意：你的回答长度为1，只需要回答正确选项的字母，"
        print("-题目：" + question_text)
        answer_text = send_msg(question_text)
        print("-GPT给的答案：" + answer_text)

        answers[0]["appear_num"] = answer_text.count("A")
        answers[1]["appear_num"] = answer_text.count("B")
        answers[2]["appear_num"] = answer_text.count("C")
        answers[3]["appear_num"] = answer_text.count("D")

        appear_max = max(answers[0]["appear_num"], answers[1]["appear_num"], answers[2]["appear_num"],
                         answers[3]["appear_num"])

        i = 0
        if answers[0]["appear_num"] == appear_max:
            i = 0
            print("--程序决定选A")
        if answers[1]["appear_num"] == appear_max:
            i = 1
            print("--程序决定选B")
        if answers[2]["appear_num"] == appear_max:
            i = 2
            print("--程序决定选C")
        if answers[3]["appear_num"] == appear_max:
            i = 3
            print("--程序决定选D")

        resp = requests.post(url="https://api.bilibili.com/x/senior/v1/answer/submit",
                             data={
                                 "csrf": csrf,
                                 "ans_text": answers[i]["ans_text"],
                                 "ans_hash": answers[i]["ans_hash"],
                                 "id": question_id,
                             },
                             headers=headers).json()
        print(f"提交成功{resp}")
        resp = requests.get(url="https://api.bilibili.com/x/senior/v1/answer/result",
                            params={
                                "csrf": csrf
                            },
                            headers=headers).json()
        print(f"目前分数：{resp['data']['scores'][0]['score']}")
        print(f"-------------------------------")
