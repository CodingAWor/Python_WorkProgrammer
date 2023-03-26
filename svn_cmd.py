# pip install pysvn
import pysvn


def svn_checkout(url, revision, dest_dir):
    # 初始化 PySVN 客户端
    client = pysvn.Client()
    # 执行 svn checkout 操作
    client.checkout(url, dest_dir, revision=pysvn.Revision(
        pysvn.opt_revision_kind.number, revision))


def get_svn_changes(svn_url, svn_username, svn_password, output_dir, output_filename, last_rev):
    # 创建 SVN 客户端并设置默认用户名和密码
    svn_client = pysvn.Client()
    svn_client.set_default_username(svn_username)
    svn_client.set_default_password(svn_password)

    # 设置输出文件路径
    output_path = os.path.join(output_dir, output_filename)

    # 获取 SVN 最新版本和上一次处理的版本
    head_rev = svn_client.info2(svn_url, recurse=False)['head_rev'].number

    # 获取 SVN 修改和新增的文件路径
    changes = svn_client.diff_summarize(svn_url, peg_revision=pysvn.Revision(
        pysvn.opt_revision_kind.number, last_rev), revision1=svn_client.rev_number(head_rev))
    added_files = [item.path for item in changes if item.summarize_kind ==
                   pysvn.diff_summarize_kind.added]
    modified_files = [item.path for item in changes if item.summarize_kind ==
                      pysvn.diff_summarize_kind.modified]
    all_changes = added_files + modified_files

    # 将修改和新增的文件路径写入指定文件
    with open(output_path, 'a') as f:
        for path in all_changes:
            f.write(path + '\n')

    print(f"成功将 SVN 中的新增和修改文件路径输出到 {output_path} 中！")
