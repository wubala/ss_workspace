#!/usr/bin/python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys


def split_sections(body: str) -> list[tuple[str, str]]:
    lines = [line.rstrip() for line in body.strip().splitlines()]
    sections: list[tuple[str, str]] = []
    current_title = ''
    current_lines: list[str] = []

    pattern = re.compile(r'^\s*(\d+)[、.．]\s*(.+?)\s*$')

    for raw in lines:
        line = raw.strip()
        matched = pattern.match(line)
        if matched:
            if current_title:
                sections.append((current_title, '\n'.join(current_lines).strip() or '无'))
            current_title = f"{matched.group(1)}、{matched.group(2).strip()}"
            current_lines = []
        else:
            if current_title:
                current_lines.append(raw)
            elif line:
                sections.append((f"{len(sections)+1}、内容", line))

    if current_title:
        sections.append((current_title, '\n'.join(current_lines).strip() or '无'))

    if not sections and body.strip():
        parts = [p.strip() for p in re.split(r'\n{2,}', body.strip()) if p.strip()]
        if len(parts) <= 1:
            sections.append(('1、内容', body.strip()))
        else:
            for i, part in enumerate(parts, start=1):
                first_line = part.splitlines()[0].strip()
                short = first_line[:18] if first_line else '内容'
                sections.append((f'{i}、{short}', part))

    return sections


def build_entry(title: str, body: str, note_type: str, source: str) -> str:
    now = datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M')
    clean_body = body.strip()
    if not clean_body:
        raise SystemExit('正文不能为空')

    sections = split_sections(clean_body)
    content_blocks = []
    for heading, content in sections:
        content_blocks.append(f'### {heading}\n\n{content.strip() or "无"}\n')
    content_text = '\n'.join(content_blocks).rstrip()

    return (
        '\n---\n\n'
        f'# {title}\n\n'
        '## 基本信息\n\n'
        f'- 时间：{ts}\n'
        f'- 来源：{source}\n'
        f'- 类型：{note_type}\n\n'
        '## 内容\n\n'
        f'{content_text}\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description='追加一条 markdown 记录到固定归档文件')
    parser.add_argument('--title', default='', help='标题；若为空则使用当天日期')
    parser.add_argument('--type', default='指定内容记录', help='记录类型')
    parser.add_argument('--source', default='与珊珊的对话', help='记录来源')
    parser.add_argument('--file', default='archives/notesPr.md', help='目标文件路径')
    parser.add_argument('--body', default='', help='正文；若为空则从标准输入读取')
    args = parser.parse_args()

    body = args.body if args.body.strip() else sys.stdin.read()
    body = body.strip()
    if not body:
        raise SystemExit('没有可写入的内容')

    now = datetime.now()
    title = args.title.strip() or now.strftime('%Y-%m-%d')

    target = Path(args.file).expanduser()
    if not target.is_absolute():
        target = Path.cwd() / target
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text('', encoding='utf-8')

    entry = build_entry(title=title, body=body, note_type=args.type.strip() or '指定内容记录', source=args.source.strip() or '与珊珊的对话')
    with target.open('a', encoding='utf-8') as f:
        f.write(entry)

    print(str(target))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
