#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""detect.py - deterministic AI-tell detector (Chinese + English). Stdlib only.

Usage:
    python3 detect.py <file>
    cat text.txt | python3 detect.py
    python3 detect.py --json <file>

It is a *quantitative base*, not a verdict. Read the text too.
"""
import sys
import re
import json

# ---- phrase lists (curated; see references/) --------------------------------

ZH_STRONG = [
    "值得注意的是", "不可否认的是", "毋庸置疑", "众所周知", "值得一提的是",
    "需要指出的是", "必须强调的是", "不容忽视的是", "归根结底",
    "从某种程度上", "从某种意义上", "平心而论", "客观来说", "坦白说", "严格来说",
    "研究表明", "有学者指出", "据调查显示", "大量研究表明", "研究证实",
    "业内专家认为", "据权威机构统计", "历史经验表明",
    "综上所述", "由此可见", "总而言之", "总的来说",
    "非常重要", "极其关键", "至关重要", "不可或缺", "不可替代", "举足轻重",
    "显著提升", "大幅度提高", "明显改善", "极大程度", "进一步优化",
    "在很大程度上", "普遍认为", "大多数人",
    "希望以上内容对你有所帮助", "希望对你有帮助", "欢迎在评论区",
    "正如前文所述", "如上所述", "限于篇幅", "恕不赘述", "这里不再展开",
    "赋能", "闭环", "抓手", "颗粒度", "底层逻辑", "对齐",
    # 空洞议论 / 万能句式(markers-zh §3/§6)
    "双刃剑", "值得我们深入思考", "值得我们深思", "是当务之急", "刻不容缓",
    "任重而道远", "既是挑战也是机遇", "既是机遇也是挑战",
    "发挥着越来越重要的作用", "扮演着不可或缺的角色",
    "具有深远的意义", "具有重要的现实意义", "必然趋势", "提供了强有力的支撑",
]
ZH_HEDGE = [
    "可能", "或许", "大概", "某种程度上", "在一定程度上", "相对而言",
    "似乎", "看起来", "往往", "通常", "一般说来", "大致", "有一定的",
]
ZH_CODAS = ["希望以上内容", "希望对你有帮助", "感谢你的阅读", "欢迎在评论区", "以上就是我的分享"]

EN_STRONG = [
    "delve", "utilize", "leverage", "facilitate", "elucidate", "embark",
    "endeavor", "encompass", "multifaceted", "tapestry", "testament",
    "paradigm", "synergy", "holistic", "catalyze", "juxtapose", "realm",
    "myriad", "plethora", "robust", "comprehensive", "seamless",
    "cutting-edge", "innovative", "streamline", "empower", "foster",
    "enhance", "elevate", "optimize", "scalable", "pivotal", "intricate",
    "profound", "resonate", "underscore", "harness", "cultivate", "bolster",
    "galvanize", "cornerstone", "game-changer",
]
EN_FILLER = [
    "it's worth noting", "it is worth noting", "it's important to note",
    "it is important to note", "let's dive", "let's explore", "let's unpack",
    "in today's", "moreover", "furthermore", "additionally", "in conclusion",
    "to summarize", "as we can see", "when it comes to", "at the end of the day",
    "it goes without saying", "without further ado", "great question",
    "that's an excellent point",
]

AI_EMOJI = set("✅🧠🔷☑️✔️")

ZH_OPENERS = [
    "值得注意的是", "不可否认", "毋庸置疑", "众所周知", "值得一提的是",
    "在当今", "随着", "在这个", "在数字化", "在信息化", "在全球化", "近年来",
    "在当前", "在万物互联", "首先", "第一",
]
EN_OPENERS = ["in today's", "it's worth noting", "it is worth noting", "in the realm of"]

ZH_NEG_PARALLEL = re.compile(r"不[只仅]是.{0,40}?(更是|也是|而且是|同时也是)")
ZH_NEG_PARALLEL2 = re.compile(r"不是.{0,30}?而是")
ZH_TRIAD = re.compile(r"首先.{0,80}?其次.{0,80}?(?:最后|最终|再次)|第一.{0,40}?第二.{0,40}?第三")
ZH_TIME_OPENER = re.compile(
    r"在当今|在信息化|在数字化|在全球化"
    r"|随着.{0,12}(?:发展|进步|普及|加速)"
    r"|在.{0,10}(?:时代|浪潮|大背景下|背景下)"
)
EN_NEG_PARALLEL = re.compile(
    r"(?:not just|isn'?t just|is not just|not merely|isn'?t merely|not only)\b"
    r".{0,60}?\b(?:but|it'?s|it is)\b",
    re.I,
)

EMOJI_RE = re.compile(
    "[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F000-\U0001F2FF"
    "\U00002B00-\U00002BFF" "\U0000FE00-\U0000FE0F" "]+"
)


def split_sentences(text):
    return [s.strip() for s in re.split(r"[。！？!?.\n]+", text) if s.strip()]


def count_phrase(text, phrase, ci=True):
    hay = text.lower() if ci else text
    needle = phrase.lower() if ci else phrase
    return hay.count(needle)


def analyze(text):
    n_chars = len(text)
    cjk = len(re.findall(r"[一-鿿]", text))
    per1k = (lambda c: round(c * 1000.0 / n_chars, 2) if n_chars else 0.0)

    # count em-dash *uses*: each "——" pair = 1, each lone "—" = 1
    em_dash = text.count("——") + max(0, text.count("—") - 2 * text.count("——"))
    colon = text.count("：") + text.count(":")
    zh_hits = {p: count_phrase(text, p, ci=False) for p in ZH_STRONG + ZH_HEDGE}
    zh_hits = {k: v for k, v in zh_hits.items() if v}
    en_hits = {p: count_phrase(text, p) for p in EN_STRONG + EN_FILLER}
    en_hits = {k: v for k, v in en_hits.items() if v}
    hedge = sum(count_phrase(text, p, ci=False) for p in ZH_HEDGE)

    emojis = EMOJI_RE.findall(text)
    ai_emoji = [e for e in emojis if any(ch in AI_EMOJI for ch in e)]

    neg = (len(ZH_NEG_PARALLEL.findall(text)) + len(ZH_NEG_PARALLEL2.findall(text))
           + len(EN_NEG_PARALLEL.findall(text)))
    triad = len(ZH_TRIAD.findall(text))
    time_opener = bool(ZH_TIME_OPENER.search(text))

    sents = split_sentences(text)
    lens = [len(s) for s in sents]
    if len(lens) >= 4:  # too few sentences -> burstiness unreliable
        mean = sum(lens) / len(lens)
        var = sum((l - mean) ** 2 for l in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0.0
    else:
        cv = None

    phrase_hits = sum(zh_hits.values()) + sum(en_hits.values())

    head = text.lstrip()
    tail = text[-30:]
    opening_formula = any(head.startswith(o) for o in ZH_OPENERS) \
        or any(head.lower().startswith(o) for o in EN_OPENERS)
    closing_formula = any(c in tail for c in ZH_CODAS) \
        or any(c in tail.lower() for c in ("in conclusion", "hope this helps", "to summarize"))

    # ---- score (0-100) ----
    score = 0.0
    score += min(30.0, phrase_hits * 3.0)                 # stock phrases (absolute)
    if n_chars >= 400:                                    # only long docs get density
        score += min(10.0, per1k(phrase_hits) * 1.2)
    score += 0.0 if em_dash <= 2 else min(15.0, (em_dash - 2) * 4.0)   # ≤2 uses is fine
    score += 0.0 if colon <= 2 else min(8.0, (colon - 2) * 2.0)
    score += 10.0 if ai_emoji else 0.0                    # ✅🧠🔷
    score += min(10.0, hedge * 2.0)                       # hedging
    score += 8.0 if neg else 0.0                          # negative parallelism
    score += 12.0 if triad else 0.0                       # 首先…其次…最后
    score += 8.0 if time_opener else 0.0                  # 在当今…/随着…发展
    if cv is not None:                                    # burstiness
        score += 20.0 if cv < 0.35 else 12.0 if cv < 0.50 else 5.0 if cv < 0.65 else 0.0
    score += 8.0 if opening_formula else 0.0              # 废话开场 / AI opening
    score += 8.0 if closing_formula else 0.0              # AI 尾气
    score = int(round(max(0.0, min(100.0, score))))

    if score <= 12:
        band = "人类"
    elif score <= 32:
        band = "基本人味(可能轻度润色)"
    elif score <= 55:
        band = "可疑 / AI 辅助"
    elif score <= 80:
        band = "AI 味明显"
    else:
        band = "纯 AI slop"

    return {
        "chars": n_chars,
        "cjk": cjk,
        "sentences": len(sents),
        "score": score,
        "band": band,
        "em_dash_uses": em_dash,
        "em_dash_per_1k": per1k(em_dash),
        "opening_formula": opening_formula,
        "closing_formula": closing_formula,
        "colon": colon,
        "colon_per_1k": per1k(colon),
        "hedge_count": hedge,
        "negative_parallelism": neg,
        "triad": triad,
        "time_opener": time_opener,
        "ai_emoji": ai_emoji,
        "sentence_cv": round(cv, 3) if cv is not None else None,
        "zh_hits": zh_hits,
        "en_hits": en_hits,
    }


def report(r):
    print(f"评分: {r['score']}/100  →  {r['band']}")
    print(f"字数: {r['chars']} (汉字 {r['cjk']}) | 句数: {r['sentences']}")
    print(f"长破折号(处): {r['em_dash_uses']}  ({r['em_dash_per_1k']}/千字)")
    if r["opening_formula"]:
        print("开场: 疑似废话开场 / AI opening")
    if r["closing_formula"]:
        print("结尾: 疑似 AI 尾气")
    print(f"冒号: {r['colon']}  ({r['colon_per_1k']}/千字)")
    print(f"软化剂: {r['hedge_count']} | 负向平行句: {r['negative_parallelism']}"
          f" | 三段式(首先其次最后): {r['triad']}"
          f" | 时间开头: {'有' if r['time_opener'] else '无'}")
    if r["ai_emoji"]:
        print(f"异常 emoji: {' '.join(r['ai_emoji'])}")
    if r["sentence_cv"] is not None:
        flag = "偏低(句长太均匀)" if r["sentence_cv"] < 0.5 else "正常"
        print(f"句长方差系数 CV: {r['sentence_cv']}  {flag}")
    if r["zh_hits"]:
        print("\n命中中文词:")
        for k, v in sorted(r["zh_hits"].items(), key=lambda x: -x[1]):
            print(f"  {v}× {k}")
    if r["en_hits"]:
        print("\n命中英文词:")
        for k, v in sorted(r["en_hits"].items(), key=lambda x: -x[1]):
            print(f"  {v}× {k}")
    print("\n注: 这是量化底座,不是结论。请同时通读文本(结构类特征脚本抓不到)。")


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]
    if args:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    r = analyze(text)
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        report(r)


if __name__ == "__main__":
    main()
