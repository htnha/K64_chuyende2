from Student import Student
from client_stock import send_request  # Nhập hàm send_request từ client_stock

class Long(Student):
    def name(self):
        return "Mai Vu Bao Long"
    def speak(self):
        return "Toi len la: Long.\nGmail: longbao112004@gmail.com"
    def address(self):
        return "Dong Hoi-Quang Binh"
    def telegram_id(self):
        return "7028049001"
    def ip(self):
        return "171.224.193.81"
    def stock(self, code):
        send_request(code)  # Gọi hàm send_request với mã chứng khoán 