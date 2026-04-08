# Bark Python Reference

This file is a quick reference for Python usage and corresponding Bark parameters based on the screenshot examples.

## Combination rules

- `title`, `subtitle`, and `body` can be used together.
- Other parameters can be added to the same request.
- A single request can include content fields and multiple optional parameters.

Common combinations:

- `title` + `body` + `url`
- `title` + `subtitle` + `body` + `group`
- `body` + `sound` + `call`
- `body` + `level=critical` + `volume`
- `body` + `copy` + `automaticallyCopy`
- `body` + `icon` + `image`

Assume you already have this helper:

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

## Features and Python usage

| Feature | Python |
| --- | --- |
| Custom message body | `send_bark(key, body="Replace this with your message body")` |
| Notification title | `send_bark(key, title="Notification title", body="Replace this with your message body")` |
| Title + subtitle + body | `send_bark(key, title="Notification title", subtitle="Notification subtitle", body="Replace this with your message body")` |
| Custom sound | `send_bark(key, body="Custom sound", sound="minuet")` |
| Continuous ringing | `send_bark(key, body="Continuous ringing", call=1)` |
| Save notification history | `send_bark(key, body="Save notification history", isArchive=1)` |
| Custom notification icon | `send_bark(key, body="Custom notification icon", icon="https://day.app/assets/images/avatar.jpg")` |
| Notification group | `send_bark(key, body="Notification group", group="groupName")` |
| Encrypted push | `send_bark(key, body="Encrypted push", ciphertext="<ciphertext>")` |
| Critical alert | `send_bark(key, body="Critical alert", level="critical", volume=5)` |
| Time-sensitive notification | `send_bark(key, body="Time-sensitive notification", level="timeSensitive")` |
| URL redirect | `send_bark(key, body="URL Test", url="https://www.baidu.com")` |
| Image notification | `send_bark(key, body="Image notification", image="https://day.app/assets/images/avatar.jpg")` |
| Copy Test | `send_bark(key, body="Copy Test", copy="test")` |
| Set badge | `send_bark(key, body="Set badge", badge=1)` |
| Automatically copy to clipboard | `send_bark(key, body="Automatically copy to clipboard", copy="optional text", automaticallyCopy=1)` |

## Combination examples

```python
send_bark(
    key,
    title="Build complete",
    subtitle="main",
    body="Tap to view details",
    url="https://www.baidu.com",
    group="dev",
)

send_bark(
    key,
    body="On-call alert",
    sound="minuet",
    call=1,
    level="critical",
    volume=5,
)

send_bark(
    key,
    body="Copy verification code",
    copy="123456",
    automaticallyCopy=1,
    isArchive=1,
)

send_bark(
    key,
    title="Image notification",
    body="With icon and image",
    icon="https://day.app/assets/images/avatar.jpg",
    image="https://day.app/assets/images/avatar.jpg",
)
```

## Matching GET URL examples

### Custom message body

```text
https://api.day.app/<key>/Replace%20this%20with%20your%20message%20body
```

### Notification title

```text
https://api.day.app/<key>/Notification%20title/Replace%20this%20with%20your%20message%20body
```

### Custom sound

```text
https://api.day.app/<key>/Custom%20sound?sound=minuet
```

### Continuous ringing

```text
https://api.day.app/<key>/Continuous%20ringing?call=1
```

### Save notification history

```text
https://api.day.app/<key>/Save%20notification%20history?isArchive=1
```

### Custom notification icon

```text
https://api.day.app/<key>/Custom%20notification%20icon?icon=https://day.app/assets/images/avatar.jpg
```

### Notification group

```text
https://api.day.app/<key>/Notification%20group?group=groupName
```

### Encrypted push

```text
https://api.day.app/<key>/Encrypted%20push?ciphertext=<ciphertext>
```

### Critical alert

```text
https://api.day.app/<key>/Critical%20alert?level=critical&volume=5
```

### Time-sensitive notification

```text
https://api.day.app/<key>/Time-sensitive%20notification?level=timeSensitive
```

### URL redirect

```text
https://api.day.app/<key>/URL%20Test?url=https://www.baidu.com
```

### Image notification

```text
https://api.day.app/<key>/Image%20notification?image=https://day.app/assets/images/avatar.jpg
```

### Copy Test

```text
https://api.day.app/<key>/Copy%20Test?copy=test
```

### Set badge

```text
https://api.day.app/<key>/Set%20badge?badge=1
```

### Automatically copy to clipboard

```text
https://api.day.app/<key>/Automatically%20copy%20to%20clipboard?copy=optional%20text&automaticallyCopy=1
```

## Notes

- `icon`: iOS 15+.
- `automaticallyCopy=1`: restricted on iOS 14.5+.
- `critical`: use only for strong alerts.
- Use GET only when a URL example is specifically needed. Default to Python POST.
