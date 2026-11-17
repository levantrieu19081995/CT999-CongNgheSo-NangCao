# Khảo sát mô hình phân loại hoa Iris

Lê Văn Triệu - M2526034. Bài thực hành 4, học phần CT999 - Công nghệ số nâng cao.

Dự án đọc dữ liệu Iris từ UCI, kiểm tra và loại dòng trùng, so sánh bốn mô hình, rồi sử dụng kết quả để tạo báo cáo PDF, bài viết LaTeX, poster và PowerPoint.

## Dữ liệu và phương pháp

- Nguồn: Fisher, R. (1936), Iris [Dataset], UCI Machine Learning Repository. DOI: [10.24432/C56C76](https://doi.org/10.24432/C56C76).
- Tệp nguồn cụ thể: `iris.data` trong [gói tải UCI](https://archive.ics.uci.edu/static/public/53/iris.zip). CSV gốc có 150 dòng và bốn đặc trưng. Cột `source_id` là số thứ tự dòng được thêm khi chuyển CSV.
- Quy tắc thực hành: giữ dòng đầu tiên trong các dòng trùng hoàn toàn theo bốn thuộc tính cùng nhãn. Loại 3 dòng, còn 147 mẫu. Các dòng bị loại được lưu riêng.
- Chia phân tầng 102 mẫu huấn luyện và 45 mẫu kiểm tra với `random_state=42`. Không có source_id chung giữa hai tập.
- Đánh giá chéo 5 fold chỉ dùng tập huấn luyện. kNN và SVM đặt StandardScaler trong Pipeline.

## Cấu trúc

```text
data/       CSV gốc, tệp UCI và nguồn dữ liệu
src/        Phân tích, tạo PDF, PowerPoint và poster
docs/       Markdown đầu vào, bài viết và tài liệu dự án
results/    CSV kết quả, hình, PDF và PowerPoint
LICENSE
CONTRIBUTING.md
CITATION.cff
THIRD_PARTY_NOTICES.md
requirements.txt
package.json
```

## Chạy phần Python

Yêu cầu Python 3.12 trở lên và font Times New Roman, Arial hỗ trợ tiếng Việt. Bản đã kiểm tra chạy trên Windows. Các tệp font được đọc từ thư mục Fonts của Windows, không phân phối lại trong kho.

```console
python -m pip install -r requirements.txt
python src/phan_tich.py --data data/iris.csv --out results
python src/tao_bao_cao.py --csv data/iris.csv --metrics results/metrics.csv --out results/Bao_cao_tu_dong.pdf
python src/tao_poster.py --project . --out results/Poster_Iris_A0.pdf
```

Mã phân tích lưu số liệu từ lần chạy vào CSV và JSON. Chương trình tạo PDF đọc các tệp này và đối chiếu số dự đoán đúng trước khi ghi báo cáo.

## Tạo PowerPoint từ Markdown

Phần này dùng Node.js và thư viện `@oai/artifact-tool` có trong môi trường thực hành. `package.json` ghi phiên bản đã sử dụng. Nếu thư viện được cài ở thư mục dùng chung, đặt `NODE_PATH` tới thư mục chứa các gói Node.js trước khi chạy.

```console
node src/tao_slide.mjs docs/noi_dung_slide.md results/Thuyet_trinh_Iris.pptx
```

Một tiêu đề `#` tạo slide đầu, mỗi tiêu đề `##` tạo một slide tiếp theo. Các dòng văn bản trở thành nội dung. Cú pháp ảnh Markdown chèn ảnh. Hai chỉ thị trong chú thích HTML dùng để đọc CSV và tạo biểu đồ hoặc bảng có thể chỉnh sửa:

```markdown
<!-- chart-csv: ../results/metrics.csv -->
<!-- table-csv: ../results/metrics.csv -->
<!-- source: Nguồn đối chiếu đưa vào ghi chú của slide -->
```

Tệp đầu vào đã chuẩn bị tạo 8 slide. Khi sửa Markdown, chạy lại lệnh để tạo phiên bản mới. PowerPoint xuất ra có thể mở và thuyết trình độc lập với môi trường tạo file.

## Kết quả ghi nhận

| Mô hình | F1 macro CV trung bình | Accuracy test | F1 macro test | Đúng/tổng |
| --- | ---: | ---: | ---: | ---: |
| kNN | 0.9602 | 0.9111 | 0.9095 | 41/45 |
| SVM | 0.9597 | 0.9111 | 0.9107 | 41/45 |
| Decision Tree | 0.9501 | 0.9333 | 0.9327 | 42/45 |
| Random Forest | 0.9501 | 0.9111 | 0.9107 | 41/45 |

CV và test dùng các tập đánh giá khác nhau. Các con số chỉ mô tả cấu hình và cách chia đã lưu. Tập kiểm tra nhỏ nên chưa đủ kết luận thuật toán nào luôn tốt hơn. Phiên bản thư viện, số mẫu và tham số chia nằm trong `results/summary.json`.

## Giấy phép và trích dẫn

Phần mã nguồn tự viết dùng **MIT**, xem [LICENSE](LICENSE). Dữ liệu Iris giữ **CC BY 4.0**. Các tệp của Springer giữ thông báo gốc và không được đổi thành MIT. Xem [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Thông tin trích dẫn dự án được lưu trong [CITATION.cff](CITATION.cff). Khi dùng dữ liệu, cần trích dẫn cả UCI Iris. Hướng dẫn đóng góp nằm trong [CONTRIBUTING.md](CONTRIBUTING.md).
