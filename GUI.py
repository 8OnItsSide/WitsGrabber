from tkinter import *
from platform import system as platform
import os
from tkinter.filedialog import  askdirectory
from tkinter.messagebox import askyesno
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
un = ''
pw = ''
f_path = os.getcwd()

is_open_output = False


class GUI:
    def __init__(self, err_msg='', pre_un='', pre_filepath=None, isOutput= False):
        self.still_running = False
        self.un_pw = []
        self.master = Tk()
        self.bottom_row = 30
        self.isOutput = isOutput
        # self.bgcolor = "#FFF0F5"
        self.bgcolor = '#808080'
        # self.widgetcolor = '#FFF0F5'
        self.widgetcolor = '#FFFFFF'
        self.input_widget_width=30
        self.input_widget_height = 2
        self.input_widget_font = 'Arial 15 bold'
        self.input_widget_bwidth = 2
        self.input_widget_brelief = 'raised'
        # -----Centering: -----------------------------------------------
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        # print(self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # size_w = int(screen_width * 0.3)
        # size_h = int(screen_height * 0.4)
        # size_w = 920
        # size_h = 410
        self.master.geometry('+{}+{}'.format(int(self.master.winfo_screenwidth()*0.01), int(self.master.winfo_screenheight()*0.01)))
        self.master.title('Login')
        self.time_left = 0
        self.master.configure(background= self.bgcolor)
        # -----Labels: -----------------------------------------------
        if not self.isOutput:
            self.make_normal_gui(err_msg=err_msg,
                                 pre_un=pre_un,
                                 pre_filepath=pre_filepath)
        else:
            self.make_output_gui()

        self.master.bind('<Return>',self.onenter)
        self.master.focus_force()
        self.master.protocol('WM_DELETE_WINDOW', self.kill)  # root is your root window
        self.num_headings=0
        if  platform() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def make_output_gui(self):

        # Output
        size_w = 920
        size_h = 450
        self.master.geometry('{}x{}+{}+{}'.format(size_w, size_h,int(self.master.winfo_screenwidth()*0.01), int(self.master.winfo_screenheight()*0.01)))
        self.master.title('Output Status')
        self.output_labels = []
        self.scroll_text_out = StringVar()
        self.outputText = StringVar()
        self.outputText.set('Status')
        self.lbl_Output = Label(self.master,
                                textvariable=self.outputText,
                                fg='Blue',
                                font='Helvetica 18 bold',
                                borderwidth=4,
                                relief='ridge',
                                background= self.widgetcolor)
        self.output_overview = scrolledtext.ScrolledText(self.master,
                                                         height=5,
                                                         # width= 100,
                                                         state=DISABLED,
                                                         font='Arial 20 bold',
                                                         background=self.bgcolor,
                                                         highlightbackground=self.bgcolor
                                                         )

        self.output_overview.grid(row=0, column=0, columnspan=1, sticky='w')

        self.output_scrolltext = scrolledtext.ScrolledText(self.master,
                                                           height=5,
                                                           # width=100,
                                                           state=DISABLED,
                                                           font='Arial 20 bold',
                                                           fg='Blue',
                                                           background = self.bgcolor,
                                                           highlightbackground=self.bgcolor
                                                           )
        self.output_scrolltext.grid(row=3, column=0, columnspan=2, sticky='w')

        self.QUIT = Button(self.master,
                           text="QUIT",
                           command=self.kill,
                           highlightbackground=self.bgcolor)

        self.QUIT.grid(row=4, column=0, columnspan=1, sticky='ew')
        self.current_row = 4

        color_dic = {'normal': ['blue', 'Arial 15'],
                     'end': ['black', 'Arial 18 bold'],
                     'err': ['red', 'Arial 18 bold']}
        for key in color_dic:
            self.output_scrolltext.tag_config(key, foreground=color_dic[key][0])
            f = color_dic[key][1]
            if f is not None:
                self.output_scrolltext.tag_config(key, font=f)

    def make_normal_gui(self, err_msg, pre_filepath, pre_un):
        # -----Labels: -----------------------------------------------
        self.lbl_pad=(10,30)
        self.lbl_heading = Label(self.master, fg='black',
                                 font='Helvetica 18 bold',
                                 borderwidth=2,
                                 relief='ridge',
                                 text="\nEnter Username & Password for sakai and choose a file where your recources will be saved:\n{}".format(
                                     '' * 100),
                                 background=self.bgcolor)

        self.lbl_heading.grid(row=0, column=0, columnspan=3)#, sticky='w')


        self.lbl_un = Label(self.master, text="Username:",
                            background=self.widgetcolor,
                            height=self.input_widget_height,
                            width=self.input_widget_width,
                            font= self.input_widget_font,
                            borderwidth=self.input_widget_bwidth,
                            relief=self.input_widget_brelief)

        self.lbl_un.grid(row=1, column=0, columnspan=1, sticky='w', padx=self.lbl_pad)


        self.lbl_pw = Label(self.master, text="Password:",
                            background=self.widgetcolor,
                            height=self.input_widget_height,
                            width=self.input_widget_width,
                            font= self.input_widget_font,
                            borderwidth=self.input_widget_bwidth,
                            relief=self.input_widget_brelief)

        self.lbl_pw.grid(row=2, column=0, columnspan=1, sticky='w', padx=self.lbl_pad)


        self.lbl_file_caption = Label(self.master, text='Location to save resources:',
                                      background=self.widgetcolor,
                                      height=self.input_widget_height,
                                      width=self.input_widget_width,
                                      font= self.input_widget_font,
                                      borderwidth=self.input_widget_bwidth,
                                      relief=self.input_widget_brelief)

        self.lbl_file_caption.grid(row=3, column=0, columnspan=1, sticky='w', padx=self.lbl_pad)


        self.uniLabel = Label(self.master, text="University:",
                              background=self.widgetcolor,
                              height=self.input_widget_height,
                              width=self.input_widget_width,
                              font= self.input_widget_font,
                              borderwidth=self.input_widget_bwidth,
                              relief=self.input_widget_brelief)

        self.uniLabel.grid(row=4, column=0, sticky='w', columnspan=1, padx=self.lbl_pad)


        # -----File path Choice: -----------------------------------------------
        self.path = StringVar()
        b_f_got = False
        if pre_filepath is not None:
            if os.path.exists(pre_filepath):
                self.path.set(pre_filepath)
                b_f_got = True
        if not b_f_got:
            self.path.set(os.getcwd())
        self.lbl_filename = Label(self.master, textvar=self.path,
                                  fg='blue',
                                  background=self.widgetcolor,
                                  borderwidth=self.input_widget_bwidth,
                                  relief=self.input_widget_brelief
                                  )

        self.lbl_filename.grid(row=3, column=1, columnspan=1, sticky='w')

        # -----Add University Coice: -----------------------------------------------
        choices = ['University Of The Witwatersrand', 'North West University']
        self.UniText = StringVar()
        self.UniText.set(choices[0])
        self.Uni = ttk.OptionMenu(self.master, self.UniText,
                                  choices[0], *choices)
        self.Uni.grid(row=4, column=1, sticky='w')

        # -----Entry Fields: -----------------------------------------------
        if pre_un is None: pre_un = ''
        self.un = StringVar()
        self.un.set(pre_un)
        self.txt_un = Entry(self.master, textvariable=self.un,
                            background=self.widgetcolor,
                            highlightbackground=self.widgetcolor,
                            borderwidth=self.input_widget_bwidth,
                            relief=self.input_widget_brelief)

        self.txt_un.grid(row=1, column=1, columnspan=1, sticky='w')
        self.txt_un.focus_set()


        self.pw = StringVar()
        self.pw.set('')
        self.txt_pw = Entry(self.master, show='*', textvariable=self.pw,
                            background=self.widgetcolor,
                            highlightbackground=self.widgetcolor,
                            borderwidth=self.input_widget_bwidth,
                            relief=self.input_widget_brelief
                            )

        self.txt_pw.grid(row=2, column=1, columnspan=1, sticky='w')

        # -----Buttons: ----------------------------------------------
        self.err = StringVar()
        self.err.set(err_msg)
        self.SPACER2 = Label(self.master,
                             textvariable=self.err,
                             fg='red',
                             font='Arial 24 bold',
                             background =self.bgcolor
                             )
        self.SPACER2.grid(row=12, column=0, columnspan=3)

        self.QUIT = Button(self.master, text="QUIT",
                           command=self.quit,
                           background=self.bgcolor,
                           highlightbackground=self.bgcolor)

        self.QUIT.grid(row=self.bottom_row, column=0, columnspan=1, padx=0)


        self.btn_submit = Button(self.master, text="Submit",
                                 command=self.submit,
                                 background=self.bgcolor,
                                 highlightbackground=self.bgcolor)
        self.btn_submit.grid(row=self.bottom_row, column=1, columnspan=1)

        self.btn_choose_file = Button(self.master, text="Choose Folder",
                                      command=self.choose_file, highlightbackground=self.bgcolor,
                                      font=self.input_widget_font)
        self.btn_choose_file.grid(row=3, column=2, columnspan=1 , sticky='w')

    def choose_file(self):
        filename = askdirectory()
        if filename !='':
            self.path.set(filename)

    def wrong(self, msg):
        self.err.set('Please enter a {}!'.format(msg))

    def decrement(self):
        self.time_left-=1
        self.master.after_cancel(self.id)
        if self.time_left<=0:
            self.master.quit()
            return
        self.id = self.master.after(self.time, self.decrement)

    def start(self, time =0):
        self.isnotquit = True
        self.time_left = 0
        self.time = time
        self.still_running = True

        if time:
            self.id =self.master.after(time, self.decrement)
        self.master.mainloop()

    def raise_above_all(self):
        self.master.attributes('-topmost', 1)

    def get_input(self):
        return self.txt_un.get(), self.txt_pw.get(), self.path.get()

    def kill(self):
        self.still_running = False
        self.master.destroy()

    def quit(self):
        self.un.set('')
        self.pw.set('')
        self.isnotquit = False
        self.master.destroy()

    def submit(self):
        global un, pw, f_path
        un, pw, f_path = gui.get_input()
        if un == '':
            self.wrong('Username')
            return 1
        if pw == '':
            self.wrong('Password')
            return 1
        if askyesno("Confirm", "Are you sure this is the correct folder to store the data in?\n{}".format(self.path.get())):
            self.kill()
            pass
        else:
            un,pw = '', ''

    def onenter(self,event):
        self.submit()

    def get_all_children(self):
        _list = self.master.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        return _list

    def del_all_children(self):
        for elem in self.master.grid_slaves():
            elem.grid_forget()

    def make_label(self,msg,name='normal'):
        # lbl_temp = Label(self.master,
        #                         text= msg,
        #                         fg= col,
        #                         font=' Helvetica 18 bold',
        #                         borderwidth=4,
        #                         relief='ridge')
        # self.output_labels.append(lbl_temp)
        # self.output_labels[-1].grid(row=self.current_row, column=0, columnspan=2, sticky='w')
        if msg=='':
            return
        self.output_scrolltext.config(state=NORMAL)
        self.output_scrolltext.insert(END, '{}\n'.format(msg), name)
        self.output_scrolltext.yview(END)
        self.output_scrolltext.config(state=DISABLED)

        if msg.find('Getting Subject ')>=0:
            end = ''
            if self.num_headings % 2==1:
                end = '\n'+'*'*100
            self.num_headings+=1
            self.output_overview.config(state=NORMAL)
            self.output_overview.insert(END,'{}\n{}{}'.format('',msg,end))
            self.output_overview.yview(END)
            self.output_overview.config(state=DISABLED)
        self.current_row+=1

    def make_new_div(self, pos='right'):
        # self.new_file_frame = Frame(self.master, background='red', height=self.master.winfo_reqheight()*3,width=400)
        # self.new_file_frame.grid(row=0, column=20, rowspan=20)

        # return
        self.new_div_text = StringVar()
        self.new_div_header = Label(self.master,
                                    textvariable= self.new_div_text,
                                    bg='green',
                                    fg='black',
                                    font= 'Arial 24 bold',
                                    justify= 'center',
                                    width=70,
                                    borderwidth=4,
                                    relief='ridge',
                                    height=1)
        self.new_div_header.grid(row=self.bottom_row+2, column= 0, pady=5, sticky='w')

        self.new_div = scrolledtext.ScrolledText(self.master,
                                                 state=NORMAL,
                                                 font= 'Arial 20 bold',
                                                 fg='blue',
                                                 bg='white',
                                                 borderwidth=2,
                                                 relief='raised',
                                                 background = self.bgcolor,
                                                 highlightbackground= 'black',
                                                 height=5)

        self.new_div.grid(column=0,row=self.bottom_row+3,rowspan=1, sticky='w')
        self.new_div.tag_config('heading',justify='center')
        self.new_div.tag_config('heading',font= 'Arial 20 bold')
        self.new_div.config(state=DISABLED)

    def output_new_files(self, li):
        try:
            self.new_div
        except Exception:
            self.make_new_div()
        finally:
            self.new_div.config(state=NORMAL)
        self.new_div_text.set('\n{} New files or announcements:\n'.format(len(li)))
        for elem in li:
            self.new_div.insert(END, '{}\n\n'.format(elem))
            pass
        self.new_div.config(state=DISABLED)


