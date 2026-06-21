# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python -m streamlit run app.py

# Run tests
pytest tests/
```

## Architecture

This is an educational Streamlit app — a deliberately broken number-guessing game. Students find bugs, fix them, refactor logic, and make tests pass.

**app.py** is the main Streamlit application (~192 lines). It owns all session state (`st.session_state`) for: `secret`, `attempts`, `score`, `status`, `history`. It also currently contains the full game logic inline.

**logic_utils.py** is the refactoring target. It defines four function stubs (raising `NotImplementedError`) that students are expected to implement by moving logic from `app.py`:
- `get_range_for_difficulty()` → returns `(low, high)` tuple
- `parse_guess()` → validates input, returns `(ok, guess_int, error)`
- `check_guess()` → compares guess to secret, returns `(outcome, message)`
- `update_score()` → computes score delta based on outcome and attempt count

**tests/test_game_logic.py** imports from `logic_utils` and tests `check_guess()` for win/too-high/too-low outcomes. Tests fail until stubs are implemented.

## Known Intentional Bugs

The app ships with several bugs for students to discover:

1. **Backwards hints** — hint logic shows "Go HIGHER" when the secret is lower and vice versa.
2. **Incomplete new-game reset** — the "New Game" button doesn't reset `attempts` back to 0.
3. **Off-by-one state lag** — attempts increment and history append fire on the *next* guess rather than the current one.
4. **Type inconsistency** — guess comparison alternates between string and int on even/odd attempt counts (around lines 158–161 in `app.py`).
