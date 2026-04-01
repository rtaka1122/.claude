from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# === カラーパレット ===
BLACK      = RGBColor(0x1A, 0x1A, 0x2E)   # 背景
DARK_GRAY  = RGBColor(0x16, 0x21, 0x3E)   # カード背景
ACCENT     = RGBColor(0xE9, 0x4F, 0x37)   # アクセント（赤）
GOLD       = RGBColor(0xF5, 0xA6, 0x23)   # ゴールド（強調）
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xB0, 0xB8, 0xC8)
TEAL       = RGBColor(0x39, 0xC0, 0xBA)   # ティール（議論マーカー）

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # 完全ブランク


# ────────────────────────────────────────────
# ヘルパー関数
# ────────────────────────────────────────────

def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=Pt(0)):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # MSO_SHAPE_TYPE.RECTANGLE
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape

def add_textbox(slide, left, top, width, height, text, font_size=Pt(14),
                bold=False, color=WHITE, align=PP_ALIGN.LEFT, wrap=True, line_spacing=None):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = color
    if line_spacing:
        from pptx.util import Pt as pt2
        from pptx.oxml.ns import qn
        from lxml import etree
        pPr = p._pPr
        if pPr is None:
            pPr = p._p.get_or_add_pPr()
        lnSpc = etree.SubElement(pPr, qn('a:lnSpc'))
        spcPts = etree.SubElement(lnSpc, qn('a:spcPts'))
        spcPts.set('val', str(int(line_spacing * 100)))
    return txBox

def bg(slide):
    """スライド全体に背景色を敷く"""
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill_color=BLACK)

def header_bar(slide, title, subtitle=None):
    """上部ヘッダーバー"""
    add_rect(slide, 0, 0, SLIDE_W, Inches(1.1), fill_color=DARK_GRAY)
    add_rect(slide, 0, Inches(1.05), SLIDE_W, Pt(3), fill_color=ACCENT)
    add_textbox(slide, Inches(0.5), Inches(0.12), Inches(11), Inches(0.6),
                title, font_size=Pt(26), bold=True, color=WHITE)
    if subtitle:
        add_textbox(slide, Inches(0.5), Inches(0.68), Inches(10), Inches(0.35),
                    subtitle, font_size=Pt(13), color=LIGHT_GRAY)

def discussion_badge(slide, left, top, text="議論"):
    """ティール色の議論バッジ"""
    add_rect(slide, left, top, Inches(0.8), Inches(0.28), fill_color=TEAL)
    add_textbox(slide, left, top, Inches(0.8), Inches(0.28),
                text, font_size=Pt(9), bold=True, color=BLACK, align=PP_ALIGN.CENTER)

def slide_number(slide, n, total):
    add_textbox(slide, Inches(12.5), Inches(7.15), Inches(0.8), Inches(0.3),
                f"{n} / {total}", font_size=Pt(9), color=LIGHT_GRAY, align=PP_ALIGN.RIGHT)


TOTAL = 10

# ════════════════════════════════════════════
# スライド 1：表紙
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
# アクセントライン
add_rect(sl, Inches(0.5), Inches(2.5), Inches(0.08), Inches(3.2), fill_color=ACCENT)
# タイトル
add_textbox(sl, Inches(0.8), Inches(2.1), Inches(10), Inches(0.8),
            "Nyans", font_size=Pt(18), color=GOLD)
add_textbox(sl, Inches(0.8), Inches(2.65), Inches(10), Inches(1.0),
            "マネジメント・プリンシプル", font_size=Pt(36), bold=True, color=WHITE)
add_textbox(sl, Inches(0.8), Inches(3.7), Inches(10), Inches(0.5),
            "Management Principles", font_size=Pt(18), color=LIGHT_GRAY)
add_textbox(sl, Inches(0.8), Inches(4.5), Inches(6), Inches(0.4),
            "経営陣協議用  |  2026-04-01  |  原案（協議中）",
            font_size=Pt(12), color=LIGHT_GRAY)
# 猫モチーフ装飾
add_textbox(sl, Inches(10.0), Inches(2.8), Inches(2.5), Inches(2.0),
            "🐱", font_size=Pt(72), color=WHITE, align=PP_ALIGN.CENTER)
slide_number(sl, 1, TOTAL)

# ════════════════════════════════════════════
# スライド 2：アジェンダ & この場で決めること
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "この場で決めること", "本日のゴール")

