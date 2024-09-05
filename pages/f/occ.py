import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io



def isco(df): 
      st.subheader("التخصص والمهنة والنشاط", divider='rainbow')

      df = df.iloc[1:, :]

      df = df.rename(columns={"B_04a : العمر بالسنوات الكاملة":"العمر","التخصص":"رمز التخصص", "التخصص.1":"التخصص",
                     "المهنه.1":"مسمى المهنه","المهنه":"رمز المهنه" , "النشاط الاقتصادى":"رمز النشاط","النشاط الاقتصادى.1":"النشاط الاقتصادي"})
      
      month = "شهر العينة"
      week = "أسبوع العينة"
      supervisor = 'المشرف'
      vice = "النائب"
      associate = "المساعد"
      inspector = "المفتش"
      researcher = "الباحث"
      sample_number = 'معرف العينة'
      sample_status = "حالة جمع البيانات"
      name = "الاسم الأول"
      gender = "وصف الجنس"
      age = "العمر"
      saudi_c = "سعودي / غير سعودي"
      nationality_no = 'B_05 : الجنسية'
      special_degree = "التخصص"
      special_degree_no = "رمز التخصص"
      isco_no = 'رمز المهنه'
      isco_name = 'مسمى المهنه'
      isic_no = "رمز النشاط"
      isic_name = "النشاط الاقتصادي"
    
      df[isco_no] = df[isco_no].fillna(0)
      df[isic_no] = df[isic_no].fillna(0)
      df[special_degree] = df[special_degree].fillna("blank")
      df[special_degree_no] = df[special_degree_no].fillna(9999)
      df[gender] = df[gender].fillna("blank")

    
      df = df.dropna(subset=week)
      df = df.dropna(subset=month)
      df = df.dropna(subset=supervisor)


     
      df[isco_no] = df[isco_no].astype(int)
      df[isic_no] = df[isic_no].astype(int)
      df[month] = df[month].astype(int)
      df[week] = df[week].astype(int)
      df[researcher] = df[researcher].astype(int)
      df[inspector] = df[inspector].astype(int)
      df[supervisor] = df[supervisor].astype(int)
      df[associate] = df[associate].astype(int)
      df[vice] = df[vice].astype(int)
      df[sample_number] = df[sample_number].astype(int)
      df[nationality_no] = df[nationality_no].astype(int)
      df[special_degree_no] = df[special_degree_no].astype(int)
      df[isco_no] = df[isco_no].astype(int)
      df[age] = df[age].astype(int)



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
            if st.checkbox("تفعيل فلتر المفتش"):
              df_inspector = df[inspector] == inspector_no
              df = df[df_inspector]

      col1,col2 , col3,col4, col5 = st.columns(5)

      st.empty()


    
      ## متغيرات اخرى في التخصص والمهنة والنشاط
      isco_other = df[df[isco_no] == 999999]
      isic_other = df[df[isic_no] == 999999]
      special_degree_other = df[df[special_degree_no] == 999999]
      nationality_no_unknown = df[df[nationality_no] == 999]
      gender_unknown = df[df[gender] == "blank"]




      family_list = []
      isco_list = []
      df_m = df
      
      for i in df_m[supervisor].unique():
        df_m_supervisor = df_m[df_m[supervisor] == i]
        for i in df_m_supervisor[vice].unique():
            df_m_vice = df_m_supervisor[df_m_supervisor[vice] == i]
            for i in df_m_vice[associate].unique():
              df_m_associate = df_m_vice[df_m_vice[associate] == i]


              for i in sorted(df_m_associate[inspector].unique()):
                df_m_inspector = df_m_associate[df_m_associate[inspector] == i]
                for i in sorted(df_m_inspector[researcher].unique()):
                  df_m_researcher = df_m_inspector[df_m_inspector[researcher] == i]
            #إجمالي الأسر
                  family_count = len(df_m_researcher[sample_number].unique())
                  family_count2 = len(df_m_researcher[sample_number])
            #الأسر السعودية
                  saudi = df_m_researcher[df_m_researcher[nationality_no] == 682]
                  f_saudi = len(saudi[sample_number].unique())
                  f_saudi_m = len(saudi[sample_number])
                #المشتغلين السعوديين
                  saudi_work1 = saudi[saudi[isco_no] > 0 ]
                  saudi_work2 = saudi_work1[saudi_work1[age] >= 15] 
                  saudi_work = len(saudi_work2)
                  len_temp = []
                  for i in saudi[sample_number].unique():
                    df_temp = saudi[saudi[sample_number] == i]
                    if df_temp[isco_no].sum() == 0:
                      len_temp.append({
                        "sample_id": df_temp[sample_number]
                      })
                  saudi_non_work_len = len(len_temp)
                  family_list.append(
                    {
                    "نسبة الأسر لا يوجد مشتغل": 0 if f_saudi == 0 else round(saudi_non_work_len / f_saudi * 100,2),
                     "أسرة سعودية لا يوجد مشتغل" : saudi_non_work_len,
                     "المشتغلين (سعوديين)": saudi_work,
                     "متوسط عدد أفراد الأسرة السعودية": 0 if f_saudi == 0 else round(f_saudi_m / f_saudi, 2),
                     "عدد الأفراد السعوديين" : f_saudi_m,
                     "عدد الأسر السعودية" : f_saudi,
                     "الباحث":int(df_m_researcher[researcher].unique()),
                     "المفتش":int(df_m_researcher[inspector].unique()),
                     "المشرف":int(df_m_researcher[supervisor].unique()),
                     
                     }
                  )
            
        for i in df[isco_no].unique():
              if i > 0:
                df_isco = df[df[isco_no] == i]
                for i in df_isco[saudi_c].unique():
                  df_isco_s = df_isco[df_isco[saudi_c] == i]
                  
              
                  isco_list.append({
                "العدد": len(df_isco_s),
                "المهنة": df_isco_s[isco_name].unique()[0],
                #"الباحث": df_isco[researcher].unique(),
                "الجنسية" : df_isco_s[saudi_c].unique()[0]
                
              })
      data_isco = pd.DataFrame(isco_list)
      nw = pd.DataFrame(family_list)
  


      with st.expander("**الأسر السعودية : لا يوجد مشتغل**"):
          df_saudi = df[df[nationality_no] == 682]
          saudi_non_work = []
          

          for i in df_saudi[sample_number].unique():
              df_saudi_filter = df_saudi[df_saudi[sample_number] == i]
              
              if df_saudi_filter[isco_no].sum() == 0:
                age15 = df_saudi_filter[df_saudi_filter[age] >= 15]
                highdegree_hi = df_saudi_filter[df_saudi_filter[special_degree_no] > 9999]
                highdegree_hi = highdegree_hi[highdegree_hi[age] < 60]

                saudi_non_work.append({
                  
                    "الأسبوع":int(df_saudi_filter[week].unique()),
                    "الشهر":int(df_saudi_filter[month].unique()),
                    "عدد الافراد دبلوم وأعلى": len(highdegree_hi),
                    "الأفراد 15سنة فأكبر وأقل من 60سنة":len(age15),
                    "عدد الأفراد": len(df_saudi_filter),
                    "رقم العينة": int(df_saudi_filter[sample_number].unique()),
                    "الباحث": int(df_saudi_filter[researcher].unique()),
                    "المفتش": int(df_saudi_filter[inspector].unique()),
                    "المساعد": int(df_saudi_filter[associate].unique()),
                    "النائب": int(df_saudi_filter[vice].unique()),
                    "المشرف": int(df_saudi_filter[supervisor].unique()),
                    
                  
                })
                
          saudi_non_work = pd.DataFrame(saudi_non_work)



      nw= nw.iloc[:, ::-1]
      df_download = df[df[isco_no] > 0]
      df_download = df_download[[supervisor,vice,associate,inspector,researcher,name,saudi_c,gender,age,special_degree,isco_name,isic_name,month,week,sample_status,sample_number]]

      #df_download = df_download.iloc[:, ::-1]
 
      saudi_non_work = saudi_non_work.iloc[:, ::-1]
      data_isco= data_isco.iloc[:, ::-1]
      now = datetime.now()
      file = "التخصص والمهنة والنشاط {}.xlsx".format(now.strftime("%d/%m/%Y %H:%M:%S"))

      st.subheader("", divider='rainbow')
      
      buffer = io.BytesIO()
      with pd.ExcelWriter(buffer) as writer:
        df_download.to_excel(writer, sheet_name='التخصص-المهنة-النشاط', index=False)
        saudi_non_work.to_excel(writer, sheet_name='الأسر السعودية لا يوجد مشتغل',index=False)
        nw.to_excel(writer, sheet_name='بيانات الأسر السعودية',index=False)
        data_isco.to_excel(writer,sheet_name="المهن",index=False)


      st.download_button(
        label=":open_file_folder: xlsx تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )