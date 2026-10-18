---
title: Figure and video
description: figure and video.
---

`figure` is media with a caption and credit. `video` is a leaf directive that takes no body.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| figure `src` | path or URL | none |
| figure `alt` | any text | empty |
| figure `caption` | any text | none |
| figure `credit` | any text | none |
| video `src` | path or URL (required) |  |
| video `title` | any text | none |
| video `poster` | path or URL | none |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Figure with everything

:::example
```markus
:::figure{src="assets/pipeline.svg" alt="Markus processing pipeline" caption="Source becomes a directive AST, then semantic HTML." credit="Anthus AI"}
:::
```
:::

### Caption only

:::example
```markus
:::figure{src="assets/pipeline.svg" alt="Markus processing pipeline" caption="Only a caption."}
:::
```
:::

### Credit only

:::example
```markus
:::figure{src="assets/pipeline.svg" alt="Markus processing pipeline" credit="Photo: Anthus AI"}
:::
```
:::

### No caption

:::example
```markus
:::figure{src="assets/pipeline.svg" alt="Markus processing pipeline"}
:::
```
:::

### Body instead of src

With no `src`, the body is the content and the caption still applies.

:::example
````markus
:::figure{caption="Any Markdown can be the figure content."}
```text
source -> AST -> HTML
```
:::
````
:::

## Video

### Video

The site ships no video file, so this uses the pipeline image as a stand-in source: the player shows controls but nothing plays. It demonstrates the markup.

:::example
```markus
::video{src="assets/pipeline.svg" title="Walkthrough"}
```
:::

### Video with poster

:::example
```markus
::video{src="assets/pipeline.svg" title="Walkthrough" poster="assets/pipeline.svg"}
```
:::

### Video, src only

:::example
```markus
::video{src="assets/pipeline.svg"}
```
:::
