# lawmaker

> 한국 법령·행정규칙 입안·심사·정비 기준(법제처) 에이전트 스킬 · An agent skill for drafting, reviewing, and plain-language revision of Korean legislation and administrative rules, built from Ministry of Government Legislation (MOLEG) standards.

한국 **법령·조례·규칙·행정규칙의 입안·심사·정비**를 돕는 에이전트 스킬(지식베이스). 법제처의 4대 실무기준을
구조화 챕터 + 토픽 인덱스 + 의사결정 치트시트 + 법령안 출력 포매터로 정리했다.
`SKILL.md`(frontmatter) 규약을 따르는 **모든 에이전트**에서 온디맨드로 로드된다(파일을 읽는 어떤 도구에서도 참조 가능; 설치 예시는 아래).

## In English
**lawmaker** is an agent skill (knowledge base) for **drafting, reviewing, and revising Korean statutes, subordinate legislation, and administrative rules**. It distills four official standards of the Korean **Ministry of Government Legislation (MOLEG, 법제처)** into 76 structured chapters + a topic index + a decision cheatsheet + a statute-format helper. It loads on demand in **any agent that follows the `SKILL.md` (frontmatter) convention**, and can be referenced by any file-reading tool.

- **Sources** (derived summaries, not verbatim copies): Statute Drafting & Review Standards (2026), Legislative Affairs Handbook (2026), Plain-Language Statute Revision Standards (10th ed.), Administrative-Rule Drafting & Review Standards (2026).
- **⚠ Disclaimer**: Unofficial study aid. Chapter summaries are **not** citation authority — verify against the original before citing, and check statute/precedent numbers against official databases. Not legal advice.
- **Install**: `git clone https://github.com/dillettante/lawmaker.git`, then symlink it into your agent's skill root (e.g. `~/.claude/skills/` or `~/.agents/skills/`).
- **License**: content CC BY 4.0 (credit 법제처/MOLEG), code MIT — see [LICENSE](LICENSE).

## 무엇을 담았나
법제처 발간 기준을 파생·정리(원문 복사가 아닌 구조화 요약):
- 「법령 입안·심사 기준」(2026) — 입안·심사 실체 기준
- 「법제업무편람」(2026) — 입법절차
- 「알기 쉬운 법령 정비기준」(제10판) — 용어·문장 정비
- 「행정규칙 입안·심사 기준」(2026) — 훈령·예규·고시

76개 챕터, 각 기준에 `원문 근거: p.NN` 페이지 포인터. 출처·판(版)은 [build/SOURCES.md](build/SOURCES.md).

## ⚠ 면책 (중요)
이 스킬은 법제처 기준의 **비공식 학습 보조물**이다. 챕터 요약은 인용 근거가 아니며, **외부 제출 문서에 인용하기
전 반드시 원문과 대조**한다. 조문·판례 번호는 원문/공식 DB로 검증한다. 하급심 판례·해석례는 확정 여부를 별도
확인한다. 법률 자문을 대체하지 않는다.

## 설치
`SKILL.md` 규약을 따르는 에이전트의 스킬 루트에 이 저장소를 두면 된다.
```bash
git clone https://github.com/dillettante/lawmaker.git
# Claude Code
ln -s "$PWD/lawmaker" ~/.claude/skills/lawmaker
# Copilot CLI / Amp 등 크로스에이전트
# ln -s "$PWD/lawmaker" ~/.agents/skills/lawmaker
```
에이전트 재시작 후 "법령 입안", "위임조문", "경과조치 규정 방식", "'여부' 순화" 등으로 트리거된다.

## 사용
- 토픽으로: "위임 한계", "입법예고 기간", "행정규칙 대외 구속력"
- 챕터로: "ch33"(조·항·호 개정 방식)
- 인덱스: `SKILL.md`의 챕터 인덱스(A~H)·토픽 인덱스
- 법령안 형식 출력: [formatting.md](formatting.md) 규칙 + `python3 tools/format_lawtext.py`

## 선택: 조문·판례 실시간 검증 (없어도 코어는 완전 동작)
정확성 자동화를 원하면:
- **korean-law MCP**(권장) 연결, 또는
- **국가법령정보 OPEN API** 키 발급: <https://open.law.go.kr/LSO/openApi/guideList.do>
  (법령·자치법규·행정규칙·판례·법령해석례·별표서식 제공). **키는 환경변수/로컬 설정에만 두고 커밋하지 않는다.**

## 업데이트
원문이 새 판으로 개정되면 관리자가 재생성해 새 버전을 릴리스한다(실시간 자동갱신 아님). 절차: [build/BUILD.md](build/BUILD.md).
개정 감지는 `.github/workflows/check-updates.yml`가 best-effort로 이슈를 생성한다.

## 라이선스
- **문서·콘텐츠**(`SKILL.md`, `chapters/`, `*.md`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) —
  자유 이용·수정·재배포·상업이용 가능, **출처표시**만 유지.
- **코드**(`build/`, `tools/`): [MIT](LICENSE).
- **원저작물 출처**: 법제처(대한민국). 원문 기준서의 저작권은 법제처에 있으며(공공저작물), 이 저장소는 그 파생 정리물이다.
자세히는 [LICENSE](LICENSE).

## 기여
새 판 반영·오류 수정 PR 환영. 변경 시 [build/BUILD.md](build/BUILD.md)의 검증 단계(링크 정합·포매터 self-check·기밀 스캔)를 통과시킬 것.
