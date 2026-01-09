from pomodoro_quest.db.models import SessionMode


def calculate_xp(mode: SessionMode) -> int:
    """
    XP rules for the MVP.

    These values are intentionally simple and easy to reason about.
    """
    if mode == SessionMode.focus:
        return 10
    if mode == SessionMode.break_short:
        return 2
    if mode == SessionMode.break_long:
        return 4
    return 0
