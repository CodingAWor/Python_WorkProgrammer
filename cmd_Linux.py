import subprocess
import os


def get_svn_info(path):
    # 构造 svn 命令
    command = ['svn', 'info', path]
    # 执行命令并捕获输出
    result = subprocess.run(command, capture_output=True, text=True)
    # 解析输出，获取 svn 地址和版本信息
    lines = result.stdout.strip().split('\n')
    url = None
    revision = None
    for line in lines:
        if line.startswith('URL:'):
            url = line.split(':', 1)[1].strip()
        elif line.startswith('Revision:'):
            revision = line.split(':', 1)[1].strip()
    return url, revision


def create_directory(file_path):
    # 获取目录路径
    print(file_path)
    dir_path = os.path.dirname(file_path)
    print(dir_path)
    # 创建目录，如果不存在的话
    if not os.path.exists(dir_path):
        try:
            # 使用 os.mkdir() 函数创建目录
            os.mkdir(dir_path)
            print(f"目录 {dir_path} 创建成功")
        except OSError as error:
            print(f"目录 {dir_path} 创建失败: {error}")
    else:
        print('is exist')


def generate_patch(from_dir, to_dir, output_path, allowed_extensions=None):
    """
    生成两个目录之间的差异并保存为一个 patch 文件。
    :param from_dir: 源目录
    :param to_dir: 目标目录
    :param output_path: patch 文件输出路径
    :param allowed_extensions: 只包括指定文件扩展名的文件列表
    :return: 成功返回 True，否则返回 False。
    """

    # 获取源目录和目标目录中的所有文件路径
    from_files = _list_files_recursive(from_dir)
    to_files = _list_files_recursive(to_dir)

    # 找到新增或修改的文件，并将其路径转换为相对于源目录的路径
    modified_files = []
    for to_file in to_files:
        rel_path = os.path.relpath(to_file, to_dir)
        if allowed_extensions and os.path.splitext(rel_path)[1] not in allowed_extensions:
            continue
        from_file = os.path.join(from_dir, rel_path)
        if os.path.exists(from_file):
            # 文件已存在，说明是修改的文件
            modified_files.append(rel_path)
        else:
            # 文件不存在，说明是新增的文件
            modified_files.append(rel_path + "\t(added)")

    # 使用 diff 命令比较源目录和目标目录，并将结果重定向到指定文件
    with open(output_path, 'w') as output_file:
        diff_command = ['diff', '-ruN', from_dir, to_dir]
        subprocess.call(diff_command, stdout=output_file)

    # 如果没有新增或修改的文件，则说明没有必要创建 patch 文件
    if not modified_files:
        print("没有需要更新的文件，无需生成 patch 文件。")
        return False

    # 将新增和修改的文件列表写入 patch 文件的头部
    with open(output_path, 'r+') as output_file:
        content = output_file.read()
        output_file.seek(0, 0)
        header = "# Modified files:\n"
        header += "# " + "\n# ".join(modified_files) + "\n"
        output_file.write(header + content)

    print(f"成功将目录 {from_dir} 和 {to_dir} 中的差异转换为 patch 并保存到 {output_path} 中！")
    return True


def _list_files_recursive(root_dir):
    """
    获取指定目录及其子目录中所有文件的路径。
    :param root_dir: 根目录
    :return: 所有文件路径的列表
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


def record_command_output(command, output_file):
    """
    记录命令行输出到指定文件中
    :param command: 要执行的命令
    :param output_file: 输出文件路径
    """
    with open(output_file, 'w') as file:
        subprocess.run(command, shell=True, stdout=file,
                       stderr=subprocess.STDOUT)


def execute_command(command):
    """
    执行Linux命令行，并返回命令行执行结果
    :param command: 要执行的命令
    :return: 命令行执行结果
    """
    result = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    error = result.stderr.decode('utf-8')
    if error:
        return error
    else:
        return output


def main():
    # create_directory('E:\\abc\\')

    # from_dir = "C:/example/from"
    # to_dir = "C:/example/to"
    # output_path = "C:/example/patch.diff"
    # allowed_extensions = ['.txt', '.log']

    # generate_patch(from_dir, to_dir, output_path, allowed_extensions)

    # output = execute_command('ls -l /') # 显示根目录下的所有文件和目录
    # print(output)
    """
    主函数，循环接收用户输入的Linux命令，并返回命令的输出结果
    """
    while True:
        command = input("请输入Linux命令：")
        if command == "exit":
            print("退出程序")
            break
        # else:
            print(command)
        # try:
            # result = subprocess.check_output(command, shell=True, encoding='utf-8')
        print(command)
        # except subprocess.CalledProcessError as e:
        # print(e.output)

    current_path = os.getcwd()
    print(current_path)


if __name__ == '__main__':
    main()
