#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('话题管理.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到两个"话题管理 &gt; 热议话题列表"出现的位置
count = 0
first_pos = None
second_pos = None

for i, line in enumerate(lines):
    if '话题管理 &gt; 热议话题列表' in line:
        count += 1
        if count == 1:
            first_pos = i
        elif count == 2:
            second_pos = i
            break

if first_pos is not None and second_pos is not None:
    print(f'Found first occurrence at line {first_pos+1}')
    print(f'Found second occurrence at line {second_pos+1}')
    
    # 找到第一个<div>...table结构的结束位置
    # 向前查找到<div>
    div_start = first_pos
    while div_start > 0 and '<div>' not in lines[div_start]:
        div_start -= 1
    
    print(f'First div starts around line {div_start+1}')
    
    # 向后查找从第二个h4往前找，到前一个</div></div>
    # 实际上，第二个块开始前应该有模态框闭包
    div_end = second_pos - 1
    while div_end > 0 and '</div>' not in lines[div_end]:
        div_end -= 1
    
    print(f'Removing lines {div_start+1} to {div_end}')
    
    # 删除这些行
    new_lines = lines[:div_start] + lines[second_pos-1:]
    
    with open('话题管理.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print('✓ 已删除重复的页面块')
else:
    print('✗ 未找到重复的内容')
