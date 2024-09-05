
import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import io
import hydralit_components as hc



now = datetime.now()


def sf(df):
    st.subheader("", divider='blue')
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
    occ_status_short = 'نتيجة الاستطلاع النهائية للهاتفي'
    block_error = "اخطاء المنع"
    EA_no = 'منطقة العد'
    lat = 'احداثية الجديدة Y'
    long = 'احداثية الجديدة X'
    m_name = 'اسم المسمى'
    hara_name = 'اسم الحي'



    # to delete last row \ error: ValueError: invalid literal for int() with base 10: 'لم يكتمل التصدير نتيجة حدوث خطأ JBO-27022: فشل تحميل قيمة في الفهرس 300 في وجود كائن جافا من النوع java.math.BigDecimal بسبب java.sql.SQLException..'
    tail = df.tail(1)
    if len(tail[month].unique()[0]) > 1:
        st.sidebar.caption("**fixed last row :** java.math.BigDecimal")
        df = df.iloc[:-1] 


    df[week] = df[week].fillna(99) # to fix week columns
    df[occ_code] = df[occ_code].fillna(0)
    
    df[month] = df[month].astype(int)
    df[week] = df[week].astype(int)
    df[researcher] = df[researcher].astype(int)
    df[inspector] = df[inspector].astype(int)
    df[supervisor] = df[supervisor].astype(int)
    df[associate] = df[associate].astype(int)
    df[vice] = df[vice].astype(int)
    df[sample_number] = df[sample_number].astype(int)
    df[block_error] = df[block_error].astype(int)

    df[occ_code] = df[occ_code].astype(int)


    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        month_no = st.selectbox('**الشهر**', sorted(df[month].unique()))
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
        supervisor_no = st.selectbox(
            '**المشرف**', sorted(df[supervisor].unique()))
        if len(df[supervisor].unique()) > 1:
            if st.checkbox("تفعيل فلتر المشرف"):
                df_supervisor = df[supervisor] == supervisor_no
                df = df[df_supervisor]
    with col4:
        vice_no = st.selectbox('**النائب**', sorted(df[vice].unique()))
        if len(df[vice].unique()) > 1:
            if st.checkbox("تفعيل فلتر النائب"):
                df_vice = df[vice] == vice_no
                df = df[df_vice]

    with col5:
        associate_no = st.selectbox(
            '**المساعد**', sorted(df[associate].unique()))
        if len(df[associate].unique()) > 1:
            if st.checkbox("تفعيل فلتر المساعد"):
                df_associate = df[associate] == associate_no
                df = df[df_associate]

    with col6:
        inspector_no = st.selectbox(
            '**المفتش**', sorted(df[inspector].unique()))
        if len(df[inspector].unique()) > 1:
            if st.checkbox("تفعيل فلتر المفتش"):
                df_inspector = df[inspector] == inspector_no
                df = df[df_inspector]

    st.subheader("", divider='rainbow')

    new_sample = df[df[sample_status] == 'جديد']
    uncomplate_sample = df[df[sample_status] == "غير مكتمل"]
    complate_sample = df[df[sample_status] == 'مكتمل']

    occ_code_1 = df[df[occ_code] == 1]
    occ_code_1[PhoneNumber] = occ_code_1[PhoneNumber].astype(int)

    invalid_phone = []
    for i in occ_code_1[PhoneNumber]:
        if i > 599999999 or i <= 500000000:

            df_invalid_no = occ_code_1[occ_code_1[PhoneNumber] == i]

            invalid_phone.append({
                "رقم العينة": int(df_invalid_no[sample_number].unique()),
                "منطقة العد": int(df_invalid_no[EA_no].unique()),
                "الشهر": int(df_invalid_no[month].unique()),
                "الأسبوع": int(df_invalid_no[week].unique()),
                "جوال المدلي": int(df_invalid_no[PhoneNumber].unique()),
                "الباحث": int(df_invalid_no[researcher].unique()),
                "المفتش": int(df_invalid_no[inspector].unique()),
                "المساعد": int(df_invalid_no[associate].unique()),
                "النائب": int(df_invalid_no[vice].unique()),
                "المشرف": int(df_invalid_no[supervisor].unique()),

            })
    invalid_phone_data = pd.DataFrame(invalid_phone)

    number_list = []
    for i in occ_code_1[PhoneNumber].unique():
        check_num = occ_code_1[occ_code_1[PhoneNumber] == i]

        if len(check_num) > 1:
            for i in check_num[sample_number]:
                check_num_samp = check_num[check_num[sample_number] == i]
                if check_num_samp[sample_number].unique() not in number_list:
                    number_list.append({
                        "رقم العينة": int(check_num_samp[sample_number].unique()),
                        #"منطقة العد": int(check_num_samp[EA_no].unique()),
                        "الشهر": int(check_num_samp[month].unique()),
                        "الاسبوع": int(check_num_samp[week].unique()),
                        "جوال المدلي": int(check_num_samp[PhoneNumber].unique()),
                        "الباحث": int(check_num_samp[researcher].unique()),
                        "المفتش": int(check_num_samp[inspector].unique()),
                        "المساعد": int(check_num_samp[associate].unique()),
                        "النائب": int(check_num_samp[vice].unique()),
                        "المشرف": int(check_num_samp[supervisor].unique()),

                    })
    number_list_data = pd.DataFrame(number_list)
    



    df_block_error = df[df[block_error] > 0]
    block_error_list = []
    if len(df_block_error) > 0:
        for i in df_block_error[sample_number]:
            df_block_error_temp = df_block_error[df_block_error[sample_number] == i]
            block_error_list.append({
                "رقم العينة": int(df_block_error_temp[sample_number].unique()),
                "الشهر": int(df_block_error_temp[month].unique()),
                "الأسبوع": int(df_block_error_temp[week].unique()),
                "خطأ المنع" : int(df_block_error_temp[block_error].unique()),
                "الباحث": int(df_block_error_temp[researcher].unique()),
                "المفتش": int(df_block_error_temp[inspector].unique()),
                "المساعد": int(df_block_error_temp[associate].unique()),
                "النائب": int(df_block_error_temp[vice].unique()),
                "المشرف": int(df_block_error_temp[supervisor].unique()),

            })

    df_block_error_data = pd.DataFrame(block_error_list)

    out_list = []
    out_list_2 = []
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
                    df_inspector_out[occ_status] = df_inspector_out[occ_status].fillna(
                        "جديد")

                    for i in sorted(df_inspector_out[researcher].unique()):
                        df_researcher_out = df_inspector_out[df_inspector_out[researcher] == i]

                        for i in df_researcher_out[week].unique():
                            df_out_week = df_researcher_out[df_researcher_out[week] == i]

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

                            for i in df_out_week[occ_status].unique():
                                df_out_2 = df_out_week[df_out_week[occ_status] == i]

                                out_list_2.append({
                                    "المشرف": df_out_2[supervisor].unique()[0],
                                    "النائب": df_out_2[vice].unique()[0],
                                    "المساعد": df_out_2[associate].unique()[0],
                                    "المفتش": df_out_2[inspector].unique()[0],
                                    "الباحث": df_out_2[researcher].unique()[0],
                                    "إسم الباحث": df_out_2[researcher_name].unique()[0],
                                    "حالة الإشغال": df_out_2[occ_status].unique()[0],
                                    "عدد الأسر": len(df_out_2),
                                    "الأسبوع": sorted(df_out_2[week].unique())[0],
                                    "الشهر": df_out_2[month].unique()[0]
                                })

    data_out = pd.DataFrame(out_list)
    data_out_2 = pd.DataFrame(out_list_2)

    pv_data = pd.pivot_table(data_out, values='عدد الأسر',
                             index=["المشرف", "النائب", "المساعد", 'المفتش',
                                    'الباحث', 'إسم الباحث', 'الشهر', 'الأسبوع'],
                             columns=['حالة الإستجابة'],
                             aggfunc=['sum'],
                             fill_value=0)
    pv_data_2 = pd.pivot_table(data_out_2, values='عدد الأسر',
                               index=["المشرف", "النائب", "المساعد", 'المفتش',
                                      'الباحث', 'إسم الباحث', 'الشهر', 'الأسبوع'],
                               columns=['حالة الإشغال'],
                               aggfunc=['sum'],
                               fill_value=0)

    list_1 = []
    for i in df[EA_no].unique():
        empty_EA = df[df[EA_no] == i]

        fulfilled = empty_EA[empty_EA[occ_code] == 1]
        out_of_scoop = empty_EA[empty_EA[occ_code] == 2]
        new = empty_EA[empty_EA[occ_code] == 0]

        total = len(fulfilled) + len(out_of_scoop) + len(new)
        list_1.append({

            "نسبة أستوفيت كلياً بمنطقة العد % ": round((len(fulfilled) / total) * 100, 2),

            "العينات جديدة": len(new),
            "خارج نطاق المسح و أخرى ": len(out_of_scoop),
            "أستوفيت كلياً": len(fulfilled),
            "إجمالي الأسر": total,
            "منطقة العد": int(empty_EA[EA_no].unique()),
            "المشرف": int(empty_EA[supervisor].unique())


        })

    ea_data = pd.DataFrame(list_1)
    ea_data = ea_data.iloc[:, ::-1]

    def status(number):
        if number == 0:
            return 'good'
        else:
             return 'bad'
    theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
    theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
    theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}

    cc = st.columns(3)
    with cc[0]:
        hc.info_card(title=len(number_list_data), content='رقم جوال مكرر', sentiment=status(len(number_list_data)),bar_value=0)

    with cc[1]:
        hc.info_card(title=len(invalid_phone_data), content='رقم الجوال غير صحيح', sentiment=status(len(invalid_phone_data)))

    with cc[2]:
        hc.info_card(title=len(df_block_error_data), content='أخطاء المنع', sentiment=status(len(df_block_error_data)))



    detail = st.checkbox("إضافة تقارير PivotTable", value=True)
    buffer = io.BytesIO()
    file = "Report- Family {}.xlsx".format(now.strftime("%d-%m-%Y"))
    with pd.ExcelWriter(buffer) as writer:
        if len(number_list_data) > 0:
            number_list_data = number_list_data.iloc[:, ::-1]
            number_list_data.to_excel(
                writer, sheet_name='رقم الهاتف مكرر', index=False)
        if len(invalid_phone_data) > 0:
            invalid_phone_data = invalid_phone_data.iloc[:, ::-1]
            invalid_phone_data.to_excel(
                writer, sheet_name='رقم الهاتف غير صحيح', index=False)
        if len(df_block_error) > 0:
            df_block_error_data.to_excel(
                writer, sheet_name='أخطاء المنع', index=False)
        ea_data.to_excel(
            writer, sheet_name='تقرير مناطق العد', index=False)
        data_out.to_excel(
            writer, sheet_name="نسبة الإستجابة-  مفصل", index=False)
        data_out_2.to_excel(
            writer, sheet_name="حالات الإشغال", index=False)
        if detail == True:
            pv_data.to_excel(
                writer, sheet_name="حالات الإستجابة-PivotTable")
            pv_data_2.to_excel(
                writer, sheet_name="حالات الإشغال -PivotTable")

    btn = st.download_button(
        label=":open_file_folder: xlsx -تحميل",
        data=buffer,
        file_name=file,
        mime="application/vnd.ms-excel"
    )
    if btn:
        # pd.ExcelWriter(buffer).close()
        st.success("تم التحميل ")
