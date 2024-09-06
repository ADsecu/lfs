
from pages.f import f_search
from pages.f import sector
from pages.f import occ
from pages.f import LaborForce
from pages.f import GenderName
from pages.f import EconOthers_EconActiv
from pages.f.d import f_searchD


from datetime import datetime
import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
from streamlit_option_menu import option_menu
import io
import os
import time




st.set_page_config(layout="wide", page_title="القوى العاملة")
now = datetime.now()
sp = st.spinner("**جاري إنشاء التقارير ...**")



with st.sidebar:
    pages = option_menu("LFS", ['القوى العاملة', 'القوى العاملة المطور'],
                        menu_icon="bi bi-menu-button-fill", default_index=0,
                        styles={
        "icon": {"color": "#FFFFFF", "font-size": "25px"},
        "nav-link": {"font-size": "22px", "text-align": "left", "margin": "0px", "--hover-color": "#e9f5f9"},


    })


if pages == 'القوى العاملة':

    selected2 = option_menu("القائمة", ["البحث عن أسرة بالعينة", "السبب الرئيسي لعدم البحث عن عمل", "التخصص والمهنة والنشاط والقطاع"],
                            orientation="horizontal",
                            default_index=0)

    if selected2 == "البحث عن أسرة بالعينة":
        st.markdown("""
               <h1 style="text-align: center; font-family: Sakkal Majalla">البحث عن أسرة بالعينة</h1>
               """, unsafe_allow_html=True)

        with st.expander("", expanded=True):
            col1, col2 = st.columns(2)

            with col1:

                st.info('رقم هاتف مدلي البيانات (ناقص أو غير صحيح)', icon="ℹ️")
                st.info('تقرير مناطق العد ', icon="ℹ️")
                st.info('تقرير مفصل لحالات الإستجابة على مستوى الأسابيع', icon="ℹ️")
            with col2:
                uploaded_file_f_search = st.file_uploader(
                     "**رفع الملف.**", accept_multiple_files=False,)

        if uploaded_file_f_search is not None:
            
            
            with sp:
                df = pd.read_html(uploaded_file_f_search, header=0)
                df = df[0]
                if 'نتيجة الاستطلاع النهائية للهاتفي' in df.columns:
                    f_search.sf(df)
                else:
                    st.error("الملف المرفق غير صحيح , فضلاً التأكد من رفع الملف الصحيح او تواصل للدعم")
            

    elif selected2 == "السبب الرئيسي لعدم البحث عن عمل":
        st.markdown("""
               <h1 style="text-align: center; font-family: Sakkal Majalla">السبب الرئيسي لعدم البحث عن عمل</h1>
               """, unsafe_allow_html=True)
        with st.expander(" ", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
               
                st.info('أعداد المشتغلين والمتعطلين وخارج قوة العمل', icon="ℹ️")
                st.info('تفصيل المتعطلين وخارج قوة العمل حسب الفئة العمرية', icon="ℹ️")

            with col2:
                uploaded_file_LaborForce = st.file_uploader(
                    "**رفع الملف**", accept_multiple_files=False,)
        if uploaded_file_LaborForce is not None:
            with sp:
                df = pd.read_html(uploaded_file_LaborForce, header=0)
                df = df[0]
                if 'القوى العاملة' and "ما السبب الرئيسي لعدم البحث عن عمل خلال الأربعة أسابيع الماضية؟ عربي" in df.columns:
                    LaborForce.LFS(df)
                else:
                    st.error("الملف المرفق غير صحيح , فضلاً التأكد من رفع الملف الصحيح او تواصل للدعم")

    if selected2 == "التخصص والمهنة والنشاط والقطاع":
        st.markdown("""
               <h1 style="text-align: center; font-family: Sakkal Majalla">التخصص والمهنة والنشاط والقطاع</h1>
               """, unsafe_allow_html=True)

        with st.expander("_", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
        
                st.info('دمج (التخصص+المهنة+جهة العمل+القطاع+النشاط الإقتصادي)', icon="ℹ️")
                st.info('بيانات الأسر السعودية (متوسط عدد افراد الأسرة-أسرة سعودية لا يوجد مشتغل-المشتغلين السعوديين)', icon="ℹ️")

            with col2:
                uploaded_file_EconOthers_EconActiv = st.file_uploader(
                    "EconOthers - التخصص والمهنة", accept_multiple_files=False,)
                uploaded_file_EconOthers_EconActiv1 = st.file_uploader(
                    "EconActiv - جهة العمل والقطاع", accept_multiple_files=False,)
        if uploaded_file_EconOthers_EconActiv and uploaded_file_EconOthers_EconActiv1 is not None:
            with sp:
                df = pd.read_html(uploaded_file_EconOthers_EconActiv, header=0)
                df = df[0]
                df1 = pd.read_html(uploaded_file_EconOthers_EconActiv1, header=0)
                df1 = df1[0]
                EconOthers_EconActiv.merge(df, df1)
          



if pages == 'القوى العاملة المطور':

    uploaded_file = st.sidebar.file_uploader(
            " اختر ملف , الصيغة المدعومة ", accept_multiple_files=False, disabled=True)
    if uploaded_file is not None:
        with sp:

            df = pd.read_html(uploaded_file,header=0)
            df = df[0]
            time.sleep(2)
            f_searchD.sfd(df)
            
