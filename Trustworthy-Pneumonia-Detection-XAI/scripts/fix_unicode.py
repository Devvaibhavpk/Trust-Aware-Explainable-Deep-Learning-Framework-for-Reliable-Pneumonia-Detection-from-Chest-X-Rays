import re

with open('scripts/build_handbook.py', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('\u2014', '--'),
    ('\u2013', '-'),
    ('\u2019', "'"),
    ('\u2018', "'"),
    ('\u201c', '"'),
    ('\u201d', '"'),
    ('\u00b7', '.'),
    ('\u2248', '~'),
    ('\u2265', '>='),
    ('\u2264', '<='),
    ('\u00d7', 'x'),
    ('\u2192', '->'),
    ('\u2212', '-'),
    ('\u221e', 'inf'),
]
for uni, asc in replacements:
    content = content.replace(uni, asc)

with open('scripts/build_handbook.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed.')
