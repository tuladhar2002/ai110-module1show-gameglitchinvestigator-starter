# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - Typical Streamlit UI with emoji icons. The game loaded but was immediately unplayable — hints were wrong and the game state wouldn't reset properly.

- List at least two concrete bugs you noticed at the start:
  1. Hints were backwards — "Go HIGHER" appeared when the guess was too high.
  2. New Game button didn't reset the game — the game-over screen reappeared immediately.
  3. Attempts counter and history only updated on the next guess, not the current one.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret is 50 | "Go LOWER" hint | "Go HIGHER" hint | N/A |
| Guess 40, secret is 50 | "Go HIGHER" hint | "Go LOWER" hint | N/A |
| Click New Game after winning | Fresh game starts | Game-over screen reappears immediately | N/A |
| Submit a guess | Attempts left decrements on current guess | Decrements on the next guess | N/A |
| Guess 9, secret is 50 (even attempt) | "Too Low" / "Go HIGHER" | "Too High" due to string comparison | N/A |
| Switch difficulty mid-game | Game resets to new range | Old secret and attempts carry over | N/A |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
=> Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

=> AI suggested an erro on even numbered guess. On even-numbered attempts, `secret` is cast to a string before being passed to `check_guess()`. Comparing `int > str` raises a `TypeError` in Python 3, which `check_guess` catches and falls back to lexicographic string comparison. String comparison is alphabetical, not numeric — so `"9" > "50"` evaluates to `True` because `'9' > '5'`. This produces completely wrong outcomes on those attempts (e.g., guessing `9` when the secret is `50` returns "Too High").

Validated it by trying it out and it was showing wrong Guess outputs. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

=> Didnt really halucinate that much for me. I pointed out some issues and it provided some mor eissues to me, which was right. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
=> Manually tested them. Also, later wrote testst for criticla functions making sure all edge cases are covered.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
=> I ran a test to ensure the guess hint works as expected. As that was the biggest flaw I expereinced, wrote a test: test_guess_too_high ensuring the logic returns if the guess was higher than secret value.

- Did AI help you design or understand any tests? How?
=> Yes, it went through the details and core logic flaws for me, so finding bugs and edge cases were much easier. Then based on the bugs, I instructed it to write the tests covering exact bugs and other edge cases as well. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
=> Since its an SPA (Single Page Application), its basically a big single file project that runs from top to bottom every run/state. So, making sure to reset the states and reload the applications is very critical and ofcourse handling the logics in a decoupled way.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
=> Definetely TDD

- What is one thing you would do differently next time you work with AI on a coding task?
=> make the agent familiar with the codebase before starting to throw questions at it. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
=> Buggy but a diamond, if in the hands of a skillfull person. 
