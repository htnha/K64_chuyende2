from Student import Student
import socket
import json

class Linh(Student):
    def name(self):
        return "Dinh Cao Linh"
    def speak(self):
        return "Toi len la: Linh.\nGmail: dinhcaolinh2004@gmail.com"
    def address(self):
        return "Dong Hoi-Quang Binh"
    def telegram_id(self):
        return "7730268153"
    def ip(self):
        return "171.224.193.81"
    def stock(self, code):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)
            client_socket.connect((self.ip(), 99))
            print("Kết nối đến server thành công.")

            # Gửi yêu cầu
            request = f"STOCK {code}\n"
            client_socket.sendall(request.encode('utf-8'))
            
            # Nhận phản hồi từ server
            response = ""
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                response += data
                if '\n' in data:
                    break
            
            # Xử lý response
            if response:
                try:
                    response_data = json.loads(response)
                    if "error" in response_data:
                        print(f"Lỗi từ server: {response_data['error']}")
                        return response_data['error']
                    else:
                        print(f"Mã chứng khoán: {response_data['stock_code']}")
                        print(f"Giá tham chiếu: {response_data['tc_price']}")
                        return response_data['tc_price']
                except json.JSONDecodeError:
                    print(f"Phản hồi không hợp lệ từ server: {response}")
                    return None
            else:
                print("Không nhận được phản hồi từ server")
                return None
                
        except socket.timeout:
            print("Timeout: Server không phản hồi sau 10 giây")
            return None
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
            return None
        except Exception as e:
            print(f"Lỗi: {str(e)}")
            return None
        finally:
            if client_socket:
                client_socket.close()

# Test chương trình
if __name__ == "__main__":
    student = Linh()
    result = student.stock("FPT")
    print(f"Kết quả: {result}")