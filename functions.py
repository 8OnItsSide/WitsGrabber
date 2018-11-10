import getpass
import os
import re
from unidecode import unidecode
def make_f_name_good(f_name):
    '''
    One of the filename functions, makes it acceptable for os's
    :param f_name: filename
    :return: Good filename
    '''
    f_name = f_name[:2] + f_name[2:].replace(':','-')
    return f_name


def get_un_pw_cmd():
    '''
    Gets un, pw, folder_path from cmdline
    :return: un, pw, folder_path
    '''
    un = input('UN?\n')
    pw = getpass.getpass('PW?\n')
    folder_path = input('In What folder should the file be saved?.\nDefaults to Desktop/WitsData')
    if folder_path == '':
        home = os.path.expanduser('~')
        desktop = os.path.join(home,'Desktop')
        folder_path = os.path.join(desktop,'WitsData')
    return un, pw, folder_path


def make_msg_pretty(message):
    '''
    Makes Announcement message pretty

    :param message: Announcements message
    :return: pretty message
    '''
    message = message.strip()
    message = re.sub('[\t]{1,}', '', message)
    message = re.sub(r'([^\n])[\n]{2}', r'\1 ', message)
    message = re.sub('\n{3}', '\n', message)
    message = re.sub('\n ', '', message)
    message = re.sub(' {1,}', ' ', message)
    message = message.replace('Attachments', '\n\n{}'.format('Attachments'))
    message = message.replace('Message', '\n\n{}'.format('Message'))
    return message



def get_url(uni_option):
    '''

    :param uni_option: choice of university
    :return: url corresponding to above choice
    '''
    uni_dict = {'University Of The Witwatersrand': 'https://cle.wits.ac.za/portal/site/',
                'North West University': 'http://efundi.nwu.ac.za/portal/xlogin/'}
    return uni_dict.get(uni_option,'https://cle.wits.ac.za/portal/site' )


def make_dirs(f_name='Resources1'):
    '''
    Makes folders if not exists and returns fname
    :param f_name: filename to make
    :return:
    '''
    if not os.path.exists(f_name):
        os.makedirs(f_name)
    f_dir = f_name
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    return f_dir


def windows_friendly_filename(name):
    '''
    returns a windows friendly filename

    :param name: filename
    :return: win friendly filename
    '''
    name = unidecode(name)
    start = ''
    # print (name)
    if name[1:3] == ':\\' or name[1:3]==':/':
        start = name[0:3]
        name = name[3:]
    forbidden = {'<','>', ':', '"', '|', '?', '*'}
    name = ''.join(i if i not in forbidden else '-' for i in name)
    name = unidecode(name)
    name = name.strip()
    name = start+name

    name = name.replace('//', '/')
    name = re.sub('\s*/\s*', '/', name)
    name = name.replace('\\\\', '\\')
    name = name[:2] + name[2:].replace(':', '-')
    
    return name
