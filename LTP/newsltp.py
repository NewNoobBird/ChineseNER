# -*- coding: utf-8 -*-

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import os
import pandas as pd

LTP_DATA_DIR = './model'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
Input_file = './data/news.csv'
Output_file = './data/output_news.txt'


def getltp(text):
    # 得到分句,返回的是句子组成的列表
    sentences = SentenceSplitter.split(text)
    #print ('\n'.join(sentences))

    # 得到词语，返回的是每行中以空格间隔的词
    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    words = []
    print_words = []
    for sentence in sentences:
        if (len(sentence) <= 1):
            continue
        word = segmentor.segment(sentence)
        print_word = (' '.join(word))
        print_words.append(print_word)
        words.append(word)
    #print ('\n'.join(print_words))
    #print (words)
    #words = '\n'.join(words)
    segmentor.release()

    # 进行词性标注
    postagger = Postagger()
    postagger.load(pos_model_path)
    #words = ''
    postags = []
    for word in words:
        postag = postagger.postag(word)
        postags.append(postag)
        #print (' '.join(postag))
        #print ('\n')
    #print (' '.join(postags))
    postagger.release()

    recognizer = NamedEntityRecognizer()
    recognizer.load(ner_model_path)
    #words = ''
    #postags = ''
    nertags = []
    for word, postag in zip(words, postags):
        #print (' '.join(word),' '.join(postag))
        word = list(word)
        postag = list(postag)
        #print (word,postag)
        nertag = recognizer.recognize(word, postag)
        nertags.append(nertag)
        #print (' '.join(nertag))
    recognizer.release()

    return words, nertags

def getchar_taglist(words, nertags):
    with open('./data/output_news2.txt', 'w', encoding='utf-8') as f:
        for word, nertag in zip(words, nertags):
            for w, n in zip(word, nertag):
                w = list(w)
                #print (len(w), w, n)
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
                elif n == 'I-Ns' or n == 'E-Ns':
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

    return charlist, taglist

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
    #print (tag_seq, char_seq)
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

if __name__ == '__main__':
    # 处理csv得到content内容并且使得每次写入[PER, LOC, ORG]到所对应的队列中去
    data = pd.read_csv(Input_file)
    text = data['content']
    columns = ['title','date','keyword','source','content','PER','LOC','ORG','link']
    data = pd.concat([data, pd.DataFrame(columns=['PER','LOC','ORG'])])
    for i, content in enumerate(text):
        words, nertags = getltp(content)
        charlist, taglist = getchar_taglist(words, nertags)
        PER, LOC, ORG = get_entity(taglist, charlist)
        data.ix[i,'content'] = 'PER: {}\nLOC: {}\nORG:{}'.format(PER,LOC,ORG)
        data.ix[i,'PER'] = ' '.join(list(set(PER)))
        data.ix[i,'LOC'] = ' '.join(list(set(LOC)))
        data.ix[i,'ORG'] = ' '.join(list(set(ORG)))
        #data.ix[i,'LOC'] = LOC
        #data.ix[i,'ORG'] = ORG    
        data.fillna('None')
    data.to_csv("NER_news.csv",index=False, encoding='utf-8',columns=columns)

    print ('done.')

