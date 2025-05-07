import os
import requests
import dotenv
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from schemas.law_meta import LawMetaSchema

dotenv.load_dotenv()

router = APIRouter(prefix="/law_metas", tags=["law_metas"])

# 국가법령정보 API 호출
def fetch_law_list_from_api(query: Optional[str], page: int, display: int) -> List[dict]:
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

    # 응답 코드가 200이 아니면 502(Bad Gateway) 에러 발생
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"법령정보 API 호출 실패: {response.status_code}")

    # JSON 형식으로 응답 데이터 파싱
    try:
        data = response.json()
    except Exception as e:
        print("법령정보 API 응답:", response.text)
        raise HTTPException(status_code=502, detail=f"법령정보 API에서 올바른 JSON을 반환하지 않음: {e}")

    # 법령 목록 추출
    laws = data.get("LawSearch", {}).get("law", [])
    if isinstance(laws, dict):  # 단일 결과도 리스트로 변환
        laws = [laws]
    return laws


# 엔드포인트 선언
@router.get("/", response_model=List[LawMetaSchema])
async def get_laws(
    query: Optional[str] = Query(None, description="법령명 검색어"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    display: int = Query(1000, ge=1, le=1000, description="페이지당 결과 수")
):
    """
    국가법령정보 법령목록조회 API(JSON) 호출 및 Pydantic 검증
    """
    raw_laws = fetch_law_list_from_api(query, page, display)

    # Pydantic 모델로 검증 및 변환
    result: List[LawMetaSchema] = []
    for law in raw_laws:
        try: # API에서 받은 각 법령 데이터를 Pydantic 모델(LawMetaSchema)로 변환(유효성 검사).
            result.append(LawMetaSchema(**law))
        except Exception as e:
            print(f"데이터 변환 오류: {e} / 데이터: {law}")
            continue

    # 여기에 DB 저장 로직을 추가할 수 있습니다.
    # 예: save_laws_to_db(result)

    return result
