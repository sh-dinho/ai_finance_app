def header(title: str) -> str:
    """
    Formats a top-level header for the report.
    Example:
        === FINANCIAL REPORT CARD ===
    """
    return f"=== {title.upper()} ==="


def section(title: str) -> str:
    """
    Formats a section header.
    Example:
        --- Summary ---
    """
    return f"\n--- {title} ---"


def line(text: str) -> str:
    """
    Formats a single line of report text.
    """
    return text
