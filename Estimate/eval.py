import os


def conlleval(label_predict, label_path, metric_path):
    """

    :param label_predict:
    :param label_path:
    :param metric_path:
    :return:
    """
    eval_perl = "./conlleval_rev.pl"
    os.system("perl {} < {} > {}".format(eval_perl, label_path, metric_path))
    with open(metric_path) as fr:
        metrics = [line.strip() for line in fr]
    return metrics

if __name__ == '__main__':
    metric_path = './result.txt'
    label_path ='./real_test.txt'
    #metric_path ='./boson_test.txt'
    label_predict = './boson_test.txt'
    metrics = conlleval(label_predict, label_path, metric_path)
    print (metrics)
