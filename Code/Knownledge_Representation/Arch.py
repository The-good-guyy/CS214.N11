import pandas as pd
import numpy as np
from operator import attrgetter
import streamlit as st

class seach_space:
    def __init__(self,price,price_lower,location,bedrooms,area,priority):
        self.price={'value': price,'pri':priority }
        self.price_lower={'value': price_lower,'pri':priority }
        self.location = {'value': location,'pri':priority  }
        self.bedrooms= {'value': bedrooms,'pri':priority }
        self.area={'value': area,'pri':priority }
    #def update(price,location,bedrooms,area):


class user(seach_space):
    def __init__(self,price,price_lower,location,bedrooms,area,priority):
        super().__init__(price,price_lower,location,bedrooms,area,priority)
        if not price:
            self.price['pri'] = 9999999999

        if not price_lower:
            self.price_lower['pri'] = 9999999999

        if not location:
            self.location['pri'] = 9999999999

        if not bedrooms:
            self.bedrooms['pri'] = 9999999999

        if not area:
            self.area['pri'] = 9999999999
        
        self.edges=[]
        self.extra_information={}
        #self.generate_edges()
    def generate_edges_2(self, Dict):
        if Dict['couple']:
            self.add_edges(['cặp đôi'])
            if Dict['married']:
                self.add_edges(['đã cưới hoặc đính hôn'])
        if Dict['Single']:
            self.add_edges(['độc thân'])
        if Dict['children']:
            self.add_edges(['có con'])
            self.extra_information['con'] = Dict['children_count']
            if Dict['young_children']:
                self.add_edges(['con cái còn nhỏ'])
        self.extra_information['thành viên'] = Dict['Family_member']
        salary = int(Dict['Salary'])
        if salary >= 15000000:
            self.add_edges(['thu nhập không cao'])
        if salary >= 30000000:
            self.add_edges(['thu nhập cao'])
        if Dict['Stable']:
            self.add_edges(['thu nhập ổn định'])
        birth_year = int(Dict['birth_year'])
        if birth_year >= 1997 and birth_year<= 2012:
            self.add_edges(['thế hệ Z'])
        if birth_year >= 1981 and birth_year<= 1996:
            self.add_edges(['thế hệ Y'])
        
        


    def generate_edges(self):
        print("Đối với câu hỏi có hoặc không - 1 tương đương với có, 0 tương đương với không")
        couple = int(input("Bạn là cặp đôi muốn mua nhà ? : "))
        if couple == 1:
            self.add_edges(['cặp đôi'])
            married = int(input("2 bạn đã đính hôn/cưới ? :"))
            if married ==1:
                self.add_edges(['đã cưới hoặc đính hôn'])
        else:
            self.add_edges(['độc thân'])

        children = int(input("Bạn có con cái không ?"))
        if children ==1:
            self.add_edges(['có con'])
            count= int(input("Bạn có bao nhiêu người con ? : "))
            self.extra_information['con'] = count
            count_individuals = int(input("Có bao nhiêu thành viên trong gia đình của bạn ? : "))
            self.extra_information['thành viên'] = count_individuals
            young = int(input("Con của bạn còn nhỏ không ? : "))
            if young ==1:
                self.add_edges(['con cái còn nhỏ'])
            

        
        salary = int(input("Lương hàng tháng của bạn là bao nhiêu ? : "))
        if salary >= 15000000:
            self.add_edges(['thu nhập không cao'])
        if salary >= 30000000:
            self.add_edges(['thu nhập cao'])

        salary_stable = int(input("Thu nhập của bạn có ổn định không ? :"))
        if salary_stable ==1:
            self.add_edges(['thu nhập ổn định'])

        birth_year = int(input("Bạn sinh năm bao nhiêu ? : "))
        if birth_year >= 1997 and birth_year<= 2012:
            self.add_edges(['thế hệ Z'])
        if birth_year >= 1981 and birth_year<= 1996:
            self.add_edges(['thế hệ Y'])

        
        #print("generated")
        return

    def add_edges(self,new_edeges):
        for edge in new_edeges:
            if edge not in self.edges:
                self.edges.append(edge)
    
    def print(self):
        print("price: ", self.price['value'],'- priority: ',self.price['pri'])
        print("price_lower: ", self.price_lower['value'],'- priority: ',self.price_lower['pri'])
        print("location: ", self.location['value'],'- priority: ',self.location['pri'])
        print("bedrooms: ", self.bedrooms['value'],'- priority: ',self.bedrooms['pri'])
        print("area: ", self.area['value'],'- priority: ',self.area['pri'])
        print("edges: ",self.edges)
    def print2(self):
        string=''
        string+="price: "+ str(self.price['value'])+'- priority: '+str(self.price['pri'])+'\n'
        string+="price_lower: "+ str(self.price_lower['value'])+'- priority: '+str(self.price_lower['pri'])+'\n'
        string+="location: "+ str(self.location['value'])+'- priority: '+str(self.location['pri'])+'\n'
        string+="bedrooms: "+ str(self.bedrooms['value'])+'- priority: '+str(self.bedrooms['pri'])+'\n'
        string+="area: "+ str(self.area['value'])+'- priority: '+str(self.area['pri'])+'\n'
        string+="edges: "+str(self.edges)+'\n'
        return string
    

    def update_search_space(self,seach_space,information):
        priority = seach_space.price['pri']

        display_string="Dựa vào nguồn tri thức: "+information+"\n"
        if seach_space.price['value'] != None:
            if priority > self.price['pri'] or  (priority == self.price['pri']  and seach_space.price['value'] >  self.price['value'] ):
                self.price['value'] = seach_space.price['value']
                self.price['pri'] = seach_space.price['pri']
                display_string = display_string + "-Phạm vi tìm kiếm cho trường giá đã thay đổi" + "\n"

        if seach_space.price_lower['value'] != None:
            if priority > self.price_lower['pri'] or  (priority == self.price_lower['pri']  and seach_space.price_lower['value'] <  self.price_lower['value'] ):
                self.price_lower['value'] = seach_space.price_lower['value']
                self.price_lower['pri'] = seach_space.price_lower['pri']
                display_string = display_string + "-Phạm vi tìm kiếm cho trường giá theo m2 đã thay đổi" + "\n"
                
        
        if seach_space.location['value'] != None:
            if priority > self.location['pri'] or  (priority == self.location['pri'] and len(seach_space.location['value']) >  len(self.location['value']) ):
                self.location['value'] = seach_space.location['value']
                self.location['pri'] = seach_space.location['pri']
                display_string = display_string + "-Phạm vi tìm kiếm cho khu vực đã thay đổi"+ "\n"

        
        if seach_space.bedrooms['value'] != None:
            if priority > self.bedrooms['pri'] or  (priority == self.bedrooms['pri'] and seach_space.bedrooms['value'] <  self.bedrooms['value'] ):
                self.bedrooms['value'] = seach_space.bedrooms['value']
                self.bedrooms['pri'] = seach_space.bedrooms['pri']
                display_string = display_string + "-Phạm vi tìm kiếm cho trường phòng ngủ đã thay đổi" + "\n"
        
        if seach_space.area['value'] != None:
            if priority > self.area['pri'] or  (priority == self.area['pri'] and seach_space.area['value'] <  self.area['value'] ):
                self.area['value'] = seach_space.area['value']
                self.area['pri'] = seach_space.area['pri']
                display_string = display_string + "-Phạm vi tìm kiếm cho trường diện tích đã thay đổi" + "\n"

        display_string = display_string +"---------------"
        #print(display_string)
        return display_string
        
        
