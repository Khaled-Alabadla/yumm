"""Convert index.html data-i18n attributes to Django {% trans %} tags."""

import re
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "templates" / "index.html"
text = INDEX.read_text(encoding="utf-8")

if "{% load i18n %}" not in text:
    text = text.replace("{% load static %}", "{% load static i18n %}", 1)

text = text.replace(
    "{% block title %}Yumm — Discover the Best Restaurants in Palestine{% endblock %}",
    '{% block title %}Yumm — {% trans "Discover the Best Restaurants in Palestine" %}{% endblock %}',
)

# Inline tags: <tag ... data-i18n="key">TEXT</tag>
inline = re.compile(
    r'(<(?:span|button|a|h2|h3|p|li|option)\b[^>]*)\sdata-i18n="[^"]+"([^>]*>)'
    r'([^<]+?)'
    r'(</(?:span|button|a|h2|h3|p|li|option)>)',
    re.DOTALL,
)
while inline.search(text):
    def _inline_sub(m):
        inner = m.group(3).strip().replace('"', '\\"')
        return (
            f'{m.group(1)}{m.group(2)}'
            f'{{% trans "{inner}" %}}'
            f'{m.group(4)}'
        )
    text = inline.sub(_inline_sub, text, count=1)

# Block tags where text is on next lines
block = re.compile(
    r'(<(?:p|h2|a)\b[^>]*)\sdata-i18n="[^"]+"([^>]*>)\s*\n\s*([^<\n][^\n]*?)\s*\n',
)
while block.search(text):
    def _block_sub(m):
        inner = m.group(3).strip().replace('"', '\\"')
        return f'{m.group(1)}{m.group(2)}\n      {{% trans "{inner}" %}}\n'
    text = block.sub(_block_sub, text, count=1)

# Input placeholder
text = re.sub(
    r'data-i18n="hero-search-ph"\splaceholder="([^"]+)"',
    lambda m: f'placeholder="{{% trans \\"{m.group(1)}\\" %}}"',
    text,
)

# Remaining data-i18n on self-closing or empty elements
text = re.sub(r'\sdata-i18n="[^"]+"', "", text)
text = text.replace("data--i18n", "")

INDEX.write_text(text, encoding="utf-8")
print("Converted", INDEX)
