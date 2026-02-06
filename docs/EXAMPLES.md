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
- Blank line before Wordle (multi-line puzzle)
- No blank lines between single-line puzzles (Framed, Quolture)

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
- No blank line added (only added *before* Wordle when there are previous puzzles)

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
- Single-line puzzles have no blank lines between them
- Blank line only before Wordle (the multi-line puzzle)

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

1. **Single-line puzzles** (Framed, Framed One Frame, Quolture):
   - No blank lines between them
   - Appear consecutively

2. **Multi-line puzzles** (Wordle, Connections, Strands):
   - Blank line added **before** each multi-line puzzle if there are previous puzzles
   - No blank line if the puzzle is first or only

### Ordering

Puzzles always appear in this order (defined in `config.json`):
1. Framed (regular)
2. Framed - One Frame Challenge
3. Quolture
4. [blank line if multi-line puzzle follows]
5. Wordle
6. [blank line if another multi-line puzzle follows]
7. Connections
8. [blank line if another multi-line puzzle follows]
9. Strands

**Missing puzzles are simply skipped** - the order is maintained for puzzles that are present.

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
