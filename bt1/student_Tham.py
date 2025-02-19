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
        return "20.0.0.237"

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
            response = client_socket.recv(1024).decode('ascii').strip()  # Loại bỏ khoảng trắng và xuống dòng
            print(f"Phản hồi từ server: {response}")  # Debug log

            if not response:
                return "Không nhận được dữ liệu từ server."

            try:
                response_data = json.loads(response)  # Giải mã JSON từ phản hồi
                if "error" in response_data:
                    return f"Lỗi từ server: {response_data['error']}"

                stock_code = response_data.get('stock_code', 'N/A')
                tc_price = response_data.get('tc_price', 'N/A')

                return f"Mã chứng khoán: {stock_code}\nGiá tham chiếu: {tc_price}"

            except json.JSONDecodeError:
                return f"Phản hồi không hợp lệ từ server: {response}"

        except ConnectionRefusedError:
            return "Không thể kết nối đến server. Vui lòng kiểm tra địa chỉ và cổng."
        except Exception as e:
            return f"Lỗi: {e}"
        finally:
            client_socket.close()


student = Tham()  # Tạo đối tượng Tham
student.stock("FPT")  # Gọi hàm stock với mã chứng khoán
