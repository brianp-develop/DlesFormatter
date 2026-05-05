# Puzzle Examples

Complete input/output examples for all supported puzzles.

## Framed

### Input
```
Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf
```

### Output
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
```

### Formatting Rules
- Collapse to single line
- Title directly followed by emoji grid (no space between title and first emoji)
- Remove URL
- Remove blank lines

---

## Framed - One Frame Challenge

### Input
```
Framed - One Frame Challenge #1427
🎥 🟥

https://framed.wtf
```

### Output
```
Framed - One Frame Challenge #1427🎥 🟥
```

### Formatting Rules
- Same as regular Framed
- Collapse to single line
- Title directly followed by emoji grid
- Remove URL

---

## Quolture

### Input
```
"Quolture"  1447  ⭐️3

🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣

https://www.quolture.com
```

### Output
```
"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣
```

### Formatting Rules
- Collapse all lines to single line
- Join with single space separator
- Preserves original spacing within each line (e.g., double space in title)
- Remove URL and blank lines

---

## Wordle

### Input
```
Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

### Output
```
Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

### Formatting Rules
- Keep multi-line structure
- Title on first line
- Grid lines preserve their structure (one line per guess)
- Remove blank line that appears after title in original input
- No URL

---

## Connections

### Input
```
Connections
Puzzle #970
🟦🟦🟦🟦
🟪🟪🟪🟪
🟩🟩🟩🟩
🟨🟨🟨🟨
```

### Output
```
Connections #970
🟦🟦🟦🟦
🟪🟪🟪🟪
🟩🟩🟩🟩
🟨🟨🟨🟨
```

### Formatting Rules
- Keep multi-line structure
- Combine "Connections" and "Puzzle #N" into single title line "Connections #N"
- Grid lines preserve their structure (one line per category)
- No URL (Connections doesn't include one)
- Multi-line output (like Wordle)

---

## Strands

### Input
```
Strands #705
"Let's face it"
🟡🔵🔵🔵
🔵🔵🔵🔵
```

### Output
```
Strands #705
"Let's face it"
🟡🔵🔵🔵🔵🔵🔵🔵
```

### Formatting Rules
- Keep multi-line structure (3 lines total)
- Title on first line
- Theme (in quotes) on second line
- Collapse all emoji rows to single line on third line
- Always has 7 blue dots (🔵) + 1 yellow dot (🟡)
- May include hint bulbs (💡) which are preserved
- No URL (Strands doesn't include one)
- Multi-line output (like Wordle and Connections)

---

## Waffle

### Input
```
#waffle1477 1/5



🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩⭐🟩🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩



🔥 streak: 2

wafflegame.net
```

### Output
```
#waffle1477 1/5
🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩⭐🟩🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩
🔥 streak: 2
```

### Formatting Rules
- Preserve title line: `#waffleXXXX X/5`
- Preserve 5x5 emoji grid (5 lines)
- Preserve streak information if present
- Remove URL (`wafflegame.net`)
- Remove all blank lines
- Multi-line output with blank line separator before it
- Positioned last (after Pips)

---

## Pips

Pips is a 3-part puzzle. Each difficulty level (Easy 🟢, Medium 🟡, Hard 🔴) is captured separately, but all captured Pips are combined into a single output line.

### Input (3 separate clipboard captures)

**Easy:**
```
Pips #173 Easy 🟢
1:25
```

**Medium:**
```
Pips #171 Medium 🟡
5:52
```

**Hard:**
```
Pips #171 Hard 🔴
35:28
```

### Output (combined)
```
Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28
```

### Formatting Rules
- Each difficulty is captured separately (press Enter after copying each)
- All captured Pips puzzles are combined into single line
- Format: `Pips #XXX [Difficulty] [Emoji] [Time] | [Difficulty] [Emoji] [Time] | ...`
- Separator between difficulties: ` | `
- User may complete only 1, 2, or all 3 difficulties (all are combined)
- Single-line output

---

## Mixed Input Examples

### Example 1: All Puzzles in Wrong Order

#### Input
```
Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩

"Quolture"  1447  ⭐️3

🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣

https://www.quolture.com

Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf
```

