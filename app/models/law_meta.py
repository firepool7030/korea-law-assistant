from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LawMetaTable(Base):
    __tablename__ = "law_metadata"

    법령일련번호 = Column(String, primary_key=True)
    현행연혁코드 = Column(String)
    법령명한글 = Column(String, nullable=False)
    법령약칭명 = Column(String)
    법령ID = Column(String, nullable=False)
    공포일자 = Column(Date)  # Date 타입 유지 (변환된 값 저장)
    공포번호 = Column(String)
    제개정구분명 = Column(String)
    소관부처명 = Column(String)
    소관부처코드 = Column(String)
    법령구분명 = Column(String)
    공동부령정보 = Column(String)
    시행일자 = Column(Date)  # Date 타입 유지 (변환된 값 저장)
    자법타법여부 = Column(String)
    법령상세링크 = Column(String)