def get_input(err_msg = '', pre_un='', pre_filepath=None):
    global gui
    gui = GUI(err_msg, pre_un=pre_un, pre_filepath=pre_filepath)
    gui.start()


def get_un_pw(err_msg = '', pre_un='', pre_filepath=None):
    # global un, pw
    global gui
    un, pw, foldername, uni = '', '', '', ''

    get_input(err_msg=err_msg, pre_un=pre_un, pre_filepath=pre_filepath)
    if gui.isnotquit:
        print(gui.UniText.get())
        un, pw, foldername, uni = gui.un.get(), gui.pw.get(), gui.path.get(), gui.UniText.get()

    del gui
    return un,pw, foldername, uni


def make_output_gui():
    global gui, is_open_output
    gui = GUI(isOutput=True)
    is_open_output = True
    gui.start(100)


def add_output(msg, is_end=0):
    global gui, is_open_output
    if not is_open_output:
        return 1
    if not gui.still_running:
        return 2
    if gui.isOutput:
        # gui.outputText.set(gui.outputText.get()+'\n' + msg)
        if is_end:
            if is_end==1:
                name = 'end'
            else:
                name = 'err'
            gui.make_label('{}\n{}'.format('-'*100,msg), name= name)
            gui.start()
        else:
            gui.make_label(msg)
            gui.start(100)
    else:
        return 1


def output_new_file_names(li):
    global gui
    gui.output_new_files(li)
    gui.start(100)


if __name__ == '__main__':
    a = GUI(isOutput=1)
    # self.master.columnconfigure(1, weight=10)
    a.output_new_files([str(i) for i in range(100)])
    for i in [str(i) for i in range(100)]:
        a.make_label(i);
    a.make_label('Getting Subject -')
    a.start()
