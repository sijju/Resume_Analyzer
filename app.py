import nltk
nltk.download('stopwords')
import spacy.cli
spacy.cli.download('en_core_web_sm','--no-deps')
import time
from pyresparser import ResumeParser
import streamlit as st
import pymysql
from streamlit_tags import st_tags
from PIL import Image
from Courses import ds_course,web_course,design_course,interview_videos,ios_course,android_course,resume_videos
from utils import pdf_reader,show_pdf,get_csv_download_link,course_recommender
import nltk
nltk.download('stopwords')




st.set_page_config(
    page_title="AI RESUME ANALYZER",
)

# connection = pymysql.connect(host='127.0.0.1',user='root',password='sijjugaduji12A',db='resume')

# cursor = connection.cursor()


# def insert_data(name,email,res_score,timestamp,page_no,reco_field,cand_level,skills,recommended_skills,courses,pdf_name):
#     DB_TABLE_NAME = 'users_info'
#     insert_sql = "insert into"+DB_TABLE_NAME + """
#                   values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     rec_values = (name,email,str(res_score),timestamp,str(page_no),reco_field,cand_level,skills,recommended_skills,courses,pdf_name)
#     cursor.execute(insert_sql,rec_values)
#     connection.commit()

def run():
    st.title("AI Resume Analyser")
    
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose User:" ,activities)
    link = '[Made with ❤️ by Karthik](https://github.com/sijju)'
    st.sidebar.markdown(link, unsafe_allow_html=True)

    # db_sql = """CREATE DATABASE IF NOT EXISTS resume"""
    # cursor.execute(db_sql)


    #creating user_data table

    # DB_TABLE_NAME = 'users_info'
    # table_sql = "CREATE TABLE IF NOT EXISTS "+DB_TABLE_NAME + """
    #             (ID INT NOT NULL AUTO_INCREMENT,
    #             Name varchar(100) NOT NULL,
    #             EMAIL_ID varchar(100) NOT NULL,
    #             resume_score varchar(8) NOT NULL,
    #             Timestamp varchar(100) NOT NULL,
    #             Page_no varchar(5) NOT NULL,
    #             Predicted_field BLOB NOT NULL,
    #             User_level BLOB NOT NULL,
    #             Skills BLOB NOT NULL,
    #             Recommended_Skills BLOB NOT NULL,
    #             Recommended_courses BLOB NOT NULL,
    #             pdf_name varchar(50) NOT NULL,
    #             PRIMARY KEY(ID)
    #             );
    #          """
    # cursor.execute(table_sql)


    if choice == 'User':
        st.markdown('<h5 style="text-align:center;color:#fd3456;">Upload Your Resume, and get smart analysis</h5>',unsafe_allow_html=True)

        pdf_file = st.file_uploader("Upload Your Resume",type=['pdf'])

        if pdf_file is not None:
            with st.spinner('Uploading your resume...'):
                time.sleep(2)
            save_pdf_path = './Uploaded_Resumes' + pdf_file.name
            with open(save_pdf_path,'wb') as f:
                f.write(pdf_file.getbuffer()) 
            
            resume_data = ResumeParser(save_pdf_path).get_extracted_data()
            if resume_data:
                resume_text = pdf_reader(save_pdf_path)
                
                
                st.success('Hello ' + resume_data['name'])
                
                

                cand_level= ''
                if resume_data['no_of_pages'] < 1:
                    cand_level = 'NA'
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">You are at fresher level</h4>''',unsafe_allow_html=True)
                elif ('INTERNSHIP' or  'INTERNSHIP'.lower()) in resume_text:
                    cand_level = 'Intermediate'
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">You are at intermediate level</h4>''',unsafe_allow_html=True)
                elif ("INTERNSHIPS" or 'INTERNSHIPS'.lower()) in resume_text:
                    cand_level = 'Intermediate'
                    
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">From the analysis we can see that you worked as an intern before</h4>''',unsafe_allow_html=True)
                elif ('EXPERIENCE' or 'EXPERIENCE'.lower()) in resume_text:
                    cand_level='Experienced'
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">From the analysis we can see that you are expereinced</h4>''',unsafe_allow_html=True)
                elif ('WORK EXPERIENCE' or 'WORK EXPERIENCES'.lower()) in resume_text:
                    cand_level='Experienced'
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">From the analysis we can see that you are expereinced</h4>''',unsafe_allow_html=True)
                else:
                    cand_level="Fresher"
                    st.markdown('''<h4 style="text-align:center; color:#45ff23;">From the analysis we can see that you are a fresher</h4>''',unsafe_allow_html=True)

                
                st.subheader("Skills Recommended 📑")

                keywords = st_tags(label='Your Current Skills',value=resume_data['skills'],key='1 ')
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit','ai']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress','javascript', 'angular js', 'C#', 'Asp.net', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','wireframe','user research','user experience']
                n_any = ['english','communication','writing', 'microsoft office', 'leadership','customer management', 'social media']

                recommended_skills =[]
                reco_field = ''
                rec_course = " "

                for i in resume_data['skills']:
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        
                        recommended_skills = ['Data Visualization','predictive Analysis','Statistical Modeling',"Web Scraping",'Keras',"Tensorflow",'Pytorch',"ML Algorithms"]
                        recommended_keywords = st_tags(label='Recommended skills for you.',
                                                       value=recommended_skills,key='2')
                        st.markdown('''<h5 style="text-align:center;color:#ff23ea;">Add these skills to your resume to boost🚀 your chances of getting a job </h5>''',unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break
                    
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        value=recommended_skills,key = '3')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        
                        rec_course = course_recommender(web_course)
                        break

                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        value=recommended_skills,key = '4')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(android_course)
                        break
                    
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        value=recommended_skills,key = '5')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(ios_course)
                        break
                    
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        
                        recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        value=recommended_skills,key = '6')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(design_course)
                        break
                        
                    elif i.lower() in n_any:
                        print(i.lower())
                        reco_field = 'NA'
                        st.warning("** Currently our tool only predicts and recommends for Data Science, Web, Android, IOS and UI/UX Development**")
                        recommended_skills = ['No Recommendations']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Currently No Recommendations',value=recommended_skills,key = '6')
                        st.markdown('''<h5 style='text-align: left; color: #092851;'>Maybe Available in Future Updates</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = "Sorry! Not Available for this Field"
                        break

run()
