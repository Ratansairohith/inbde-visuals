# INBDE visuals: how to build daily cards

This repo hosts the images embedded in Sathvika's daily INBDE study emails. Everything here is public, so only generic study material goes in. Nothing personal.

## Layout
- `cards/dayNN/cards.html`: source for that day's cards (NN = two-digit day number, e.g. day07).
- `dayNN/*.png`: rendered images, embedded in the email.
- `scripts/render_cards.py`: renders every `.card` element (each needs a `data-name`) to `dayNN/<data-name>.png` at 2x.
- `scripts/draw_universal_tooth_chart.py`: matplotlib example for anatomical drawings.
- Use `cards/day01/cards.html` as the reference template for style and structure.

## Daily steps
1. Write `cards/dayNN/cards.html` using the design system below.
2. Run `python3 scripts/render_cards.py cards/dayNN/cards.html dayNN`.
3. Open every PNG with the Read tool and check it: nothing cut off, no overlapping text, colors correct, facts match the fact sheet. Fix and re-render if needed.
4. Commit and push to `main` (author "Ratan Sai Rohith Kokku" <ratan2513@gmail.com>).
5. Embed in the email with `<img src="https://raw.githubusercontent.com/Ratansairohith/inbde-visuals/main/dayNN/<name>.png" width="592" style="max-width:100%;height:auto;border-radius:14px" alt="...">`.

## Cards to make each day
- **Cheat sheet** (`cheatsheet`, 1000px wide): the whole topic on one saveable card, with title, a visual or diagram, key numbers, anchors, traps, and a source line.
- **Visual memory drawing(s)** (`drawing-1`, ...): a shape-based picture of the main structure, such as a loop, ladder, pyramid, flowchart, traffic light, timeline or Venn. Use HTML/CSS shapes, or matplotlib for anatomy-like drawings. Each gets a one-line caption on the card explaining the memory hook.
- **Flashcards** (`flashcard-1`..`flashcard-4`, 640px wide): question in serif, answer in a white box marked "ANSWER · cover this, then check", plus a one-line reason.
- Optional **mnemonic card** (`mnemonic`) when the fact sheet has a strong one.

## Design system
- Background cream #f7f5f0; white inner panels with 20px radius; card radius 28px.
- Fonts: Inter for body, DejaVu Serif for titles and flashcard questions. Emoji may not render, so avoid them on cards.
- Calm palette (accent / tint): sage #6b9080 / #e3efe8, dusty blue #5b7db1 / #e6eef8, lavender #8b7fb8 / #efecf7, sand #c9a46a / #f8f1e4, muted rose #c08497 / #f7e9ee; deep accent #2f5d62; ink #1f3a3a; text #374151; muted #8a8f8c.
- Never use bright red, neon or pure black. Use muted rose for warnings.
- Big, bold key facts; short phrases, not paragraphs; lots of white space.
- No em dash characters anywhere.
- Facts must come only from that day's research fact sheet.
