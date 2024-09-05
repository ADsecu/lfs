import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io
import hydralit_components as hc


def merge(df, df1):

    df = df.iloc[1:, :]


    df = df.rename(columns={"B_04a : العمر بالسنوات الكاملة": "العمر", "التخصص": "رمز التخصص", "التخصص.1": "التخصص",
                   "المهنه.1": "مسمى المهنه", "المهنه": "رمز المهنه", "النشاط الاقتصادى": "رمز النشاط", "النشاط الاقتصادى.1": "النشاط الاقتصادي"})

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



    # to delete last row \ error: ValueError: invalid literal for int() with base 10: 'لم يكتمل التصدير نتيجة حدوث خطأ JBO-27022: فشل تحميل قيمة في الفهرس 300 في وجود كائن جافا من النوع java.math.BigDecimal بسبب java.sql.SQLException..'
    tail = df.tail(1)
    if len(tail[month].unique()[0]) > 1:
        st.sidebar.caption("**fixed last row :** java.math.BigDecimal")
        df = df.iloc[:-1] 



    df[isco_no] = df[isco_no].fillna(0)
    df[isic_no] = df[isic_no].fillna(0)
    df[week] = df[week].fillna(99) # to fix week row with researcher no 99
    df[special_degree] = df[special_degree].fillna("blank")
    df[special_degree_no] = df[special_degree_no].fillna(0)
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
    df[age] = df[age].astype(int)

    df1 = df1.iloc[1:, :]
    df1 = df1.rename(columns={"B_04a : العمر بالسنوات الكاملة": "العمر", "C_09 :ما نوع المنتجات أو الخدمات التي تقدمها المنشأة التي (تعمل بها/يعمل بها الفرد) ؟": "النشاط الاقتصادي", "C_10 : في أي قطاع (تعمل/يعمل الفرد)؟": "القطاع",
                              "الحالة العملية.1": "الحالة العمليه", "جهة العمل.2": "إسم جهة العمل"})

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
    isic_name = 'النشاط الاقتصادي'
    sector = "القطاع"
    work_status_no = "الحالة العملية"
    work_status = "الحالة العمليه"
    work_no = 'جهة العمل'
    work_name = "إسم جهة العمل"

    # to delete last row \ error: ValueError: invalid literal for int() with base 10: 'لم يكتمل التصدير نتيجة حدوث خطأ JBO-27022: فشل تحميل قيمة في الفهرس 300 في وجود كائن جافا من النوع java.math.BigDecimal بسبب java.sql.SQLException..'
    tail1 = df1.tail(1)
    if len(tail1[month].unique()[0]) > 1:
        st.write(tail)
        df1 = df1.iloc[:-1] 





    df1[month] = df1[month].astype(int)
    df1[week] = df1[week].astype(int)
    df1[researcher] = df1[researcher].astype(int)
    df1[inspector] = df1[inspector].astype(int)
    df1[supervisor] = df1[supervisor].astype(int)
    df1[associate] = df1[associate].astype(int)
    df1[vice] = df1[vice].astype(int)
    df1[sample_number] = df1[sample_number].astype(int)
    df1[work_name] = df1[work_name].fillna('blank')

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        month_no = st.selectbox('الشهر', sorted(df[month].unique()))
        if len(df[month].unique()) > 1:
            st.caption(":white_check_mark:"+"فلتر الشهر مفعل")
            df_month = df[month] == month_no
            df = df[df_month]

    with col2:
        week_no = st.selectbox('**الأسبوع**', sorted(df[week].unique()))
        if len(df[week].unique()) > 1:
            # st.caption("فلتر المفتش مفعل!")
            if st.checkbox("تفعيل فلتر الأسبوع"):
                df_week = df[week] == week_no
                df = df[df_week]

    with col3:
        supervisor_no = st.selectbox('المشرف', sorted(df[supervisor].unique()))
        if len(df[supervisor].unique()) > 1:
            if st.checkbox("تفعيل فلتر المشرف"):
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

    new_data_list = []
    for i in df['FMId']:
        temp = df[df['FMId'] == i]
        temp1 = df1[df1['FMId'] == i]
        if len(temp) > 0 and len(temp1) > 0:

            new_data_list.append({
                "المشرف": temp[supervisor].unique()[0],
                'النائب': temp[vice].unique()[0],
                "المساعد": temp[associate].unique()[0],
                "المفتش": temp[inspector].unique()[0],
                "الباحث": temp[researcher].unique()[0],
                "الإسم الأول": temp[name].unique()[0],
                "الجنسية" : temp["وصف الجنسية"].unique()[0],
                "وصف الجنس": temp[gender].unique()[0],
                "العمر": temp[age].unique()[0],
                "التخصص": temp[special_degree].unique()[0],
                "رمز المهنة" : temp[isco_no].unique()[0],
                'المهنة': temp[isco_name].unique()[0],
                'إسم جهة العمل': temp1[work_name].unique()[0],
                "نوع القطاع": temp1[sector].unique()[0],
                "النشاط الإقتصادي": temp1[isic_name].unique()[0],
                "الحالة العملية": temp1[work_status].unique()[0],
                "الشهر": temp1[month].unique()[0],
                "الإسبوع": temp1[week].unique()[0],
                "حالة العينة": temp1[sample_status].unique()[0],
                "رقم العينة": temp1[sample_number].unique()[0],
                "FMid": i

            })

    new_data = pd.DataFrame(new_data_list)
    # new_data = new_data.iloc[:, ::-1]

    # متغيرات اخرى في التخصص والمهنة والنشاط
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
            # إجمالي الأسر
                        family_count = len(df_m_researcher[sample_number].unique())
                        family_count2 = len(df_m_researcher[sample_number])
            # الأسر السعودية
                        saudi = df_m_researcher[df_m_researcher[nationality_no] == 682]
                        
                        f_saudi = len(saudi[sample_number].unique())
                        f_saudi_m = len(saudi[sample_number])
                    # المشتغلين السعوديين
                        saudi_work1 = saudi[saudi[isco_no] > 0]
                        #saudi_work2 = saudi_work1[saudi_work1[age] >= 15]
                        saudi_work = len(saudi_work1)
                       
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
                                "نسبة الأسر لا يوجد مشتغل": 0 if f_saudi == 0 else round(saudi_non_work_len / f_saudi * 100, 2),
                                "أسرة سعودية لا يوجد مشتغل": saudi_non_work_len,
                                "المشتغلين (سعوديين)": saudi_work,
                                "متوسط عدد أفراد الأسرة السعودية": 0 if f_saudi == 0 else round(f_saudi_m / f_saudi, 2),
                                "عدد الأفراد السعوديين": f_saudi_m,
                                "عدد الأسر السعودية": f_saudi,
                                "الباحث": int(df_m_researcher[researcher].unique()),
                                "المفتش": int(df_m_researcher[inspector].unique()),
                                "المشرف": int(df_m_researcher[supervisor].unique()),

                            }
                        )

    nw = pd.DataFrame(family_list)


    df_saudi = df[df[nationality_no] == 682]
    saudi_non_work = []


    for i in df_saudi[sample_number].unique():
            df_saudi_filter = df_saudi[df_saudi[sample_number] == i]

    
            age15 = df_saudi_filter[df_saudi_filter[age] >= 15]
            worker = df_saudi_filter[df_saudi_filter[isco_no] > 0]
            highdegree_hi = df_saudi_filter[df_saudi_filter[special_degree_no] > 9999]

            age30_40 = df_saudi_filter[df_saudi_filter[age] >= 30]
            age30_40 = df_saudi_filter[df_saudi_filter[age] <= 40]
            age30_40 = age30_40[age30_40[special_degree_no] > 9999]
            age30_40 = age30_40[age30_40[isco_no] == 0]

            
            

            saudi_non_work.append({

                    "الأسبوع": int(df_saudi_filter[week].unique()),
                    "الشهر": int(df_saudi_filter[month].unique()),
                    "شهادة دبلوم وأعلى والعمر بين30و40 ولا يعمل" : len(age30_40),
                    "المشتغلين" : len(worker),
                    #"عدد الافراد دبلوم وأعلى": len(highdegree_hi),
                    "الأفراد 15سنة فأكبر": len(age15),
                    "إجمالي افراد الأسرة": len(df_saudi_filter),
                    "رقم العينة": int(df_saudi_filter[sample_number].unique()),
                    "الباحث": int(df_saudi_filter[researcher].unique()),
                    "المفتش": int(df_saudi_filter[inspector].unique()),
                    "المساعد": int(df_saudi_filter[associate].unique()),
                    "النائب": int(df_saudi_filter[vice].unique()),
                    "المشرف": int(df_saudi_filter[supervisor].unique()),


                })


    saudi_non_work = pd.DataFrame(saudi_non_work)


    s_blank1 = new_data[new_data['إسم جهة العمل'] != "blank"]
    s_blank1 = s_blank1[s_blank1['نوع القطاع'] == 'عمالة منزلية']

    s_blank2 = new_data[new_data['إسم جهة العمل'] == "blank"]
    s_blank2 = s_blank2[s_blank2['نوع القطاع'] != 'عمالة منزلية']


    def status(number):
        if number == 0:
            return 'good'
        else:
             return 'bad'

    cc = st.columns(3)
    with cc[0]:
        hc.info_card(title=len(s_blank1), content='عمالة منزلية ويوجد اسم جهة', sentiment=status(len(s_blank1)),bar_value=0)

    with cc[1]:
        hc.info_card(title=len(s_blank2), content='لايوجد اسم جهة ', sentiment=status(len(s_blank2)))

    now = datetime.now()
    nw = nw.iloc[:, ::-1]
    saudi_non_work= saudi_non_work.iloc[:, ::-1]
    file = "advanced_mergeB.xlsx".format(now.strftime("%d/%m/%Y %H:%M:"))

    st.subheader("", divider='rainbow')
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        new_data.to_excel(
            writer, sheet_name='اسم الجهة-القطاع-النشاط', index=False)
        nw.to_excel(writer, sheet_name='بيانات الأسر السعودية', index=False)
        saudi_non_work.to_excel(writer, sheet_name='تفصيل الأسر السعودية', index=False)

    st.download_button(
        label=":open_file_folder: xlsx -تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
