import streamlit as st
# import nltk
# nltk.download('stopwords')
from pyresparser import ResumeParser
import streamlit_tags as st_tags
import time
from utils import pdf_reader,get_similarity


st.set_page_config(
    page_title="AI RESUME MATCHER",
)


def run():
    st.title('AI RESUME MATCHER')
    link = '[Made with ❤️ by Karthik](https://github.com/sijju)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.markdown('<h5 style="text-align:center;color:#2dff34;">Upload Your Resume, and JD(Job Description) to check for matching job.</h5>',unsafe_allow_html=True)
    JD = st.text_input(label='JD', placeholder="Enter the job description...")
    pdf_file = st.file_uploader("Upload Your Resume",type=['pdf'])
    button =  st.button('Get Score')
    resume_text = ''
    if pdf_file is not None:
        with st.spinner('Uploading your resume ...'):
            time.sleep(2)
        save_pdf_path = '\Uploaded_Resumes ' + pdf_file.name
        with open(save_pdf_path,'wb') as f:
            f.write(pdf_file.getbuffer()) 
        resume_data = ResumeParser(save_pdf_path).get_extracted_data()
        
        if resume_data:
            resume_text = pdf_reader(save_pdf_path)
           
    if button:       
        resume_score = get_similarity(resume_text,JD)
        st.markdown(f'''<h2 style="text-align:center"> Similarity score between resume and JD is {resume_score} </h2>''',unsafe_allow_html=True)



run()