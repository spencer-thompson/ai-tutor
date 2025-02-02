<script lang="ts">
	import { marked } from 'marked';
</script>

<div>
	{@html marked.parse(
		"Of course, Joshua! Here are some regular emojis for you:\n\n- \ud83d\ude0a\n- \ud83d\udc4d\n- \u2728\n- \u2764\ufe0f\n- \ud83d\udcda\n\nI hope you like them! If you need anything else, just let me know! \ud83d\ude0aAbsolutely! Here's a basic example of Markdown to get you started:\n\nmarkdown\n# Heading 1\n\n## Heading 2\n\n### Heading 3\n\n**Bold Text**\n\n*Italic Text*\n\n- Bullet Point 1\n- Bullet Point 2\n - Nested Bullet Point\n\n1. Numbered List Item 1\n2. Numbered List Item 2\n\n[Link to UVU](https://www.uvu.edu)\n\n![Image Alt Text](https://www.uvu.edu/logo.png)\n\n> Blockquote\n\n`Inline code hi `\n\n\nCode block\n\n\n\nFeel free to ask if you have any more questions or need further assistance! \ud83d\ude0a"
	)}
	<pre>The quick brown fox jumps over the lazy dog.</pre>
	Press<kbd>⌘ + C</kbd> to copy.
	<del><s>Always</s> Gonna Give You Up</del>
	<ins cite="https://youtu.be/dQw4w9WgXcQ" datetime="10-31-2022"> Never Gonna Give You Up </ins>

	{@html marked(
		`${"\ud83d\ude04 Sure! Here's a simple example of markdown text:\n\nmarkdown\n# Welcome to Utah Valley University!\n\nUtah Valley University (UVU) is a public university located in **Orem, Utah**. It's an exciting place to learn, grow, and achieve your academic goals.\n\n## Why Choose UVU?\n\n- **Diverse Programs**: UVU offers a wide range of programs to suit your interests, from arts to sciences.\n- **Flexible Learning**: With both in-person and online classes, you can learn on your terms.\n- **Supportive Community**: UVU provides excellent resources to support students' success.\n\n## How to Apply\n\n1. Visit the [UVU Admissions](https://www.uvu.edu/admissions) page.\n2. Submit your application online.\n3. Send your transcripts and test scores.\n4. Await your acceptance letter!\n\n## Contact Us\n\nFor more information, feel free to reach out:\n\n- **Email**: info@uvu.edu\n- **Phone**: (801) 863-INFO\n\nJoin us at UVU, where your future begins!\n\n---\n\n> \Education is the most powerful weapon which you can use to change the world.\ \u2013 Nelson Mandela\n\n\nFeel free to use and modify this markdown to suit your needs! \ud83d\ude0a \ud83c\udf1f"}`
	)}
</div>
