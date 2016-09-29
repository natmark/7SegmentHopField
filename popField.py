#!/usr/bin/env python
# -*- coding: utf-8 -*-

#16*16のパターンから文字認識する
import numpy as np
from numpy import linalg as la
import sys

def calc_energy(size,W,pattern):
    s = 0
    for i in range(size):
        for j in range(size):
            s += W[i][j] * pattern[i] * pattern[j]
    return -s / 2

def found_pattern(memory,pattern):
    for key,value in memory.iteritems():
        if pattern == value:
            return {key:value}
    return None

def print_segment(pattern):
    str = ""
    if pattern[0] == 1:
        str += "#####\n"
    else:
        str +=  "     \n"
    if pattern[5] == 1:
        str +=  "#   "
    else:
        str +=  "    "
    if pattern[1] == 1:
        str +=  "#\n"
    else:
        str +=  " \n"
    if pattern[6] == 1:
        str += "#####\n"
    else:
        str +=  "     \n"
    if pattern[4] == 1:
        str +=  "#   "
    else:
        str +=  "    "
    if pattern[2] == 1:
        str +=  "#\n"
    else:
        str +=  " \n"
    if pattern[3] == 1:
        str += "#####\n"
    else:
        str +=  "     \n"

    return str

f = open("pattern.txt","r")
#文字と対応するパターンの辞書配列
dic = {}
for row in f:
    if '#' in row:
        print row
        continue
    mark = row[0]
    #1か-1にしたい
    row = row[2:]
    row = row.replace("0","-1")
    pattern = map(int,row.split(','))
    dic[mark] = pattern
f.close()

pattern_len = len(dic.values()[0])
#重み配列
W = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
for i in range(pattern_len):
    for j in range(pattern_len):
        if i == j:
            W[i][j] = 0
        else:
            Weight = 0
            for key,value in dic.iteritems():
                Weight += value[i] * value[j]
            W[i][j] = Weight

print "pattern:"

#   ##1##
#   6   2
#   ##7##
#   5   3
#   ##4##
row = "1,0,1,1,0,0,1"
# row = raw_input()

#1か-1にしたい
row = row.replace("0","-1")
pre_pattern = map(int,row.strip("\n")[0:].split(','))
initial_pattern = pre_pattern
print "重み配列:"
print np.array(W)

#想起演算最大数
recall_max = 10
count = 0

recalled_pattern_array = []

while count < recall_max:
    print "\t[想起演算回数]\t>",count + 1
    print "初期パターン",np.array(pre_pattern)
    print print_segment(pre_pattern)

    pre_energy = calc_energy(pattern_len,W,pre_pattern)
    print "初期エネルギー",pre_energy
    #転置
    transpose = np.array(pre_pattern)[:, np.newaxis]
    #想起演算
    WP = np.dot(W,transpose)
    #想起
    for i in range(len(WP)):
        if WP[i] > 0:
            WP[i] = 1
        else:
            WP[i] = -1
    recalled_pattern = WP.transpose().tolist()[0]
    print "想起後パターン",np.array(recalled_pattern)
    print print_segment(recalled_pattern)

    recalled_energy = calc_energy(pattern_len,W,recalled_pattern)
    print "想起後エネルギー",recalled_energy

    if initial_pattern == recalled_pattern:
        #初期パターンと想起後パターンが同じ場合終了。
        d = found_pattern(dic,recalled_pattern)
        if d != None:
            #パターン発見
            print "想起成功"
            print d.keys()[0]
            print d.values()[0]
            print print_segment(d.values()[0])
        else:
            #失敗
            print "想起失敗"
            print recalled_pattern
            print print_segment(recalled_pattern)
        break
    else:
        if pre_pattern == recalled_pattern:
            print "想起成功"
            print found_pattern(dic,recalled_pattern)
            print print_segment(recalled_pattern)
            break
        else:
            if recalled_pattern in recalled_pattern_array:
                min_energy = calc_energy(pattern_len,W,recalled_pattern_array[0])
                consecutive = False
                min_energy_pattern = recalled_pattern_array[0]
                for pattern in recalled_pattern_array:
                    if min_energy == calc_energy(pattern_len,W,pattern):
                        consecutive = True
                    else:
                        min_energy = calc_energy(pattern_len,W,pattern)
                        consecutive = False
                        min_energy_pattern = pattern

                if consecutive == True:
                    print "極小値止まり。想起失敗"
                    print found_pattern(dic,min_energy_pattern)
                    print min_energy_pattern
                    print print_segment(min_energy_pattern)
                else:
                    print "局所解"
                    print found_pattern(dic,min_energy_pattern)
                    print min_energy_pattern
                    print print_segment(min_energy_pattern)
                break
            else:
                print "再想起"
                recalled_pattern_array.append(recalled_pattern)
    pre_pattern = recalled_pattern
    count+=1

if count >= recall_max:
    print "想起演算最大数超え"
    print recalled_pattern
    print print_segment(recalled_pattern)
