def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def normalize_text(text):
    if not text:
        return ""
    return text.strip()


def paginate(page: int, limit: int):
    page = max(page, 1)
    limit = min(max(limit, 1), 50)
    offset = (page - 1) * limit
    return offset, limit
