# セッション引継ぎ資料

**作成日**: 2026-04-05  
**リポジトリ**: `rtaka1122/.claude`  
**作業ブランチ**: `claude/nail-file-pricing-strategy-CoKQO`

---

## 1. プロジェクト概要

**ブランド**: TSUMETOGI MAFIA  
**新商品**: ヤスリ付き爪とぎ（シンプル形状・シュリンク包装）

### 商品特徴
- 強化段ボール素材：研ぎくず65%削減 / 耐久3倍
- シンプル形状（平型）
- ヤスリ機能付き（爪の長さを整えられる）
- シュリンク包装

### コスト構造
| 項目 | 数値 |
|------|------|
| 単品原価（シュリンク込） | 222円 |
| ケース入数 | 60本 |
| ケース原価 | 13,320円 + 送料 |
| **最低卸値/ケース** | **29,400円** |
| **最低卸値/本** | **490円** |
| 最低卸値でのメーカー粗利率 | 約54.7% |

### 既存商品との関係
| 商品 | 形状 | 価格 | チャネル |
|------|------|------|----------|
| つめまる | 独自形状 | 6,980円 | EC専売（高原価のため小売なし） |
| **本商品** | シンプル | **TBD** | **小売主力** |

---

## 2. ターゲットチャネル

- ホームセンター（カインズ・コーナン等）
- ペット専門店（コジマペット・ペットセンターグループ等）
- ドラッグストア・GMS（ウエルシア・ドン・キホーテ等）

---

## 3. 作成済みドキュメント

### `docs/pricing-research/nail-file-scratcher-pricing-strategy.md`
- Phase 1: コスト・チャネル構造の整理
- Phase 2: 市場競合調査設計
- Phase 3: PSM分析（Van Westendorp）設計書
- Phase 4: Gabor-Granger調査設計書（680〜2,980円の6価格帯）
- Phase 5: チャネル別価格戦略設計
- Phase 6: テスト販売計画

### 現時点の価格仮説
| チャネル | 推奨上代 |
|----------|----------|
| ホームセンター | 980〜1,280円 |
| ペット専門店 | 1,480〜1,980円 |
| ドラッグストア・GMS | 980〜1,480円 |
| EC | 1,480〜2,480円 |
| 最低卸値/本 | 490円（固定） |

---

## 4. 次セッションでやること（最優先）

### 未完了タスク: 市場調査データの読み込みと調査設計の更新

ユーザーがWindows PC（`C:\Users\RT\claude\input\`）に以下のファイルを保有している：

```
C:\Users\RT\claude\input\爪とぎ市場調査と価格設定提案.md
```

**内容**: 実際に店舗で販売されている爪とぎの価格帯調査データ

**やること**:
1. 上記ファイルをリポジトリの `input/` フォルダに追加してもらう（またはチャットに貼り付けてもらう）
2. 内容を読み込む
3. 実際の市場データを踏まえて `docs/pricing-research/nail-file-scratcher-pricing-strategy.md` を更新する
4. 価格仮説を実態に即して修正する

### ファイルの取り込み方法（ユーザーに伝えること）

以下のいずれかを依頼する：

**A. GitHubにpush（推奨）**
```powershell
cd C:\Users\RT\claude
git checkout claude/nail-file-pricing-strategy-CoKQO
git add input/
git commit -m "add market research input"
git push origin claude/nail-file-pricing-strategy-CoKQO
```
→ push後 `git pull` して読み込む

**B. チャットに貼り付け**
- ファイルを開いて全文コピー → チャットに貼り付け

---

## 5. Git状態

```
ブランチ: claude/nail-file-pricing-strategy-CoKQO
最新コミット: 5a63453 add pricing research design for nail-file cat scratcher
リモート: origin (rtaka1122/.claude) にpush済み
```

---

## 6. 保留・中止した作業

- **経営報告用LINEボット**: ユーザーの意図と合わなかったため中止。必要になれば改めて要件定義から実施する。

---

## 7. 備考

- ユーザーのローカル環境: Windows (`C:\Users\RT\claude`)
- Linux環境（このClaude Code）とWindows間のファイル共有はGit経由で行う
- 価格調査の目標: 小売で「無双できる状態」を作ること
- 2,980円までの価格帯も視野に入れて調査設計済み
