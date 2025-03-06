import socket

# Cấu hình server
SERVER_HOST = '127.0.0.1'  # Địa chỉ IP của server
SERVER_PORT = 99  # Cổng server

def query_stock(stock_symbol):
    try:
        # Khởi tạo socket và kết nối đến server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Đang kết nối tới {SERVER_HOST}:{SERVER_PORT}...")
            sock.connect((SERVER_HOST, SERVER_PORT))

            # Gửi yêu cầu tới server
            request_message = f"STOCK {stock_symbol}\n"
            sock.sendall(request_message.encode('utf-8'))

            # Nhận phản hồi từ server
            response_data = sock.recv(4096).decode('utf-8')
            print(f"Phản hồi từ server: {response_data}")

    except ConnectionRefusedError:
        print("Không thể kết nối đến server. Đảm bảo rằng server đang hoạt động.")
    except Exception as error:
        print(f"Đã xảy ra lỗi: {error}")

if __name__ == "__main__":
    print("Nhập mã chứng khoán để truy vấn thông tin giá:")
    stock_symbol = input("Mã chứng khoán: ").strip()
    query_stock(stock_symbol)
