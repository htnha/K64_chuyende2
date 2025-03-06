import socket
import json
from Student import Student

class Tham(Student):
    def name(self):
        return "Tham"

    def speak(self):
        return "Toi len la: Tham \nEmail: nguyenvantham.vtabd@gmail.com"

    def address(self):
        return "Quang Trach - Quang Binh"

    def telegram_id(self):
        return "6751406624"

    def ip(self):
        return "127.0.0.1"

    def stock(self, code: str):
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
                    return {
                        "stock_code": response_data['stock_code'],
                        "tc_price": response_data['tc_price']
                    }

            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()
        return {"stock_code": code, "tc_price": ""}

    def weather(self, city: str):
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
                    print(f"🌤️ Thời tiết tại {response_data['city']}:")
                    print(f"🌡️ Nhiệt độ: {response_data['temperature']}°C")
                    print(f"☁️ Trạng thái: {response_data['weather'].capitalize()}")
                    print(f"💧 Độ ẩm: {response_data['humidity']}%")
                    print(f"🌬️ Gió: {response_data['wind_speed']}m/s")

                    return {
                        "city": response_data["city"],
                        "temperature": response_data["temperature"],
                        "humidity": response_data["humidity"],
                        "weather": response_data["weather"],
                        "wind_speed": response_data["wind_speed"]
                    }
            except json.JSONDecodeError:
                print(f"Phản hồi không hợp lệ từ server: {response}")
        except ConnectionRefusedError:
            print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            client_socket.close()
        return {"city": city, "temperature": "", "humidity": "", "weather": "", "wind_speed": ""}


#student = Tham()  # Tạo đối tượng Tham và gọi hàm stock, weather
#student.stock("FPT")  # Gọi hàm stock với mã chứng khoán
#print(student.weather("Dong Hoi, VN"))  # gọi hàm weather với tên thành phố
