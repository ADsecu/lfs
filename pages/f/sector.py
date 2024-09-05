
import streamlit as st
import pandas as pd
import openpyxl
from streamlit_extras.stoggle import stoggle
from datetime import datetime
from streamlit_option_menu import option_menu
import io



def isic(df):
      st.subheader("جهة العمل والقطاع", divider='rainbow')
      
      df = df.iloc[1:, :]
  
      df = df.rename(columns={"B_04a : العمر بالسنوات الكاملة":"العمر","C_09 :ما نوع المنتجات أو الخدمات التي تقدمها المنشأة التي (تعمل بها/يعمل بها الفرد) ؟":"النشاط الاقتصادي", "C_10 : في أي قطاع (تعمل/يعمل الفرد)؟":"القطاع",
                              "الحالة العملية.1":"الحالة العمليه","جهة العمل.2":"إسم جهة العمل"})
      
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
      isic_name = 'النشاط الاقتصادي'
      sector = "القطاع"
      work_status_no = "الحالة العملية"
      work_status = "الحالة العمليه"
      work_no = 'جهة العمل'
      work_name = "إسم جهة العمل"

      df[month] = df[month].astype(int)
      df[week] = df[week].astype(int)
      df[researcher] = df[researcher].astype(int)
      df[inspector] = df[inspector].astype(int)
      df[supervisor] = df[supervisor].astype(int)
      df[associate] = df[associate].astype(int)
      df[vice] = df[vice].astype(int)
      df[sample_number] = df[sample_number].astype(int)
      df[work_name] = df[work_name].fillna('blank')





      

  
      col1 , col2 , col3,col4, col5,col6 = st.columns(6)
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
          if st.checkbox("تفعيل فلتر النائب"):
            df_vice = df[vice] == vice_no
            df = df[df_vice]

      with col5:
        associate_no = st.selectbox('المساعد', sorted(df[associate].unique()))
        if len(df[associate].unique()) > 1:
          if st.checkbox("تفعيل فلتر المساعد"):
            df_associate = df[associate] == associate_no
            df = df[df_associate]

      with col6:
        inspector_no = st.selectbox('المفتش', sorted(df[inspector].unique()))
        if len(df[inspector].unique()) > 1:
            if st.checkbox("تفعيل فلتر المفتش"):
              df_inspector = df[inspector] == inspector_no
              df = df[df_inspector]
      

      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")




      sector_pr = df[sector] == 'عمالة منزلية'
      df_private = df[sector_pr]
      sector_pr_no = df_private[work_no] == 1
      df_private = df_private[sector_pr_no]


      work_no_pr = df[work_no] == 2
      df_private2 = df[work_no_pr]
      sector_pr2 = df_private2[sector] != 'عمالة منزلية'
      df_private2 = df_private2[sector_pr2]


  

      "---"
      m_f = []
      for i in df[vice].unique():
        vice_temp = df[df[vice] == i]
        for i in vice_temp[associate].unique():
          associate_temp = vice_temp[vice_temp[associate] == i]
          for i in associate_temp[sector].unique():
            sector_temp = associate_temp[associate_temp[sector] == i]
            male = len(sector_temp[sector_temp[gender] == "ذكر"])
            female = len(sector_temp[sector_temp[gender] == "أنثى"])
            m_f.append({
              "الإجمالي" : male + female,
              "ذكر" : female,
              "أنثى" : male,
              "القطاع": sector_temp[sector].unique()[0],
              "المساعد" : sector_temp[associate].unique()[0],
              "النائب": sector_temp[vice].unique()[0],
              "المشرف": sector_temp[supervisor].unique()[0]
            })


      m_f_t = pd.DataFrame(m_f)
      m_f_t = m_f_t.iloc[:, ::-1]



          
      df_download = df
      df_download = df_download[[supervisor,vice,associate,inspector,researcher,name,gender,age,work_name,sector,isic_name,work_status,month,week,sample_status,sample_number]]


      now = datetime.now()
      file = "جهة العمل والقطاع {}.xlsx".format(now.strftime("%d/%m/%Y %H:%M:"))

      st.subheader("", divider='rainbow')
      buffer = io.BytesIO()
      with pd.ExcelWriter(buffer) as writer:
        df_download.to_excel(writer, sheet_name='اسم الجهة-القطاع-النشاط', index=False)
        m_f_t.to_excel(writer, sheet_name='المشتغلين حسب القطاع', index=False)

        if len(df_private) >0:
          df_private = df_private[[supervisor,vice,associate,inspector,researcher,name,gender,age,work_name,sector,isic_name,work_status,month,week,sample_status,sample_number]]
          df_private.to_excel(writer, sheet_name='إسم جهة عمل للعمالة المنزلية', index=False)
        if len(df_private2) >0: 
          df_private2 = df_private2[[supervisor,vice,associate,inspector,researcher,name,gender,age,work_name,sector,isic_name,work_status,month,week,sample_status,sample_number]]
          df_private2.to_excel(writer, sheet_name='القطاع لللعمالة المنزلية', index=False)



      st.download_button(
        label=":open_file_folder: xlsx -تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
    

