# Dữ liệu đầu vào

Nguồn: https://archive.ics.uci.edu/dataset/53/iris . Gói tải: https://archive.ics.uci.edu/static/public/53/iris.zip . DOI: 10.24432/C56C76 . Tác giả được UCI ghi nhận: R. A. Fisher (1936). Giấy phép: CC BY 4.0.

- `iris.data`: tệp gốc có 150 dòng, không có dòng tiêu đề.
- `iris.names`: mô tả đi kèm gói UCI.
- `iris.csv`: chuyển từ iris.data, thêm tiêu đề cột và source_id từ 1 đến 150. Bốn số đo có đơn vị cm.

Bài thực hành dùng chính biến thể iris.data này. Trang UCI có ghi nhận khác biệt giữa một số bản Iris; không thay dữ liệu bằng bản từ thư viện khác khi chạy đối chiếu.

Mã băm SHA-256 của ba tệp được lưu trong `sha256.json`. Dữ liệu sạch và các dòng trùng bị loại nằm trong results, không ghi đè tệp gốc.
