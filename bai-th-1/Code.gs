
function taoBaiKhaoSatTH2() {
  // 1. T?o Google Form
  const form = FormApp.create(
    "KH?O SÁT HI?U QU? QU?N LÝ CÔNG VI?C NHÓM PHÁT TRI?N PH?N M?M"
  );

  form.setDescription(
    "BÀI TH?C HÀNH 2 - CÔNG DÂN S? NÂNG CAO\n\n" +
    "M?c tiêu: Kh?o sát th?c tr?ng phân công, theo dõi ti?n d? " +
    "và ph?i h?p trong các nhóm phát tri?n ph?n m?m.\n\n" +
    "Ð?i tu?ng: L?p trình viên, sinh viên và h?c viên " +
    "dã t?ng tham gia d? án phát tri?n ph?n m?m.\n\n" +
    "D? li?u ch? ph?c v? m?c dích h?c t?p và nghiên c?u. " +
    "Không yêu c?u cung c?p thông tin cá nhân."
  );

  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setConfirmationMessage(
    "C?m on Anh/Ch? dã tham gia kh?o sát!"
  );

  // Hàm thêm câu h?i tr?c nghi?m
  function tracNghiem(title, options) {
    form.addMultipleChoiceItem()
      .setTitle(title)
      .setChoiceValues(options)
      .setRequired(true);
  }

  // Hàm thêm câu h?i ch?n nhi?u dáp án
  function nhieuLuaChon(title, options) {
    form.addCheckboxItem()
      .setTitle(title)
      .setChoiceValues(options)
      .setRequired(true);
  }

  // Hàm thêm câu h?i thang do 1-5
  function thangDo(title, low, high) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels(low, high)
      .setRequired(true);
  }

  // Câu 1
  tracNghiem(
    "1. Vai trò c?a Anh/Ch? trong nhóm phát tri?n ph?n m?m?",
    [
      "L?p trình viên",
      "Ki?m th? ph?n m?m (Tester/QA)",
      "Phân tích nghi?p v? (BA)",
      "Tru?ng nhóm / Qu?n lý d? án",
      "Sinh viên / H?c viên th?c hi?n d? án",
      "Vai trò khác"
    ]
  );

  // Câu 2
  tracNghiem(
    "2. Kinh nghi?m tham gia làm vi?c nhóm phát tri?n ph?n m?m?",
    [
      "Du?i 1 nam",
      "T? 1 d?n du?i 3 nam",
      "T? 3 d?n du?i 5 nam",
      "T? 5 nam tr? lên"
    ]
  );

  // Câu 3
  nhieuLuaChon(
    "3. Nhóm c?a Anh/Ch? s? d?ng công c? nào d? qu?n lý công vi?c?",
    [
      "Trello",
      "Jira",
      "GitHub Projects / GitLab",
      "Google Sheets / Excel",
      "Notion",
      "Chua s? d?ng công c? chuyên bi?t",
      "Công c? khác"
    ]
  );

  // Câu 4
  tracNghiem(
    "4. Nhóm thu?ng c?p nh?t ti?n d? công vi?c v?i t?n su?t nào?",
    [
      "H?ng ngày",
      "2-3 l?n m?i tu?n",
      "M?i tu?n m?t l?n",
      "Ít hon m?t l?n m?i tu?n",
      "Không có l?ch c?p nh?t c? d?nh"
    ]
  );

  // Câu 5
  thangDo(
    "5. M?c d? rõ ràng khi phân công nhi?m v? trong nhóm?",
    "1 - R?t không rõ ràng",
    "5 - R?t rõ ràng"
  );

  // Câu 6
  thangDo(
    "6. M?c d? d? dàng khi theo dõi ti?n d? công vi?c?",
    "1 - R?t khó",
    "5 - R?t d?"
  );

  // Câu 7
  tracNghiem(
    "7. Nhóm có thu?ng xuyên x?y ra tình tr?ng tr? h?n công vi?c không?",
    [
      "R?t thu?ng xuyên",
      "Thu?ng xuyên",
      "Th?nh tho?ng",
      "Hi?m khi",
      "Không bao gi?"
    ]
  );

  // Câu 8
  nhieuLuaChon(
    "8. Nh?ng khó khan nào thu?ng g?p khi ph?i h?p công vi?c?",
    [
      "Phân công nhi?m v? chua rõ ràng",
      "Khó theo dõi ti?n d?",
      "Trao d?i thông tin chua k?p th?i",
      "Thay d?i yêu c?u liên t?c",
      "Thi?u tài li?u ho?c thông tin",
      "Kh?i lu?ng công vi?c chua h?p lý",
      "Không g?p khó khan dáng k?"
    ]
  );

  // Câu 9
  thangDo(
    "9. M?c d? hi?u qu? c?a vi?c giao ti?p trong nhóm?",
    "1 - R?t kém",
    "5 - R?t hi?u qu?"
  );

  // Câu 10
  thangDo(
    "10. M?c d? hài lòng v?i phuong pháp qu?n lý công vi?c hi?n t?i?",
    "1 - R?t không hài lòng",
    "5 - R?t hài lòng"
  );

  // Câu 11
  tracNghiem(
    "11. Anh/Ch? có s?n sàng s? d?ng Trello d? qu?n lý công vi?c nhóm?",
    [
      "R?t s?n sàng",
      "S?n sàng",
      "C?n tìm hi?u thêm",
      "Không s?n sàng",
      "Ðang s? d?ng Trello"
    ]
  );

  // Câu 12
  form.addParagraphTextItem()
    .setTitle(
      "12. Anh/Ch? d? xu?t gi?i pháp gì d? nâng cao " +
      "hi?u qu? qu?n lý công vi?c nhóm phát tri?n ph?n m?m?"
    )
    .setRequired(false);

  // 2. T?o Google Sheets nh?n ph?n h?i
  const sheet = SpreadsheetApp.create(
    "TH2 - Du lieu khao sat quan ly nhom phat trien phan mem"
  );

  form.setDestination(
    FormApp.DestinationType.SPREADSHEET,
    sheet.getId()
  );

  // 3. Ghi liên k?t d? ngu?i dùng m?
  Logger.log("=== T?O KH?O SÁT THÀNH CÔNG ===");
  Logger.log("CH?NH S?A FORM: " + form.getEditUrl());
  Logger.log("G?I KH?O SÁT: " + form.getPublishedUrl());
  Logger.log("GOOGLE SHEETS: " + sheet.getUrl());
  Logger.log("S? CÂU H?I: " + form.getItems().length);
}
