#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse


LOG = logging.getLogger(__name__)
__version__ = "3.0.0"    #设置版本信息
__author__ = ("Boya Xu",)   #输入作者信息
__email__ = "834786312@qq.com"
__all__ = []


def add_help_args(parser):   #帮助函数
    parser.add_argument('--file', type=str, default=False, help="输入文件")
    parser.add_argument('-p', type=int, default=1000, help="间隔bp")
    parser.add_argument('-l', type=int, default=False, help="基因组长度")
    parser.add_argument('--pre', type=str, default=False, help="out")
    parser.add_argument('--interval', type=str, default="ALL", help="是否选取间隔细分")
    return parser


def read_file(file):
    f = open(file, 'r')
    data = {}
    m = []
    for i in f:
        i = i.strip().split()
        if float(i[2]) >= 90:
            m.append(int(i[3]))
            m.append(int(i[4]))
            data[i[0]] = [int(i[3]), int(i[4]), str(i[5])]
    f.close()
    #print(data)
    return data


def tiqu(data, dire):
    d = {}
    for i in data:
        if data[i][2] == dire:
            d[i] = [int(data[i][0]), int(data[i][1])]
        else:
            continue
    return d


def tongji_ALL(d, data_dire, l):
    for i in data_dire:
        for k in d:
            n_1 = int(min(data_dire[i]))
            m_1 = int(max(data_dire[i]))
            if abs(m_1-n_1)<=100:
                if n_1 >= d[k][0] and m_1 <= d[k][1]:
                    d[k][2] = int(d[k][2]) + 1
                    d[k][3].append(i)
                elif m_1 > d[k][1] and d[k][0] < n_1 < d[k][1] and (m_1 - n_1) / 2 <= d[k][1] - n_1:
                    d[k][2] = int(d[k][2]) + 1
                    d[k][3].append(i)
                elif d[k][0] < m_1 < d[k][1] and n_1 < d[k][0] and (m_1 - n_1) / 2 <= m_1 - d[k][0]:
                    d[k][2] = int(d[k][2]) + 1
                    d[k][3].append(i)
            if abs(m_1-n_1)>100:
                if (int(l)-m_1+n_1)/2<=int(l)-m_1:
                    last_key = list(d.keys())[-1]
                    d[last_key][2] = int(d[k][2]) + 1
                    d[k][3].append(i)
                elif (int(l)-m_1+n_1)/2>=int(l)-m_1:
                    first_key = list(d.keys())[0]
                    d[first_key][2] = int(d[k][2]) + 1
                    d[k][3].append(i)
    return d

def tongji_dire(file, l, inter, dire, q=1000):
    d = {}
    p = 0
    data = read_file(file)
    data_dire = tiqu(data, dire)
    if inter=="ALL":
        for start in range(1, int(l), q):
            p = p+1
            end = min(start + q - 1, int(l))
            d['spacer' + '_' + str(p)] = [start, end, int(0), []]
        out = tongji_ALL(d, data_dire, l)
    else:
        gap=inter.split('-')
        gap1 = gap[0]
        gap2 = gap[1]
        if int(gap2)>int(l):
            print("error：区间大于基因组总长")
        else:
            for start in range(int(gap1), int(gap2), q):
                p = p + 1
                end = min(start + q - 1, int(gap2))
                d['spacer' + '_' + str(p)] = [start, end, int(0), []]
            out = tongji_ALL(d, data_dire, l)
    return out

    # for start in range(1, int(len), q):
    #     p = p+1
    #     end = min(start + 99, 8953)
    #     for i in data_minus:
    #         n_1 = int(min(data_minus[i]))
    #         m_1 = int(max(data_minus[i]))
    #         if n_1 >= start and m_1 <= end:
    #             u += 1
    #         elif m_1 > end and start < n_1 < end and (m_1 - n_1) / 2 <= end - n_1:
    #             u += 1
    #         elif start < m_1 < end and n_1 < start and (m_1 - n_1) / 2 <= m_1 - start:
    #             u += 1
    #     d['spacer' + '_' + str(p)] = [int[start], int[end], int[u]]
def print_max_3(d, dd):
    lst = [int(value[2]) for value in d.values()]
    top3 = sorted(lst, reverse=True)[:3]
    for key, value in d.items():
        if int(value[2]) in top3:
            print(dd + '\t' + key +'\t'+ str(value[0])+'\t'+str(value[1])+'\t'+str(value[2])+'\t'+"".join(str(value[3])))


def tongji(file, l, inter, prefix, q=1000):
    d_plus = tongji_dire(file, l, inter, 'plus', q)
    d_minus = tongji_dire(file, l, inter, 'minus', q)
    f = open(file, 'r')
    o_plus = open(prefix+'_'+inter+'_plus', 'w')
    o_minus = open(prefix+'_'+inter+'_minus', 'w')
    lines = f.readlines()
    first_line = lines[0]  # 取第一行
    chr = first_line.strip().split()[1]
    f.close()
    print_max_3(d_plus, 'plus')
    print_max_3(d_minus, 'minus')
    for i in d_plus:
        n = min(d_plus[i][0], d_plus[i][1])
        m = max(d_plus[i][0], d_plus[i][1])
       # if d[i][0]>d[i][1]:
       #     di = '-'
       # elif d[i][0]<d[i][1]:
       #     di = '+'
        o_plus.write(i+'\t'+ chr + '\t' +str(n) +'\t' + str(m) +'\t' + str(d_plus[i][2]) + '\t'+'-'+'\n')
    o_plus.close()

    for i in d_minus:
        n = min(d_minus[i][0], d_minus[i][1])
        m = max(d_minus[i][0], d_minus[i][1])
       # if d[i][0]>d[i][1]:
       #     di = '-'
       # elif d[i][0]<d[i][1]:
       #     di = '+'
        o_minus.write(i+'\t'+ chr + '\t' +str(n) +'\t' + str(m) +'\t' + str(d_minus[i][2]) +'\t'+'-'+ '\n')
    o_minus.close()


def main():   #主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
name:statistic.py 
attention: python tongji.py --file  --pre  -p -l
version: %s
contact: %s <%s>\ 
将比对序列划分成区间进行比较统计,并按照正负链输出,并输出数量最多的三个区间
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    tongji(args.file, args.l, args.interval, args.pre, args.p)


if __name__ == "__main__":           #固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
