#!/usr/bin/env python3
"""법령안 텍스트 결정론적 포매터 (LLM 불필요, 표준 라이브러리만).

번호체계·마커는 법제처 기준(ch31, ch33)을 따른다:
  조=제N조 / 항=①②③(원문자) / 호=1.2.3. / 목=가.나.다.
조 제목은 조 번호 뒤 괄호로 붙인다: 제5조(허가).
항이 하나뿐이면 항 마커(①)를 생략하고 본문을 바로 쓴다 (ch31).

개정지시문 헬퍼는 ch32/ch33의 자구 일부개정문을 조립한다:
  제○조제○항 중 「옛」을 「새」로 한다. (조사 을/를·로/으로 자동 선택)

입력 예시 (구조화 dict):
    article = {
        "num": 5,
        "title": "허가",
        "paragraphs": [
            {"text": "허가를 받으려는 자는 신청서를 제출하여야 한다."},
            {
                "text": "제1항의 신청서에는 다음 각 호의 서류를 첨부한다.",
                "items": [                         # 호
                    {"text": "사업계획서"},
                    {"text": "정관", "subitems": [  # 목
                        {"text": "목적"},
                    ]},
                ],
            },
        ],
    }
    print(format_article(article))

주의: 물리 편집규격(줄간격·글씨·들여쓰기 폭)은 공식 법령안편집기 몫이다(ch56).
이 포매터는 마커·조립만 결정론적으로 처리한다. 최종 형식은 원문·편집기로 확인.
"""

# 원문자 항 마커 ①..⑮ (ch31). 15개 초과 항은 실무상 드물다.
_CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮"
# 목 마커 가.나.다.… (ch31).
_MOK = "가나다라마바사아자차카타파하"


def _circled(n):
    if not 1 <= n <= len(_CIRCLED):
        raise ValueError(f"항 번호 {n}은 마커 범위(1~{len(_CIRCLED)}) 밖 (ch31)")
    return _CIRCLED[n - 1]


def _mok(n):
    if not 1 <= n <= len(_MOK):
        raise ValueError(f"목 번호 {n}은 마커 범위(1~{len(_MOK)}) 밖 (ch31)")
    return _MOK[n - 1] + "."


def format_article(article):
    """구조화 dict 하나를 법령안 조문 텍스트로 포맷한다.

    article: {"num": int, "title": str(optional), "paragraphs": [para, ...]}
    para:    {"text": str, "items": [item, ...](optional)}   # 항, 하위 호
    item:    {"text": str, "subitems": [sub, ...](optional)}  # 호, 하위 목
    sub:     {"text": str}                                    # 목
    """
    head = f"제{article['num']}조"
    if article.get("title"):
        head += f"({article['title']})"

    paras = article.get("paragraphs", [])
    lines = []
    single = len(paras) == 1  # 항이 하나면 ① 생략 (ch31)

    for pi, para in enumerate(paras, start=1):
        marker = "" if single else _circled(pi) + " "
        # 첫 항 본문은 조 제목과 같은 줄에 붙인다.
        if pi == 1:
            lines.append(f"{head} {marker}{para['text']}")
        else:
            lines.append(f"{marker}{para['text']}")
        for hi, item in enumerate(para.get("items", []), start=1):
            lines.append(f"  {hi}. {item['text']}")  # 호 (ch31)
            for mi, sub in enumerate(item.get("subitems", []), start=1):
                lines.append(f"    {_mok(mi)} {sub['text']}")  # 목 (ch31)
    return "\n".join(lines)


def _cite(article, paragraph=None, item=None):
    """조·항·호 인용 문자열. 조·항·호는 붙여 쓴다 (ch32)."""
    s = f"제{article}조"
    if paragraph is not None:
        s += f"제{paragraph}항"
    if item is not None:
        s += f"제{item}호"
    return s


def _batchim(word):
    """마지막 한글 음절의 종성 코드(0=없음). 한글이 아니면 None."""
    ch = word[-1]
    if "가" <= ch <= "힣":
        return (ord(ch) - 0xAC00) % 28
    return None


def amend_directive(article, old, new, paragraph=None, item=None):
    """자구 일부개정문 한 줄 (ch32, ch33).

    제○조제○항 중 「옛」을 「새」로 한다.
    낫표 「 」로 자구를 감싼다(ch32·formatting.md). 조사는 인용 자구의
    끝 글자를 따른다 — 받침 유무로 을/를, 받침(ㄹ 제외)으로 로/으로.
    """
    b_old = _batchim(old)
    eul = "을" if (b_old is None or b_old) else "를"
    b_new = _batchim(new)
    # 종성 8 = ㄹ: "…물로 한다"처럼 ㄹ 받침 뒤엔 '로'
    ro = "으로" if (b_new is not None and b_new not in (0, 8)) else "로"
    return f'{_cite(article, paragraph, item)} 중 「{old}」{eul} 「{new}」{ro} 한다.'


if __name__ == "__main__":
    # self-check: 2개 항, 그중 둘째 항에 2개 호 (ch31, ch33)
    art = {
        "num": 5,
        "title": "허가",
        "paragraphs": [
            {"text": "허가를 받으려는 자는 신청서를 제출하여야 한다."},
            {
                "text": "제1항의 신청서에는 다음 각 호의 서류를 첨부한다.",
                "items": [
                    {"text": "사업계획서"},
                    {"text": "정관"},
                ],
            },
        ],
    }
    expected = (
        "제5조(허가) ① 허가를 받으려는 자는 신청서를 제출하여야 한다.\n"
        "② 제1항의 신청서에는 다음 각 호의 서류를 첨부한다.\n"
        "  1. 사업계획서\n"
        "  2. 정관"
    )
    got = format_article(art)
    assert got == expected, f"format_article mismatch:\n{got!r}\n!=\n{expected!r}"

    # 항 하나면 ① 생략 (ch31)
    single = format_article({"num": 1, "title": "목적", "paragraphs": [
        {"text": "이 법은 …을 목적으로 한다."}]})
    assert single == "제1조(목적) 이 법은 …을 목적으로 한다.", single

    # 목까지 (ch31)
    with_mok = format_article({"num": 2, "paragraphs": [
        {"text": "본문", "items": [
            {"text": "호1", "subitems": [{"text": "목1"}, {"text": "목2"}]}]}]})
    assert with_mok == "제2조 본문\n  1. 호1\n    가. 목1\n    나. 목2", with_mok

    # 개정지시문 (ch32, ch33)
    d = amend_directive(5, "국토해양부장관", "국토교통부장관", paragraph=1)
    assert d == "제5조제1항 중 「국토해양부장관」을 「국토교통부장관」으로 한다.", d
    # 조사 자동 선택: 모음 끝→를, ㄹ받침→로
    assert amend_directive(3, "허가", "인가") == '제3조 중 「허가」를 「인가」로 한다.'
    assert amend_directive(3, "물", "물건") == '제3조 중 「물」을 「물건」으로 한다.'
    assert amend_directive(3, "건물", "시설물") == '제3조 중 「건물」을 「시설물」로 한다.'

    print("self-check passed")
