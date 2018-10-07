# -*- coding: utf-8 -*-
import jieba.posseg as jbpos

# 把token序列组合成原句
def get_sentence(token):
    sentence= ''
    for t in token:
        sentence += t[0]
    return sentence

# 为token填充分词标记和词性标记
def get_cut_and_seg(token):
    wordlist = jbpos.cut(get_sentence(token))
    res = list()
    index=0
    for w in wordlist:
        for i in range(len(w.word)):
            if len(w.word) == 1:
                status = 'S'
            elif i == 0:
                status = 'B'
            elif i == len(w.word) - 1:
                status = 'E'
            else:
                status = 'I'
            token[index][1]=status
            token[index][2]=w.flag
            index += 1
    return res

# 读入数据
def load_data(path):
    file=open(path,'r',encoding='utf-8')
    res=list()
    try:

        lines=file.readlines()
        # print(lines)
        res_line=list()
        for item in lines:
            if item.split(' ').__len__()>=2:
                word=item.split(' ')[0]
                type=item.split(' ')[1].replace('\n','').replace('\r','')
                res_line.append([word,'','',type])
            else:
                get_cut_and_seg(res_line)
                res.append(res_line)
                res_line=list()
    finally:
        file.close()
        # print(res)
    return res

def format_boson_data(file_name='output.txt'):
    res=list()
    tmp = load_data(file_name)
    for line in tmp:
        state=0
        lastc=''
        ename=""

        for c in line:
            if c=='{' and state==0:
                state=1
            elif c=='{' and lastc=='{' and state==1:
                state=2
            elif c==':' and state==2:
                state=3
            elif c=='}' and state==4:
                state=5
            elif c=='}' and lastc=='}' and state==5:
                state=0
            elif state==0 and c!=' ' and c!='\n':
                res.append(c+" O")
            elif state==2:
                ename+=c
            elif state==3 and c!=' ':
                ename=get_type(ename)
                res.append(c+" B-"+ename)
                state=4
            elif state==4:
                res.append(c + " I-" + ename)
            lastc=c
        res.append("")
    print(res)
    # save
    file=open("haha.txt",'w',encoding='utf-8')
    try:
        # file.writelines(res)
        for item in res:
            file.write(item+"\n")
            # file.write("\r\n")
            # print("\r")
    finally:
        file.close()

if __name__ == "__main__":
    format_boson_data()