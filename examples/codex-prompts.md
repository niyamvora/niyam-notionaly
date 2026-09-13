# Codex Prompts

Copy any of these straight into Codex. They assume `./install.sh` has been run.

Three skills are installed. Name the right one and Codex does the rest:

| Skill | For |
|---|---|
| `$niyam-notionaly-illustrations` | one asset — illustration, character, icon, spot |
| `$niyam-notionaly-article` | a whole article — shot list, then a set of body illustrations |
| `$niyam-notionaly-infographic` | a poster, slide or social card — real HTML with real type |

---

## Plan only — no images yet

```text
Use $niyam-notionaly-article. Do not generate anything yet.
Work out which passages of the article below actually deserve an illustration, and give me
a shot list of about five. For each one:
- which paragraph it sits after
- the idea, in one sentence with no "and"
- the structure
- what the figure is physically doing
- the one or two props
- the caption that will sit under it

<paste the article>
```

## Illustrate the article

```text
Use $niyam-notionaly-article to draw four body illustrations for the article below.
Monochrome, 16:9, solid white ground, no text of any kind inside the images.
Lock one character and keep them identical across all four. One idea per image.
Save them to examples/articles/<slug>/ with the shot list.

<paste the article>
```

## Long piece — strategy first

```text
Use $niyam-notionaly-article. This is a long piece, so do not space the images evenly.
Pick only the cognitive anchors: the central claim, a split, a loop, a before-and-after,
a common trap, the change of state at the end. Six to eight.
Shot list first, no images until I say so.

<paste the article>
```

## One idea, one image

```text
Use $niyam-notionaly-article to draw a single 16:9 body illustration for this claim:

Trust isn't announced. It gets laid down one piece of evidence at a time.

Translate it into a person doing an ordinary physical thing. No lettering in the image,
no arrows with labels, no diagram. Run the removal test before you commit: if the idea
still reads with the person deleted, start again.
```

## A single asset, not a set

```text
Use $niyam-notionaly-illustrations to draw a person carrying a stack of books. PNG.
Use $niyam-notionaly-illustrations — 6 icons: book, calendar, inbox, plant, coffee, checklist. SVG.
Use $niyam-notionaly-illustrations to redraw the attached photo in this style. Keep it recognisable.
```

## Fix: text got into the image

```text
Use $niyam-notionaly-illustrations to edit this image.
Remove every piece of text, lettering and labelling, including anything in the corners,
and fill those areas with clean white to match the surrounding paper.
Change nothing else — same figure, props, line weight, ink, accent marks and aspect ratio.
```

## Fix: the figure is just standing there

```text
Use $niyam-notionaly-article. The idea in this image is right, but the person is decoration —
they are standing next to the point instead of making it.
Same meaning, same sparse layout, but have them physically perform the action.
Keep the character, the ink and the empty margins exactly as they are.
```

## Fix: it came back as a diagram

```text
Use $niyam-notionaly-article. This reads as a flow chart, not an illustration.
Strip the boxes, the connector arrows and the grid. One person, one physical action,
one or two ordinary props, large empty margins.
```

## A style sample set

```text
Use $niyam-notionaly-article to draw five body illustrations on five different ideas:
information overload, validating a product, compounding effort, working alone, earning trust.
Same character throughout. Different prop and different action in every single one.
Generate each separately — never tile them onto one canvas.
```

## Compose a page instead

```text
Use $niyam-notionaly-infographic to build a poster from examples/japan-buffers.md
Use $niyam-notionaly-infographic — 16:9 slide, monochrome, one illustration, export PNG at 2x
```

---

## 中文文章配图

技能默认就支持中文文章。规则不变：**文字一律放在图外，用真实排版**；提示词本身仍用英文
（风格规范是按英文测量和书写的，图像模型照做更稳），配文用中文。

```text
Use $niyam-notionaly-article 先不要生图。
请分析下面这篇文章哪里值得配图，输出 5 张左右的 shot list。每张写清楚：
放在哪个段落后 / 核心意思（一句话，不要用"和"）/ 结构类型 / 人物在做什么 / 物件 / 中文配文

<粘贴文章>
```

```text
Use $niyam-notionaly-article 为下面这篇文章生成 4 张正文配图。
16:9 横版、纯白背景、单色手绘、图里不要出现任何文字。
中文配文写在图外面。四张图用同一个人物，不要中途换发型或换衣服。

<粘贴文章>
```

```text
Use $niyam-notionaly-article 为这个观点生成一张 16:9 正文配图：

真正拖慢进度的不是做事，是交接。

把抽象概念换成一个普通人的具体动作，用一两个普通物件。
不要画流程图，不要在图上写字，不要用箭头加标注。
```

**注意**：本项目不是红橙蓝手写批注风格。只有一种墨色 `#231F20`，没有第二种颜色，
图内没有任何文字。要那种风格请去看
[Ian Xiaohei Illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations)。
