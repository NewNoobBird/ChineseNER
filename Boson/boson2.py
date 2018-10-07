# -*- coding: utf-8 -*-

# 识别的包括：time,location,person_name,org_name,company_name,product_name,job_title
# 参数 sensitivity: 1-5之间的，5更加精确
# 返回三元组: entity, tag, word
# 成都商报记者 姚永忠
# [{"entity": [[0, 2, "product_name"],  (s,t,entity_type)
#              [2, 3, "job_title"],
#              [3, 4, "person_name"]],
#   "tag": ["ns", "n", "n", "nr"],
#   "word": ["成都", "商报", "记者", "姚永忠"]}]
# {'entity': [[0, 2, 'product_name'],
#              [3, 4, 'time']],
#   'tag': ['nz', 'nx', 'nl', 't', 'ad', 'v'],
#   'word': ['微软', 'XP', '操作系统', '今日', '正式', '退休']}
# location -> LOC
# person_name -> PER
# org_name, company_name, product_name -> ORG

from bosonnlp import BosonNLP
import os

api = 'avzp5h2G.21940.kBiq3cew8Oct'
nlp = BosonNLP(api)

Input_file = './data/original.txt'
Output_file = './data/output_news.txt'
# 得到分句,返回的是句子组成的列表

LOC_type = ['location']
PER_type = ['person_name']
ORG_type = ['org_name','company_name','product_name']



