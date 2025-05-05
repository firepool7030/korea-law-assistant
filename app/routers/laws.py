import os
import requests
import dotenv
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from schemas.law import Law

dotenv.load_dotenv()

router = APIRouter(prefix="/laws", tags=["laws"])

@router.get("/", response_model=List[Law])
async def get_laws(
    query: Optional[str] = Query(None, description="법령명 검색어"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    display: int = Query(1000, ge=1, le=1000, description="페이지당 결과 수")
):
    """
    국가법령정보 법령목록조회 API(JSON) 호출
    """
    OC = os.getenv("OC")
    if not OC:
        raise HTTPException(status_code=500, detail="OC 환경변수가 없습니다.")

    base_url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": OC,
        "target": "law",
        "type": "JSON",
        "page": page,
        "display": display,
    }
    if query:
        params["query"] = query

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="법령정보 API 호출 실패")

    try:
        data = response.json()
    except Exception:
        # 실제 응답 내용을 로그로 남기면 디버깅에 도움이 됩니다.
        print("법령정보 API 응답:", response.text)
        raise HTTPException(status_code=502, detail="법령정보 API에서 올바른 JSON을 반환하지 않음")

    # 법령 목록은 data["LawSearch"]["law"]에 들어 있음
    laws = data.get("LawSearch", {}).get("law", [])
    if isinstance(laws, dict):
        laws = [laws]

    # Pydantic 모델에 맞게 변환
    result = []
    for law in laws:
        try:
            result.append(Law(**law))
        except Exception:
            # 필드 누락 등 예외 처리
            continue
    return result
