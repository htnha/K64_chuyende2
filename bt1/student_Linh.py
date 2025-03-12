from Student import Student
import socket  
import json 
class Linh(Student):
    def name(self):
        return "Linh"
    def speak(self):
        return "Toi len la: linh.\nGmail: dinhcaolinh2004@gmail.com"
    def address(self):
        return "Dong Hoi-Quang Binh"
    def telegram_id(self):
        return "7730268153"
    def ip(self):
        return "127.0.0.1"
    

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

    def weather(self, city):
        try:
            # Tạo socket và kết nối đến server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))
            print("Kết nối đến server thành công.")

            # Gửi yêu cầu thời tiết
            request = f"WEATHER {city}\n"
            client_socket.sendall(request.encode('ascii'))
            
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode('ascii')
            try:
                response_data = json.loads(response)
                if "error" in response_data:
                    print(f"Lỗi từ server: {response_data['error']}")
                    return response_data['error']
                else:
                    weather_info = (
                        f"Thời tiết tại {response_data.get('city', city)}:\n"
                        f"- Nhiệt độ: {response_data.get('temperature', 'N/A')}°C\n"
                        f"- Độ ẩm: {response_data.get('humidity', 'N/A')}%\n"
                        f"- Trạng thái: {response_data.get('description', 'N/A')}"
                    )
                    return weather_info
            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
                return "Lỗi: Không thể xử lý dữ liệu từ server"
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
            return "Lỗi: Không thể kết nối đến server"
        except Exception as e:
            print(f"Lỗi: {e}")
            return f"Lỗi: {str(e)}"
        finally:
            client_socket.close()