def get_all():
    readfile = open('./data/output_news.txt', 'r', encoding='utf-8').readlines()
    with open('./data/output_news2.txt', 'w', encoding='utf-8') as f:
        for line in readfile:
            line.strip('\r\n')
            line.replace('\n','')
            line = line.split(' ')
            w = line[0]
            n = line[1][:-1]

            print (len(w), w, n)
            #print (n=='O', n=='S-Ns')
            if n == 'O' or n=='S' :
                for i in range(len(w)):
                    f.write(w[i] + ' O\n')
            elif n == 'S-Nh' or n == 'B-Nh':
                f.write(w[0] + ' B-PER\n')
                for i in range(len(w)):
                    if (i==0):
                        continue
                    f.write(w[i] + ' I-PER\n')
            elif n == 'I-Nh' or n == 'E-Nh':
                for i in range(len(w)):
                    f.write(w[i] + ' I-PER\n')
            elif n == 'S-Ns' or n == 'B-Ns':
                f.write(w[0] + ' B-LOC\n')
                for i in range(len(w)):
                    if (i == 0):
                        continue
                    f.write(w[i] + ' I-LOC\n')
            elif n == 'I-Ns' or n == 'E-Ns':
                for i in range(len(w)):
                    f.write(w[i] + ' I-LOC\n')
            elif n == 'S-Ni' or n == 'B-Ni':
                f.write(w[0] + ' B-ORG\n')
                for i in range(len(w)):
                    if (i == 0):
                        continue
                    f.write(w[i] + ' I-ORG\n')
            elif n == 'I-Ni' or n == 'E-Ni':
                for i in range(len(w)):
                    f.write(w[i] + ' I-ORG\n')

    print ('done.')

    readfile = open('./data/output_news2.txt', 'r', encoding='utf-8').readlines()
    charlist = []
    taglist = []
    for line in readfile:
        line.strip('\r\n')
        line.replace('\n','')
        line = line.split(' ')
        charlist.append(line[0])
        taglist.append(line[1][:-1])

    def get_PER_entity(tag_seq, char_seq):
        length = len(char_seq)
        PER = []
        for i, (char,tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-PER':
                if 'per' in locals().keys():
                    PER.append(per)
                    del per
                per = char
                if i+1 == length:
                    PER.append(per)
            if tag == 'I-PER':
                per += char
                if i+1 == length:
                    PER.append(per)
            if tag not in ['I-PER','B-PER']:
                if 'per' in locals().keys():
                    PER.append(per)
                    del per
                continue
        return PER

    def get_LOC_entity(tag_seq, char_seq):
        print (tag_seq, char_seq)
        length = len(char_seq)
        LOC = []
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-LOC':
                if 'loc' in locals().keys():
                    LOC.append(loc)
                    del loc
                loc = char
                if i+1 == length:
                    LOC.append(loc)
            if tag == 'I-LOC':
                loc += char
                if i+1 == length:
                    LOC.append(loc)
            if tag not in ['I-LOC', 'B-LOC']:
                if 'loc' in locals().keys():
                    LOC.append(loc)
                    del loc
                continue
        return LOC


    def get_ORG_entity(tag_seq, char_seq):
        length = len(char_seq)
        ORG = []
        for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
            if tag == 'B-ORG':
                if 'org' in locals().keys():
                    ORG.append(org)
                    del org
                org = char
                if i+1 == length:
                    ORG.append(org)
            if tag == 'I-ORG':
                org += char
                if i+1 == length:
                    ORG.append(org)
            if tag not in ['I-ORG', 'B-ORG']:
                if 'org' in locals().keys():
                    ORG.append(org)
                    del org
                continue
        return ORG

    def get_entity(tag_seq, char_seq):
        PER = get_PER_entity(tag_seq, char_seq)
        LOC = get_LOC_entity(tag_seq, char_seq)
        ORG = get_ORG_entity(tag_seq, char_seq)
        return PER, LOC, ORG

    with open('./data/entity_new.txt', 'w', encoding='utf-8') as f:
        PER, LOC, ORG = get_entity(taglist, charlist)
        print ('PER: {}\nLOC: {}\nORG:{}'.format(PER,LOC,ORG))
        f.write ('PER: {}\nLOC: {}\nORG:{}'.format(PER,LOC,ORG))

    print ('done.')

if __name__ == '__main__':
    Input_file = open(Input_file, 'r', encoding='utf-8').readlines()

    text = []
    index = 0
    entities = []
    tags = []
    words = []
    cnt = 0
    flag = 0
    for line in Input_file:
        cnt += 1
        print (len(Input_file), cnt)
        if index < 78:
            text.append(line)
            index += 1
            if (cnt == len(Input_file)):
                flag = 1
            #print (index, line)
        if (index >= 78) or (flag == 1):
            index = 0
            text_str = '\n'.join(text)
            print (text_str)
            ner_dict = nlp.ner(text_str)
            print (ner_dict)
            entity = ner_dict[0]['entity']
            word = ner_dict[0]['word']
            tag = ner_dict[0]['tag']
            print (entity, word)
            entities.append(entity)
            tags.append(tag)
            words.append(word)
            text = []
			#text.append(line)

    with open(Output_file, 'w', encoding='utf-8') as f:
        for entity, word in zip(entities,words):
            print (entity, word)
            lastindex = 0
            for s, t, entity_type in entity:
                if s >  lastindex:
                    entity_name = word[lastindex:s]
                    entity_name = ''.join(entity_name)
                    f.write(entity_name + ' ' + 'O')
                    f.write('\n')
                lastindex = t

                if entity_type in LOC_type:
                    entity_name = word[s:t]
                    entity_name = ''.join(entity_name)
                    f.write(entity_name + ' ' + 'S-Ns')
                    f.write('\n')
                elif entity_type in PER_type:
                    entity_name = word[s:t]
                    entity_name = ''.join(entity_name)
                    f.write(entity_name + ' ' + 'S-Nh')
                    f.write('\n')
                elif entity_type in ORG_type:
                    entity_name = word[s:t]
                    entity_name = ''.join(entity_name)
                    f.write(entity_name + ' ' + 'S-Ni')
                    f.write('\n')
                else:
                    entity_name = word[s:t]
                    entity_name = ''.join(entity_name)
                    f.write(entity_name + ' ' + 'O')
                    f.write('\n')
            if lastindex < len(word):
                entity_name = word[lastindex:len(word)]
                entity_name = ''.join(entity_name)
                f.write(entity_name + ' ' + 'O')
                f.write('\n')

    get_all()
