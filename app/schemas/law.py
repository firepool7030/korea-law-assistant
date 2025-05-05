from pydantic import BaseModel
from typing import Optional

class Law(BaseModel):
    법령일련번호: str
    현행연혁코드: Optional[str]
    법령명한글: str
    법령약칭명: Optional[str]
    법령ID: str
    공포일자: Optional[str]
    공포번호: Optional[str]
    제개정구분명: Optional[str]
    소관부처명: Optional[str]
    소관부처코드: Optional[str]
    법령구분명: Optional[str]
    공동부령정보: Optional[str]
    시행일자: Optional[str]
    자법타법여부: Optional[str]
    법령상세링크: Optional[str]

    class Config:
        extra = "ignore"