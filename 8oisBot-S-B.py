'''
    Readme
    -------
    Name: 8oisBot-S-B
    Version: V17
    Description: This program takes a users username and password to the
    University of The witwatersrand e-learning website (https://cle.wits.ac.za/portal/site) sakai
    and Downloads all the resources of the student to the local file system

    Changelog:
        Adding windows filename restriction things
'''
# import libraries
from requests import Session, post as r_post
from bs4 import BeautifulSoup
import traceback
import os
from timeit import default_timer as tmr
from GUI import get_un_pw, make_output_gui, add_output, output_new_file_names
from saveLoadVars import *
import sys
import json
from toPdf import write_to_pdf
from functions import *
import logging


new_files = []
var_li = ['config', 'vars']
var_dir = os.getcwd()
for i in var_li:
    var_dir = os.path.join(var_dir, i)
var_f_name = 'vars.txt'
# -----Authentication & Login: -----------------------------------------------

def get_auth(s_num, url='http://localhost:8000/checkIsIn.php', default= False):
    '''
    Checks if a certain student number has a valid 'licence'

    :param url: URL from which to get authentication from, will be 8onitsside.com/... when actually in production
    :param s_num: student number with which to authenticate
    :param default: If an error occurred with the authentication what should happen?
    :return: Boolean True if is authenticated, False else
    '''
    try:
        data = {'sNum':s_num, 'submit':'Submit', 'extra':'obfuscate342'}
        page = r_post(url=url, data=data)
        soup = BeautifulSoup(page.text, 'html.parser')
        ans_div = soup.find('div', {'id':'answer'})
        return ans_div.text.find('true')>=0
    except Exception:
        return default


def login(url, un, pw):
    '''
    Logs a user in to the url with un and pw

    :param url: Url to try logging in to (this wil be the main page of your university's page
    :param un: Username
    :param pw: Password
    :return: returns 1 if wrong login, 0 if correct
    '''
    data = {'eid': un, 'pw': pw}
    r = session.post(url, data=data)
    form_page = session.get(url)
    soup = BeautifulSoup(form_page.text, 'html.parser')
    form = soup.find('form', {'id':'Mrphs-xlogin'})
    find_text = (soup.text.find('Login Required'))
    if form is None:
        return 0
    return 1


def initialize_vars():
    '''
    Gets the initial (previous) values of username and foldername where data was stored last

    :return: Username that is stored, previous foldername that is stored
    '''
    if not os.path.exists(var_dir):
        os.makedirs(var_dir)
        with open(os.path.join(var_dir,var_f_name), 'w+') as f:
            f.write('')
        raise FileNotFoundError
    vars = total_load(os.path.join(var_dir,var_f_name))
    pre_un = vars.username
    pre_filepath = vars.filepath
    return pre_un, pre_filepath


def start_logs():
    if not os.path.exists('config/logs'):
        os.makedirs('config/logs')
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='config/logs/log.log',
    #                     format='Time: [%(asctime)s] - fName: [%(funcName)s] - name:[%(name)s] - level:[%(levelname)s] - msg:[%(message)s]')
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.CRITICAL)
    # create a file handler
    handler = logging.FileHandler('config/logs/log.log')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    # formatter = logging.Formatter('%(asctime)s -%(funcName)%- %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('Time: [%(asctime)s] - fName: [%(funcName)s] - name:[%(name)s] - level:[%(levelname)s] - msg:[%(message)s]')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


# -----Messages & errors: -----------------------------------------------

def error(e,trace_back, where):
    '''
    Displays error with given parameters

    :param e: error name
    :param trace_back: python's traceback
    :param where: in which function the error occurred
    :return: None
    '''
    # msg('An error ({}) occurred at function {}\n.Traceback: {}'.format(e,where,trace_back), 0, is_end_of_program=2)
    msg('An error ({}) occurred at function {}.\n We apologize, please contact support at {}'.format(e, where, 'support@8onitsside.com'), 0, is_end_of_program=2)
    logger.error('An error ({}) occurred at function {}\n.Traceback: {}'.format(e,where,trace_back))


