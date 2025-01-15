import time
import json
from playwright.sync_api import sync_playwright
import socket

# Hàm cuộn trang xuống
def scroll_down(page, scroll_element_selector, step=50, max_height=300):
    scroll_position = 0
    while scroll_position < max_height:
        page.eval_on_selector(scroll_element_selector, f"el => el.scrollTop = {scroll_position}")
        scroll_position += step
        time.sleep(0.5)

# Hàm chạy Playwright và lấy dữ liệu
def fetch_stock_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False để xem quá trình chạy
        page = browser.new_page()

        page.goto("https://iboard.ssi.com.vn/")
        time.sleep(10)

        scroll_down(page, ".ag-body-viewport.ag-layout-normal.ag-row-animation.scroll-base")
        scroll_down(page, ".ag-center-cols-clipper")
        time.sleep(3)

        elements = page.query_selector_all(".ag-pinned-left-cols-container")
        stock_codes = []
        if len(elements) >= 2:
            content = elements[1].inner_text()
            stock_codes = content.split("\n")
        else:
            print("Không tìm thấy đủ phần tử.")

        tc_cells = page.query_selector_all(".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-ref.ag-cell-bg-highlight.cursor-pointer.ag-cell-value")
        tc_prices = [cell.inner_text() for cell in tc_cells] if tc_cells else []

        browser.close()

        result = {}
        for i in range(min(len(stock_codes), len(tc_prices))):
            result[stock_codes[i]] = tc_prices[i]
        return result

# Tạo server TCP để xử lý yêu cầu
HOST = '0.0.0.0'  # Lắng nghe trên tất cả các địa chỉ IP
PORT = 99         # Cổng server

# Khởi tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server đang chạy trên {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Kết nối từ {client_address}")

    try:
        data = ""
        while True:
            chunk = client_socket.recv(1024).decode('ascii')
            if not chunk:
                break
            data += chunk
            if "\n" in data:  # Dừng lại khi nhận đủ một dòng
                break
        data = data.strip()
        if not data:
            response = json.dumps({"error": "Dữ liệu rỗng. Vui lòng gửi yêu cầu hợp lệ."})
            client_socket.sendall(response.encode('ascii'))
            continue

        print(f"Yêu cầu nhận được: {data}")

        if data.startswith("STOCK "):
            stock_code = data.split(" ")[1]
            print("Đang lấy dữ liệu, vui lòng đợi...")
            stock_data = fetch_stock_data()
            if stock_code in stock_data:
                response = json.dumps({"stock_code": stock_code, "tc_price": stock_data[stock_code]})
            else:
                response = json.dumps({"error": "Không tìm thấy mã chứng khoán."})
        else:
            response = json.dumps({"error": "Yêu cầu không hợp lệ."})

        # Gửi phản hồi tới client
        client_socket.sendall(response.encode('ascii'))
    except Exception as e:
        error_message = json.dumps({"error": str(e)})
        client_socket.sendall(error_message.encode('ascii'))
    finally:
        client_socket.close()