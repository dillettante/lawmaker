# BUILD — 새 판(版)으로 스킬 재생성하기

이 스킬은 **정적 산출물(버전 고정)** 이다. 원문이 개정되면 관리자가 아래 절차로 재생성해 새 릴리스를 낸다.
자동 실시간 웹갱신이 아니다(추출+요약이 LLM 비용·검수를 수반하므로).

## 사전 준비
```bash
python3 -m pip install docling pypdf --break-system-packages
python3 -c "import docling; print('docling ok')"
```

## 1. 원문 PDF 확보
[SOURCES.md](SOURCES.md)의 공식 페이지/데이터셋에서 최신판 PDF를 내려받는다.
경로에 `[ ] * ?` 같은 glob 문자가 있으면 단순 경로로 복사(docling이 입력을 glob 처리).

## 2. 텍스트 추출 (결정적, 로컬)
```bash
python3 build/extract_docling.py out \
  "입안심사기준=경로/law_drafting.pdf" \
  "법제업무편람=경로/handbook.pdf" \
  "정비기준=경로/plain_language.pdf" \
  "행정규칙입안심사기준=경로/admin_rule.pdf"
```
→ `out/p1.md … p4.md`(페이지 마커 `[원문: <라벨> p.N-M]` 포함), `out/full_text.txt`, `out/metadata.json`.

## 3. 챕터 생성 (LLM 단계 — 검수 필요, 결정적 아님)
각 책을 페이지 범위별로 나눠 LLM 에이전트가 챕터를 생성한다. 기존 챕터가 따른 규격:
- 파일: `chapters/ch<NN>-<slug>.md`, 블록 배정(입안심사 ch01–39 / 편람 ch40–56 / 정비 ch60–72 / 행정규칙 ch80–86)
- reference 깊이. 각 챕터 헤더 `**원문**: <자료> p.범위`, 모든 기준·요점에 `원문 근거: p.NN`
- 섹션: `## 핵심 / ## 기준·규칙 / ## 주의·함정 / ## 요점 / ## 연결`
- **§2 규칙(법률 정확성)**: 문언 왜곡·추측 인용 금지, 불확실하면 "원문 확인 필요", 원문 raw 통째 복사 금지(구조화), 표는 markdown 표로 보존
- 페이지 마커로 슬라이스해 해당 범위만 읽어 생성(전체 통독 금지)

이 단계는 사람이 결과를 검수한다(판례·조문 인용 정확성 우선).

## 4. 지원 파일·인덱스 갱신
- `glossary.md` / `patterns.md` / `cheatsheet.md` 재생성(챕터 근거, chNN 출처)
- `formatting.md`·`tools/format_lawtext.py`는 체제·개정 챕터가 바뀐 경우에만 갱신 후 `python3 tools/format_lawtext.py`로 self-check
- `SKILL.md`의 출처·챕터수·챕터 인덱스(A~H)·토픽 인덱스·페이지 기준·생성일 갱신
- [SOURCES.md](SOURCES.md)의 반영 판/시점·데이터셋 최종수정일 갱신

## 5. 검증
```bash
# 챕터 링크 정합성
grep -oE "chapters/[a-z0-9-]+\.md" SKILL.md | sort -u | while read L; do [ -f "$L" ] || echo "MISSING: $L"; done
# 포매터 self-check
python3 tools/format_lawtext.py
# 기밀 스캔(공개 저장소)
grep -rniE "cloudstorage|googledrive|/Users/|의뢰인|사건번호" . && echo "!! 확인" || echo "clean"
```

## 6. 릴리스
변경을 커밋하고 판(版) 기준으로 태그: 예) `git tag v2026.1 && git push --tags`.
사용자는 `git pull`로 최신 판을 받는다.
