import time
import json
from playwright.sync_api import sync_playwright
import socket
import requests

# Cấu hình API Key cho OpenWeatherMap
OPENWEATHER_API_KEY = "YOUR_API_KEY"  # Thay YOUR_API_KEY bằng API key của bạn


# Hàm cuộn trang xuống
def perform_scroll(page, selector, step=50, max_scroll=300):
    current_scroll = 0
    while current_scroll < max_scroll:
        page.eval_on_selector(selector, f"el => el.scrollTop = {current_scroll}")
        current_scroll += step
        time.sleep(0.5)


# Hàm lấy dữ liệu chứng khoán
def collect_stock_data():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)  # Đặt headless=True để chạy ngầm
            page = browser.new_page()

            page.goto("https://iboard.ssi.com.vn/", timeout=60000, wait_until="networkidle")
            time.sleep(10)

            perform_scroll(page, ".ag-body-viewport.ag-layout-normal.ag-row-animation.scroll-base")
            perform_scroll(page, ".ag-center-cols-clipper")
            time.sleep(3)

            stock_elements = page.query_selector_all(".ag-pinned-left-cols-container")
            stock_names = []
            if len(stock_elements) >= 2:
                stock_text = stock_elements[1].inner_text()
                stock_names = stock_text.split("\n")
            else:
                print("Không tìm thấy các phần tử phù hợp.")

            price_cells = page.query_selector_all(
                ".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-ref.ag-cell-bg-highlight.cursor-pointer.ag-cell-value")
            prices = [cell.inner_text() for cell in price_cells] if price_cells else []

            browser.close()

            stock_data = {}
            for index in range(min(len(stock_names), len(prices))):
                stock_data[stock_names[index]] = prices[index]
            print("Dữ liệu chứng khoán thu thập được:", stock_data)
            return stock_data
    except Exception as e:
        print(f"Lỗi khi thu thập dữ liệu chứng khoán: {e}")
        return {}


# Hàm lấy dữ liệu thời tiết từ OpenWeatherMap
def get_weather_data(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric&lang=vi"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code == 200:
            return {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "weather": weather_data["weather"][0]["description"],
                "wind_speed": weather_data["wind"]["speed"]
            }
        else:
            return {
                "error": f"Không thể lấy dữ liệu thời tiết cho {city_name}: {weather_data.get('message', 'Lỗi không xác định')}"}
    except Exception as e:
        return {"error": f"Lỗi khi gọi API thời tiết: {e}"}


# Tạo server TCP để xử lý yêu cầu
SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 99

# Khởi động server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(5)
print(f"Server đang lắng nghe tại {SERVER_ADDRESS}:{SERVER_PORT}")

while True:
    connection, client_addr = server_socket.accept()
    print(f"Kết nối từ địa chỉ: {client_addr}")

    try:
        request_data = ""
        while True:
            try:
                received = connection.recv(1024).decode('utf-8')
            except ConnectionResetError:
                print("Client đóng kết nối đột ngột khi nhận dữ liệu.")
                continue
            if not received:
                break
            request_data += received
            if "\n" in request_data:
                break

        request_data = request_data.strip()
        if not request_data:
            response = json.dumps({"error": "Không nhận được dữ liệu. Vui lòng gửi yêu cầu hợp lệ."})
            try:
                connection.sendall(response.encode('utf-8'))
            except ConnectionResetError:
                print("Không thể gửi phản hồi, client đã đóng kết nối.")
                continue

        print(f"Yêu cầu từ client: {request_data}")

        if request_data.startswith("STOCK"):
            requested_code = request_data.split(" ")[1]
            print("Đang xử lý dữ liệu...")
            data = collect_stock_data()

            if not data:
                response = json.dumps({"error": "Không thể thu thập dữ liệu chứng khoán. Vui lòng thử lại sau."})
            else:
                normalized_data = {key.upper(): value for key, value in data.items()}  # Chuẩn hóa dữ liệu
                if requested_code.upper() in normalized_data:
                    response = json.dumps({
                        "stock_code": requested_code.upper(),
                        "tc_price": normalized_data[requested_code.upper()]
                    })
                else:
                    response = json.dumps({
                        "error": f"Mã chứng khoán '{requested_code}' không tồn tại.",
                        "valid_codes": list(data.keys()),  # Danh sách mã hợp lệ
                        "suggestion": f"Kiểm tra lại mã chứng khoán, ví dụ: {list(data.keys())[:5]}"
                    })

        # Xử lý yêu cầu lấy dữ liệu thời tiết
        elif request_data.startswith("WEATHER"):
            city_name = " ".join(request_data.split(" ")[1:])
            print(f"Đang lấy dữ liệu thời tiết cho {city_name}...")
            weather_info = get_weather_data(city_name)

            response = json.dumps(weather_info)

        else:
            response = json.dumps(
                {"error": "Lệnh không hợp lệ. Hãy dùng: STOCK <mã_chứng_khoán> hoặc WEATHER <tên_thành_phố>."}
            )

        connection.sendall(response.encode('utf-8'))

    except Exception as error:
        error_response = json.dumps({"error": str(error)})
        connection.sendall(error_response.encode('utf-8'))

    finally:
        connection.close()