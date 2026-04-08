---
name: bark-skills
description: Send Bark / api.day.app notifications with Python, including title, subtitle, body, url, group, sound, icon, image, badge, copy, archive, ciphertext, and notification level settings.
---

# Bark

## Rules

- Default to Python POST.
- Use Python stdlib `urllib.parse` + `urllib.request`.
- Keep Bark parameter names unchanged.
- Parameters can be combined.
- Only add GET examples when the user explicitly asks for URLs.

## Template

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

## Script

```bash
python3 scripts/send_bark.py <key> --body "Replace this with your message body" --dry-run
```

- `--dry-run`: print only, do not send
- `--show-get-url`: print the GET URL

## Parameter mapping

- Content fields can be combined:
  - body only: `body`
  - title + body: `title` + `body`
  - title + subtitle + body: `title` + `subtitle` + `body`
- Optional parameters can be added to the same request.
- Common combinations:
  - `title` + `body` + `url`
  - `title` + `subtitle` + `body` + `group`
  - `body` + `sound` + `call`
  - `body` + `level` + `volume`
  - `body` + `copy` + `automaticallyCopy`
  - `title` + `body` + `icon` + `image`

- Title: `title`
- Subtitle: `subtitle`
- Body: `body`
- Jump URL: `url`
- Group: `group`
- Sound: `sound`
- Continuous ringing: `call=1`
- Save to history: `isArchive=1`
- Icon: `icon`
- Image: `image`
- Copy content: `copy`
- Automatically copy: `automaticallyCopy=1`
- Badge: `badge`
- Encryption: `ciphertext`
- Time-sensitive notification: `level=timeSensitive`
- Critical alert: `level=critical`

## Common patterns

```python
send_bark("<key>", body="Replace this with your message body")
send_bark("<key>", title="Notification title", body="Replace this with your message body")
send_bark("<key>", title="Notification title", subtitle="Notification subtitle", body="Replace this with your message body")
send_bark("<key>", title="Build complete", body="Tap to view details", url="https://www.baidu.com")
send_bark("<key>", title="Dev notice", subtitle="branch: feature", body="Unit tests failed", group="dev")
send_bark("<key>", body="Custom sound", sound="minuet")
send_bark("<key>", body="Continuous ringing", call=1)
send_bark("<key>", body="On-call alert", sound="minuet", call=1)
send_bark("<key>", body="Save notification history", isArchive=1)
send_bark("<key>", body="Custom notification icon", icon="https://day.app/assets/images/avatar.jpg")
send_bark("<key>", body="Image notification", icon="https://day.app/assets/images/avatar.jpg", image="https://day.app/assets/images/avatar.jpg")
send_bark("<key>", body="Notification group", group="groupName")
send_bark("<key>", body="Encrypted push", ciphertext="<ciphertext>")
send_bark("<key>", body="Critical alert", level="critical", volume=5)
send_bark("<key>", body="Time-sensitive notification", level="timeSensitive")
send_bark("<key>", body="URL Test", url="https://www.baidu.com")
send_bark("<key>", body="Image notification", image="https://day.app/assets/images/avatar.jpg")
send_bark("<key>", body="Copy Test", copy="test")
send_bark("<key>", body="Set badge", badge=1)
send_bark("<key>", body="Automatically copy to clipboard", copy="optional text", automaticallyCopy=1)
```

## Output

- Group the parameters first, then write the code
- Put the Python example first
- List the actual parameters used
- Add a GET URL only when needed

## References

- `references/python-examples.md`
- `scripts/send_bark.py`
