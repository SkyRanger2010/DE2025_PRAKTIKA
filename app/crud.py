from sqlalchemy import func, or_, cast, String
from sqlalchemy.orm import Session
from app import models


def get_users_by_keywords(db: Session, keywords: set[str], start_idx: int, end_idx: int):
    db_fields = [
        models.UserIn.username,
        models.UserIn.fullname,
        models.UserIn.biography,
        models.UserIn.sex,
        models.UserIn.external_url,
        models.UserIn.account_type,
        models.UserIn.is_private,
        models.UserIn.avatar,
        models.UserIn.is_verified,
        models.UserIn.follower_count,
        models.UserIn.following_count,
        models.UserIn.media_count,
        models.UserIn.last_time
    ]

    conditions = []
    for keyword in keywords:
        conditions_to_search_by_keyword = [func.lower(db_field).contains(func.lower(keyword)) for db_field in db_fields]
        conditions.append(or_(*conditions_to_search_by_keyword))

    return (
        db.query(models.UserIn)
        .filter(or_(*conditions))
        .offset(start_idx)
        .limit(end_idx - start_idx)
        .all()
    )
