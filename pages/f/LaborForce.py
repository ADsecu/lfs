import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io



def get_age_group(age):

    c_download = False
    if age <= 14:
        return 'اقل من 15سنة'
    elif age >= 15 and age < 20:
        return '15-19'
    elif age >= 20 and age < 30:
        return '20-29'
    elif age >= 30 and age < 40:
        return '30-39'
    elif age >= 40 and age < 50:
        return '40-49'
    elif age >= 50 and age < 60:
        return '50-59'
    else:
        return '65+'


def LFS(df):
    st.caption(":red[unstable version]")


    df = df.rename(columns={"ما أعلى مؤهل علمي (حصلت عليه/حصل عليه الفرد) بنجاح؟ عربي": "أعلى مؤهل حصل عليه الفرد",
                            "ما السبب الرئيسي لعدم البحث عن عمل خلال الأربعة أسابيع الماضية؟ عربي": "السبب الرئيسي لعدم البحث عن عمل"})

    month = "شهر العينة"
    week = "رقم العينة الاسبوعية"
    supervisor = 'المشرف'
    vice = "النائب"
    associate = "المساعد"
    inspector = "المفتش"
    researcher = "الباحث"
    count = "عدد الافراد"
    labor_force = "القوى العاملة"
    seq = "تسلسل"
    reason = "السبب الرئيسي لعدم البحث عن عمل"
    age = "العمر"
    highdegree = "أعلى مؤهل حصل عليه الفرد"
    age_bin = 'الفئة العمرية'


    df[seq] = df[seq].replace("x", 99)  # No degree
    df[seq] = df[seq].fillna(999)  # less than 15y old
    df[seq] = df[seq].astype(int)
    df = df.dropna(subset=labor_force)
    df[labor_force] = df[labor_force].astype(int)
    df[count] = df[count].astype(int)




    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        month_no = st.selectbox('الشهر', sorted(df[month].unique()))
        if len(df[month].unique()) > 1:
            st.caption(":white_check_mark:"+"فلتر الشهر مفعل")
            df_month = df[month] == month_no
            df = df[df_month]

    with col2:
        week_no = st.selectbox('الأسبوع', sorted(df[week].unique()))
        if len(df[week].unique()) > 1:
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




    
    df['الفئة العمرية'] = df[age].apply(get_age_group)
    df_2 = df[df[labor_force] == 2]
    pv_data_2 = pd.pivot_table(df_2, values=count,
                                index=[supervisor,age_bin,highdegree], 
                                #columns=['عدد الافراد'], 
                                aggfunc=['sum'],
                                fill_value=0)


    df_3 = df[df[labor_force] == 3]
    pv_data_3 = pd.pivot_table(df_3, values=count,
                                index=[supervisor,age_bin,reason], 
                                #columns=['عدد الافراد'], 
                                aggfunc=['sum'],
                                fill_value=0)

################# مستوى المفتش والباحث ###################


    pv_data_22 = pd.pivot_table(df[df[labor_force] == 2], values=count,
                                index=[supervisor,vice,associate,inspector,researcher,age_bin,highdegree], 
                                #columns=['عدد الافراد'], 
                                aggfunc=['sum'],
                                fill_value=0)



    pv_data_33 = pd.pivot_table(df[df[labor_force] == 3], values=count,
                                index=[supervisor,vice,associate,inspector,researcher,age_bin,reason], 
                                #columns=['عدد الافراد'], 
                                aggfunc=['sum'],
                                fill_value=0)



    lfs_list = []
    df_lfs = df
    for i in sorted(df_lfs[supervisor].unique()):
        df_lfs_supervisor = df_lfs[df_lfs[supervisor] == i]

        for i in sorted(df_lfs_supervisor[vice].unique()):
            df_lfs_vice = df_lfs_supervisor[df_lfs_supervisor[vice] == i]

            for i in sorted(df_lfs_vice[associate].unique()):
                df_lfs_associate = df_lfs_vice[df_lfs_vice[associate] == i]

                for i in sorted(df_lfs_associate[inspector].unique()):
                    df_lfs_inspector = df_lfs_associate[df_lfs_associate[inspector] == i]
        
                    for i in sorted(df_lfs_inspector[researcher].unique()):
                        df_lfs_researcher = df_lfs_inspector[df_lfs_inspector[researcher] == i]
                        lfs_1 = df_lfs_researcher[df_lfs_researcher[labor_force] == 1]
                        lfs_2 = df_lfs_researcher[df_lfs_researcher[labor_force] == 2]
                        lfs_3 = df_lfs_researcher[df_lfs_researcher[labor_force] == 3]
                        total = lfs_1[count].sum() + lfs_2[count].sum()
                        lfs_list.append(
                    {
                        "نسبة المتعطلين" : round(lfs_2[count].sum() / total *100,2),
                        "داخل قوة العمل": total ,
                        "خارج قوة العمل": lfs_3[count].sum(),
                        "المتعطلين": lfs_2[count].sum(),
                        "المشتغلين": lfs_1[count].sum(),
                        "الباحث": int(df_lfs_researcher[researcher].unique()),
                        "المفتش": int(df_lfs_researcher[inspector].unique()),
                        "المساعد": int(df_lfs_researcher[associate].unique()),
                        "النائب": int(df_lfs_researcher[vice].unique()),
                        "المشرف": int(df_lfs_researcher[supervisor].unique()),
                    }
                )
    lfs_data_count = pd.DataFrame(lfs_list)
    lfs_data_count = lfs_data_count.iloc[:, ::-1]


    st.subheader("", divider='rainbow')
    check = st.checkbox("مستوى الباحث", value=True)


    now = datetime.now()
    buffer = io.BytesIO()
    file = "report {}.xlsx".format(now.strftime("%d/%m/%Y %H:%M:%S"))
    with pd.ExcelWriter(buffer) as writer:

        lfs_data_count.to_excel(
            writer, sheet_name='القوى العاملة', index=False)
        pv_data_2.to_excel(
            writer, sheet_name='المتعطلين', )
        pv_data_3.to_excel(
            writer, sheet_name='خارج قوة العمل', )
        if check :
                pv_data_22.to_excel(
            writer, sheet_name='المتعطلين-مفصل', )
                pv_data_33.to_excel(
            writer, sheet_name='خارج قوة العمل- مفصل', )


    c_download = True
    if c_download == True:
        st.download_button(
        label=":open_file_folder: xlsx تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
