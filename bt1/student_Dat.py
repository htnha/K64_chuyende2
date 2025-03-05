import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import socket
import json
from unidecode import unidecode  # Chuẩn hóa văn bản

# Cấu hình API Weatherstack
API_URL = "http://api.weatherstack.com/current"

# Load biến môi trường
load_dotenv()
API_KEY = os.getenv("WEATHERSTACK_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    print("⚠️ Lỗi: API key chưa được thiết lập! Vui lòng thêm WEATHERSTACK_API_KEY vào file .env")
    exit(1)

# Danh sách tỉnh thành
locations = {
    "Hà Nội": "Hanoi",
    "Hồ Chí Minh": "Ho Chi Minh City",
    "Đà Nẵng": "Da Nang",
    "Hải Phòng": "Haiphong",
    "Cần Thơ": "Can Tho"
}

# Chuẩn hóa tên tỉnh
def standardize_name(name):
    return unidecode(name).lower().strip()

# Map tìm kiếm tỉnh
defined_locations = {standardize_name(v): (v, e) for v, e in locations.items()}

def fetch_weather(city_name):
    params = {"access_key": API_KEY, "query": city_name, "units": "m"}
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
        return data if 'current' in data else {"error": "Không tìm thấy dữ liệu"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Lỗi kết nối API: {str(e)}"}

def fetch_stock_data(code):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(30)
        
        server_ip = "192.168.1.21"  # Địa chỉ IP server
        server_port = 99
        
        print(f"Đang kết nối đến server {server_ip}:{server_port}")
        client_socket.connect((server_ip, server_port))
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

def search_weather():
    while True:
        user_input = standardize_name(input("\nNhập tỉnh cần tra cứu (hoặc 'q' để thoát): "))
        if user_input == 'q':
            break
        
        matched_location = defined_locations.get(user_input)
        if matched_location:
            vn_name, en_name = matched_location
            data = fetch_weather(en_name)
            if 'current' in data:
                current = data['current']
                print(f"\n⛅ THỜI TIẾT {vn_name.upper()} (Cập nhật: {datetime.now().strftime('%H:%M %d/%m/%Y')})")
                print(f"🌡 Nhiệt độ: {current['temperature']}°C (Cảm giác: {current['feelslike']}°C)")
                print(f"💧 Độ ẩm: {current['humidity']}% | 🌬 Gió: {current['wind_speed']} km/h")
                print(f"🌤 {current['weather_descriptions'][0]}")
            else:
                print(f"⚠️ {data.get('error', 'Lỗi không xác định')}")
        else:
            print("❌ Không tìm thấy tỉnh này. Vui lòng thử lại.")

if __name__ == "__main__":
    search_weather()
