import types
import unicodedata
import re
from time import perf_counter
from collections.abc import Iterable
import csv


html_tag = re.compile(r"<[^>]*?>")


flatten = lambda x: [z for y in x for z in (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]


def time_func(func, args):
    start = perf_counter()
    if isinstance(args, Iterable):
        func(*args)
    else:
        func(args)
    end = perf_counter()
    return end - start


def explain(item, shows_private=False, shows_method=False):
    '''
    与えた python オブジェクトの詳細を表示します。
    '''
    print('EXPLAIN ------------------')
    print(item)
    print(type(item))
    print('ATTRIBUTES:')
    for d in dir(item):
        if d == 'type':
            continue
        if not shows_private and d.startswith('_'):
            continue
        attr = getattr(item, d)
        if not shows_method and (
                isinstance(attr, types.MethodType) or
                isinstance(attr, types.BuiltinMethodType) or
                isinstance(attr, types.CoroutineType) or
                isinstance(attr, types.FunctionType) or
                isinstance(attr, types.BuiltinFunctionType) or
                isinstance(attr, types.GeneratorType)
        ):
            continue
        print('{}:\t{}'.format(d, attr))


def remove_html_tags(text):
    return html_tag.sub("", text)


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def is_all_japanese(string):
    ans = True
    for ch in string:
        ans &= is_japanese(ch)
    return ans

#品詞と特徴のタプルのリストを返す
def mecab_list(text):
    tagger = MeCab.Tagger("-Ochasen")
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_class = []
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != u'BOS/EOS':
            if wclass[6] == None:
                word_class.append((word,wclass[0],wclass[1],wclass[2],""))
            else:
                word_class.append((word,wclass[0],wclass[1],wclass[2],wclass[6]))
        node = node.next
    return word_class


def load_csv(filename):
    with open(filename) as fin:
        reader = csv.reader(fin)
        inputs = [l for l in reader]
    return inputs