class vertex():
    def __init__(self,information,edges_needed,new_edeges,seach_space):
        self.information= information
        self.edges_needed= edges_needed
        self.new_edeges= new_edeges
        self.affected_domain = seach_space
        self.priority= seach_space.price['pri']
        
    def Activate(self,user):
        for edege in self.edges_needed:
            if not edege in user.edges:
                return
        user.add_edges(self.new_edeges)
        log = user.update_search_space(self.affected_domain,self.information)
        return log
        #User.print()


@st.cache
def insert_knowlegde(User):
    List_vertex = []

    Filter = seach_space(None,None,None,None,None,1)
    List_vertex.append(vertex("So what is a family? A husband, a wife, and two children — maybe even a pet — served as the model for the traditional Canadian family for most of the 20th century - Chapter 14. Marriage and Family",['đã cưới hoặc đính hôn'],['gia đình'],Filter))

    Filter = seach_space(None,None,None,1, None,2)
    List_vertex.append(vertex("Single buyers can usually skate by with just one room, but it’s also important to consider the potential for roommates. While you might not need anything large, having an extra office space can be nice for those who have hobbies or work from home. A house with one to three bedrooms should be large enough - HOW MANY BEDROOMS DO YOU TRULY NEED?",['độc thân'],[],Filter))

    Filter = seach_space(None,None,None,2, None,2)
    List_vertex.append(vertex("Couples should also have some flexibility. While a single-bedroom home can be nice and cozy, it is also convenient to have a space where you can get some much-needed alone time. A two- to three-bedroom home is often suitable - HOW MANY BEDROOMS DO YOU TRULY NEED?",['cặp đôi'],[],Filter))

    Filter = seach_space(None,None,None,3, None,3)
    List_vertex.append(vertex("How many bedrooms do you need when you have a whole family to think of? It really depends on the size of your family. It is convenient to allow each child to have his or her own bedroom, or you can have them share rooms. A family of four should fit comfortably in a house with three to four bedrooms. Consider an additional room for every one to two children or if you plan on your family growing - HOW MANY BEDROOMS DO YOU TRULY NEED?",['cặp đôi', 'gia đình'],[],Filter))

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

    return List_vertex