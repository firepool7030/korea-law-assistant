from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class LawMetaSchema(BaseModel):
    법령일련번호: str
    현행연혁코드: Optional[str]
    법령명한글: str
    법령약칭명: Optional[str]
    법령ID: str
    공포일자: Optional[str]  # API에서 문자열로 받음 (예: "20230808")
    공포번호: Optional[str]
    제개정구분명: Optional[str]
    소관부처명: Optional[str]
    소관부처코드: Optional[str]
    법령구분명: Optional[str]
    공동부령정보: Optional[str]
    시행일자: Optional[str]  # API에서 문자열로 받음 (예: "20230808")
    자법타법여부: Optional[str]
    법령상세링크: Optional[str]

    # 공포일자/시행일자를 datetime.date 객체로 변환
    @field_validator("공포일자", "시행일자", mode="before")
    @classmethod
    def parse_date(cls, value):
        if value:
            try:
                return datetime.strptime(value, "%Y%m%d").date()
            except ValueError:
                return None
        return None