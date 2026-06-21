import pytest
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_exact_match_is_win(self):
        outcome, _ = check_guess(50, 50)
        assert outcome == "Win"

    def test_win_returns_correct_message(self):
        _, message = check_guess(50, 50)
        assert "Correct" in message

    def test_guess_too_high(self):
        outcome, _ = check_guess(60, 50)
        assert outcome == "Too High"

    def test_too_high_message_says_lower(self):
        _, message = check_guess(60, 50)
        assert "LOWER" in message

    def test_guess_too_low(self):
        outcome, _ = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_too_low_message_says_higher(self):
        _, message = check_guess(40, 50)
        assert "HIGHER" in message

    def test_one_above_secret(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_one_below_secret(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"

    def test_zero_equals_zero(self):
        outcome, _ = check_guess(0, 0)
        assert outcome == "Win"

    def test_negative_numbers(self):
        outcome, _ = check_guess(-5, -10)
        assert outcome == "Too High"

    def test_large_numbers(self):
        outcome, _ = check_guess(999999, 1000000)
        assert outcome == "Too Low"

    def test_always_returns_two_values(self):
        result = check_guess(10, 20)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_valid_integer(self):
        ok, value, err = parse_guess("42")
        assert ok is True
        assert value == 42
        assert err is None

    def test_valid_zero(self):
        ok, value, err = parse_guess("0")
        assert ok is True
        assert value == 0

    def test_valid_negative(self):
        ok, value, err = parse_guess("-3")
        assert ok is True
        assert value == -3

    def test_float_string_truncates(self):
        ok, value, err = parse_guess("3.9")
        assert ok is True
        assert value == 3

    def test_empty_string(self):
        ok, value, err = parse_guess("")
        assert ok is False
        assert value is None
        assert err is not None

    def test_none_input(self):
        ok, value, err = parse_guess(None)
        assert ok is False
        assert value is None
        assert err is not None

    def test_alphabetic_input(self):
        ok, value, err = parse_guess("abc")
        assert ok is False
        assert value is None
        assert err is not None

    def test_mixed_alphanumeric(self):
        ok, value, err = parse_guess("12abc")
        assert ok is False
        assert value is None

    def test_whitespace_only(self):
        ok, value, err = parse_guess("   ")
        assert ok is False
        assert value is None

    def test_multiple_decimals(self):
        ok, value, err = parse_guess("1.2.3")
        assert ok is False
        assert value is None

    def test_always_returns_three_values(self):
        result = parse_guess("5")
        assert len(result) == 3


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_normal_range(self):
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_hard_range(self):
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50

    def test_unknown_difficulty_returns_default(self):
        low, high = get_range_for_difficulty("Extreme")
        assert low == 1
        assert high == 100

    def test_low_is_always_less_than_high(self):
        for difficulty in ["Easy", "Normal", "Hard"]:
            low, high = get_range_for_difficulty(difficulty)
            assert low < high

    def test_always_returns_two_values(self):
        result = get_range_for_difficulty("Normal")
        assert len(result) == 2


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    def test_win_early_gives_high_score(self):
        new_score = update_score(0, "Win", 1)
        assert new_score == 90  # max(10, 100 - 10*1)

    def test_win_late_gives_minimum_points(self):
        new_score = update_score(0, "Win", 10)
        assert new_score == 10  # max(10, 100 - 100) = 10

    def test_win_floor_never_below_10_points(self):
        new_score = update_score(0, "Win", 50)
        assert new_score >= 10

    def test_too_high_deducts_score(self):
        new_score = update_score(100, "Too High", 1)
        assert new_score == 95

    def test_too_low_deducts_score(self):
        new_score = update_score(100, "Too Low", 1)
        assert new_score == 95

    def test_unknown_outcome_no_change(self):
        new_score = update_score(50, "Draw", 1)
        assert new_score == 50

    def test_score_can_go_negative(self):
        new_score = update_score(0, "Too High", 1)
        assert new_score == -5

    def test_score_accumulates_across_calls(self):
        score = update_score(0, "Too High", 1)   # -5
        score = update_score(score, "Too Low", 2)  # -10
        score = update_score(score, "Win", 3)      # -10 + max(10, 70) = 60
        assert score == 60
