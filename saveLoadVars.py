import os

class Variables():
    def __init__(self):
        self.username = None
        self.filepath = None
    def from_dict(self,dic):
        self.username = dic.get('username',None)
        self.filepath = dic.get('filepath',None)

    def to_dict(self):
        dic = {}
        dic['username'] = self.username
        dic['filepath'] = self.filepath
        return dic


def load_vars(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError
    with open(filename, 'r') as f:
        li = f.readlines()
    li = [i.split('###=>') for i in li]
    dic = {i[0].strip(): i[1].strip() for i in li}
    return dic


def save_vars(filename,dic_vars, overwrite = True):
    if os.path.exists(filename) and not overwrite:
        raise FileExistsError
    with open(filename, 'w+') as f:
        for key in dic_vars:
            f.write('{}###=>{}\n'.format(key, dic_vars[key]))
    return 0


def get_variables_from_dic(dic):
    variables = Variables()
    variables.from_dict(dic)
    return variables


def variable_to_dict(var):
    dic = var.to_dict()
    return dic


def total_load(filename):
    dic = load_vars(filename)
    vars = get_variables_from_dic(dic)
    return vars


def total_save(filename, dic):
    save_vars(filename,dic,True)