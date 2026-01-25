from sqlalchemy.orm import Session

from pomodoro_quest.db.models import User


DEMO_USERNAME = "demo"


def get_or_create_demo_user(db: Session) -> User:
    """
    Ensure a demo user exists for Phase 0.

    This allows us to track XP and stats without real authentication.
    """
    user = db.query(User).filter(User.username == DEMO_USERNAME).one_or_none()
    if user:
        return user

    user = User(username=DEMO_USERNAME, xp=0, level=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
