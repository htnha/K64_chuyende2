import requests
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
        return "20.0.0.237"

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

    def weather(self):
        API_KEY = "83e847ddd998ae0b2d451f688f791fa9"  # Thay bằng API Key từ OpenWeatherMap
        CITY = "Dong Hoi, VN"
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=vi"

        try:
            response = requests.get(URL)
            data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                weather_description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                return f"🌤️ Thời tiết tại {CITY}:\n🌡️ Nhiệt độ: {temp}°C\n☁️ Trạng thái: {weather_description.capitalize()}\n💧 Độ ẩm: {humidity}%\n🌬️ Gió: {wind_speed} m/s"
            else:
                return f"Không thể lấy dữ liệu thời tiết. Lỗi: {data.get('message', 'Không rõ lỗi')}"
        except Exception as e:
            return f"Lỗi khi lấy dữ liệu thời tiết: {str(e)}"


# Test phương thức weather()
#student = Tham()
#print(student.weather())
