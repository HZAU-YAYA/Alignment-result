#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import argparse

LOG = logging.getLogger(__name__)
__version__ = "1.0.0"    #设置版本信息
__author__ = ("Boya Xu",)   #输入作者信息
__email__ = "834786312@qq.com"
__all__ = []


def add_help_args(parser):   #帮助函数
    parser.add_argument('--f1', type=str, default=False, help="输入文件+")
    parser.add_argument('--f2', type=str, default=False, help="输入文件-")
    #parser.add_argument('--out', type=str, default=False, help="输出文件")
    return parser


def run_f(file1, file2):
    f1 = open(file1, 'r')
    d = {}
    for i in f1:
        if len(i.strip().split()) != 0:
            i = i.strip().split()
            d[str(i[2]) + '-' + str(i[3])] = [int(i[4])]
    f1.close()
    f2 = open(file2, 'r')
    for i in f2:
        if len(i.strip().split()) != 0:
            i = i.strip().split()
            d[str(i[2]) + '-' + str(i[3])].append(int(i[4]))
    f2.close()
    print('position'+'\t' + 'plus' + '\t' + 'minus')
    for i in d:
        print(i +'\t' + str(d[i][0]) + '\t' + str(d[i][1]))
    
def main():   #主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
version: %s
contact: %s <%s>\ 
fa转列表
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    run_f(args.f1, args.f2)

if __name__ == "__main__":           #固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()

