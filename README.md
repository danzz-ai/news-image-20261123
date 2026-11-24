# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/danzz-ai/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/danzz-ai/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026: Nvidia's board unanimously reinstating Jensen Huang as chief executive 11 days after he resigned, with shares jumping about 30%; NATO sending early-warning aircraft to Poland after Russian missiles landed there; the EU unveiling its 22nd package of sanctions against Russia; the US Treasury sanctioning more than two dozen Iranian entities tied to shadow banking; the US blacklisting Singapore AI firm Megaspeed over alleged AI-chip diversion to China; the NHS launching the world's largest AI breast screening trial; and explosive drones hitting a police base in Cúcuta, Colombia — plus the day's other big stories in the ticker below.

## The image

A newspaper front page, dated **MONDAY, 23 NOVEMBER 2026 — THE WORLD TODAY**. The hero panel shows Nvidia reinstating Jensen Huang as CEO. Below it, six panels: NATO's response in Poland, the EU's 22nd Russia sanctions, the US Treasury's Iran sanctions, the Megaspeed blacklist, the NHS AI screening trial, and the Cúcuta drone attack. The "ALSO TODAY" strip covers Russia ruling out a new Black Sea grain deal, Zelensky warning of new Russian strikes, the Riemann proof clearing machine checks, Tajikistan quitting the ICC, and Trump limiting Congress's data demands. Every story was reported on 23 November 2026.

The image was drawn with `render_front_page.py` (Python + Pillow) so every headline and the date are crisp and legible — no garbled text.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`. The output is a JPEG (1024×1024, well under 1 MiB), inside the gate limits (≤ 1 MiB, ≤ 1024×1024). Running it twice produces byte-identical output: it is a plain file copy with a size check.

---

<sub>Entered on [make.fun](https://make.fun/?ref=magsnez0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
