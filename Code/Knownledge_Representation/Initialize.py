import pandas as pd
import numpy as np
from operator import attrgetter

import streamlit as st
import Arch
import Utils

def suggest(User):
    print("---------  Xây dựng gợi ý  ---------")
    User.generate_edges()
    List_vertex = []

    Filter = seach_space(None,None,None,None,None,1)
    List_vertex.append(vertex("So what is a family? A husband, a wife, and two children — maybe even a pet — served as the model for the traditional Canadian family for most of the 20th century - Chapter 14. Marriage and Family",['đã cưới hoặc đính hôn'],['gia đình'],Filter))

    Filter = seach_space(None,None,None,1, None,2)
    List_vertex.append(vertex("Single buyers can usually skate by with just one room, but it’s also important to consider the potential for roommates. While you might not need anything large, having an extra office space can be nice for those who have hobbies or work from home. A house with one to three bedrooms should be large enough - HOW MANY BEDROOMS DO YOU TRULY NEED?",['độc thân'],[],Filter))

    Filter = seach_space(None,None,None,2, None,2)
    List_vertex.append(vertex("Couples should also have some flexibility. While a single-bedroom home can be nice and cozy, it is also convenient to have a space where you can get some much-needed alone time. A two- to three-bedroom home is often suitable - HOW MANY BEDROOMS DO YOU TRULY NEED?",['cặp đôi'],[],Filter))

    Filter = seach_space(None,None,None,3, None,3)
    List_vertex.append(vertex("How many bedrooms do you need when you have a whole family to think of? It really depends on the size of your family. It is convenient to allow each child to have his or her own bedroom, or you can have them share rooms. A family of four should fit comfortably in a house with three to four bedrooms. Consider an additional room for every one to two children or if you plan on your family growing - HOW MANY BEDROOMS DO YOU TRULY NEED?",['cặp đôi, gia đình'],[],Filter))

    Filter = seach_space(None,None,['1', '10', '11', '12', '2', '4', '5', '6', '7', '8', '9', 'Bình Chánh', 'Bình Thạnh', 'Bình Tân', 'Củ Chi', 'Gò Vấp', 'Hóc Môn', 'Nhà Bè', 'Phú Nhuận', 'Thủ Đức', 'Tân Bình', 'Tân Phú'],None, None,2)
    List_vertex.append(vertex("Gen Z đói việc chấp nhận đi làm xa nhà hơn 20km, làm thế nào để không muốn vứt bỏ tất cả sau một ngày dài kiệt quệ? ",['thế hệ Z'],[],Filter))

    Filter = seach_space(None,None,['Hóc Môn','Bình Chánh','Nhà Bè','Cần Giờ'],2, None,2)
    List_vertex.append(vertex("Bên cạnh đó, với tình trạng giá nhà đất ngày càng leo thang, thế hệ trẻ ngày nay không tìm kiếm những căn hộ có diện tích quá lớn. Họ thường tìm kiếm các căn vừa phải ở ngoại ô, với giá hợp lý nhưng cần được thiết kế thông minh, đủ công năng hiện đại với 2 phòng ngủ, một phòng khách, không gian bếp riêng biệt… - XU HƯỚNG MUA NHÀ CỦA GIỚI TRẺ HIỆN NAY",['thế hệ Y'],[],Filter))

    if User.price['value']:
        Filter = seach_space(User.price['value']*1.3,None,None,None, None,2)
        List_vertex.append(vertex("TS. Trịnh Thị Phan Lan, Đại học Kinh tế - ĐHQGHN – Vay thời gian càng ngắn thì lãi suất và gốc trả hàng tháng cũng sẽ cao, những gói vay này phù hợp người có thu nhập hàng tháng cao. Những người có thu nhập ổn định nhưng không cao thì nên chọn gói vay có thời gian dài 10-25 năm - Lương tháng 10 triệu có nên đi vay mua nhà?",['thu nhập không cao','thu nhập ổn định'],[],Filter))


        Filter = seach_space(User.price['value']*1.5,200000000,None,None, None,2)
        List_vertex.append(vertex("High income people would also prefer to buy high-cost house (McCarthy, 1976 Borsch-Supan et al., 2001; Ariffin, 2010) và vay thời gian càng ngắn thì lãi suất và gốc trả hàng tháng cũng sẽ cao, những gói vay này phù hợp người có thu nhập hàng tháng cao - Lương tháng 10 triệu có nên đi vay mua nhà?",['thu nhập cao'],[],Filter))


    if 'thành viên' in User.extra_information and 'con' in User.extra_information:
        Filter = seach_space(None,None,['1','3','4','5','6','8','10','11','Phú Nhuận','Bình Thạnh','Tân Phú','Tân Bình','Gò Vấp'],User.extra_information['thành viên'] + User.extra_information['con'], 111,4)
        List_vertex.append(vertex("Are you planning to add to your family, and if so will any of your children be sharing rooms? Younger kids can share very happily, but as they reach the teenage years they may want more space. The age gap between your kids, and whether they’re the same gender, will also come into the equation - HOW MANY BEDROOMS DO YOU TRULY NEED?",['gia đình','con cái còn nhỏ'],[],Filter))

    List_vertex.sort(key=attrgetter('priority'))

    for Obj in List_vertex:
        Obj.Activate(User)
    display_data = filter_table(User,df)
    print("---------  kết quả của gợi ý tìm kiếm ---------")
    display(display_data)
    if not display_data.empty:
        compare(display_data)
    else:
        print("--------- Không tìm thấy ---------")


