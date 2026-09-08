#!/usr/bin/env python3
"""Compare a verbose source payload with a packetised payload.

Token counts are reported only when tiktoken is available. Character and word
counts are always shown and are explicitly proxies rather than token counts.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def count_basic(text: str) -> dict[str, int]:
    return {
        "bytes": len(text.encode("utf-8")),
        "characters": len(text),
        "words_proxy": len(text.split()),
        "lines": len(text.splitlines()),
    }


def token_count(text: str, encoding_name: str) -> int | None:
    try:
        import tiktoken  # type: ignore
    except ImportError:
        return None
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def reduction(before: int, after: int) -> str:
    if before == 0:
        return "n/a"
    return f"{(before - after) / before * 100:.1f}%"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare source and SP/1 payload sizes")
    parser.add_argument("source", type=Path)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--encoding", default="o200k_base", help="tiktoken encoding name")
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    packet = args.packet.read_text(encoding="utf-8")

    src = count_basic(source)
    pkt = count_basic(packet)

    print("metric\tsource\tpacket\treduction")
    for key in src:
        print(f"{key}\t{src[key]}\t{pkt[key]}\t{reduction(src[key], pkt[key])}")

    src_tokens = token_count(source, args.encoding)
    pkt_tokens = token_count(packet, args.encoding)
    if src_tokens is None or pkt_tokens is None:
        print("tokens\tunavailable\tunavailable\tn/a")
        print("note\ttiktoken not installed; character and word counts are proxies only")
    else:
        print(f"tokens[{args.encoding}]\t{src_tokens}\t{pkt_tokens}\t{reduction(src_tokens, pkt_tokens)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
