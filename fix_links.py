#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

file_path = 'topic-management.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

original_count = content.count("编辑话题.html")
content = content.replace("编辑话题.html", "edit-topic.html")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'已完成替换，共替换 {original_count} 处编辑话题.html -> edit-topic.html')
