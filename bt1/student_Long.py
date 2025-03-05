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
        return "171.224.199.63"  # Đảm bảo sử dụng IP của server đang chạy, ở đây là localhost cho máy chủ cục bộ.
    
    def stock(self, code):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))  # Kết nối đến server ở port 99
            print("Kết nối đến server thành công.")

            # Gửi yêu cầu chứng khoán cho server
            request = f"STOCK {code}\n"
            client_socket.sendall(request.encode('utf-8'))
            
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode('utf-8')
            try:
                response_data = json.loads(response)  # Giải mã JSON từ phản hồi
                if "error" in response_data:
                    print(f"Lỗi từ server: {response_data['error']}")
                else:
                    print(f"Mã chứng khoán: {response_data['stock_code']}")
                    print(f"Giá tham chiếu: {response_data['tc_price']}")
            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
                return(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()

    def weather(self, city):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))  # Kết nối đến server ở port 99

            # Gửi yêu cầu thời tiết cho server (bao gồm khoảng trắng nếu có)
            request = f"WEATHER {city}\n"
            client_socket.sendall(request.encode('utf-8'))
            
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode('utf-8')
            try:
                response_data = json.loads(response)  # Giải mã JSON từ phản hồi
                if "error" in response_data:
                    print(f"Lỗi từ server: {response_data['error']}")
                    return(f"Lỗi từ server: {response_data['error']}")
                else:
                    print(f"Thời tiết tại {response_data['city']}:\n"
                        f"Nhiệt độ: {response_data['temperature']}°C\n"
                        f"Cảm giác như: {response_data['feels_like']}°C\n"
                        f"Độ ẩm: {response_data['humidity']}%\n"
                        f"Mô tả: {response_data['description']}\n"
                        f"Tốc độ gió: {response_data['wind_speed']} m/s\n"
                        f"Lượng mưa (1 giờ): {response_data['rain']} mm")
                    return(f"Thời tiết tại {response_data['city']}:\n"
                        f"Nhiệt độ: {response_data['temperature']}°C\n"
                        f"Cảm giác như: {response_data['feels_like']}°C\n"
                        f"Độ ẩm: {response_data['humidity']}%\n"
                        f"Mô tả: {response_data['description']}\n"
                        f"Tốc độ gió: {response_data['wind_speed']} m/s\n"
                        f"Lượng mưa (1 giờ): {response_data['rain']} mm")

            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()

# # Tạo đối tượng Long và gọi hàm stock và weather
# student = Long()

# # # Gọi hàm stock với mã chứng khoán
# # stock_code = input("Nhập mã chứng khoán để kiểm tra: ")
# # student.stock(stock_code)  # Gọi hàm stock với mã chứng khoán

# # Gọi hàm weather với tên thành phố
# city = input("Nhập tên thành phố để lấy thông tin thời tiết: ")
# student.weather(city)  # Gọi hàm weather với tên thành phố
