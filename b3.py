import logging
import sys

# Cấu hình logging ghi ra file tournament_app.log theo chuẩn định dạng yêu cầu
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("tournament_app.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


def determine_winner(match: dict) -> str:
    """ Phân định kết quả thắng, hòa hoặc chưa diễn ra của một trận đấu.

    Args:
        match (dict): Dictionary chứa thông tin chi tiết của một trận đấu.

    Returns:
        str: Tên đội thắng, hoặc "Draw" nếu hòa, hoặc "Not Started" nếu chưa đá.
    """
    try:
        if match.get("status") == "Pending":
            return "Not Started"
        
        score_a = match["score_a"]
        score_b = match["score_b"]
        
        if score_a > score_b:
            return match["team_a"]
        elif score_b > score_a:
            return match["team_b"]
        else:
            return "Draw"
    except KeyError as e:
        logger.error(f"Missing key in match data: {e}")
        return "Data Error"


def display_matches(match_list: list) -> None:
    """ Hiển thị lịch thi đấu và kết quả hiện tại dưới dạng bảng định dạng cột.

    Args:
        match_list (list): Danh sách các trận đấu đang quản lý.
    """
    if not match_list:
        print("\nHiện chưa có trận đấu nào trong hệ thống.")
        logger.info("User viewed an empty match list.")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<7} | Trạng thái")
    print("-" * 70)
    
    for match in match_list:
        try:
            score_str = f"{match['score_a']}-{match['score_b']}"
            print(f"{match['match_id']:<10} | {match['team_a']:<15} | {match['team_b']:<15} | {score_str:<7} | {match['status']}")
        except KeyError as e:
            logger.error(f"Failed to display match due to missing key: {e}")
            
    logger.info("User viewed the match list.")


def add_match(match_list: list) -> None:
    """ Tiếp nhận dữ liệu đầu vào và thêm một trận đấu mới vào hệ thống.

    Args:
        match_list (list): Danh sách các trận đấu hiện tại.
    """
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    match_id = input("Nhập mã trận đấu: ").strip()
    if not match_id:
        print("\nMã trận đấu không được để trống.")
        logger.warning("User tried to add a match with empty match ID.")
        return

    for match in match_list:
        if match.get("match_id") == match_id:
            print(f"\nLỗi: Mã trận đấu {match_id} đã tồn tại.")
            logger.warning(f"Match ID {match_id} already exists.")
            return

    team_a = input("Nhập tên Đội A: ").strip()
    if not team_a:
        print("\nTên đội không được để trống.")
        logger.warning("User tried to add a match with empty team name.")
        return

    team_b = input("Nhập tên Đội B: ").strip()
    if not team_b:
        print("\nTên đội không được để trống.")
        logger.warning("User tried to add a match with empty team name.")
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
    logger.info(f"Match {match_id} added successfully")


def _get_valid_score(team_label: str) -> int:
    """ Hàm phụ trợ yêu cầu nhập điểm số hợp lệ dưới dạng số nguyên không âm.

    Args:
        team_label (str): Tên nhãn hiển thị cho đội cần nhập (VD: 'Đội A').

    Returns:
        int: Điểm số hợp lệ lớn hơn hoặc bằng 0.
    """
    while True:
        try:
            score_input = input(f"Nhập điểm {team_label}: ").strip()
            score = int(score_input)
            if score < 0:
                print("\nĐiểm số phải lớn hơn hoặc bằng 0.")
                logger.error(f"Negative score input detected: {score}")
                continue
            return score
        except ValueError as e:
            print("\nĐiểm số phải là số nguyên. Vui lòng nhập lại.")
            logger.error(f"Invalid score input. Error: {e}")


def update_score(match_list: list) -> None:
    """ Tìm kiếm trận đấu theo mã và cập nhật tỷ số do trọng tài nhập vào.

    Args:
        match_list (list): Danh sách các trận đấu chứa mục cần cập nhật.
    """
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    
    target_match = None
    for match in match_list:
        if match.get("match_id") == match_id:
            target_match = match
            break

    if not target_match:
        print(f"\nKhông tìm thấy trận đấu mang mã {match_id}.")
        logger.warning(f"User tried to update non-existing match {match_id}")
        return

    print(f"\nTrận đấu: {target_match['team_a']} vs {target_match['team_b']} ({target_match['status']})")
    
    score_a = _get_valid_score("Đội A")
    score_b = _get_valid_score("Đội B")

    # Xử lý triệt để bẫy logic tỷ số 0 - 0
    if score_a == 0 and score_b == 0:
        confirm = input("\nTỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
        if confirm == 'y':
            target_match["status"] = "Completed"
        else:
            target_match["status"] = "Pending"
    else:
        target_match["status"] = "Completed"

    target_match["score_a"] = score_a
    target_match["score_b"] = score_b

    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
    logger.info(f"Match {match_id} score updated successfully")


def generate_report(match_list: list) -> None:
    """ Tính toán và hiển thị thống kê danh sách các trận đấu đã hoàn thành.

    Args:
        match_list (list): Danh sách các trận đấu cần tổng hợp báo cáo.
    """
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    completed_count = 0
    
    for match in match_list:
        if match.get("status") == "Completed":
            winner = determine_winner(match)
            try:
                print(f"{match['match_id']}: {match['team_a']} {match['score_a']}-{match['score_b']} {match['team_b']} | Kết quả: {winner}")
                completed_count += 1
            except KeyError as e:
                logger.error(f"Failed to generate report item due to missing key: {e}")

    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")
        
    print(f"\nTổng số trận đã hoàn thành: {completed_count}")
    logger.info("User generated tournament report.")


def main() -> None:
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

    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. CẬP NHẬT TỶ SỐ TRẬN ĐẤU")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()
        
        if choice == "1":
            display_matches(matches)
        elif choice == "2":
            add_match(matches)
        elif choice == "3":
            update_score(matches)
        elif choice == "4":
            generate_report(matches)
        elif choice == "5":
            logger.info("Tournament management system closed by user.")
            print("\nĐang đóng hệ thống... Tạm biệt!")
            sys.exit() 
        else:
            print("\nLựa chọn không hợp lệ! Vui lòng nhập từ 1 đến 5.")
            logger.warning("Invalid menu choice selected.")


if __name__ == "__main__":
    main()
