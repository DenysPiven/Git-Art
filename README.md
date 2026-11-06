# Git Art

Personal repository for customizing my [GitHub contribution graph](https://github.com/DenysPiven).

Inspired by [GitArt](https://gitart.pages.dev/) — a tool that generates backdated commits to paint patterns on the contribution calendar.

## What's here

| File | Description |
|------|-------------|
| `foobar.txt` | Log of generated commit entries |
| `generate_noise.py` | Script to fill missing days with 1–5 commits each (skips 2024) |

## Usage

```bash
pip install tqdm
python3 generate_noise.py
```

The script appends a line to `foobar.txt` on every commit and backdates it to the target day. Year 2024 is left untouched.

## Note

This repo exists solely to maintain contribution graph activity. There is no application code here.
