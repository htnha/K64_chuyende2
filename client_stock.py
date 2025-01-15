import socket

# Cấu hình server
HOST = '116.98.247.127'  # Địa chỉ server (localhost)
PORT = 99           # Cổng server

def send_request(stock_code):
    try:
        # Tạo socket và kết nối đến server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # Gửi yêu cầu
        request = f"STOCK {stock_code}"
        client_socket.sendall(request.encode('utf-8'))
        
        # Nhận phản hồi từ server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Phản hồi từ server: {response}")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("Nhập mã chứng khoán để lấy giá tham chiếu:")
    stock_code = input("Mã chứng khoán: ").strip()
    send_request(stock_code)
