""" """

import os

os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-21"
import time
import json
from cores.normalizer import TextNormalizer


TEST_TEXTS = [
    "1. Những ngân hàng đang có lãi suất cho vay bình quân cao như Liên Việt, Bản Việt, Kiên Long với lãi suất từ 8,07 $ -  8,94$...",
    "2. Từ lâu công viên 30/4 đã trở thành nơi lý tưởng để giới trẻ, du khách chụp ảnh, nhâm nhi ly cà phê hay ngồi dưới tán cây trò chuyện tránh những ngày nắng nóng. Công viên 23-9 nằm giữa hai con đường Lê Lai và Phạm Ngũ Lão, trải dài từ công trường Quách Thị Trang đến đường Nguyễn Trãi. Công viên gồm 3 khu và bị ngăn cách nhau bởi đường Nguyễn Thị Nghĩa.",
    "3. Bộ Quốc phòng Nga đồng thời tuyên bố hệ thống phòng không Nga đã bắn hạ 46 máy bay không người lái của Ukraine, một tên lửa ATACMS và 8 quả bom thông minh Hammer trong 24 giờ qua.",
    "4. Lấy cảm hứng từ chiếc xe quan tài Dracula xuất hiện trong tập phim năm 1965 của series phim truyền hình The Munsters",
    "5. Lãnh đạo Sở GD-ĐT TP.HCM cho biết về nguyên tắc xét điểm chuẩn lớp 10 trường, lớp chuyên như sau: Chỉ xét tuyển đối với thí sinh tham dự đủ các bài thi quy định, không vi phạm nội quy trong kỳ thi tuyển sinh và các bài thi đều đạt điểm lớn hơn 2.",
]


if __name__ == "__main__":
    tik = time.time()
    text_normalizer = TextNormalizer("./exps/vncorenlp/")
    print(f"[*] take {time.time() - tik} seconds to load model")
    tik = time.time()
    for text_inputs in TEST_TEXTS:
        text_outputs = text_normalizer(text_inputs)
    print(f"[*] take {time.time() - tik} seconds to normalize {len(TEST_TEXTS)} texts")
