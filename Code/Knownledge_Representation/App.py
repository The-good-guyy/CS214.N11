import pandas as pd
import numpy as np
from operator import attrgetter
import streamlit as st
import Arch
import Utils
import Initialize as Ini

def filter_compare(User,display_data_cleaned,display_data):
    st.header('Thông tin đã lọc')
    display_data_frame = st.dataframe(display_data_cleaned,use_container_width=1)
    compare_form = st.form("compare_form")

    st.header('So sánh')
    indx1 = int(st.text_input('index 1','0'))
    indx2 = int(st.text_input('index 2','0'))

    indx_list = display_data_cleaned.index.values.tolist() 
    display_table = True

    
    if int(indx1) not in indx_list:
        st.warning('index 1 is not in the filtered data', icon="⚠️")
        display_table = True
    if int(indx2) not in indx_list:
        st.warning('index 2 is not in the filtered data', icon="⚠️")
        display_table = True
    if int(indx2) in indx_list and int(indx1) in indx_list:
        display_table =False


    display_table=st.button("display comparision",disabled =display_table)
    if display_table:
        comparision_res = Utils.comparision(indx1,indx2,display_data)
        st.dataframe(comparision_res,use_container_width=1)
if __name__ == "__main__":
    
    st.set_page_config(layout="wide")
    st.header('Thông tin cần lọc')

    form = st.form("my_form")

    Holder={}

    price = Ini.input_process(form.text_input("Giá tiền : ",value=None))
    
    price_lowerbound =Ini.input_process(form.text_input("Giá đất trên m2 ít nhất: ",value=None))
    location = form.text_input(r'Khu vực/ quận (lưu ý định dạng ", "): ',value=None)
    location=location.split(", ")
    if len(location) ==1 and location[0] == 'None':
        location = None

    bedrooms = Ini.input_process(form.text_input("Số phòng ngủ : ",value=None))

    area = Ini.input_process(form.text_input("Diện tích căn hộ : ",value=None))

    submitted = form.form_submit_button("Submit")

    if 'form_button_pressed' not in st.session_state:
        st.session_state['form_button_pressed'] = False

    if submitted:
        st.session_state['form_button_pressed'] = True

    if st.session_state['form_button_pressed']:
        Holder['price']=price
        Holder['price_lowerbound']=price_lowerbound
        Holder['location']=location
        Holder['bedrooms']=bedrooms
        Holder['area']=area



        User = Arch.user( Holder['price'],Holder['price_lowerbound'],Holder['location'],Holder['bedrooms'],Holder['area'],0)
        df = pd.read_csv('cleaned.csv')
        df = df.dropna()
        #st.dataframe(df)

        display_data = Utils.filter_table(User,df)
        display_data_cleaned = display_data.drop(['Unnamed: 0'], axis=1)

        if not display_data.empty:
            st.success('tìm kiếm được kết quả', icon="✅")
            filter_compare(User,display_data_cleaned,display_data)
        else:
            Holder_suggest={}
            couple=False
            married=False
            Single=False
            children=False
            children_count=None
            Family_member = None
            young_children = False
            Salary=None
            Stable=False
            birth_year=None

            st.error('Không tìm kiếm được kết quả', icon="🚨")
            st.header('Thông tin hỏi thêm')
            couple = st.checkbox('Bạn là cặp đôi muốn mua nhà ?') 
            if couple:
                married = st.checkbox('2 bạn đã đính hôn/cưới ?') 
            else:
                Single = True
            children = st.checkbox('Bạn có con cái không ?') 
            if children:
                children_count = st.number_input('Bạn có bao nhiêu người con ?',1)
                young_children = st.checkbox('Con của bạn còn nhỏ không ?')
            Family_member = st.number_input('Có bao nhiêu thành viên trong gia đình của bạn ?',2)

            Salary = st.number_input('Lương hàng tháng của bạn là bao nhiêu ?')
            Stable = st.checkbox('Thu nhập của bạn có ổn định không')
            birth_year = st.number_input('Bạn sinh năm bao nhiêu',1980)


            Holder_suggest['couple']=couple
            Holder_suggest['married']=married
            Holder_suggest['Single']=Single
            Holder_suggest['children']=children
            Holder_suggest['children_count']=children_count
            Holder_suggest['Family_member']=Family_member
            Holder_suggest['young_children']=young_children
            Holder_suggest['Salary']=Salary
            Holder_suggest['Stable']=Stable
            Holder_suggest['birth_year']=birth_year
            if Holder_suggest:
                #st.write(Holder_suggest)
                User.generate_edges_2(Holder_suggest)
                #st.write(User.print2())
                List_vertex = Arch.insert_knowlegde(User)

                st.header('Gợi ý')
                for Obj in List_vertex:
                    log = Obj.Activate(User)
                    if log:
                        st.text(log)
                    
                display_data = Utils.filter_table(User,df)
                display_data_cleaned = display_data.drop(['Unnamed: 0'], axis=1)
                filter_compare(User,display_data_cleaned,display_data)


                


                



                
            





