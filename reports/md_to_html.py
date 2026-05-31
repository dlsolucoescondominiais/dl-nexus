import re

def md_to_html(md_text):
    # Basic markdown to HTML conversion
    html = md_text
    # Headers
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # Code blocks/inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    # Lists
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    # Wrap lists
    html = re.sub(r'(<li>.*?</li>\n)+', lambda m: "<ul>\n" + m.group(0) + "</ul>\n", html)

    # Tables (very basic)
    lines = html.split('\n')
    in_table = False
    new_lines = []
    for line in lines:
        if line.startswith('|') and not line.startswith('|-'):
            if not in_table:
                new_lines.append('<table border="1" cellpadding="5" style="border-collapse: collapse;">')
                in_table = True
            cells = [c.strip() for c in line.split('|')[1:-1]]
            new_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        elif line.startswith('|-'):
            continue
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            new_lines.append(line)

    if in_table:
        new_lines.append('</table>')

    html = '\n'.join(new_lines)

    # Paragraphs (basic)
    html = html.replace('\n\n', '<br><br>')

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>N8N Status Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
table {{ margin-top: 20px; margin-bottom: 20px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f2f2f2; }}
h1, h2 {{ color: #333; }}
code {{ background-color: #f9f2f4; padding: 2px 4px; border-radius: 4px; color: #c7254e; }}
</style>
</head>
<body>
{html}
</body>
</html>"""

with open('reports/n8n_status_report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = md_to_html(md_content)

with open('reports/n8n_status_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML generated at reports/n8n_status_report.html")
