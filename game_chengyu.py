
# -*- coding: utf-8 -*-
import importlib
import sys
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
import json
import random
import pypinyin
# [
#     {
#         "derivation": "语出《法华经·法师功德品》下至阿鼻地狱。”",
#         "example": "但也有少数意志薄弱的……逐步上当，终至堕入～。★《上饶集中营·炼狱杂记》",
#         "explanation": "阿鼻梵语的译音，意译为无间”，即痛苦无有间断之意。常用来比喻黑暗的社会和严酷的牢狱。又比喻无法摆脱的极其痛苦的境地。",
#         "pinyin": "ā bí dì yù",
#         "word": "阿鼻地狱",
#         "abbreviation": "abdy"
#     },
#     ...
# ]


chengyu_dict = {} # {“阿鼻地狱”：“阿鼻梵语的译音，意译为无间”，即痛苦无有间断之意。常用来比喻黑暗的社会和严酷的牢狱。又比喻无法摆脱的极其痛苦的境地。”}
counter = {
    "count": 0,
    "time": 10000,
    "chengyu": "",
    "level": 1
}

def init():
    chengyu_dict = parse_chengyu('chengyu.json')

def parse_chengyu(path):
    try:
        f = open('chengyu.json', 'r', encoding='UTF-8')
        cy_str = f.read()
        chengyu_list = json.loads(cy_str)
        for entity in chengyu_list:
            word = entity["word"]
            if len(word) is 4:
                chengyu_dict[word] = entity["explanation"]
        return chengyu_dict
    finally:
        if f:
            f.close()
        # return None

#随机产生成语
def random_chengyu(chengyu_dict):
    dict_len = len(chengyu_dict)
    pos = random.randint(0, dict_len - 1)
    return list(chengyu_dict.keys())[pos]


def check_chengyu(chengyu, chengyu_dict): 
    return chengyu in chengyu_dict


#检查拼音是否相同
def check_pinyin_same(input, match_word):
    input_pinyin = pypinyin.pinyin(input, style=pypinyin.NORMAL)[0][0]
    match_word_pinyin = pypinyin.pinyin(match_word, style=pypinyin.NORMAL)[3][0]
    return input_pinyin == match_word_pinyin
    
#检查拼音和声调是否相同
def check_pinyin_tone_same(input, match_word):
    input_pinyin = pypinyin.pinyin(input, style=pypinyin.TONE)[0][0]
    match_word_pinyin = pypinyin.pinyin(match_word, style=pypinyin.TONE)[3][0]
    return input_pinyin == match_word_pinyin
    
#判断是否是四字词语且以关键字开头
def is_like_chengyu(input, match_word):
    # if key_word.decode("utf-8") == input.decode("utf-8")[0:1]:
    if(len(input) != 4):
        return False
    if(counter["level"] == 1):
        return input[0:1] == match_word[3:4]
    if(counter["level"] == 2):
        return check_pinyin_tone_same(input, match_word)
    if(counter["level"] == 3):
        return check_pinyin_same(input, match_word)
    

    
def game_run(msg_text, sender):
    if("重新开始成语接龙" in msg_text) and (counter["count"] > 0):
        counter["chengyu"] = random_chengyu(chengyu_dict)
        counter["count"] = 1
        return u"选择游戏难度：1同字；2同音且同调；3同音"
        
    if ("成语接龙" in msg_text) and (counter["count"] is 0):
        counter["chengyu"] = random_chengyu(chengyu_dict)
        counter["count"] = 1
        return u"选择游戏难度：1同字；2同音且同调；3同音"
    
    # 设置游戏难度
    if(counter["count"] == 1):
        if(not msg_text.isdigit()):
            return u"选择游戏难度：1同字；2同音且同调；3同音"
        else:
            counter["level"] = int(msg_text)
            counter["count"] = 2
            return u'成语接龙游戏开始：' + counter["chengyu"]
    
    if (counter["count"] > 1) and is_like_chengyu(msg_text, counter["chengyu"]):
        ischengyu = check_chengyu(msg_text, chengyu_dict)

        if ischengyu :
            result = u"@%s 回答正确: 【%s】, 游戏继续" % (sender, msg_text)
            counter["count"] = counter["count"] + 1
            counter["chengyu"] = msg_text
            if counter["count"] >= 15:
                counter["count"] = 0
                return result + u", 游戏结束"
            else:
                return result
        else:
            return u"%s 不是成语" % (msg_text) 
    else:
        return None



if __name__ == '__main__':
    chengyu_dict = parse_chengyu('chengyu.json')
    random_c = random_chengyu(chengyu_dict)
    # print(len(random_c))
    print(random_c)
    # print("你".decode("utf-8") == "你好".decode("utf-8")[0:1])

    # try:
    #     f = open('chengyu.json', 'r')
    #     cy_str = f.read()
    #     new_dict = json.loads(cy_str)
    #     output = ""
    #     for entity in new_dict:
    #         print(entity["word"])
    #         output += entity["word"]
    #         output += "\n"
    #     with open('chengyu.txt', mode='w+', encoding='utf-8') as of:
    #         of.write(output)
    # finally:
    #     if f:
    #         f.close()