def msg(m, end, t_count=0, is_end_of_program=0):
    '''
    This function outputs a message to stdout and gui

    :param m: Message
    :param end: is end of message, will add and 'Complete' to the message
    :param t_count: indent level of message
    :param is_end_of_program:   0 => Not end, just normal
                                1 => Normal end of program
                                2 => Program terminated with an error
    :return: None
    '''
    s= ''
    if end:
        e = ' Complete\n{}'.format('-'*10)
        s = ' Done\n'
    else:
        e = '...'
    if m!='':
        print('\t'*t_count+m+e)
    err = add_output('\t'*t_count+m+s, is_end_of_program)
    logger.debug('{}, isEnd: {}, s: {}'.format(m, is_end_of_program, s))
    if is_end_of_program==2:
        logger.error('msg: {}, isEnd: {}, s: {}'.format(m, is_end_of_program, s))
    if err ==2:
        sys.exit()


# -----Getting Data: -----------------------------------------------

def get_all_urls_from_home(home_url ='https://cle.wits.ac.za/portal', id = 'selectSiteModal'):
    '''
    Gets all the urls and filenames of all the subjects from the home_url

    :param home_url: url of logged in home page
    :param id: html div element id where the courses are stored
    :return: links to subject pages and the filenames
    '''
    hrefs, filenames =[], []
    home_page = session.get(home_url)
    soup = BeautifulSoup(home_page.text, 'html.parser')
    div_modal = soup.find_all('div', {'id':id})
    for div in div_modal:
        select_site = div.find('div', {'id':'selectSite'})
        ul = select_site.find('ul' , {'class':'otherSitesCategorList favoriteSiteList'})
        div_links = ul.find_all('div', {'class':'fav-title '})
        for div_link in div_links:
            a_s = div_link.find_all('a')
            for a in a_s:
                href = a.get('href', 'null')
                if href=='null':
                    continue
                f_name = a.get('title','null')
                href = href.replace('portal/site','access/content')
                hrefs.append(href)
                filenames.append(f_name)
    return hrefs, filenames



# -----Main writing to file code: -----------------------------------------------

def write_one_subject(subject_url, subject_file_name, f_dir):
    '''
    Downloads and writes all resources from  one subject to the disk

    :param subject_url: url where to find subject directory
    :param subject_file_name: subject filename
    :param f_dir: directory where files should be saved
    :return: subject filename
    '''
    # subject_file_name = subject_file_name.replace(':', '-')
    subject_file_name = windows_friendly_filename(subject_file_name)
    msg('Getting Subject {} '.format(subject_file_name),0)
    written = iterate_over_files_v2(os.path.join(f_dir, subject_file_name),subject_url,write=True)
    msg('Getting Subject {} '.format(subject_file_name), 1)
    return subject_file_name


def iterate_over_files_v2(f_dir, page_url, write = True, write_duplicates = False, tab_count=1):
    '''
    Recursively iterates over files and folders within a directory and saves them to disk

    :param f_dir: filedirectory where files need to be saved
    :param page_url: url where files and folders are (most of the time subject directory)
    :param write: True if actual writing to disk should occur, False if not. For testing
    :param write_duplicates: True if duplicates should be overwritten, else duplicates will be bypassed
    :param tab_count: level of indentation of folder
    :return:
    '''
    page_text = session.get(page_url)
    msg('',0)
    soup = BeautifulSoup(page_text.text, 'html.parser')
    lis_files = soup.find_all('li', {'class':'file'})
    lis_folders = soup.find_all('li', {'class':'folder'})

    # -----Files: -----------------------------------------------

    for file_li in lis_files:
        a_s = file_li.find_all('a')
        for a in a_s:
            href = (a.get('href', ''))
            if page_url[-1] != '/':
                page_url += '/'
            if f_dir.find('%') >= 0:
                f_dir = f_dir.replace('%20', ' ')

            #
            # f_dir = f_dir.replace('//', '/')
            # f_dir = re.sub('\s*/\s*', '/', f_dir)
            # f_dir = f_dir.replace('\\\\', '\\')
            # f_dir = f_dir[:2] + f_dir[2:].replace(':','-')
            #

            f_dir = windows_friendly_filename(f_dir)
            # Added this b4 instead of after end

            online_file_name = a.text.strip()

            # Added 18/07/17
            online_file_name = windows_friendly_filename(online_file_name)
            # Added 18/07/17 end
            filename_write = os.path.join(f_dir, online_file_name)

            if not write_duplicates:
                if os.path.exists(filename_write):
                    continue
            if href.find('/') >= 0:
                continue

            # -----Write: -----------------------------------------------

            if write:
                file_url = page_url + href
                file = session.get(file_url, stream = True)
                if not os.path.exists(f_dir):
                    os.makedirs(f_dir)
                with open(filename_write, 'wb+') as f:
                    msg('Getting new file {}'.format(filename_write.split('/')[-1]), 0, t_count=tab_count)
                    for chunk in file.iter_content(chunk_size=1024*1024):
                        msg('', 0)
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                new_files.append(online_file_name)
            else:
                pass

    # -----Folders: -----------------------------------------------

    for folder_li in lis_folders:
        a_s = folder_li.find_all('a')
        for a in a_s:
            href = (a.get('href', ''))
            name_f = a.text.strip()
            #Added 18/07/17
            name_f = windows_friendly_filename(name_f)
            #Added 18/07/17 end
            msg('Downloading folder ({})'.format(name_f),0, t_count= tab_count)
            if page_url[-1] != '/':
                page_url+='/'
            folder_url = page_url + href
            iterate_over_files_v2(os.path.join(f_dir, name_f), folder_url, tab_count=tab_count+1)
            msg('Downloading folder ({})'.format(name_f), 1,t_count=tab_count)