#### Output
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣

Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Notes
- Puzzles automatically reordered to: Framed → Quolture → Wordle
- The blank line before Wordle comes from a `"---"` marker in `config.json.example`'s `puzzle_order` between `quolture` and `wordle`. Remove the marker if you want them flush.

---

### Example 2: Only Some Puzzles

#### Input
```
Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf

Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Output
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥

Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Notes
- Missing Quolture and Framed One Frame (no problem!)
- Only formats puzzles that are present
- Still follows ordering rules (Framed before Wordle)

---

### Example 3: Just Wordle

#### Input
```
Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Output
```
Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Notes
- Single puzzle works perfectly
- The leading marker (if any) before this puzzle is a no-op when there's no prior output

---

### Example 4: All Four Puzzles

#### Input
```
Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf

Framed - One Frame Challenge #1427
🎥 🟥

https://framed.wtf

"Quolture"  1447  ⭐️3

🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣

https://www.quolture.com

Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Output
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
Framed - One Frame Challenge #1427🎥 🟥
"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣

Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

#### Notes
- All four puzzles present
- Ordering: Framed → Framed One Frame → Quolture → [blank line] → Wordle
- The blank line before Wordle comes from the `"---"` marker between `quolture` and `wordle` in `config.json.example`. Add or remove markers in `config.json` to change spacing.

---

## Edge Cases

### Puzzle with Extra Blank Lines

#### Input
```
Framed #1427


🎥 🟥 🟥 🟥 🟥 🟥 🟥


https://framed.wtf
```

#### Output
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
```

#### Notes
- Extra blank lines automatically removed
- Parser strips whitespace and filters empty lines

---

### Puzzle with Unusual Spacing

#### Input
```
"Quolture"  1447  ⭐️3
🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣
https://www.quolture.com
```

#### Output
```
"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣
```

#### Notes
- Missing blank lines in input (no problem)
- Still parses correctly
- Original spacing within lines preserved

---

## Understanding the Output Format

### Spacing Rules

Blank lines between puzzles are fully driven by `"---"` marker entries in `config.json`'s `puzzle_order`. There is no implicit "single vs multi-line" rule.

- A `"---"` between two puzzle names inserts a blank line before the second
- Multiple consecutive `"---"` collapse to one blank line
- A `"---"` at the start or end of the array (or before a puzzle that isn't present in the input) is a no-op
- No marker = puzzles emit back-to-back

### Ordering

Puzzles appear in the order defined in `config.json` (or `config.json.example` if you haven't customized — see the [Configuration section in README.md](../README.md#configuration)). The recommended layout looks roughly like:

1. Framed (regular)
2. Framed - One Frame Challenge
3. Framed - Title Shot Challenge
4. Quolture
5. *(blank line marker)*
6. Wordle
7. *(blank line marker)*
8. Connections
9. *(blank line marker)*
10. Strands
11. *(blank line marker)*
12. Pips (combined into single line)
13. *(blank line marker)*
14. Waffle
15. *(blank line marker)*
16. Numble
17. *(blank line marker)*
18. Word Bunny

**Missing puzzles are simply skipped** — markers tied to absent puzzles also drop out, so the spacing remains clean.

Without a `config.json`, puzzles appear in detection order (the order you pasted them) with no blank lines.

### URL Removal

All `https://...` lines are automatically removed from output.

### Title Formatting

- **Framed/Framed One Frame**: Title directly followed by grid (no space)
  - Example: `Framed #1427🎥 🟥 🟥`
- **Quolture**: Title and grid joined with spaces
  - Example: `"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣`
- **Wordle**: Title on separate line, grid below
  ```
  Wordle 1,692 4/6
  🟩⬛🟩⬛⬛
  ```
- **Connections**: Title on separate line, grid below
  ```
  Connections #970
  🟦🟦🟦🟦
  ```
- **Strands**: Title and theme on separate lines, collapsed emoji grid below
  ```
  Strands #705
  "Let's face it"
  🟡🔵🔵🔵🔵🔵🔵🔵
  ```
- **Waffle**: Title on first line, 5x5 grid below, optional streak at end
  ```
  #waffle1477 1/5
  🟩🟩🟩🟩🟩
  🟩⬜🟩⬜🟩
  🟩🟩⭐🟩🟩
  🟩⬜🟩⬜🟩
  🟩🟩🟩🟩🟩
  🔥 streak: 2
  ```
