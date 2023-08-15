# *_*coding:utf-8 *_*
# @Author : YueMengRui
import re


def have_chinese(s: str):
    """
    字符串中是否包含中文
    """
    for i in s:
        if '\u4e00' <= i <= '\u9fa5':
            return True

    return False


def remove_special_characters(s: str, remove_punctuation: bool = True, remove_digit: bool = True):
    """
    去掉特殊字符
    :param s:
    :param remove_punctuation: 是否去除标点符号
    :param remove_digit: 是否去除数字
    :return:
    """
    # 去掉标点
    punctuation = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
    # 去掉数字
    digit = '[0-9]'

    if remove_punctuation:
        s = re.sub(punctuation, '', s)

    if remove_digit:
        s = re.sub(digit, '', s)

    return s


def is_en(s: str):
    """
    是否是英文
    """
    en = 'qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'

    for i in s:
        if i not in en:
            return False

    return True