def input_process(Input):
    if Input == 'None':
        return None
    return int(Input)



def compare(display_data):
    indx_list = display_data.index.values.tolist() 
    ask_comparision = int(input("Bạn có muốn so sánh không ? : "))
    if ask_comparision != 0 :
        comparision_continue = 1
        while comparision_continue == 1:
            id1= int(input("id của căn hộ 1: "))
            while id1 not in indx_list:
                print("id không có trong list, vui lòng nhập lại")
                id1= int(input("id của căn hộ 1: "))
            
            id2= int(input("id của căn hộ 2: "))
            while id2 not in indx_list:
                print("id không có trong list, vui lòng nhập lại")
                id2= int(input("id của căn hộ 2: "))

            print("---------  bảng so sánh   ---------")
            comparision(id1,id2,display_data)
            comparision_continue = int(input("Bạn có muốn tiếp tục so sánh không ? :"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    text4 = st.empty()
    Holder={}
    with text4.container():
        form = st.form("my_form")
        price = input_process(form.text_input("Giá tiền : ",value=None))
        
        price_lowerbound =input_process(form.text_input("Giá đất trên m2 ít nhất: ",value=None))
        location = form.text_input(r'Khu vực/ quận (lưu ý định dạng ", "): ',value=None)
        location=location.split(", ")
        if len(location) ==1 and location[0] == 'None':
            location = None

        bedrooms = input_process(form.text_input("Số phòng ngủ : ",value=None))

        area = input_process(form.text_input("Diện tích căn hộ : ",value=None))




        # Every form must have a submit button.
        submitted = form.form_submit_button("Submit")

        if submitted:
            Holder['price']=price
            Holder['price_lowerbound']=price_lowerbound
            Holder['location']=location
            Holder['bedrooms']=bedrooms
            Holder['area']=area

            text4.empty()
    if submitted:
        User = Arch.user( Holder['price'],Holder['price_lowerbound'],Holder['location'],Holder['bedrooms'],Holder['area'],0)
        df = pd.read_csv('cleaned.csv')
        df = df.dropna()
        #st.dataframe(df)

        display_data = Utils.filter_table(User,df)
        display_data_cleaned = display_data.drop(['Unnamed: 0'], axis=1)

        if not display_data.empty:
            st.dataframe(display_data_cleaned,use_container_width=1)





        

    
