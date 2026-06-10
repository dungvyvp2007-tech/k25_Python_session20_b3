import unittest
from b3 import determine_winner


class TestDetermineWinner(unittest.TestCase):

    def test_team_a_wins(self):
        """Test trường hợp Đội A chiến thắng (score_a > score_b)"""
        match = {
            "match_id": "M01",
            "team_a": "T1",
            "team_b": "GenG",
            "score_a": 2,
            "score_b": 1,
            "status": "Completed"
        }
        result = determine_winner(match)
        self.assertEqual(result, "T1")

    def test_team_b_wins(self):
        """Test trường hợp Đội B chiến thắng (score_b > score_a)"""
        match = {
            "match_id": "M03",
            "team_a": "G2",
            "team_b": "FNC",
            "score_a": 0,
            "score_b": 3,
            "status": "Completed"
        }
        result = determine_winner(match)
        self.assertEqual(result, "FNC")

    def test_match_draw(self):
        """Test trường hợp trận đấu kết thúc với kết quả Hòa (score_a == score_b)"""
        match = {
            "match_id": "M04",
            "team_a": "DK",
            "team_b": "DRX",
            "score_a": 1,
            "score_b": 1,
            "status": "Completed"
        }
        result = determine_winner(match)
        self.assertEqual(result, "Draw")

    def test_match_not_started(self):
        """Test trường hợp trận đấu chưa diễn ra (status == 'Pending')"""
        match = {
            "match_id": "M02",
            "team_a": "JDG",
            "team_b": "BLG",
            "score_a": 0,
            "score_b": 0,
            "status": "Pending"
        }
        result = determine_winner(match)
        self.assertEqual(result, "Not Started")

    def test_missing_key_handling(self):
        """Test khả năng phòng thủ dữ liệu lỗi khi thiếu các key bắt buộc"""
        invalid_match = {
            "match_id": "M05",
            "team_a": "TES",
            "team_b": "WBG",
            "status": "Completed"
            # Thiếu score_a và score_b
        }
        result = determine_winner(invalid_match)
        self.assertEqual(result, "Data Error")


if __name__ == "__main__":
    unittest.main()