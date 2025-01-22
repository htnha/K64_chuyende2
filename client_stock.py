import socket
import json

# Cấu hình server
HOST = '117.0.110.242'  # Địa chỉ server
PORT = 99               # Cổng server

def send_request(stock_code):
    try:
        # Tạo socket và kết nối đến server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print("Kết nối đến server thành công.")

        # Gửi yêu cầu, thêm ký tự kết thúc dòng để server dễ xử lý
        request = f"STOCK {stock_code}\n"
        client_socket.sendall(request.encode('ascii'))
        
        # Nhận phản hồi từ server
        response = client_socket.recv(1024).decode('ascii')
        try:
            response_data = json.loads(response)  # Giải mã JSON từ phản hồi
            if "error" in response_data:
                print(f"Lỗi từ server: {response_data['error']}")
            else:
                print(f"Mã chứng khoán: {response_data['stock_code']}")
                print(f"Giá tham chiếu: {response_data['tc_price']}")
        except json.JSONDecodeError:
            print(f"Phản hồi không hợp lệ từ server: {response}")
    except ConnectionRefusedError:
        print("Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng.")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("Nhập mã chứng khoán để lấy giá tham chiếu:")
    stock_code = input("Mã chứng khoán: ").strip().upper()  # Đảm bảo mã viết hoa
    send_request(stock_code)
