from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserInSchema(BaseModel):
    userid: int
    username: Optional[str]
    fullname: Optional[str]
    biography: Optional[str]
    sex: Optional[str]
    is_private: Optional[bool]
    external_url: Optional[str]
    account_type: Optional[str]
    avatar: Optional[int]
    is_verified: Optional[bool]
    follower_count: Optional[int]
    following_count: Optional[int]
    media_count: Optional[int]
    last_time: Optional[datetime]

    class Config:
        orm_mode = True


class UserInSearchResults(BaseModel):
    count: int
    res: list[UserInSchema]
