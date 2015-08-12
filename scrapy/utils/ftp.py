from ftplib import error_perm
from posixpath import dirname

def ftp_makedirs_cwd(ftp, path, first_call=True):
    """Set the current directory of the FTP connection given in the `ftp`
    argument (as a ftplib.FTP object), creating all parent directories if they
    don't exist. The ftplib.FTP object must be already connected and logged in.
    """
    #与ftp连接相关的一些函数，但是很奇怪，与一般的文件系统上面的操作不具有一致性
    #只有最后一次需要进入到working directory，其余的时候若存在/a/b那么可以直接创建/a/b/c
    try:
        ftp.cwd(path)
    except error_perm:
        ftp_makedirs_cwd(ftp, dirname(path), False)
        ftp.mkd(path)
        if first_call:
            ftp.cwd(path)
