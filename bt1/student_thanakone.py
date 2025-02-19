from Student import Student
import socket
import json

class Thanakone(Student):
    def name(self):
        return "Thanakone"
    
    def speak(self):
        return "Toi Ten la: THANAKONE.\nGmail: thanakone7536@gmail.com"
    
    def address(self):
        return "Savannakhet - Laos"
    
    def telegram_id(self):
        return "6836821198"
    
    def ip(self):
        return "20.0.0.105"  # Đổi thành localhost vì server chạy trên máy local
    
    def stock(self, code):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))

            # Gửi yêu cầu
            request = f"STOCK {code}\n"
            client_socket.sendall(request.encode('utf-8'))
            
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)
            
            if "error" in response_data:
                return response_data['error']
            return response_data['current_price']
            
        except ConnectionRefusedError:
            return "Lỗi: Server chưa được khởi động"
        except Exception as e:
            return f"Lỗi: {str(e)}"
        finally:
            client_socket.close()

# Test thử
if __name__ == "__main__":
    student = Thanakone()
    print(student.stock("FPT"))
