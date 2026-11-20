# Mini-project nhóm về dữ liệu Iris

Thành viên: Lê Văn Triệu, La Quỳnh Như, Đinh Hoàng Minh, Võ Thị Thùy Trang.

Dùng tiếp dữ liệu UCI Iris và phần so sánh bốn mô hình trong bài thực hành. CSV gốc có 150 dòng. Sau khi loại ba dòng trùng theo bốn thuộc tính cùng nhãn, còn 147 mẫu. Chia phân tầng 102 mẫu huấn luyện và 45 mẫu kiểm tra, random_state=42; kiểm định chéo năm fold chỉ dùng phần huấn luyện.

Mã nguồn và dữ liệu nằm trong `../iris-phan-loai`. Xem hướng dẫn tại `../iris-phan-loai/README.md`, phần Dashboard. Chạy `../iris-phan-loai/scripts/5_Dashboard.cmd` rồi mở `http://127.0.0.1:8504`.

Giao diện có bộ lọc loài, chọn trục X/Y, ba loại biểu đồ và bảng dữ liệu. Tab tải kết quả xuất PDF và CSV theo bộ lọc. Bảng kết quả mô hình ghi riêng phạm vi toàn bộ dữ liệu đã làm sạch, không thay đổi theo loài đang xem.

`Bao_cao_Iris_theo_bo_loc.pdf` là tệp tải trực tiếp từ dashboard khi chỉ chọn setosa: 48 mẫu, trục X là chiều dài cánh hoa, trục Y là chiều rộng cánh hoa. PDF gồm hai trang. Báo cáo tổng hợp ban đầu ở `../iris-phan-loai/results/Bao_cao_tu_dong.pdf`.

Minh chứng: `../minh_chung/20_dashboard_tong_quan.jpg`, `21_dashboard_bo_loc.jpg`, `22_dashboard_tai_bao_cao.jpg`; nhật ký kiểm thử `../minh_chung/log_dashboard.txt`.

Mã nguồn dùng MIT; dữ liệu Iris dùng CC BY 4.0, DOI 10.24432/C56C76. Kho mã nguồn: https://github.com/levantrieu19081995/ct999-iris-phan-loai. Dashboard và kết quả mới đã cập nhật lên nhánh main ngày 20/11/2026, commit 591ac1a. Mã commit trên máy và GitHub đã được đối chiếu trùng nhau. Bản PDF tải thử có thêm hướng phát triển ở cuối mục nhận xét.
