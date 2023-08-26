from pyresparser import ResumeParser
from pdfminer3.layout import LAParams,LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter


import base64
import io
import streamlit as st



def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)

    b64 = base64.b64decode(csv.encode()).decode()

    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}>{text}</a>'
    return href


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_manager = io.StringIO()
    converter  = TextConverter(resource_manager,fake_file_manager,laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager,converter)
    with open(file,"rb") as f:
        for page in PDFPage.get_pages(f,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_manager.getvalue()
    
    converter.close()
    fake_file_manager.close()
    return text


def show_pdf(file_path):
    with open(file_path,'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="720" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display,unsafe_allow_html=True)


def course_recommender(course_list):
    st.subheader('Courses & Certifications recommended')
    c=0
    rec_course = []
    for c_name,c_link in course_list:
        c+=1
        st.markdown(f'({c})[{c_name}]({c_link})')
        rec_course.append(c_name)
    return rec_course

