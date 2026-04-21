def make_issue(level, issue_code, path, message, *, target=None, field=None, value=None, blocking=True, ai_action="stop_and_fix"):
    return {
        "level": level,
        "issue_code": issue_code,
        "path": path,
        "target": target,
        "field": field,
        "value": value,
        "blocking": blocking,
        "ai_action": ai_action,
        "message": message,
    }
