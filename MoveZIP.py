import os
import shutil
import pandas as pd
import sys
sys.setrecursionlimit(3000)

def mkdirs(path):
    path = path.strip()
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)  # 创建目录
        print('目标路径:' + path + ' ' + '已创建')
        return True
    else:
        return False


'''将原根目录路径下所有子文件移动到新文件夹中,分类依据为文件名称包含文件夹名称'''


def search_file(row_root_path, foldername, new_root_path):
    queue = []
    queue.append(row_root_path)
    while len(queue) > 0:
        tmp = queue.pop(0)
        if (os.path.isdir(tmp)):  # 如果该路径是文件夹,遍历该路径中文件和文件夹
            for item in os.listdir(tmp):
                queue.append(os.path.join(tmp, item))  # 将所得路径加入队列queue
        elif (os.path.isfile(tmp)):  # 如果该路径是文件,获取文件名和文件目录，将文件名与文件目录连接起来，形成完整路径
            name = os.path.basename(tmp)
            dirname = os.path.dirname(tmp)
            row_full_path = os.path.join(dirname, name)
            new_full_path = new_root_path + '/' + name  # 定义新路径，匹配符合条件的文件
            if foldername in name:
                shutil.move(row_full_path, new_full_path)

if __name__ == '__main__':
    data = pd.read_excel('路径映射表.xlsx')
    for i in data['压缩包目标路径']:
        mkdirs(i)
    for i in range(len(data['身份证号'])):
        root_path = data['压缩包当前路径'][i]
        goal_path = data['压缩包目标路径'][i]
        data_ID = data['身份证号'][i].astype(str).strip()

        if len(data_ID) == 18:
            print('---' + 'ID:' + data_ID + '-' + '文件已成功转移' + '---')
            search_file(root_path, data_ID, goal_path)
        else:
            print('---' + 'ID:' + data_ID + '-' + '身份证号码有误' + '-' + '待人工核验' + '---')

