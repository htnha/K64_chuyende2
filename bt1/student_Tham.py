from Student import Student
import socket
import json


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

# Tạo đối tượng Tham và gọi hàm stock
#student = Tham()
#student.stock("FPT")  # Gọi hàm send_request với mã chứng khoán