items = [
    ("01", "言葉への合意",    "本プリンシプルの表現に全員が納得しているか\n合意 or 修正箇所の特定"),
    ("02", "現状とのギャップ", "自分たちの現状と、どれくらいズレがあるか\n認識を合わせる"),
    ("03", "最初の一手",      "まず何から動かすか\nアクションを決定する"),
]
for i, (num, title, desc) in enumerate(items):
    lft = Inches(0.4 + i * 4.28)
    add_rect(sl, lft, Inches(1.35), Inches(4.0), Inches(5.6), fill_color=DARK_GRAY)
    add_rect(sl, lft, Inches(1.35), Inches(4.0), Pt(3), fill_color=ACCENT)
    add_textbox(sl, lft + Inches(0.2), Inches(1.55), Inches(3.6), Inches(0.7),
                num, font_size=Pt(32), bold=True, color=ACCENT)
    add_textbox(sl, lft + Inches(0.2), Inches(2.25), Inches(3.6), Inches(0.55),
                title, font_size=Pt(18), bold=True, color=WHITE)
    add_textbox(sl, lft + Inches(0.2), Inches(2.9), Inches(3.5), Inches(2.5),
                desc, font_size=Pt(13), color=LIGHT_GRAY)
slide_number(sl, 2, TOTAL)

# ════════════════════════════════════════════
# スライド 3：アジェンダ（流れ）
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "本日のアジェンダ")

agenda = [
    ("1.  基本思想（Core Philosophy）",  "共通の哲学・言語を確認する"),
    ("2.  マネージャーの定義",           "役割・スタンスへの合意"),
    ("3.  3 つの柱（Pillars）",          "行動指針の具体化"),
    ("4.  Do / Don't",                   "推奨・禁止行動の確認"),
    ("5.  セルフチェック",               "運用方法を決める"),
    ("6.  クロージング",                 "アクション・担当・期限を決定"),
]
for i, (title, sub) in enumerate(agenda):
    top = Inches(1.3 + i * 0.97)
    add_rect(sl, Inches(0.5), top + Inches(0.1), Pt(4), Inches(0.65), fill_color=ACCENT)
    add_textbox(sl, Inches(0.7), top, Inches(9.5), Inches(0.48),
                title, font_size=Pt(16), bold=True, color=WHITE)
    add_textbox(sl, Inches(0.7), top + Inches(0.46), Inches(9.5), Inches(0.38),
                sub, font_size=Pt(12), color=LIGHT_GRAY)
slide_number(sl, 3, TOTAL)

# ════════════════════════════════════════════
# スライド 4：Core Philosophy
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "1. マネジメントの基本思想（Core Philosophy）")

# 哲学ステートメント
add_rect(sl, Inches(0.5), Inches(1.25), Inches(12.33), Inches(1.5), fill_color=DARK_GRAY)
add_rect(sl, Inches(0.5), Inches(1.25), Pt(4), Inches(1.5), fill_color=GOLD)
add_textbox(sl, Inches(0.75), Inches(1.35), Inches(11.8), Inches(1.3),
            "「譲れない誇りを土台に、圧倒的スピードで顧客インサイトに迫るチームを創る」",
            font_size=Pt(18), bold=True, color=GOLD)

# 猫メタファー
add_textbox(sl, Inches(0.5), Inches(3.0), Inches(7.5), Inches(0.35),
            "Nyans の猫メタファー", font_size=Pt(13), bold=True, color=TEAL)
add_textbox(sl, Inches(0.5), Inches(3.35), Inches(7.5), Inches(1.8),
            "猫が高い場所から躊躇なくジャンプできるのは、\n「ここなら安全に着地できる」という確かな足場があるから。\n\n→ 守るべき境界線を明確にすることで、\n　 メンバーは忖度なく最速で動ける。",
            font_size=Pt(13), color=LIGHT_GRAY)

# 議論ボックス
add_rect(sl, Inches(8.4), Inches(2.85), Inches(4.4), Inches(3.8), fill_color=DARK_GRAY)
add_rect(sl, Inches(8.4), Inches(2.85), Inches(4.4), Pt(3), fill_color=TEAL)
discussion_badge(sl, Inches(8.55), Inches(3.0))
add_textbox(sl, Inches(8.55), Inches(3.35), Inches(4.0), Inches(0.4),
            "議論 1-A", font_size=Pt(12), bold=True, color=TEAL)
add_textbox(sl, Inches(8.55), Inches(3.75), Inches(4.0), Inches(1.3),
            "この哲学に「自分たちらしさ」を感じるか？\n違和感のある言葉や、抜け落ちている\n視点はあるか？",
            font_size=Pt(12), color=WHITE)
