import streamlit as st

st.set_page_config(page_title="About Page")

st.markdown("About")

link = '[Made with ❤️ by Karthik](https://github.com/sijju)'
st.sidebar.markdown(link, unsafe_allow_html=True)