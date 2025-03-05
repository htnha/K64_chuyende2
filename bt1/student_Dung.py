from Student import Student
import socket
import json
class Dung(Student):
    def name(self):
        return "Dung"
    def speak(self):
        return "Toi len la: Dung \nEmail: sevensoderfive@gmail.com"
    def address(self):
        return "DH city"
    def telegram_id(self):
        return "6133213893"
    def ip(self):
        return "20.0.0.109"
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
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip(), 99))  # Đổi sang cổng 99
            print("Kết nối đến server thời tiết thành công.")

            request = f"WEATHER {city}\n"
            client_socket.sendall(request.encode('utf-8'))

            response = client_socket.recv(4096).decode('utf-8')
            try:
                weather_data = json.loads(response)
                if "error" in weather_data:
                    print(f"Lỗi từ server: {weather_data['error']}")
                    return weather_data['error']
                else:
                    print(f"Thời tiết tại {city}: {weather_data['weather']}")
                    print(f"Nhiệt độ: {weather_data['temperature']}°C")
                    print(f"Độ ẩm: {weather_data['humidity']}%")
                    print(f"Gió: {weather_data['wind_speed']} m/s")
                return(f"Thời tiết tại {city}: {weather_data['weather']}\n"
                    f"Nhiệt độ: {weather_data['temperature']}°C"
                    f"Độ ẩm: {weather_data['humidity']}%\n"
                    f"Gió: {weather_data['wind_speed']} m/s")
            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()
    # def weather(self, city):
    #     try:
    #         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         client_socket.connect((self.ip(), 99))

    #         request = f"WEATHER {city}\n"
    #         client_socket.sendall(request.encode('utf-8'))

    #         response = client_socket.recv(4096).decode('utf-8')
    #         weather_data = json.loads(response)

    #         client_socket.close()
    #         return weather_data  # Trả về dữ liệu thời tiết đầy đủ
    #     except (ConnectionRefusedError, json.JSONDecodeError, Exception) as e:
    #         return {"error": str(e)}



