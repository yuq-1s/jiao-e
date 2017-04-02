#! /usr/bin/env python3

import pickle
# from spider.summer import Spider
from pdb import set_trace
from spider.utils.parsers import parse_time

if __name__ == '__main__':
    content = '''行课安排为第1周 --- 第16周,其中:
单周
星期三 第1节--第2节
东上院507(1-16周).蔡国平
星期五 第1节--第2节
东上院507(1-16周).蔡国平
双周
星期三 第1节--第2节
东上院507(1-16周).蔡国平'''
    print([s for s in parse_time(content)])
    set_trace()
    # spider = Spider()
    # with open('data2.pickle', 'wb') as f:
    #     pickle.dump(list(spider.run()), f)
