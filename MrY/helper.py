#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
"""
@contact: Yun Yan (yy1533@nyu.edu)
"""
import os
import io
import time
import shutil
import subprocess
# import sys
# import pandas as pd
# import yaml


def join_path(*args):
    x = map(str, args)
    return(os.path.join(*x))


def paste(*args, sept=' '):
    x = map(str, args)
    return(sept.join(x))


def paste0(*args):
    return(paste(*args, sept=""))


def ymdhms():
    return(time.strftime('%Y%m%d%H%M%S%Z', time.gmtime()))


def ymd():
    return(time.strftime('%Y%m%d%Z', time.gmtime()))


def print_logger(msg):
    localtime = time.asctime(time.localtime(time.time()))
    # sys.stderr.write("[ {} ] {}\n".format(localtime, msg))
    print("[ {} ] {}\n".format(localtime, msg))


def mkfolder(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError:
        pass


def rmfolder(dirpath):
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


def resetfolder(dirpath, remove_only=False):
    if not os.path.isdir(dirpath):
        raise OSError('Not a directory')
    try:
        shutil.rmtree(dirpath)
        if not remove_only:
            os.makedirs(dirpath)
    except OSError:
        raise OSError(paste("Fail to reset folder", dirpath))
    return(None)


def is_nonempty_file(fpath, verbose=False):
    if os.path.exists(fpath):
        if os.path.isfile(fpath):
            try:
                return(os.path.getsize(fpath) != 0)
            except OSError:
                return(False)
        else:
            if verbose:
                print_logger(paste(fpath, "is not a legal file"))
            return(False)
    else:
        if verbose:
            print_logger(paste(fpath, " does not exist or not-accessed"))
        return(False)


def resetfpath(fpath):
    if is_nonempty_file(fpath):
        os.remove(fpath)
    return(None)


def rmfile(fpath):
    try:
        os.remove(fpath)
    except FileNotFoundError:
        pass


def base_name(fpath, ext=None, auto=True):
    bs = os.path.basename(fpath)
    if not auto:
        return(bs)
    if not (ext is None or ext == ""):
        bs = bs.replace(ext, '')
    bs = os.path.splitext(bs)[0]
    return(bs)


def dir_name(fpath):
    return(os.path.dirname(fpath))


def popen_communicate(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except ValueError:
        print_logger(paste0("Fail to run: ", cmd, "\n"))
        return(None)
    (pout, perr) = p.communicate()
    return(pout)


def filehandle_fastq_gz(fpath):
    # pout = popen_communicate('zcat {}'.format(fpath))
    # fh = io.BytesIO(pout)
    p = subprocess.Popen('gunzip -c {}'.format(fpath),
                         shell=True, stdout=subprocess.PIPE)
    fh = io.TextIOWrapper(p.stdout, encoding='ascii')
    return(fh)


def main():
    print_logger("This is function: helper.py")


if __name__ == '__main__':
    main()
