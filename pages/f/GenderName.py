import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io


def gender_name(df):
      st.header('الإسم و الجنس', divider='rainbow')
      
      
      df = df.rename(columns={"B_04a : العمر بالسنوات الكاملة":"العمر"})
      
      month = "شهر العينة"
      week = "رقم العينة الإسبوعية"
      supervisor = 'المشرف'
      vice = "النائب"
      associate = "المساعد"
      inspector = "المفتش"
      researcher = "الباحث"
      sample_number = 'معرف العينة'
      sample_status = "حالة العينة عند الباحث"
      name = "الاسم الأول"
      gender = "وصف الجنس"
      age = "العمر"
      add_status = 'إضافة الفرد'

      df[add_status] = df[add_status].fillna("يدويا")
      
      col1 , col2 , col3,col4, col5, col6 = st.columns(6)
      with col1:
        month_no = st.selectbox('الشهر', sorted(df[month].unique()))
        if len(df[month].unique()) > 1:
            st.caption(":white_check_mark:"+"فلتر الشهر مفعل")
            df_month = df[month] == month_no
            df = df[df_month]      

      with col2:
        week_no = st.selectbox('**الأسبوع**', sorted(df[week].unique()))
        if len(df[week].unique()) > 1:
            #st.caption("فلتر المفتش مفعل!")
            if st.checkbox("تفعيل فلتر الأسبوع"):
              df_week = df[week] == week_no
              df = df[df_week]

      with col3:
        supervisor_no = st.selectbox('المشرف', sorted(df[supervisor].unique()))
        if len(df[supervisor].unique()) > 1:
          st.caption( ":white_check_mark:"+ "فلتر المشرف مفعل")
          df_supervisor = df[supervisor] == supervisor_no
          df = df[df_supervisor]
      with col4:
        vice_no = st.selectbox('النائب', sorted(df[vice].unique()))
        if len(df[vice].unique()) > 1:
          st.caption(':white_check_mark:' + "فلتر النائب مفعل" )
          df_vice = df[vice] == vice_no
          df = df[df_vice]

      with col5:
        associate_no = st.selectbox('المساعد', sorted(df[associate].unique()))
        if len(df[associate].unique()) > 1:
          st.caption(":white_check_mark:" + "فلتر المساعد مفعل")
          df_associate = df[associate] == associate_no
          df = df[df_associate]

      with col6:
        
        inspector_no = st.selectbox('المفتش', sorted(df[inspector].unique()))
        if len(df[inspector].unique()) > 1:
            #st.caption("فلتر المفتش مفعل!")
            if st.checkbox("تفعيل فلتر المفتش"):
              df_inspector = df[inspector] == inspector_no
              df = df[df_inspector]
      st.subheader("", divider='rainbow')


      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")


      add_man = df[add_status] == 'يدويا'
      add_man = df[add_man]
      

      add_nic = df[add_status] == "بالربط مع مركز المعلومات الوطني"
      add_nic = df[add_nic]
      col1,col2, col3= st.columns(3)
      with col1:
        st.metric(label=":green[بالربط مع مركز المعلومات الوطني]", value=len(add_nic))
      with col2:
        st.metric(label=":red[**يــدوي**]", value=len(add_man))
      with col3:
        st.metric(label=':blue[المجموع]', value=len(add_man)+len(add_nic))

      buffer = io.BytesIO()
      now = datetime.now()
      file = "الإسم والجنس{}.xlsx".format(now.strftime("%d/%m/%Y %H:%M:"))
      with pd.ExcelWriter(buffer) as writer:
          df = df[[supervisor,vice,associate,inspector,researcher,name,gender,age,add_status,month,week,sample_status,sample_number]]
          df.to_excel(writer, sheet_name='الإسم-الجنس', index=False)
  

      st.download_button(
        label=":open_file_folder: xlsx -تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
    


      