import os
import google.generativeai as genai
import streamlit as st

# 1. ページの基本設定（タイトルとアイコン）
st.set_page_config(
    page_title="🌸 詩と言葉の鑑賞室", page_icon="🌸", layout="centered"
)

# 2. タイトルと説明の表示
st.title("🌸 詩と言葉の鑑賞室")
st.caption(
    "あなたが綴った言葉を受け止め、温かい感想と「返歌（短い詩）」をお届けします。"
)
st.markdown("---")

# 3. APIキーの読み込み（ネット公開用 ＆ テスト用）
api_key = os.getenv("GEMINI_API_KEY")

# APIキーが未設定の場合だけ、画面の横（サイドバー）に入力欄を出す
if not api_key:
    with st.sidebar:
        st.header("⚙️ APIキー設定")
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Google AI Studioで取得したAPIキーを入力してください",
        )

# 4. ポエムの入力欄
poem_text = st.text_area(
    "📝 あなたのポエム・文章を入力してください",
    height=180,
    placeholder="静寂の夜に落とした\nひとつぶの青い言葉\n誰にも届かなくていいと\n掌で温めていた",
)

# 5. AIへの指示（プロンプト）
SYSTEM_PROMPT = """
あなたは繊細な感性と豊かな語彙力を持つ「詩人・文章鑑賞のプロ」です。
ユーザーから投稿されたポエム（詩・文章）を鑑賞し、作者の感性を尊重しながら以下のフォーマットで温かい評価と「返歌（へんか）」を出力してください。

【出力フォーマット】
✨ **立ち現れた世界観・情景**
（読んだ時に浮かんだビジュアル、空気感、感情を100文字程度で描写）

💎 **心に響いたフレーズ**
（特に言葉選びや表現が素晴らしい部分を引用し、なぜ良いかを解説）

📊 **感性パラメータ**
・世界観の深さ：★★★★☆
・言葉選びの美しさ：★★★★★
・リズム・響き：★★★☆☆
・余韻の残り方：★★★★★

🌸 **AIからの「返歌（へんか）」**
（投稿されたポエムのモチーフや感情、言葉の響きを優しく受け止め、それに応答するように紡いだ2〜4行程度の短い詩）

💡 **さらに表現を研ぎ澄ますためのヒント**
（批判は絶対にせず、「ここをこう変えるとさらに情景が際立つ」という温かい提案を1つだけ）

※語り口調は柔らかく、共感的で、作者の書きたい気持ちを応援するトーンを徹底してください。
"""

# 6. ボタンを押した時の処理
if st.button("✨ 鑑賞・返歌を受け取る", type="primary"):
    if not api_key:
        st.error(
            "🔑 APIキーが読み込めていません。画面左側のメニューからAPIキーを入力してください。"
        )
    elif not poem_text.strip():
        st.warning("✍️ ポエム本文を入力してください。")
    else:
        with st.spinner("言葉の余韻を味わっています..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"{SYSTEM_PROMPT}\n\n【評価対象のポエム】\n{poem_text}"
                response = model.generate_content(prompt)

                st.markdown("---")
                st.subheader("📖 鑑賞結果 & 返歌")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")