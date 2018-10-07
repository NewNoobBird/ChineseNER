# ChineseNER
Final Year projects on Chinese NER and the paper is attached on https://newnoobbird.github.io/index.html Paper2.
This code shows the process to deal with data.


[newsdata means BaiduData crawled from baidu]
[testdata means data used for training]

-- BaiduData: The Data Source.
		Run readcsv.py to deal with data.
-- Boson: Boson NLP API.
		Run boson.py to get NER.
-- LTP: LTP API.
		Run ltp.py to get NER. You need download model from LTP website.
-- NER_CRF:NER with CRF.
		Run main.py to get NER.
-- NER_NN: NER with Neural Network.
		Run train_bilstm_crf.py to train data with BiLSTM
		Run train_bilstm_crf_add_word.py to traiin data with CNN-LSTM
-- Estimate: How to judge Different estimation.
		Run eval.py to get estimation.

这是"Research on Named Entity Recognition Methods in Terrorism Text"(涉恐文本中的命名实体识别方法研究)论文中对应的程序和实验数据的。