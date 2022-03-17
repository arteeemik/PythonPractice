import argparse
import ast
import astunparse
import importlib
import inspect
import textwrap
import difflib


SERVICE_PREFIX = '__'
ATTRIBUTES = ['name', 'id', 'arg', 'attr']
MIN_RATIO = 0.95


def get_preparete_func(function_obj):
    code = inspect.getsource(function_obj)
    if code.startswith(' '):
        code = textwrap.dedent(code)
    tree = ast.parse(code)
    for v in ast.walk(tree):
        for attribute in ATTRIBUTES:
            if hasattr(v, attribute):
                setattr(v, attribute, '_')
    return astunparse.unparse(tree)


def get_parse_data(data, prefix):
    ans = []

    function_members = inspect.getmembers(data, inspect.isfunction)
    for function_name, function_obj in function_members:
        ans.append((prefix + '.' + function_name, get_preparete_func(function_obj)))

    classes = inspect.getmembers(data, inspect.isclass)
    for name, obj in classes:
        if not name.startswith(SERVICE_PREFIX):
            ans.extend(get_parse_data(obj, prefix + '.' + name))

    return ans


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dublicate finder.')
    parser.add_argument('modules', nargs='+', type=str, help='name of python module')

    args = parser.parse_args()

    modules = args.modules

    data_list = []
    for module in modules:
        imported_module = importlib.import_module(module)
        data_list.extend(get_parse_data(imported_module, module))

    data_dict = {}
    for func_name, func_code in data_list:
        data_dict[func_name] = func_code

    ans = []
    for key1, value1 in data_dict.items():
        ratio = -1
        ans_key_2 = None
        for key2, value2 in data_dict.items():
            if key2 == key1:
                continue
            ratio_test = difflib.SequenceMatcher(None, value1, value2).ratio()
            if ratio_test > MIN_RATIO and ratio_test > ratio:
                ans_key_2 = key2
                ratio = ratio_test
        if ratio > MIN_RATIO and (key1, ans_key_2) not in ans and (ans_key_2, key1) not in ans:
            ans.append((key1, ans_key_2))

    ans = sorted(ans, reverse=False)
    for key1, key2 in ans:
        print(f'{key1} {key2}')
