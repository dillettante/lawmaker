# Sources — 원본 출처와 반영 판(版)

이 스킬은 아래 **법제처 발간 실무기준**을 파생·정리한 것이다. 원문은 법제처 저작물(공공저작물)이며,
이 저장소의 챕터는 원문 복사가 아닌 구조화 요약이다. 인용 시 원문 대조 필수(SKILL.md ⚠ 참조).

| # | 자료 | 반영 판/시점 | 면수 | 공식 페이지 | 안정 식별자 |
|---|------|------|---|---|---|
| 1 | 법령 입안·심사 기준 | 2026 | 880 | [법제처](https://www.moleg.go.kr/menu.es?mid=a10105030000) | **공공데이터포털 데이터셋 `15031101`** ([링크](https://www.data.go.kr/data/15031101/fileData.do), 최종수정 2025-12-22) |
| 2 | 법제업무편람 | 2026 | 507 | [정부입법지원센터](https://www.lawmaking.go.kr/lmKnlg/wrkHndbk/list) | (데이터셋 ID 미확인 — 랜딩페이지 모니터) |
| 3 | 알기 쉬운 법령 정비기준 | 제10판 증보판 | 396 | [정부입법지원센터](https://www.lawmaking.go.kr/lmKnlg/abRprStd) · [법제처](https://www.moleg.go.kr/menu.es?mid=a10108030000) | (랜딩페이지 모니터) |
| 4 | 행정규칙 입안·심사 기준 | 2026 | 152 | [법제처](https://www.moleg.go.kr/menu.es?mid=a10103030000) | (랜딩페이지 모니터) |

## 추출 설정 (재현용)
- 도구: `docling`(technical), `pypdf`
- 설정: `do_ocr=False`, 10-page chunk, `KMP_DUPLICATE_LIB_OK=TRUE`, `OMP_NUM_THREADS=1`
- 명령: `python3 build/extract_docling.py <out> "라벨=<pdf경로>" …`  → 자세히는 [BUILD.md](BUILD.md)

## 페이지 기준
`원문 근거: p.NN`은 docling PDF 마커면 기준(자료별 인쇄쪽과의 관계는 SKILL.md "페이지 기준" 표 참조).

## 갱신 모니터링
- 이 세 책은 **연속이 아니라 판(版) 단위**로 개정된다(예: 정비기준 9판 2019 → 10판 2023).
- 자동 감지(best-effort): `.github/workflows/check-updates.yml`가 데이터셋 `15031101`의 최종수정일을
  기준값과 비교해 변하면 이슈를 생성한다. 나머지 3종은 위 랜딩페이지를 수동 확인.
- 새 판 확인 시 재생성 절차는 [BUILD.md](BUILD.md).
