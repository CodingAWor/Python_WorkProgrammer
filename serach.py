import os
import shutil

# 模糊查找数字字典中key的值,不区分大小写


def fuzzy_search(num_dict, keyword):
    result = []
    for key in num_dict.keys():
        if str(keyword).lower() in str(key).lower():
            result.append((key, num_dict[key]))
    return result

# 模糊查找列表中的值,不区分大小写


def fuzzy_search2(my_list, keyword):
    result = []
    for element in my_list:
        if str(keyword).lower() in str(element).lower():
            result.append(element)
    return result


# 获取指定目录下最新的修改文件
def get_latest_modified_file(dir_path):
    latest_file = ""
    latest_modified_time = 0
    for file_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isfile(full_path):
            modified_time = os.path.getmtime(full_path)
            if modified_time > latest_modified_time:
                latest_file = file_name
                latest_modified_time = modified_time
    if latest_file:
        print("最新修改的文件是：", latest_file)
        print("最新修改的时间是：", latest_modified_time)
    else:
        print("指定目录下没有文件")


# 指定路径文件移动到另一个路径下
def move_file(src_file_path, dst_path):
    # 获取源文件名
    src_file_name = os.path.basename(src_file_path)
    # 获取目标路径下同名的文件路径
    dst_file_path = os.path.join(dst_path, src_file_name)
    # 判断目标路径下是否存在同名文件
    if os.path.exists(dst_file_path):
        choice = input("目标路径下已经存在同名文件，是否覆盖？(y/n)")
        # 如果用户输入的是 y，则覆盖同名文件；否则不进行任何操作
        if choice == 'y':
            shutil.move(src_file_path, dst_path)
            print(f"文件 {src_file_name} 已成功移动到目录 {dst_path}")
        else:
            print("移动操作已取消")
    # 如果目标路径下不存在同名文件，则直接执行移动操作
    else:
        shutil.move(src_file_path, dst_path)
        print(f"文件 {src_file_name} 已成功移动到目录 {dst_path}")


my_list = ["libptz.a", "libptzcivil.a", "banana", "grape", "kiwi"]
keyword = "A"

result = list(filter(lambda x: keyword.lower() in x.lower(), my_list))

result2 = fuzzy_search2(my_list, 'PTZ')

print(result)
print(result2)
