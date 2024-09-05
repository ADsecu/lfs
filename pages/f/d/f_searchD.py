
import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io


now = datetime.now()


def sfd(df):
    st.header('البحث عن أسرة بالعينة', divider='rainbow')
    df = df.iloc[1:, :]

    df = df.rename(columns={
                   "تنبيهات واخطاء على الإستمارة": "اخطاء المنع", "Unnamed: 27": "أخطاء التنبيه"})

    month = "شهر العينة"
    week = "أسبوع العينة"
    supervisor = 'مشرف'
    vice = "نائب"
    associate = "مساعد"
    inspector = "مفتش"
    researcher = "باحث"
    researcher_name = 'إسم الباحث'
    sample_number = 'معرف العينة'
    sample_status = 'حالة الإستمارة'
    PhoneNumber = 'جوال المدلي'
    occ_code = 'رمز المعاينة'
    occ_status = "حالة الاشغال"
    occ_status_short = 'وصف حالة المعاينة'
    block_error = "اخطاء المنع"
    EA_no = 'منطقة العد'
    lat = 'احداثية الجديدة Y'
    long = 'احداثية الجديدة X'
    m_name = 'اسم المسمى'
    hara_name = 'اسم الحي'

    df[month] = df[month].astype(int)
    df[week] = df[week].astype(int)
    df[researcher] = df[researcher].astype(int)
    df[inspector] = df[inspector].astype(int)
    df[supervisor] = df[supervisor].astype(int)
    df[associate] = df[associate].astype(int)
    df[vice] = df[vice].astype(int)
    df[sample_number] = df[sample_number].astype(int)
    df[block_error] = df[block_error].astype(int)
    df[occ_code] = df[occ_code].fillna(0)
    df[occ_code] = df[occ_code].astype(int)

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

            if st.checkbox("تفعيل فلتر الأسبوع"):
                df = df[df[week] == week_no]

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

    st.subheader("", divider='rainbow')

    new_sample = df[df[sample_status] == 'جديد']
    uncomplate_sample = df[df[sample_status] == "غير مكتمل"]
    complate_sample = df[df[sample_status] == 'مكتمل']

    out_list = []
    re_per = []

    for i in sorted(df[supervisor].unique()):
        df_supervisor_out = df[df[supervisor] == i]
        for i in sorted(df_supervisor_out[vice].unique()):
            df_vice_out = df_supervisor_out[df_supervisor_out[vice] == i]
            for i in df_vice_out[associate].unique():
                df_associate_out = df_vice_out[df_vice_out[associate] == i]

                for i in sorted(df_associate_out[inspector].unique()):
                    df_inspector_out = df_associate_out[df_associate_out[inspector] == i]
                    df_inspector_out[occ_status_short] = df_inspector_out[occ_status_short].fillna(
                        "جديد")
                    df_inspector_out[researcher_name] = df_inspector_out[researcher_name].fillna(
                        "null")

                    for i in sorted(df_inspector_out[researcher].unique()):
                        df_researcher_out = df_inspector_out[df_inspector_out[researcher] == i]

                        for i in df_researcher_out[week].unique():
                            df_out_week = df_researcher_out[df_researcher_out[week] == i]

                            
                            new_sample = df_out_week[df_out_week[sample_status] == 'جديد']
                            uncomplate_sample = df_out_week[df_out_week[sample_status] == "غير مكتمل"]
                            complate_sample = df_out_week[df_out_week[sample_status] == 'مكتمل']
                            re_per.append({
                                "المشرف": df_out_week[supervisor].unique()[0],
                                "النائب": df_out_week[vice].unique()[0],
                                "المساعد": df_out_week[associate].unique()[0],
                                "المفتش": df_out_week[inspector].unique()[0],
                                "الباحث": df_out_week[researcher].unique()[0],
                                "إسم الباحث": df_out_week[researcher_name].unique()[0],
                                "إجمالي الأسر" : len(df_out_week),
                                "جديد" : len(new_sample),
                                "غير مكتمل" : len(uncomplate_sample),
                                "مكتمل" : len(complate_sample),
                                "النسبة" : "{}%".format(round((len(complate_sample) / len(df_out_week)) *100,2)),
                                "الأسبوع": df_out_week[week].unique()[0],
                                "الشهر": df_out_week[month].unique()[0]

                            })


                            for i in df_out_week[occ_status_short].unique():
                                df_out = df_out_week[df_out_week[occ_status_short] == i]
                                total_temp = len(df_out_week)

                                out_list.append({
                                    "المشرف": df_out[supervisor].unique()[0],
                                    "النائب": df_out[vice].unique()[0],
                                    "المساعد": df_out[associate].unique()[0],
                                    "المفتش": df_out[inspector].unique()[0],
                                    "الباحث": df_out[researcher].unique()[0],
                                    "إسم الباحث": df_out[researcher_name].unique()[0],
                                    "حالة الإستجابة": df_out[occ_status_short].unique()[0],
                                    "عدد الأسر": len(df_out),
                                    "إجمالي الأسر": total_temp,
                                    "النسبة من الإجمالي": round((len(df_out) / total_temp) * 100, 2),
                                    "الأسبوع": sorted(df_out[week].unique())[0],
                                    "الشهر": df_out[month].unique()[0]
                                })

    data_out = pd.DataFrame(out_list)
    perc_res = pd.DataFrame(re_per)


    pv_data = pd.pivot_table(data_out, values='عدد الأسر',
                             index=["المشرف", "النائب", "المساعد", 'المفتش',
                                    'الباحث', 'إسم الباحث', 'الشهر', 'الأسبوع'],
                             columns=['حالة الإستجابة'],
                             aggfunc=['sum'],
                             fill_value=0)

    detail = st.checkbox("إضافة تقارير PivotTable", value=True)
    buffer = io.BytesIO()
    file = "Report- Family المطور {}.xlsx".format(now.strftime("%d-%m-%Y"))
    with pd.ExcelWriter(buffer) as writer:
        
        perc_res.to_excel(
            writer, sheet_name="الإنتاجية", index=False)
        data_out.to_excel(
            writer, sheet_name="نسبة الإستجابة-  مفصل", index=False,)
        if detail == True:
            pv_data.to_excel(
                writer, sheet_name="حالات الإستجابة-PV")


    btn = st.download_button(
        label=":open_file_folder: xlsx -تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
    if btn:
        st.success("تم التحميل ")
