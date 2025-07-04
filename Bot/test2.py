response_stream = """
- **Bold text** (`**Bold text**`)
- *Italic text* (`*Italic text*`)
- Code blocks (`inline code` or ``` ` ``` for multi-line code)
- Lists (`- Item 1`, `1. Item 1`)
- Links (`[text](url)`)

If you want to convert Markdown to HTML for use in a `<div>`, you can either:

1. **Manually convert it** (e.g., replace `# Header` with `<h1>Header</h1>`).
2. Use a **Markdown-to-HTML converter** (many libraries/tools exist for this, like `marked.js` in JavaScript or Python's `markdown` library).

Let me know if you'd like an example of converting Markdown to HTML!"""
print(response_stream)