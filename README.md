# PASS CHECKER

A simple Python dashboard that exposes the massive gap between **human habits** and **true machine randomness**. 

Traditional websites flag your password as "strong" if it merely hits a basic checklist (like 8 characters, a number, and a symbol). Because of this rule, humans instinctively create predictable shortcuts to save memory (like typing `Password123!`). 

Hackers exploit these exact muscle-memory patterns first. This app intercepts those lazy typing habits in real time and generates a mathematically perfect, secure alternative on the fly.



## What This Tool Does

1. Calculates the exact "Bits of Entropy" to show how many trillions of combinations a computer would have to guess before breaking your password.
2. Checks what you type against common keyboard shortcuts (like `123`, `qwerty`, or `pass`) and flags those predictable risks instantly.
3. Uses Python's secure `secrets` library to completely eliminate human bias, spawning truly random, high-entropy machine passwords on demand.


## Setup & Launch
```bash
pip install streamlit
streamlit run app.py
