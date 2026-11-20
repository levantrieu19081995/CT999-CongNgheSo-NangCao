# Biên bản họp nhóm

Hệ thống đặt vé máy bay phân tán
sử dụng CockroachDB và Cassandra

## Thông tin cuộc họp

Hình thức: Họp trực tuyến qua Google Meet.

Thời gian: Khoảng 20 giờ 13 đến 20 giờ 17 ngày 19/11/2026, theo đồng hồ hiển thị trong video.

Thành viên: Lê Văn Triệu, La Quỳnh Như, Đinh Hoàng Minh và Võ Thị Thùy Trang.

Tệp ghi cuộc họp: videoCuochopNhom.mp4, thời lượng khoảng 4 phút 17 giây.

Mục đích: Rà lại đề tài, xác định những phần cần hoàn thiện và phân công công việc cho bốn thành viên.

## Nội dung trao đổi

Lê Văn Triệu nêu các thao tác của hệ thống gồm chọn chuyến bay, chọn ghế, tạo đặt chỗ và ghi nhận thanh toán. Nhóm cần kiểm tra trường hợp nhiều yêu cầu cùng đặt một ghế, làm rõ vị trí dữ liệu trên các node và cách hệ thống hoạt động khi có sự cố.

La Quỳnh Như đề nghị giải thích vai trò của từng cơ sở dữ liệu, bổ sung sơ đồ dữ liệu và sơ đồ các node. Đinh Hoàng Minh đề nghị chuẩn bị bảng tình huống, thao tác và kết quả mong đợi trước khi chạy thử. Võ Thị Thùy Trang đề nghị trình bày kết quả theo từng bước và thống nhất tên ảnh minh chứng để tránh nhầm lẫn.

Nhóm xác định bảy công việc chính:

1. Rà lại chức năng đặt vé và luồng xử lý từ chọn chuyến bay đến kết quả đặt chỗ.

2. Kiểm tra cấu trúc dữ liệu trên CockroachDB và Cassandra, xác định vai trò của từng bảng.

3. Kiểm tra giao diện phân tán, số lượng bản ghi, danh sách dữ liệu và thông tin node.

4. Chuẩn bị tình huống nhiều yêu cầu cùng đặt một ghế để kiểm tra xử lý đồng thời.

5. Chuẩn bị tình huống gián đoạn kết nối hoặc node gặp sự cố trong phạm vi môi trường nhóm có thể thực hiện.

6. Chạy thử, lưu kết quả và chụp ảnh minh chứng.

7. Tổng hợp báo cáo, làm slide và chuẩn bị thứ tự trình diễn.

## Phân công công việc

| Thành viên | Nội dung phụ trách |

| --- | --- |

| Lê Văn Triệu | Phụ trách chức năng và giao diện của hệ thống. |

| La Quỳnh Như | Phụ trách dữ liệu và sơ đồ; rà cấu trúc dữ liệu và gửi sơ đồ để nhóm góp ý. |

| Đinh Hoàng Minh | Phụ trách kiểm thử; chuẩn bị bảng tình huống, phối hợp chạy và đối chiếu kết quả. |

| Võ Thị Thùy Trang | Phụ trách báo cáo, minh chứng và slide; chuẩn bị sườn báo cáo, ghi nhận phân công và các mốc thời gian. |

## Kết luận cuộc họp

Bốn thành viên thống nhất thực hiện các phần việc đã nhận. Kết quả đưa vào báo cáo phải lấy từ lần chạy thực tế; phần chưa kiểm tra cần ghi rõ để tiếp tục thực hiện. Trước khi nộp, nhóm cùng xem lại báo cáo và chạy thử phần trình diễn. Các vướng mắc được trao đổi trong nhóm để xử lý.

Cuộc họp chưa chốt ngày giờ hoàn thành từng phần việc.

## Các mốc đối chiếu trong video

00:04 - 00:55: Nêu mục đích cuộc họp và vấn đề của hệ thống.

00:55 - 01:48: Các thành viên góp ý về dữ liệu, kiểm thử và cách trình bày báo cáo.

01:49 - 03:14: Liệt kê bảy công việc và bổ sung cách chuẩn bị sơ đồ, tình huống, minh chứng.

03:15 - 03:45: Tổng hợp phân công và thống nhất cách ghi nhận kết quả chạy.

03:46 - 04:17: Các thành viên xác nhận phần việc và kết thúc cuộc họp.

## Tệp minh chứng

Video cuộc họp được lưu cùng thư mục với biên bản: [videoCuochopNhom.mp4](videoCuochopNhom.mp4).