# -----Getting Announcements: -----------------------------------------------

def get_announcements_sites_dic(links, names, home_url ='https://cle.wits.ac.za/portal'):
    '''
    Gets the urls of the subjects' Announcement page as a dictionary, indexed by subject name

    :param links: list of links to subject sites
    :param names: list of subject names
    :param home_url: url of home logged in page
    :return:
    '''
    answer = {}
    for link, name in zip(links, names):
        temp = link.replace('access/content', 'direct/site')
        if temp[-1] !='/':
            temp+='/'
        temp += 'pages.json'
        page = session.get(temp)
        a = json.loads(page.text)
        for dic in a:
            tools = dic.get('tools',None)
            siteId = dic.get('siteId',None)
            if tools is not None:
                for page in tools:
                        toolId = page.get('toolId',None)
                        if toolId=='sakai.announcements':
                            url = page.get('url', None)
                            if url is not None:
                                answer[name] = url
    #Main Page
    page = session.get(home_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    nav_menu = soup.find('nav', {'id': 'toolMenu'})
    list = nav_menu.find('ul')
    lis = list.find_all('li')
    for li in lis:
        try:
            a = li.find('a')
            href = a.get('href', None)
            title = a.get('title', None)
            if title.find('Announcements') >= 0 and href is not None:
                answer['Main'] = href
        except Exception:
            pass


    return answer


def get_announcements(site_dic, f_dir):
    '''
    Gets, and writes top 10 announcements of each subject  in f_dir/_subject_name/Announcements

    :param site_dic: Dictionary of subject_name:url
    :param f_dir: filedirectory where Announcements should be stored
    :return:
    '''
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    for subject_title in site_dic:
        msg('Getting {} Announcements'.format(subject_title),0)
        if subject_title !='Main':
            folder_path = os.path.join(f_dir, subject_title,'Announcements')

        else:
            folder_path = os.path.join(f_dir,'Announcements')

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        url = site_dic[subject_title]
        announcement_page = session.get(url)
        soup = BeautifulSoup(announcement_page.text, 'html.parser')
        titles = soup.find_all('th', {'headers':'subject'})
        l = len(titles)
        i=0
        for announcement_link in titles[::-1]:
            i+=1
            msg('Getting Announcement {} out of {}'.format(i,l),end=0,t_count=1)
            a = announcement_link.find('a')
            href = a.get('href')
            announcement = session.get(href)
            announcement_soup = BeautifulSoup(announcement.text,'html.parser')
            body = announcement_soup.find('div', {'class':'portletBody'})
            header = body.find('div', {'class':'page-header'})
            header = header.find('h2').text
            header = windows_friendly_filename(header)
            # header = re.sub('[/\\\:%]','-',header)
            message=body.text.strip()
            folder = os.path.join(folder_path, header)
            folder = folder.strip()
            attach_li = body.find('ul', {'class':'attachList'})
            if not os.path.exists(folder):
                os.makedirs(folder)
            if attach_li is not None:
                lis = attach_li.find_all('li')
                for li in lis:
                    a = li.find('a')
                    href = a.get('href',None)
                    name = a.text.strip()
                    name = windows_friendly_filename(name)
                    if href ==None:
                        continue
                    filename= os.path.join(folder, name)
                    if os.path.exists(filename):
                        continue
                    file = session.get(href)
                    with open(filename, 'wb+') as f:
                        f.write(file.content)
            # header = windows_friendly_filename(header)
            header = header.replace('/','-')
            name = os.path.join(folder, '{}_{}.pdf'.format(header, 'message'))
            try:
                if os.path.exists(name) or os._exists(name[:-3] + '.txt'):
                    continue
                else:
                    message = make_msg_pretty(message)
                try:
                    write_to_pdf(message,name, header_name=header)
                except Exception:
                    name = name[:-3]
                    name +='txt'
                    with open(name, 'w+', encoding='utf-8') as f:
                        f.write(message)
                if subject_title.lower() !='main':
                    new_files.append(header)
            except Exception:
                pass
        msg('Getting {} Announcements'.format(subject_title), 1)
    return


# -----Driver: -----------------------------------------------

def driver(do_gui = True, add_s_number = True, url=None):
    '''
    A driver function for the entire program, handles logins, getting files etc.

    :param do_gui: Should there be a gui
    :param add_s_number: Add student number to url, e.g. cle../portal/site/ -> cle../portal/site/~<student_number>
    :param url: url of page to login and do stuff with
    :return:
    '''
    try:
        err_msg = ''
        while True:
            if do_gui:
                try:
                    pre_un, pre_filepath = initialize_vars()
                except FileNotFoundError:
                    pre_un, pre_filepath = None, None
                un, pw, folder_path, uni = get_un_pw(err_msg=err_msg,
                                   pre_un=pre_un,
                                   pre_filepath=pre_filepath)
            else:
                print(err_msg)
                un, pw, folder_path = get_un_pw_cmd()
                uni = 'University Of The Witwatersrand'
            if un =='' or pw == '':
                msg('Username or Password is empty. Exiting',0)
                return 1,1
            msg('Logging in',0)
            if url is None:
                url = get_url(uni)
            if add_s_number and url =='https://cle.wits.ac.za/portal/site/':
                url +='~'+un
            #Check Auth:
            is_valid = get_auth(s_num = un, url='https://8onitsside.com/Commerce/checkIsIn.php')
            if not is_valid:
                err_msg = 'Sorry, your student number is not registered to use this software. Please contact {} to purchase a license'.format('support@8OnItsSide.com')
                continue
            is_wrong_login = login(url, un, pw)
            if is_wrong_login:
                err_msg = 'Wrong username or password. Please Try again.'
            else:
                msg('Logging In',1)
                break
    except Exception as e:
        error(e,traceback.format_exc(),'Driver, logging in')
        return 1,1
    try:
        print(folder_path)
        make_output_gui()
        url_list, folder_names = get_all_urls_from_home()
        f_dir = make_dirs(f_name= folder_path)
        name_list = []
        for url_name, file_name in zip(url_list, folder_names):
            name_list.append( write_one_subject(url_name, file_name, f_dir))
        site_dic = (get_announcements_sites_dic(links=url_list,names=name_list, home_url=url))
        site_dic = {windows_friendly_filename(i): site_dic[i] for i in site_dic}
        try:
            get_announcements(site_dic=site_dic, f_dir=f_dir)
        except Exception as e:
            error(e, traceback.format_exc(), 'Getting Announcements')
        session.close()
        try:
            var_dic = {'username':un,
                       'filepath':folder_path}
            total_save(filename=os.path.join(var_dir,var_f_name), dic=var_dic)
            output_new_file_names(new_files)
            return 0, folder_path
        except Exception as e:
            error(e, traceback.format_exc(), 'Saving vars')
    except Exception as e:
        error(e, traceback.format_exc(), 'Driver, getting data')
        return 1,1


do_driver = 1

if __name__ == '__main__':
    url = 'https://cle.wits.ac.za/portal/site/'
    logger = start_logs()
    session = Session()
    if do_driver:
        s = tmr()
        err = driver(do_gui=True,
                    add_s_number=True)
        e= tmr()
        if not err[0]:
            a = divmod(e-s, 60)
            msg('Time taken: {} minutes {} seconds'.format(round(a[0]), round(a[1])),0, is_end_of_program=0)
            msg('Completed Succesfully.\nAll the files are saved in\n{}'.format(err[1]),0, is_end_of_program=1)
        else:
            msg('An error occurred while writing to the folder', 0, is_end_of_program=2)
    else:
        gui = make_output_gui()
