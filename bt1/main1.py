from student_Nha import Nha
from student_Long import Long
from student_Dung import Dung
from student_Ekalat import Ekalat
from student_Tham import Tham
from student_Linh import Linh
from student_Phong import Phong
from student_Dat import Dat

# Create a list of students
k64_class = [Nha(), Long(), Dung(), Ekalat(), Tham(), Linh(), Phong(), Dat()]

for student in k64_class:
    try:
        print(student.name())
        print(student.speak())
        print(student.address())
    except NotImplementedError as e:
        print(f"Co loi cho sinh vien: {type(student).__name__} - {e}")