add_textbox(sl, Inches(8.55), Inches(5.1), Inches(4.0), Inches(0.4),
            "議論 1-B", font_size=Pt(12), bold=True, color=TEAL)
add_textbox(sl, Inches(8.55), Inches(5.5), Inches(4.0), Inches(1.0),
            "「圧倒的スピード」vs「譲れない誇り」\n今の Nyans はどちらをより強調すべきか？",
            font_size=Pt(12), color=WHITE)
slide_number(sl, 4, TOTAL)

# ════════════════════════════════════════════
# スライド 5：マネージャーの定義
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "2. Nyans における「マネージャー」の定義")

# 2カラム：役割
cols = [
    ("🛡️  防波堤（シールド）", "理不尽な要求や過度なノイズから\nメンバーを守る盾になること。\n\n心理的安全性をマネージャーが\n自ら担保するからこそ、メンバーは\n安心して圧倒的スピードで挑戦できる。"),
    ("🏃  成長の伴走者", "業務を通じて本人の内発的動機\n（Will）を引き出すこと。\n\n「この仕事でこのメンバーに\nどう成長してほしいか」という\n育成責任を負う。"),
]
for i, (ttl, desc) in enumerate(cols):
    lft = Inches(0.4 + i * 4.0)
    add_rect(sl, lft, Inches(1.3), Inches(3.7), Inches(4.0), fill_color=DARK_GRAY)
    add_rect(sl, lft, Inches(1.3), Inches(3.7), Pt(3), fill_color=ACCENT)
    add_textbox(sl, lft + Inches(0.2), Inches(1.5), Inches(3.3), Inches(0.5),
                ttl, font_size=Pt(14), bold=True, color=WHITE)
    add_textbox(sl, lft + Inches(0.2), Inches(2.1), Inches(3.3), Inches(3.0),
                desc, font_size=Pt(12), color=LIGHT_GRAY)

# 議論ボックス
add_rect(sl, Inches(8.4), Inches(1.3), Inches(4.4), Inches(5.5), fill_color=DARK_GRAY)
add_rect(sl, Inches(8.4), Inches(1.3), Inches(4.4), Pt(3), fill_color=TEAL)
discussion_badge(sl, Inches(8.55), Inches(1.45))
add_textbox(sl, Inches(8.55), Inches(1.8), Inches(4.0), Inches(0.4),
            "議論 2-A", font_size=Pt(12), bold=True, color=TEAL)
add_textbox(sl, Inches(8.55), Inches(2.2), Inches(4.0), Inches(1.2),
            "「防波堤」と「伴走者」、\n今の自分はどちら寄りか？\n足りていないのはどちらか？",
            font_size=Pt(12), color=WHITE)
add_textbox(sl, Inches(8.55), Inches(3.5), Inches(4.0), Inches(0.4),
            "議論 2-B", font_size=Pt(12), bold=True, color=TEAL)
add_textbox(sl, Inches(8.55), Inches(3.9), Inches(4.0), Inches(1.5),
            "「自分のモノサシを捨てる」は\n具体的にどんな場面で難しいか？\n直近の事例を一つ挙げてみる。",
            font_size=Pt(12), color=WHITE)
slide_number(sl, 5, TOTAL)

# ════════════════════════════════════════════
# スライド 6：3つの柱
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "3. マネジメントを支える 3 つの柱（Pillars）")

