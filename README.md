# bark-skills

A Bark skill for building Bark / api.day.app notification requests with Python.

## What it includes

- `SKILL.md`: skill instructions
- `agents/openai.yaml`: UI metadata
- `references/python-examples.md`: parameter and example reference
- `scripts/send_bark.py`: reusable Python script for sending Bark notifications

## Quick start

Dry run:

```bash
python3 scripts/send_bark.py <key> --title "Test Title" --body "Test Body" --dry-run --show-get-url
```

Send a notification:

```bash
python3 scripts/send_bark.py <key> --title "Test Title" --body "Test Body"
```

## Example

```python
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def send_bark(key, body=None, title=None, subtitle=None, **params):
    payload = {}
    if title is not None:
        payload["title"] = title
    if subtitle is not None:
        payload["subtitle"] = subtitle
    if body is not None:
        payload["body"] = body
    payload.update(params)

    request = Request(
        url=f"https://api.day.app/{key}",
        data=urlencode(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        print(response.status)
        print(response.read().decode("utf-8", errors="replace"))
```

## Supported Bark fields

`title`, `subtitle`, `body`, `url`, `group`, `sound`, `call`, `icon`, `image`, `badge`, `copy`, `automaticallyCopy`, `isArchive`, `ciphertext`, `level`, `volume`
