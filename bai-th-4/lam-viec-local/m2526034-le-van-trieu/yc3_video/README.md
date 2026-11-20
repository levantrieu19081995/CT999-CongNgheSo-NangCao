# Video nghiên cứu về phân loại hoa Iris

Thành viên: Lê Văn Triệu, La Quỳnh Như, Đinh Hoàng Minh, Võ Thị Thùy Trang. Đơn vị: Đại học Cần Thơ. Học phần CT999 – Công nghệ số nâng cao.

`Video_nghien_cuu_Iris.mp4` là bản video 16:9, 1280 × 720, có tiếng và phụ đề tiếng Việt được ghi trực tiếp vào hình. Thời lượng khoảng 2 phút 50 giây. Phụ đề rời ở `Phu_de_Iris.srt`. `Thuyet_minh_Iris.mp3` là phần âm thanh của bản video.

Video dùng giọng đọc tiếng Việt tự động qua gTTS, không phải giọng thu của các thành viên. Từng đoạn lời được lưu trong `kich_ban.json`; âm thanh và mốc phụ đề được lưu ở `am_thanh`. Mốc phụ đề căn theo thời lượng từng đoạn âm thanh, thời gian từ trong đoạn được nội suy. Tám khung hình nguồn ở `khung_hinh` dùng biểu đồ thực nghiệm và ảnh chụp dashboard, không dùng dữ liệu minh họa thay kết quả chạy.

Nội dung chia theo đề bài: mở đầu 13 giây; vấn đề 24 giây; phương pháp 44 giây; kết quả 47 giây; phân tích và kết luận 30 giây; kết thúc 12 giây. Tổng các cảnh là 170 giây. Thông số và mã băm video ở `thong_tin_video.json`.

Muốn dựng lại trên máy Windows đã có Python 3.12, chạy từ thư mục `iris-phan-loai`:

```console
.venv\Scripts\python -m pip install -r ../yc3_video/requirements.txt
.venv\Scripts\python ../yc3_video/tao_video.py
```

Chương trình xuất bản dựng `Video_dung_tu_khung_hinh.mp4` và `thong_tin_ban_dung.json`. Bản nộp `Video_nghien_cuu_Iris.mp4` được tải riêng từ Canva sau khi đưa bản dựng vào dòng thời gian và xuất MP4 720p. Thao tác trên Canva được ghi trong `Canva_video.txt` và các ảnh minh chứng.

Nếu đã có âm thanh và tệp nguồn tương ứng, chương trình dùng lại âm thanh; nếu sửa lời sẽ tạo lại cảnh đó. Khi tạo mới giọng đọc cần kết nối Internet. FFmpeg ghép hình, âm thanh và phụ đề; font Arial lấy từ máy Windows và không phân phối lại. Bộ nhớ tạm `.tts_cache` có thể bỏ sau khi dựng.

Biểu đồ lấy từ `../iris-phan-loai/results/figures`, ảnh dashboard lấy từ `../minh_chung/20_dashboard_tong_quan.jpg`. Kết quả dùng cùng dữ liệu, cách chia và cấu hình của bài viết, poster và slide. Dữ liệu UCI Iris dùng CC BY 4.0. Mã nguồn tự viết dùng MIT của dự án.

Thiết kế Canva và tệp xuất được ghi trong `Canva_video.txt`. Kiểm tra ngày 20/11/2026: bản xuất có thời lượng 170,05 giây, H.264/AAC, 1280 × 720; giải mã toàn bộ hình và âm thanh không có lỗi.
