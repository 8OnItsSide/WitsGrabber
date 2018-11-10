from fpdf import FPDF
from unidecode import unidecode

# -*- coding: utf-8 -*-

class PDF(FPDF):
    def add_attributes(self,f_name):
        # index = test.find('/')
        self.filename = f_name
        # self.filename = self.filename[-index:]
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 0,txt= 'University of the Witwatersrand Announcement', ln=1,align='C')

        self.multi_cell(0, 10,txt= self.filename,align='C')
        # self.image('config/images/8oislogoV2.png', 0, 0, 10)
        self.line(0,20,self.w,20)
        self.set_font('Arial', 'B', 8)
        self.ln()

    def footer(self):
        pass


def write_to_pdf(msg,fname, header_name=''):
    '''
    :param msg: string of message
    :return: None
    writes pdf to fname
    '''
    # print(msg[332])
    # msg = str(msg.encode('utf-8'))
    # msg = ''.join([i for i in msg])

    # msg = msg.replace(u'\u2013',u'-')
    try:
        msg = unidecode(msg)
        # fname = unidecode(fname)
        li = [i.strip() for i in msg.split('\n')]
        pdf = PDF(orientation='P')
        pdf.add_attributes(f_name=header_name)
        effective_page_width = pdf.w - 2 * pdf.l_margin
        cell_size = effective_page_width*0.9
        pdf.add_page()
        pdf.set_font('arial', 'B', 8.0)
        i=0
        h=5
        msgbool = False
        for line in li:
            if i==0:
                (pdf.set_font('Arial', 'B', 20.0))
                i+=1
                h=10
            elif not msgbool:
                h = 5
                pdf.set_font('Arial', 'B', 8.0)
            x = pdf.get_x()
            y = pdf.get_y()
            if y>=180:
                pdf.add_page()
            w = cell_size
            if line.lower() =='message':
                pdf.set_font('Arial', 'B', 20.0)
                h=10
                msgbool = True
            if line=='':
                continue
            else:
                pdf.multi_cell(w, h, txt=str(line), border=0)  # , align='L')
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.ln()
        pdf.output(fname)
    except:
        raise Exception
if __name__ =='__main__':
    pass