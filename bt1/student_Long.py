from Student import Student
import socket
import json

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
        return "171.233.21.220"
    def stock(self, code):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))
            print("Kết nối đến server thành công.")

            # Gửi yêu cầu, thêm ký tự kết thúc dòng để server dễ xử lý
            request = f"STOCK {code}\n"
            client_socket.sendall(request.encode('ascii'))
            
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode('ascii')
            try:
                response_data = json.loads(response)  # Giải mã JSON từ phản hồi
                if "error" in response_data:
                    print(f"Lỗi từ server: {response_data['error']}")
                    return response_data['error']
                else:
                    print(f"Mã chứng khoán: {response_data['stock_code']}")
                    print(f"Giá tham chiếu: {response_data['tc_price']}")
                    return response_data['tc_price']
            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()

# # Tạo đối tượng Long và gọi hàm stock
# student = Long()
# student.stock("FPT")  # Gọi hàm send_request với mã chứng khoán 