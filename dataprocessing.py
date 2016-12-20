# coding=utf8
# author=PlatinumGod
# created on 

import pandas as pd
import re


class DataClean:

    def __init__(self):
        self.trainpath = 'train.csv'
        self.testpath = 'test.csv'
        self.descriptionpath = 'data_description.txt'
        self.mean = []
        self.cls = []
        self.clsdescrption = {'SalePrice': {'is_continue': True, 'attr': []}}
        self._preprocess()


    def _preprocess(self, path=None):
        if path is None:
            path = self.descriptionpath
        cls_now = ''
        with open(path, 'r') as f:
            m_cls = re.compile("([a-zA-Z0-9]+): ")
            m_category = re.compile('       ([a-zA-Z0-9]+)')
            for line in f.readlines():
                res_category = m_category.findall(line)
                res_cls = m_cls.findall(line)
                if res_cls:
                    # print '\n'
                    # print res_cls[0], ':',
                    self.clsdescrption[res_cls[0]] = {'is_continue': True, 'attr': []}
                    cls_now = res_cls[0]
                elif res_category:
                    self.clsdescrption[cls_now]['attr'].append(res_category[0])
                    self.clsdescrption[cls_now]['is_continue'] = False
                    # print res_category[0],
        # print '\n', len(self.clsdescrption.keys())


    def _getnum(self, element, cls):
        is_continue = self.clsdescrption[cls]['is_continue']
        if is_continue:
            return [float(element)]
        else:
            attr = self.clsdescrption[cls]['attr']
            newele = []
            for ele in attr:
                if ele == element:
                    # print element,
                    newele.append(1)
                else:
                    newele.append(0)
            # print attr
            # print '\t', newele
            return newele

    def _getdata(self, path, end=None):
        data = pd.read_csv(path)
        for cls in data:
            self.cls.append(cls)
        if end is not None:
            self.cls = self.cls[1:end]
        else:
            self.cls = self.cls[1:80]
        # print len(self.cls)
        # print len(data)
        matrix = []
        for i in range(1, len(data)):
            vector = []
            for cls in self.cls:
                vector_piece = self._getnum(data[cls][i], cls)
                for v in vector_piece:
                    vector.append(v)
            matrix.append(vector)
        return matrix

    def getdata(self, path, end=None):
        if path == 'train':
            return self._getdata(self.trainpath, end)
        elif path == 'test':
            return self._getdata(self.testpath, end)


if __name__ == '__main__':
    DC = DataClean()
    train = DC.getdata('train', 81)
    print train
    print 'finish!'