pillars = [
    ("Pillar 1", "「譲れない土台」×\n「圧倒的スピード」",
     "品質・コンプライアンスは1ミリも妥協しない。\nその枠の中では「まずやってみる」を求める。",
     "「絶対に守るべきライン」とは何か？\n全員が同じものを思い浮かべているか\n今ここで言語化する。"),
    ("Pillar 2", "「経験則」を捨て\n「事実」で対話する",
     "判断軸は「ユーザーインサイト」と「データ」のみ。\nヒト（感情）とコト（成果）を切り離して対話。",
     "「ヒトとコトを切り離す」ことが\n今の社内でできているか？\nできていない場面はいつか？"),
    ("Pillar 3", "「聴き切る」対話で\n可能性を最大化する",
     "1on1 は「指導の場」ではなく「思考整理の場」。\n積極的傾聴で自燃性を育てる。",
     "1on1 の現状は？\n「聴き切る場」として機能しているか？"),
]
for i, (num, ttl, desc, disc) in enumerate(pillars):
    lft = Inches(0.35 + i * 4.3)
    add_rect(sl, lft, Inches(1.25), Inches(4.0), Inches(5.7), fill_color=DARK_GRAY)
    add_rect(sl, lft, Inches(1.25), Inches(4.0), Pt(3), fill_color=ACCENT)
    add_textbox(sl, lft + Inches(0.2), Inches(1.4), Inches(3.6), Inches(0.4),
                num, font_size=Pt(12), bold=True, color=ACCENT)
    add_textbox(sl, lft + Inches(0.2), Inches(1.8), Inches(3.6), Inches(0.85),
                ttl, font_size=Pt(15), bold=True, color=WHITE)
    add_textbox(sl, lft + Inches(0.2), Inches(2.7), Inches(3.6), Inches(1.5),
                desc, font_size=Pt(11), color=LIGHT_GRAY)
    # 区切り線
    add_rect(sl, lft + Inches(0.2), Inches(4.2), Inches(3.6), Pt(1), fill_color=TEAL)
    # 議論
    discussion_badge(sl, lft + Inches(0.2), Inches(4.35))
    add_textbox(sl, lft + Inches(0.2), Inches(4.7), Inches(3.5), Inches(1.8),
                disc, font_size=Pt(11), color=TEAL)
slide_number(sl, 6, TOTAL)

# ════════════════════════════════════════════
# スライド 7：Do / Don't
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "4. マネージャーの行動原則（Do / Don't）")

rows = [
    ("事実（データ・ユーザーの声）に基づき「次はどうすれば最速でうまくいくか」を共に考える",
     "経験則や感情でメンバーの提案を否定し、過去の失敗を責める"),
    ("「なぜこの仕事をお願いするか（目的・期待）」をセットで伝え、自由裁量の範囲を決めて任せる",
     "作業だけ丸投げし、途中のプロセスをマイクロマネジメントする"),
    ("トラブル・失敗の際、自ら最前線に出てメンバーを背中で守る",
     "メンバーを矢面に立たせ、自分は安全な場所から批判する"),
    ("意見を最後まで「聴き切り」、問いかけで本人の気づきを引き出す",
     "話の途中で遮り、自分の「正解」をすぐに押し付ける"),
]
# ヘッダー
add_rect(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(0.4), fill_color=RGBColor(0x22, 0x7B, 0x3C))
add_rect(sl, Inches(6.7), Inches(1.25), Inches(5.9), Inches(0.4), fill_color=RGBColor(0xB0, 0x26, 0x26))
add_textbox(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(0.4),
            "✅  Do", font_size=Pt(13), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(sl, Inches(6.7), Inches(1.25), Inches(5.9), Inches(0.4),
            "❌  Don't", font_size=Pt(13), bold=True, color=WHITE, align=PP_ALIGN.CENTER)

for i, (do, dont) in enumerate(rows):
    top = Inches(1.75 + i * 1.3)
    add_rect(sl, Inches(0.4), top, Inches(5.9), Inches(1.15), fill_color=DARK_GRAY)
    add_rect(sl, Inches(6.7), top, Inches(5.9), Inches(1.15), fill_color=DARK_GRAY)
    add_textbox(sl, Inches(0.6), top + Inches(0.12), Inches(5.5), Inches(0.95),
                do, font_size=Pt(11), color=WHITE)
    add_textbox(sl, Inches(6.9), top + Inches(0.12), Inches(5.5), Inches(0.95),
                dont, font_size=Pt(11), color=LIGHT_GRAY)

# 議論バッジ
discussion_badge(sl, Inches(0.4), Inches(7.0), "議論")
add_textbox(sl, Inches(1.3), Inches(7.0), Inches(11.5), Inches(0.35),
            "議論 4-A: 今の自分が最も「できていない Don't」はどれか？  　議論 4-B: 追加すべき Do / Don't はあるか？",
            font_size=Pt(11), color=TEAL)
slide_number(sl, 7, TOTAL)

# ════════════════════════════════════════════
# スライド 8：セルフチェック
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "5. 経営陣のセルフチェック", "日常の判断に迷った際、自らのスタイルを是正するためのチェックリスト")

