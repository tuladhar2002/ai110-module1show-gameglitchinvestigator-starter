# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game where the player picks a difficulty, gets a limited number of attempts to guess a secret number, and receives higher/lower hints after each guess. Score is based on how quickly you win.

- [x] **Bugs found:**
  1. Hints were backwards — "Go HIGHER" showed when the guess was too high, and vice versa.
  2. New Game button didn't fully reset — `status`, `score`, and `history` carried over from the old game, causing the game-over screen to immediately reappear.
  3. Attempts counter and history lagged by one interaction due to Streamlit's top-to-bottom render order.
  4. On every even-numbered attempt, the secret was cast to a string, causing lexicographic comparison and completely wrong outcomes (e.g. `"9" > "50"` is `True`).
  5. Changing difficulty mid-game didn't reset state, leaving the old secret and attempt count in place.

- [x] **Fixes applied:**
  1. Swapped hint messages in `check_guess` so "Too High" → "Go LOWER" and "Too Low" → "Go HIGHER".
  2. Added full state reset (`status`, `score`, `history`, `attempts`, `secret`) in the New Game handler.
  3. Used `st.empty()` as a placeholder for the attempts counter, filled after the submit logic runs so it always shows the current value.
  4. Removed the even/odd string-conversion entirely — `check_guess` now always compares int to int.
  5. Stored active difficulty in `session_state` and reset the full game state when it changes.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess 50, secret is 70 
2. Game returns "Guess Higher"
3. User enters a guess of 80
4. Game returns "Guess Lower"
5. User enters a guess of 70
6. Game ends after correct guess

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
=============================== test session starts ================================
platform darwin -- Python 3.12.4, pytest-7.4.4, pluggy-1.0.0 -- /opt/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/tuladhar2002/Documents/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.2.0
collected 37 items                                                                 

tests/test_game_logic.py::TestCheckGuess::test_exact_match_is_win PASSED     [  2%]
tests/test_game_logic.py::TestCheckGuess::test_win_returns_correct_message PASSED [  5%]
tests/test_game_logic.py::TestCheckGuess::test_guess_too_high PASSED         [  8%]
tests/test_game_logic.py::TestCheckGuess::test_too_high_message_says_lower PASSED [ 10%]
tests/test_game_logic.py::TestCheckGuess::test_guess_too_low PASSED          [ 13%]
tests/test_game_logic.py::TestCheckGuess::test_too_low_message_says_higher PASSED [ 16%]
tests/test_game_logic.py::TestCheckGuess::test_one_above_secret PASSED       [ 18%]
tests/test_game_logic.py::TestCheckGuess::test_one_below_secret PASSED       [ 21%]
tests/test_game_logic.py::TestCheckGuess::test_zero_equals_zero PASSED       [ 24%]
tests/test_game_logic.py::TestCheckGuess::test_negative_numbers PASSED       [ 27%]
tests/test_game_logic.py::TestCheckGuess::test_large_numbers PASSED          [ 29%]
tests/test_game_logic.py::TestCheckGuess::test_always_returns_two_values PASSED [ 32%]
tests/test_game_logic.py::TestParseGuess::test_valid_integer PASSED          [ 35%]
tests/test_game_logic.py::TestParseGuess::test_valid_zero PASSED             [ 37%]
tests/test_game_logic.py::TestParseGuess::test_valid_negative PASSED         [ 40%]
tests/test_game_logic.py::TestParseGuess::test_float_string_truncates PASSED [ 43%]
tests/test_game_logic.py::TestParseGuess::test_empty_string PASSED           [ 45%]
tests/test_game_logic.py::TestParseGuess::test_none_input PASSED             [ 48%]
tests/test_game_logic.py::TestParseGuess::test_alphabetic_input PASSED       [ 51%]
tests/test_game_logic.py::TestParseGuess::test_mixed_alphanumeric PASSED     [ 54%]
tests/test_game_logic.py::TestParseGuess::test_whitespace_only PASSED        [ 56%]
tests/test_game_logic.py::TestParseGuess::test_multiple_decimals PASSED      [ 59%]
tests/test_game_logic.py::TestParseGuess::test_always_returns_three_values PASSED [ 62%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_easy_range PASSED  [ 64%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_normal_range PASSED [ 67%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_hard_range PASSED  [ 70%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_unknown_difficulty_returns_default PASSED [ 72%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_low_is_always_less_than_high PASSED [ 75%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_always_returns_two_values PASSED [ 78%]
tests/test_game_logic.py::TestUpdateScore::test_win_early_gives_high_score PASSED [ 81%]
tests/test_game_logic.py::TestUpdateScore::test_win_late_gives_minimum_points PASSED [ 83%]
tests/test_game_logic.py::TestUpdateScore::test_win_floor_never_below_10_points PASSED [ 86%]
tests/test_game_logic.py::TestUpdateScore::test_too_high_deducts_score PASSED [ 89%]
tests/test_game_logic.py::TestUpdateScore::test_too_low_deducts_score PASSED [ 91%]
tests/test_game_logic.py::TestUpdateScore::test_unknown_outcome_no_change PASSED [ 94%]
tests/test_game_logic.py::TestUpdateScore::test_score_can_go_negative PASSED [ 97%]
tests/test_game_logic.py::TestUpdateScore::test_score_accumulates_across_calls PASSED [100%]

================================ 37 passed in 0.03s ================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
