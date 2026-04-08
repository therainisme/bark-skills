#!/usr/bin/env python3
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


def parse_kv(items):
    result = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --param value: {item!r}. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit(f"Invalid --param value: {item!r}. Key cannot be empty.")
        result[key] = value
    return result


def build_get_url(base_url, device_key, title=None, subtitle=None, body=None, query=None):
    parts = [device_key]
    for item in (title, subtitle, body):
        if item is not None:
            parts.append(quote(item, safe=""))
    url = base_url.rstrip("/") + "/" + "/".join(parts)
    if query:
        url += "?" + urlencode(query)
    return url


def main():
    parser = argparse.ArgumentParser(description="Send Bark notifications with Python stdlib.")
    parser.add_argument("device_key", help="Bark device key")
    parser.add_argument("--base-url", default="https://api.day.app")
    parser.add_argument("--title")
    parser.add_argument("--subtitle")
    parser.add_argument("--body")
    parser.add_argument("--url", dest="jump_url")
    parser.add_argument("--group")
    parser.add_argument("--icon")
    parser.add_argument("--image")
    parser.add_argument("--sound")
    parser.add_argument("--call", type=int, choices=[0, 1])
    parser.add_argument("--ciphertext")
    parser.add_argument("--level", choices=["active", "timeSensitive", "passive", "critical"])
    parser.add_argument("--volume")
    parser.add_argument("--is-archive", type=int, choices=[0, 1])
    parser.add_argument("--copy")
    parser.add_argument("--automatically-copy", type=int, choices=[0, 1])
    parser.add_argument("--badge")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-get-url", action="store_true")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Append any extra Bark parameter. Can be used multiple times.",
    )
    args = parser.parse_args()

    payload = parse_kv(args.param)

    option_map = {
        "title": args.title,
        "subtitle": args.subtitle,
        "body": args.body,
        "url": args.jump_url,
        "group": args.group,
        "icon": args.icon,
        "image": args.image,
        "sound": args.sound,
        "ciphertext": args.ciphertext,
        "level": args.level,
        "volume": args.volume,
        "copy": args.copy,
        "badge": args.badge,
    }
    for key, value in option_map.items():
        if value is not None:
            payload[key] = str(value)

    if args.call is not None:
        payload["call"] = str(args.call)
    if args.is_archive is not None:
        payload["isArchive"] = str(args.is_archive)
    if args.automatically_copy is not None:
        payload["automaticallyCopy"] = str(args.automatically_copy)

    if args.show_get_url or args.dry_run:
        query = dict(payload)
        title = query.pop("title", None)
        subtitle = query.pop("subtitle", None)
        body = query.pop("body", None)
        get_url = build_get_url(
            args.base_url,
            args.device_key,
            title=title,
            subtitle=subtitle,
            body=body,
            query=query,
        )
        print("# GET URL")
        print(get_url)
        print()

    print("# Python payload")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()

    if args.dry_run:
        print("# Dry run only; request not sent.")
        return

    request = Request(
        url=f"{args.base_url.rstrip('/')}/{args.device_key}",
        data=urlencode(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            print("# Response")
            print(f"status: {response.status}")
            print(response.read().decode("utf-8", errors="replace"))
    except HTTPError as exc:
        print("# Response")
        print(f"status: {exc.code}")
        body = exc.read().decode("utf-8", errors="replace")
        print(body)
        sys.exit(1)
    except URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
