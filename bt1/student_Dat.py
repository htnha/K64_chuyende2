from Student import Student
import socket  
import json 

class Dat(Student):
    def name(self):
        return "Dat"
    
    def speak(self):
        return "Toi ten la: Dat.\nGmail: phamnguyenbaodat946phamnguyenbaodat946@gmail.com"
    
    def address(self):
        return "DHDH"
    
    def telegram_id(self):
        return "6459433858"
    
    def ip(self):
        return "192.168.238.108"
    
    def stock(self, code):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))
            print("Kết nối đến server thành công.")

            request = f"STOCK {code}\n"
            client_socket.sendall(request.encode('ascii'))
            
            response = client_socket.recv(1024).decode('ascii')
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
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()
    
    def weather(self, city):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))
            print("Kết nối đến server thành công.")

            request = f"WEATHER {city}\n"
            client_socket.sendall(request.encode('ascii'))
            
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