checks = [
    "「自分の過去の経験則」でジャッジしていないか？",
    "スピードを阻害するような「マイクロマネジメント」をしていないか？",
    "相手の意見を途中で遮らず、最後まで「聴き切って」いるか？",
    "トラブル時に、自ら「矢面に立つ覚悟」を持てているか？",
]
for i, text in enumerate(checks):
    top = Inches(1.4 + i * 1.2)
    add_rect(sl, Inches(0.5), top, Inches(8.8), Inches(1.0), fill_color=DARK_GRAY)
    add_rect(sl, Inches(0.5), top, Pt(4), Inches(1.0), fill_color=GOLD)
    # チェックボックス風
    add_rect(sl, Inches(0.75), top + Inches(0.25), Inches(0.45), Inches(0.45),
             fill_color=BLACK, line_color=GOLD, line_width=Pt(1.5))
    add_textbox(sl, Inches(1.35), top + Inches(0.2), Inches(7.8), Inches(0.6),
                text, font_size=Pt(14), color=WHITE)

# 議論ボックス
add_rect(sl, Inches(9.7), Inches(1.25), Inches(3.3), Inches(5.2), fill_color=DARK_GRAY)
add_rect(sl, Inches(9.7), Inches(1.25), Inches(3.3), Pt(3), fill_color=TEAL)
discussion_badge(sl, Inches(9.85), Inches(1.4))
add_textbox(sl, Inches(9.85), Inches(1.8), Inches(2.9), Inches(0.4),
            "議論 5-A", font_size=Pt(12), bold=True, color=TEAL)
add_textbox(sl, Inches(9.85), Inches(2.2), Inches(2.9), Inches(3.5),
            "このチェックリストを\n「いつ・どこで・どう使うか」\nを決める。\n\n例：\n・週次定例の冒頭で1問確認\n・月次振り返りで全項目チェック",
            font_size=Pt(12), color=WHITE)
slide_number(sl, 8, TOTAL)

# ════════════════════════════════════════════
# スライド 9：クロージング
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
header_bar(sl, "6. クロージング：この場で決めること", "記入しながら合意形成を進める")

# テーブルヘッダー
cols_w = [Inches(3.0), Inches(4.5), Inches(2.5), Inches(2.5)]
cols_x = [Inches(0.4), Inches(3.5), Inches(8.1), Inches(10.7)]
headers = ["項目", "内容・決定事項", "担当", "期限"]
for j, (hdr, lft, w) in enumerate(zip(headers, cols_x, cols_w)):
    add_rect(sl, lft, Inches(1.25), w, Inches(0.42), fill_color=ACCENT)
    add_textbox(sl, lft + Inches(0.1), Inches(1.27), w - Inches(0.1), Inches(0.38),
                hdr, font_size=Pt(12), bold=True, color=WHITE)

table_rows = [
    "言葉の修正",
    "最初の一手（実践導入）",
    "共有範囲・展開方法",
    "次回確認日",
]
for i, label in enumerate(table_rows):
    top = Inches(1.77 + i * 1.18)
    row_color = DARK_GRAY if i % 2 == 0 else BLACK
    for j, (lft, w) in enumerate(zip(cols_x, cols_w)):
        add_rect(sl, lft, top, w, Inches(1.08), fill_color=row_color,
                 line_color=RGBColor(0x33, 0x3A, 0x52), line_width=Pt(0.5))
    add_textbox(sl, cols_x[0] + Inches(0.1), top + Inches(0.25), cols_w[0] - Inches(0.1), Inches(0.6),
                label, font_size=Pt(12), bold=True, color=WHITE)
slide_number(sl, 9, TOTAL)

# ════════════════════════════════════════════
# スライド 10：エンドカード
# ════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
bg(sl)
add_rect(sl, 0, 0, SLIDE_W, SLIDE_H, fill_color=BLACK)
add_rect(sl, Inches(0.5), Inches(3.5), Inches(12.33), Pt(1.5), fill_color=ACCENT)
add_textbox(sl, 0, Inches(1.6), SLIDE_W, Inches(1.0),
            "🐱", font_size=Pt(48), color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(sl, 0, Inches(2.8), SLIDE_W, Inches(0.6),
            "猫はジャンプする前に、着地点を見極める。",
            font_size=Pt(16), color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
add_textbox(sl, 0, Inches(3.7), SLIDE_W, Inches(0.7),
            "Nyans のマネージャーも、メンバーが安心して跳べる場所をつくり続ける。",
            font_size=Pt(16), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(sl, 0, Inches(5.0), SLIDE_W, Inches(0.5),
            "Nyans Management Principles  |  2026-04-01",
            font_size=Pt(12), color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
slide_number(sl, 10, TOTAL)

# ════════════════════════════════════════════
# 保存
# ════════════════════════════════════════════
out = "/home/user/.claude/nyans_management_principles.pptx"
prs.save(out)
print(f"Saved: {out}")
