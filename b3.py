import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("tournament_app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]


def display_matches(match_list):
    logging.info("User viewed the match list.")
    
    if not match_list:
        print("\nHiện chưa có trận đấu nào trong hệ thống.")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<7} | Trạng thái")
    print("-" * 70)
    
    for match in match_list:
        try:
            m_id = match["match_id"]
            t_a = match["team_a"]
            t_b = match["team_b"]
            s_a = match["score_a"]
            s_b = match["score_b"]
            status = match["status"]
            print(f"{m_id:<10} | {t_a:<15} | {t_b:<15} | {s_a}-{s_b:<5} | {status}")
        except KeyError as e:
            logging.error(f"Missing key in match dictionary data. Detail: {e}")
            print(f"[Lỗi dữ liệu] Trận đấu bị thiếu thông tin: {e}")


def add_new_match(match_list):
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    
    match_id = input("Nhập mã trận đấu: ").strip()
    if not match_id:
        print("Mã trận đấu không được để trống.")
        logging.warning("User tried to add a match with empty match ID.")
        return

    if any(m["match_id"].upper() == match_id.upper() for m in match_list):
        print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại.")
        logging.warning(f"Match ID {match_id} already exists.")
        return

    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()
    if not team_a or not team_b:
        print("Tên đội không được để trống.")
        logging.warning("User tried to add a match with empty team name.")
        return

    new_match = {
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
    match_list.append(new_match)
    print(f"\nThành công: Đã thêm trận đấu {match_id}.")
    logging.info(f"Match {match_id} added successfully")


def _get_valid_score(team_label):
    while True:
        try:
            score_input = input(f"Nhập điểm {team_label}: ")
            score = int(score_input)
            if score < 0:
                print("Điểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score}")
                continue
            return score
        except ValueError as e:
            print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: {e}")


def update_score(match_list):
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()

    target_match = None
    for m in match_list:
        if m["match_id"].upper() == match_id.upper():
            target_match = m
            break

    if not target_match:
        print(f"Không tìm thấy trận đấu mang mã {match_id}.")
        logging.warning(f"User tried to update non-existing match {match_id}")
        return

    print(f"\nTrận đấu: {target_match['team_a']} vs {target_match['team_b']} ({target_match['status']})")
    
    score_a = _get_valid_score("Đội A")
    score_b = _get_valid_score("Đội B")

    if score_a == 0 and score_b == 0:
        while True:
            confirm = input("Tỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
            if confirm == 'y':
                status = "Completed"
                break
            elif confirm == 'n':
                status = "Pending"
                break
            print("Vui lòng chỉ nhập 'y' hoặc 'n'.")
    else:
        status = "Completed"

    target_match["score_a"] = score_a
    target_match["score_b"] = score_b
    target_match["status"] = status

    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
    logging.info(f"Match {match_id} score updated successfully")


def determine_winner(match):
    try:
        if match["status"] != "Completed":
            return "Not Started"
        if match["score_a"] > match["score_b"]:
            return match["team_a"]
        elif match["score_b"] > match["score_a"]:
            return match["team_b"]
        else:
            return "Draw"
    except KeyError as e:
        logging.error(f"KeyError inside determine_winner wrapper: {e}")
        return "Data Error"


def generate_report(match_list):
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    completed_count = 0

    for match in match_list:
        if match.get("status") == "Completed":
            winner = determine_winner(match)
            print(f"{match['match_id']}: {match['team_a']} {match['score_a']}-{match['score_b']} {match['team_b']} | Kết quả: {winner}")
            completed_count += 1

    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")
        
    print(f"\nTổng số trận đã hoàn thành: {completed_count}")
    logging.info("User generated tournament report.")


def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. Cập nhật tỷ số trận đấu")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            display_matches(matches)
        elif choice == "2":
            add_new_match(matches)
        elif choice == "3":
            update_score(matches)
        elif choice == "4":
            generate_report(matches)
        elif choice == "5":
            logging.info("System is shutting down. Exiting program.")
            print("\nHệ thống đóng. Cảm ơn bạn đã sử dụng dịch vụ!")
            break
        else:
            print("\nLựa chọn không hợp lệ! Vui lòng nhập lại số từ 1 đến 5.")
            logging.warning(f"Invalid menu choice selected: '{choice}'")


main()