# Bug Report: Game Glitch Investigator

## Bug 1: Hints are backwards

**Location:** `app.py:38-40` inside `check_guess()`

**Root cause:** The outcome labels (`"Too High"` / `"Too Low"`) are correct, but the hint messages are swapped. When `guess > secret` (guess is too high), the player needs to go lower — but the message says "Go HIGHER!".

```python
# Current (wrong)
if guess > secret:
    return "Too High", "📈 Go HIGHER!"
else:
    return "Too Low", "📉 Go LOWER!"
```

**Fix:** Swap the messages so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!".

---

## Bug 2: New game doesn't fully reset state

**Location:** `app.py:134-138`

**Root cause:** The "New Game" button only resets `attempts` and `secret`. It leaves `status`, `score`, and `history` from the old game. The fatal one is `status` — because right after `st.rerun()`, lines 140–145 check:

```python
if st.session_state.status != "playing":
    ...
    st.stop()  # execution halts every time after a finished game
```

Since `status` is still `"won"` or `"lost"`, the app immediately stops and the new game never starts.

**Fix:** Also reset `status`, `score`, and `history` inside the `if new_game:` block.

---

## Bug 3: Attempts counter and history lag by one interaction

**Location:** `app.py:111`, `app.py:119`, `app.py:147-156`

**Root cause:** Streamlit re-runs the entire script top-to-bottom on every interaction. The "Attempts left" counter renders at line 111 and the history renders at line 119 — both *before* the `if submit:` block at line 147 executes. So:

1. Streamlit draws `st.info` with the old `attempts` value.
2. Then `st.session_state.attempts += 1` runs (line 148).
3. Then `st.session_state.history.append(...)` runs (line 156).

The incremented count and new history entry are saved to session state, but the UI elements that display them have already been drawn with stale values. Updates only appear on the next re-run.

**Fix:** Move the `st.session_state.attempts += 1` and `history.append()` calls to happen before rendering the counter and history display, or restructure to only display after the submit logic runs.

---

## Bug 4: Wrong hints on every even-numbered attempt

**Location:** `app.py:158-163`

**Root cause:** On even-numbered attempts, `secret` is cast to a string before being passed to `check_guess()`. Comparing `int > str` raises a `TypeError` in Python 3, which `check_guess` catches and falls back to lexicographic string comparison. String comparison is alphabetical, not numeric — so `"9" > "50"` evaluates to `True` because `'9' > '5'`. This produces completely wrong outcomes on those attempts (e.g., guessing `9` when the secret is `50` returns "Too High").

```python
# The type-switching logic (lines 158-161)
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)  # causes string comparison in check_guess
else:
    secret = st.session_state.secret
```

**Fix:** Remove the even/odd branching entirely and always pass `st.session_state.secret` as an integer to `check_guess()`.
