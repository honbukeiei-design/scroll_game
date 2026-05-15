import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="院内トラブル即応シミュレーション", layout="wide")

st.title("院内トラブル即応シミュレーション：部署別ステージ版")
st.caption("受付・総務課・医事課・経営企画課・人事課で発生する突発イベントに即応する横スクロール型ゲーム")

GAME_HTML = r"""
<div id="gameRoot">
  <div class="topPanel">
    <div>
      <div class="mainTitle">🏥 院内トラブル即応ランナー</div>
      <div class="subtitle">部署を選び、発生するトラブルに正しく対応してください</div>
    </div>
    <div class="scorePanel">
      <div>部署: <span id="departmentName">未選択</span></div>
      <div>ステージ: <span id="stageNo">0</span>/<span id="stageTotal">0</span></div>
      <div>スコア: <span id="score">0</span></div>
      <div>状態: <span id="statusText">部署選択中</span></div>
    </div>
  </div>
  <div class="departmentSelect">
    <button onclick="selectDepartment('reception')">受付</button>
    <button onclick="selectDepartment('general')">総務課</button>
    <button onclick="selectDepartment('medical')">医事課</button>
    <button onclick="selectDepartment('planning')">経営企画課</button>
    <button onclick="selectDepartment('hr')">人事課</button>
  </div>
  <div id="scene" class="scene reception">
    <div class="parallax back"></div><div class="parallax mid"></div>
    <div class="sign" id="placeSign">部署を選択</div>
    <div class="eventCard"><div class="eventIcon" id="eventIcon">🏥</div><div><div class="eventTitle" id="eventTitle">部署を選択してください</div><div class="eventDesc" id="eventDesc">上のボタンから部署を選ぶとゲームが始まります。</div></div></div>
    <div class="runner" id="runner"><div class="runnerShadow"></div><div class="runnerBody" id="runnerBody">👩‍💼</div></div>
    <button class="choiceButton choiceA" onclick="jumpTo('A')"><span class="choiceKey">A</span><span class="choiceText" id="choiceAText">A</span></button>
    <button class="choiceButton choiceB" onclick="jumpTo('B')"><span class="choiceKey">B</span><span class="choiceText" id="choiceBText">B</span></button>
    <button class="choiceButton choiceC" onclick="jumpTo('C')"><span class="choiceKey">C</span><span class="choiceText" id="choiceCText">C</span></button>
    <div class="ground"></div>
    <div class="message" id="messageBox"><div id="messageText">部署を選択してください。</div></div>
    <div class="gameOver" id="gameOver"><h2>アウト！</h2><p id="gameOverReason"></p><button onclick="restartDepartment()">同じ部署でもう一度</button><button onclick="backToDepartmentSelect()">部署選択へ戻る</button></div>
    <div class="gameClear" id="gameClear"><h2>クリア！</h2><p id="clearMessage">全イベントを適切に対応できました。</p><p>最終スコア: <span id="finalScore"></span></p><button onclick="restartDepartment()">同じ部署でもう一度</button><button onclick="backToDepartmentSelect()">部署選択へ戻る</button></div>
  </div>
  <div class="help">操作：ゲーム画面内の <b>A/B/Cボタン</b> をクリック、またはキーボードの <b>A / B / C</b>。正解なら次へ進み、不正解ならアウトです。出題順は部署選択のたびにランダムです。</div>
</div>
<style>
#gameRoot { font-family: "Yu Gothic", "Meiryo", system-ui, sans-serif; color: #0f172a; }
.topPanel { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 12px; }
.mainTitle { font-size: 24px; font-weight: 900; }
.subtitle { color: #475569; font-weight: 700; }
.scorePanel { display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
.scorePanel div { background: #fff; border: 1px solid #cbd5e1; border-radius: 999px; padding: 8px 12px; font-weight: 900; box-shadow: 0 4px 12px rgba(15,23,42,.08); }
.departmentSelect { display: flex; gap: 10px; flex-wrap: wrap; margin: 8px 0 14px; }
.departmentSelect button { border: 0; border-radius: 999px; padding: 11px 18px; font-weight: 900; color: white; background: #2563eb; box-shadow: 0 8px 16px rgba(37,99,235,.22); cursor: pointer; }
.departmentSelect button:hover { transform: translateY(-2px); filter: brightness(1.05); }
.scene { position: relative; height: 650px; overflow: hidden; border-radius: 24px; border: 2px solid #cbd5e1; box-shadow: 0 20px 40px rgba(15,23,42,.12); background: linear-gradient(#bfdbfe, #eff6ff 42%, #f8fafc 42%); }
.scene.reception { --accent:#2563eb; --bg1:#dbeafe; --bg2:#eff6ff; }
.scene.general { --accent:#0f766e; --bg1:#ccfbf1; --bg2:#f0fdfa; }
.scene.medical { --accent:#7c3aed; --bg1:#ede9fe; --bg2:#faf5ff; }
.scene.management { --accent:#ea580c; --bg1:#ffedd5; --bg2:#fff7ed; }
.scene.hr { --accent:#db2777; --bg1:#fce7f3; --bg2:#fff1f2; }
.parallax { position: absolute; inset: 0; background-repeat: repeat-x; }
.parallax.back { background: linear-gradient(var(--bg1), var(--bg2)); }
.parallax.mid { background-image: linear-gradient(90deg, transparent 0 30px, rgba(255,255,255,.88) 30px 120px, transparent 120px 180px), linear-gradient(90deg, transparent 0 60px, rgba(15,23,42,.10) 60px 64px, transparent 64px 180px); background-size: 260px 190px, 260px 190px; background-position: 0 190px, 0 190px; animation: scrollBg 18s linear infinite; }
.scene.running .parallax.mid { animation-duration: 5.5s; }
.sign { position: absolute; left: 32px; top: 28px; font-size: 24px; font-weight: 900; color: white; background: var(--accent); border-radius: 999px; padding: 10px 18px; box-shadow: 0 10px 20px rgba(15,23,42,.16); z-index: 5; }
.eventCard { position: absolute; left: 50%; top: 42px; transform: translateX(-50%); width: 650px; min-height: 96px; background: rgba(255,255,255,.95); border: 3px solid var(--accent); border-radius: 22px; display: flex; gap: 16px; align-items: center; padding: 14px 18px; box-shadow: 0 16px 34px rgba(15,23,42,.16); z-index: 10; }
.eventIcon { font-size: 44px; animation: warningPulse .8s infinite alternate; }
.eventTitle { font-size: 22px; font-weight: 900; }
.eventDesc { font-size: 14px; line-height: 1.55; color: #334155; }
.runner { position: absolute; left: 118px; bottom: 95px; width: 78px; height: 96px; z-index: 20; }
.runnerBody { position: absolute; font-size: 64px; left: 0; top: 0; filter: drop-shadow(0 10px 12px rgba(15,23,42,.22)); animation: runBob .45s infinite alternate; }
.runnerShadow { position: absolute; width: 72px; height: 16px; left: 3px; bottom: 0; background: rgba(15,23,42,.18); border-radius: 50%; filter: blur(1px); }
.runner.jumpA, .runner.jumpB, .runner.jumpC { animation: jumpArc .72s ease-out forwards; }
.choiceButton { position: absolute; right: -380px; width: 330px; min-height: 88px; background: white; border: 3px solid var(--accent); border-radius: 20px; padding: 12px 14px 12px 58px; box-sizing: border-box; z-index: 12; box-shadow: 0 16px 28px rgba(15,23,42,.14); cursor: pointer; text-align: left; color: #0f172a; }
.choiceButton:hover { transform: scale(1.03); filter: brightness(1.02); }
.choiceA { top: 220px; } .choiceB { top: 350px; } .choiceC { top: 480px; }
.scene.active .choiceButton { animation: choicesIn 1.2s ease forwards; }
.scene.running .choiceButton { animation: choicesMove 5.0s linear forwards; }
.choiceKey { position: absolute; left: 12px; top: 18px; width: 34px; height: 34px; border-radius: 999px; background: var(--accent); color: white; display: grid; place-items: center; font-weight: 900; }
.choiceText { font-weight: 900; font-size: 14px; line-height: 1.45; }
.ground { position: absolute; left: 0; right: 0; bottom: 0; height: 92px; background: linear-gradient(90deg, rgba(255,255,255,.35) 0 30px, transparent 30px 70px), linear-gradient(#64748b, #334155); background-size: 120px 100%; animation: scrollGround 1.2s linear infinite; }
.message { position: absolute; left: 50%; bottom: 122px; transform: translateX(-50%); background: rgba(255,255,255,.96); border: 2px solid #cbd5e1; border-radius: 18px; padding: 14px 18px; text-align: center; width: 650px; z-index: 50; box-shadow: 0 16px 32px rgba(15,23,42,.18); font-weight: 800; }
.gameOver, .gameClear { display: none; position: absolute; inset: 80px 12% auto 12%; min-height: 250px; background: white; border-radius: 24px; text-align: center; z-index: 80; padding: 28px; box-shadow: 0 22px 50px rgba(15,23,42,.28); }
.gameOver { border: 5px solid #dc2626; } .gameClear { border: 5px solid #16a34a; }
.gameOver h2 { color: #dc2626; font-size: 42px; } .gameClear h2 { color: #16a34a; font-size: 42px; }
.gameOver button, .gameClear button { border: 0; border-radius: 999px; padding: 10px 16px; font-weight: 900; background: #2563eb; color: white; cursor: pointer; margin: 6px; }
.help { margin-top: 10px; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; }
@keyframes scrollBg { from { background-position: 0 190px, 0 190px; } to { background-position: -520px 190px, -520px 190px; } }
@keyframes scrollGround { from { background-position: 0 0, 0 0; } to { background-position: -120px 0, 0 0; } }
@keyframes warningPulse { from { transform: scale(1) rotate(-4deg); } to { transform: scale(1.15) rotate(5deg); } }
@keyframes runBob { from { transform: translateY(0) rotate(-3deg); } to { transform: translateY(-8px) rotate(4deg); } }
@keyframes choicesIn { to { right: 70px; } }
@keyframes choicesMove { from { right: 70px; } to { right: 65%; } }
@keyframes jumpArc { 0% { bottom: 95px; transform: translateX(0) scale(1); } 45% { bottom: 270px; transform: translateX(290px) scale(1.15); } 100% { bottom: 95px; transform: translateX(565px) scale(1); } }
.flashGood { animation: goodFlash .7s ease 2; } .flashBad { animation: badShake .5s ease 2; }
@keyframes goodFlash { 0%, 100% { box-shadow: inset 0 0 0 0 rgba(22,163,74,0); } 50% { box-shadow: inset 0 0 0 999px rgba(22,163,74,.18); } }
@keyframes badShake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-12px); } 40% { transform: translateX(12px); } 60% { transform: translateX(-8px); } 80% { transform: translateX(8px); } }
</style>
<script>
const departments = {"reception": {"name": "受付", "scene": "reception", "runner": "👩‍💼", "stages": [{"place": "総合受付", "icon": "🤒", "title": "発熱患者が通常受付に来院", "desc": "予約なしの患者が発熱と咳を訴えています。待合には高齢患者もいます。", "choices": {"A": "通常受付で問診票を書いてもらう", "B": "マスク着用・距離確保の上、発熱導線へ案内", "C": "診療科が分からないのでその場で待機"}, "correct": "B", "success": "感染対策導線へ案内し、待合でのリスクを抑えました。", "fail": "通常待合に滞留し、感染対策上のリスクが高まりました。"}, {"place": "受付カウンター", "icon": "🪪", "title": "保険証なし・財布も忘れた患者", "desc": "軽症で歩行可能。保険証も現金もないと言っています。", "choices": {"A": "受診を断る", "B": "医事相談へつなぎ、自費・後日精算等を説明", "C": "何も確認せず通常受付へ通す"}, "correct": "B", "success": "診療機会を妨げず、未収リスクにも配慮できました。", "fail": "説明不足により、会計トラブルや未収リスクが高まりました。"}, {"place": "外来待合", "icon": "😡", "title": "待ち時間への強いクレーム", "desc": "患者が大きな声で怒っています。周囲の患者も不安そうです。", "choices": {"A": "個別スペースへ案内し、傾聴と見通し説明", "B": "順番なのでその場で待つよう説明", "C": "すぐ診察順を早める"}, "correct": "A", "success": "待合全体への波及を抑え、患者の不満を受け止められました。", "fail": "不公平感や二次クレームが生じ、待合全体の緊張が高まりました。"}, {"place": "救急入口", "icon": "🚑", "title": "胸痛を訴える予約外患者", "desc": "胸痛、冷汗、息苦しさを訴えています。受付票の記入もつらそうです。", "choices": {"A": "受付票を最後まで書いてもらう", "B": "通常の順番で内科へ案内", "C": "看護師へ即時共有し、救急・優先対応へつなぐ"}, "correct": "C", "success": "受付手続きより重症度を優先し、安全な初動ができました。", "fail": "重症疾患への対応が遅れる可能性があります。"}, {"place": "受付カウンター", "icon": "📄", "title": "紹介状を持参したが予約時間が不明", "desc": "紹介元から来た患者が、検査予約があると言っていますが詳細が分かりません。", "choices": {"A": "地域連携・紹介窓口で予約と紹介内容を確認", "B": "通常受付で空いている診療科へ回す", "C": "患者に紹介元へ電話してもらうだけにする"}, "correct": "A", "success": "紹介情報と予約枠を確認し、紹介患者の導線を整理できました。", "fail": "紹介元対応や検査枠に混乱が生じる可能性があります。"}, {"place": "外来入口", "icon": "🧓", "title": "高齢患者が院内で迷っている", "desc": "検査場所が分からず、同じ場所を何度も行き来しています。", "choices": {"A": "地図を渡して自力で行ってもらう", "B": "声をかけ、本人確認後に目的地まで案内・必要時連絡", "C": "混雑しているので様子を見る"}, "correct": "B", "success": "迷子・転倒・検査遅れのリスクを下げられました。", "fail": "患者安全や検査遅延のリスクが残ります。"}, {"place": "受付カウンター", "icon": "👶", "title": "小児がぐったりしている", "desc": "高熱の小児が保護者に抱えられて来院。水分が取れていない様子です。", "choices": {"A": "通常受付後、小児科の順番を待つ", "B": "発熱外来に案内して終わり", "C": "看護師へ即時共有し、優先対応へつなぐ"}, "correct": "C", "success": "小児の重症化サインを見逃さず、優先対応につなげました。", "fail": "脱水や重症感染症の対応が遅れる可能性があります。"}, {"place": "受付カウンター", "icon": "🏢", "title": "勤務中のけがで来院", "desc": "勤務中に転倒して手首を痛めた患者。労災かもしれません。", "choices": {"A": "保険確認・医事相談で労災可能性を確認", "B": "通常の健康保険として処理", "C": "会社に聞いてから出直してもらう"}, "correct": "A", "success": "労災・健康保険の扱いを確認し、後日の請求修正リスクを下げました。", "fail": "保険種別の誤りによる請求修正やトラブルが起こり得ます。"}, {"place": "総合案内", "icon": "🗣️", "title": "外国語対応が必要な患者", "desc": "日本語での意思疎通が難しい患者が来院。症状をうまく説明できません。", "choices": {"A": "分かる単語だけで受付を進める", "B": "通訳ツール・多言語資料・必要部署連携で確認", "C": "家族が来るまで診療案内を止める"}, "correct": "B", "success": "安全な確認と説明につなげ、誤案内を防げました。", "fail": "症状や同意内容の誤解が発生する可能性があります。"}, {"place": "外来待合", "icon": "📣", "title": "呼び出しに反応しない患者", "desc": "診察呼び出しに反応がなく、待合にも見当たりません。", "choices": {"A": "関係部署へ共有し、最終確認場所と院内導線を確認", "B": "順番を飛ばして終了扱いにする", "C": "院内全体放送でフルネームを呼ぶ"}, "correct": "A", "success": "個人情報に配慮しつつ、安全確認と所在確認に進めました。", "fail": "個人情報配慮や患者安全の面で問題が残ります。"}]}, "general": {"name": "総務課", "scene": "general", "runner": "🧑‍💼", "stages": [{"place": "総務課", "icon": "⚡", "title": "院内の一部で停電", "desc": "外来棟の一部照明と複合機が停止。患者案内にも影響が出始めています。", "choices": {"A": "設備担当へ連絡し、影響範囲を把握して院内共有", "B": "復旧まで各部署判断に任せる", "C": "患者には説明せず通常運用"}, "correct": "A", "success": "影響範囲を把握し、混乱を抑えながら復旧対応に入れました。", "fail": "部署ごとに情報がばらつき、問い合わせと混乱が増えました。"}, {"place": "代表電話", "icon": "📞", "title": "報道機関から突然の問い合わせ", "desc": "救急受入問題について、代表電話に取材問い合わせが入りました。", "choices": {"A": "電話を受けた職員が分かる範囲で説明", "B": "広報・管理者へ集約し、記録を残す", "C": "忙しいので折り返しせず放置"}, "correct": "B", "success": "情報を一本化し、組織として適切な対応ルートに乗せました。", "fail": "組織見解と異なる説明や対応遅れのリスクが生じました。"}, {"place": "施設管理", "icon": "💧", "title": "待合スペースで雨漏り", "desc": "雨漏りで床が濡れ、患者が転倒しそうです。", "choices": {"A": "診療が忙しいので後で対応", "B": "雑巾だけ置いて様子を見る", "C": "立入制限・清掃・設備連絡・代替導線を確保"}, "correct": "C", "success": "転倒リスクを防ぎ、患者導線を安全に確保しました。", "fail": "転倒事故や苦情につながるリスクが残りました。"}, {"place": "総務課", "icon": "📦", "title": "重要物品の納品遅延", "desc": "検査部門で使う消耗品の納品が遅れています。明日以降の診療に影響しそうです。", "choices": {"A": "部署へ影響確認し、代替品・在庫融通・業者確認を同時に進める", "B": "納品されるまで待つ", "C": "現場に節約を依頼するだけにする"}, "correct": "A", "success": "診療影響を把握し、代替策を早期に検討できました。", "fail": "診療停止や現場混乱につながる可能性があります。"}, {"place": "防災センター", "icon": "🔥", "title": "火災報知器が作動", "desc": "外来エリアで火災報知器が作動。誤報か実火災か不明です。", "choices": {"A": "誤報と思って放置", "B": "初動手順に従い、現場確認・通報体制・避難準備を進める", "C": "患者に何も伝えず通常運用"}, "correct": "B", "success": "安全確認と避難準備を同時に進められました。", "fail": "初動遅れにより安全確保が遅れる可能性があります。"}, {"place": "総務課", "icon": "🧹", "title": "清掃委託スタッフが急に欠員", "desc": "感染対策上重要なエリアの清掃人員が不足しています。", "choices": {"A": "委託業者・感染対策担当・現場と優先順位を調整", "B": "清掃頻度を一律で下げる", "C": "現場職員に全て任せる"}, "correct": "A", "success": "リスクの高いエリアを優先し、現実的な代替体制を組めました。", "fail": "感染対策や現場負担に悪影響が出ます。"}, {"place": "駐車場", "icon": "🚗", "title": "駐車場で接触事故", "desc": "患者同士の車両接触事故が発生。双方が興奮しています。", "choices": {"A": "当事者同士で解決してもらう", "B": "安全確保、必要時警察連絡、記録、院内共有を行う", "C": "病院敷地内ではないことにする"}, "correct": "B", "success": "安全確保と記録を行い、二次トラブルを防げました。", "fail": "苦情や責任問題が拡大する可能性があります。"}, {"place": "総務課", "icon": "🔐", "title": "不審者が院内を徘徊", "desc": "職員証のない人物が管理区域付近を歩いています。", "choices": {"A": "一人で強く問い詰める", "B": "見なかったことにする", "C": "複数名で声かけし、警備・管理者へ共有"}, "correct": "C", "success": "職員の安全を保ちながら、適切な確認と共有ができました。", "fail": "職員安全や情報管理上のリスクが残ります。"}, {"place": "会議室", "icon": "📝", "title": "重要会議の資料が未印刷", "desc": "理事会前に配布資料の印刷漏れが判明しました。時間がありません。", "choices": {"A": "優先資料を確認し、電子配布・分担印刷・差替説明を整理", "B": "全員で慌てて最初から印刷", "C": "資料なしで進める"}, "correct": "A", "success": "重要資料を優先し、会議運営への影響を最小化できました。", "fail": "混乱し、会議進行や信頼に影響します。"}, {"place": "総務課", "icon": "📢", "title": "院内掲示に誤情報", "desc": "外来休診案内の日付が誤って掲示されています。患者から指摘がありました。", "choices": {"A": "そのまま次回更新時に直す", "B": "正しい情報を確認し、掲示・Web・関係部署を即時修正", "C": "指摘した患者にだけ説明する"}, "correct": "B", "success": "誤案内の拡大を防ぎ、情報の整合性を保てました。", "fail": "患者の来院ミスや問い合わせ増加につながります。"}]}, "medical": {"name": "医事課", "scene": "medical", "runner": "👨‍💻", "stages": [{"place": "医事課", "icon": "💻", "title": "レセコン・受付システム停止", "desc": "朝の受付直後、レセコンと受付システムが停止。待合には患者が増えています。", "choices": {"A": "紙運用へ切替＋情報システム連絡＋患者説明", "B": "復旧するまで受付を止める", "C": "各窓口が現場判断でばらばらに対応"}, "correct": "A", "success": "BCPに沿って診療継続。患者説明もでき、混乱を抑えました。", "fail": "受付が混乱し、患者不満と診療遅延が拡大しました。"}, {"place": "会計窓口", "icon": "💰", "title": "会計で未収リスク発生", "desc": "自費扱いの患者が支払い困難を申し出ています。", "choices": {"A": "その場の雰囲気で免除する", "B": "相談窓口・分納等のルールに沿って説明し記録", "C": "強い口調で即時支払いを求める"}, "correct": "B", "success": "患者対応と未収管理の両立ができました。", "fail": "説明トラブルや会計処理の不整合が発生しました。"}, {"place": "書類窓口", "icon": "🪪", "title": "患者情報を別患者へ渡しそうになる", "desc": "同姓同名に近い患者。書類を渡す直前に本人確認が不十分かもしれないと気づきました。", "choices": {"A": "急いでいるためそのまま渡す", "B": "名前だけ再確認して渡す", "C": "氏名＋生年月日等で再確認し、書類を照合"}, "correct": "C", "success": "誤交付を防止。ヒヤリハットとして再発防止につなげました。", "fail": "個人情報インシデントのリスクが高まりました。"}, {"place": "医事課", "icon": "📄", "title": "返戻が大量発生", "desc": "同じ診療科で病名漏れと思われる返戻が複数発生しました。", "choices": {"A": "個別修正だけして終了", "B": "原因を分析し、診療科・算定担当と再発防止を共有", "C": "担当者のミスとして注意するだけ"}, "correct": "B", "success": "個別対応に加え、再発防止につながる仕組み化ができました。", "fail": "同じ返戻が繰り返される可能性があります。"}, {"place": "入院係", "icon": "🏥", "title": "DPC期間超過が目立つ", "desc": "複数病棟でDPC期間II超えが増え、収益に影響しています。", "choices": {"A": "退院支援・病棟・診療科と情報共有し要因確認", "B": "医事課だけで点数を調整する", "C": "仕方ないとして放置"}, "correct": "A", "success": "在院日数管理を多職種で考える入口を作れました。", "fail": "収益悪化や病床運営課題が見えないままになります。"}, {"place": "会計窓口", "icon": "🧾", "title": "患者から領収書の内容に疑問", "desc": "患者が『前回と金額が違う』と不安そうにしています。", "choices": {"A": "制度が複雑なので仕方ないと説明", "B": "会計根拠を確認し、分かる言葉で説明・必要時再確認", "C": "診療科に聞いてくださいと返す"}, "correct": "B", "success": "不安を受け止め、説明責任を果たせました。", "fail": "不信感やクレームにつながる可能性があります。"}, {"place": "医事課", "icon": "📊", "title": "査定率が上昇", "desc": "最近、特定検査の査定が増えています。", "choices": {"A": "診療録記載・病名・算定要件を確認し、傾向を共有", "B": "査定された分だけ再請求する", "C": "現場には知らせない"}, "correct": "A", "success": "査定傾向を可視化し、診療録・病名・算定の改善につなげました。", "fail": "根本原因が残り、査定が続く可能性があります。"}, {"place": "窓口", "icon": "🗂️", "title": "限度額認定証の相談", "desc": "入院予定患者が医療費の支払いを心配しています。", "choices": {"A": "制度案内と必要手続きを説明し、不安を軽減", "B": "入院後に考えればよいと伝える", "C": "支払えないなら入院できないと伝える"}, "correct": "A", "success": "制度利用を案内し、患者の経済的不安に対応できました。", "fail": "患者不安や未収リスクが高まります。"}, {"place": "医事課", "icon": "🕒", "title": "月初の保険確認が滞留", "desc": "月初で保険確認が集中し、受付待ちが伸びています。", "choices": {"A": "全員を同じ列に並べる", "B": "確認対象を整理し、声かけ・導線・応援体制を調整", "C": "確認せずに後回し"}, "correct": "B", "success": "混雑を緩和しつつ、資格確認の精度を保てました。", "fail": "待ち時間増加や資格確認漏れが起こり得ます。"}, {"place": "医事課", "icon": "💬", "title": "診療科から算定相談", "desc": "新しい処置を始めるため、算定可否や記録要件を確認したいと相談がありました。", "choices": {"A": "早見表・通知・施設基準を確認し、記録要件も共有", "B": "たぶん算定できると回答", "C": "医事課では判断しないと断る"}, "correct": "A", "success": "算定と記録をセットで確認し、適正請求につなげました。", "fail": "誤算定や算定漏れのリスクが高まります。"}]}, "planning": {"name": "経営企画課", "scene": "management", "runner": "📊", "stages": [{"place": "経営企画課", "icon": "📉", "title": "月次収支が急激に悪化", "desc": "入院単価低下と材料費増加で、月次収支が予算を大きく下回りました。", "choices": {"A": "診療科別・病棟別・DPC別に要因分析し改善案を整理", "B": "とりあえず全体に経費削減を指示", "C": "一時的なものとして放置"}, "correct": "A", "success": "要因を分解し、現場と共有できる改善テーマに落とし込めました。", "fail": "原因不明のまま対策が空回りし、現場の納得感も低下しました。"}, {"place": "会議室", "icon": "🏥", "title": "病床利用率が低下", "desc": "病床利用率が下がり、稼働病床のあり方が課題になっています。", "choices": {"A": "すぐ病床削減だけを提案", "B": "紹介経路・退院支援・病床機能をセットで分析", "C": "現場に患者を増やすよう依頼だけする"}, "correct": "B", "success": "病床稼働の構造を捉え、経営と地域医療の両面で検討できました。", "fail": "単純な削減・増患指示となり、現場との溝が深まりました。"}, {"place": "企画会議", "icon": "🤖", "title": "AI導入提案が出た", "desc": "AI問診や議事録要約の提案がありますが、費用対効果が不明です。", "choices": {"A": "流行しているので全院一斉導入", "B": "リスクがあるので全て禁止", "C": "小規模PoCで効果指標を決めて検証"}, "correct": "C", "success": "小さく試し、効果とリスクを見ながら展開する方針を作れました。", "fail": "過剰投資または機会損失につながりました。"}, {"place": "経営企画課", "icon": "📈", "title": "救急件数は増えたが赤字", "desc": "救急受入件数は増加しましたが、人件費・材料費も増えています。", "choices": {"A": "救急停止を即提案", "B": "救急の収支・地域役割・人員負担を分けて分析", "C": "件数が増えているので成功と判断"}, "correct": "B", "success": "経営と地域医療の両面から、継続可能な救急体制を検討できます。", "fail": "短絡的な判断となり、現場や地域との調整が難しくなります。"}, {"place": "企画会議", "icon": "🧭", "title": "中期計画のKPIが曖昧", "desc": "中期計画に多くの目標がありますが、進捗管理が難しい状態です。", "choices": {"A": "重点KPIを絞り、担当部署・頻度・データ源を明確化", "B": "全部重要なので全部同じ重みで管理", "C": "年度末にまとめて確認"}, "correct": "A", "success": "実行管理しやすい計画に整理できました。", "fail": "計画が作って終わりになりやすくなります。"}, {"place": "経営企画課", "icon": "🏘️", "title": "地域人口が減少", "desc": "将来推計で外来・入院需要の変化が見込まれます。", "choices": {"A": "現状維持で様子を見る", "B": "人口推計・疾患構成・病床機能をもとに将来像を検討", "C": "患者数が減るなら広報だけ強化"}, "correct": "B", "success": "人口変化を前提に、病院機能の再設計を考えられました。", "fail": "需要変化への対応が遅れる可能性があります。"}, {"place": "経営企画課", "icon": "💡", "title": "職員から改善提案が多数", "desc": "現場から業務改善アイデアが集まりましたが、優先順位が必要です。", "choices": {"A": "全部一斉に始める", "B": "声の大きい部署から始める", "C": "効果・難易度・安全性で評価し、優先順位をつける"}, "correct": "C", "success": "実行可能性と効果を見ながら改善を進められます。", "fail": "改善活動が散漫になり、疲弊につながります。"}, {"place": "理事会資料", "icon": "📑", "title": "理事会資料の数字が合わない", "desc": "複数資料で患者数と収支の数字が一致していません。", "choices": {"A": "提出前にデータ源・集計条件・版管理を確認", "B": "見栄えのよい数字を使う", "C": "細かい差なのでそのまま出す"}, "correct": "A", "success": "意思決定資料の信頼性を守れました。", "fail": "会議での信頼低下や誤った意思決定につながります。"}, {"place": "経営企画課", "icon": "🤝", "title": "近隣病院との連携提案", "desc": "近隣病院から機能分化・共同広報の相談がありました。", "choices": {"A": "競合なので全て断る", "B": "地域医療構想・患者導線・自院機能を踏まえて検討", "C": "相手に任せる"}, "correct": "B", "success": "競争と連携のバランスを取り、地域全体で考えられました。", "fail": "地域連携の機会を逃す可能性があります。"}, {"place": "経営企画課", "icon": "📣", "title": "採用広報で病院の魅力が伝わらない", "desc": "学生向け資料が無難で、病院事務の面白さが伝わっていません。", "choices": {"A": "現場改善・DX・経営参画の具体事例を発信", "B": "福利厚生だけを並べる", "C": "例年通りの説明で済ませる"}, "correct": "A", "success": "病院事務の先進性と実践性を伝えられます。", "fail": "他組織との差別化が難しくなります。"}]}, "hr": {"name": "人事課", "scene": "hr", "runner": "🧑‍🏫", "stages": [{"place": "人事課", "icon": "😰", "title": "若手職員から退職相談", "desc": "入職2年目の職員が、業務負担と相談しづらさを理由に退職を迷っています。", "choices": {"A": "面談で状況把握し、所属長と支援策を調整", "B": "本人の意思なので即退職手続きへ進める", "C": "忙しい時期なので後回し"}, "correct": "A", "success": "本人の声を受け止め、組織的な支援につなげました。", "fail": "離職防止の機会を逃し、職場課題も放置されました。"}, {"place": "研修室", "icon": "📚", "title": "個人情報研修の理解不足", "desc": "ヒヤリハット後の確認で、個人情報の扱いに部署差があることが分かりました。", "choices": {"A": "規程をメール送付して完了", "B": "事例型研修と確認テストで実務に近く学ばせる", "C": "問題を起こした職員だけ注意"}, "correct": "B", "success": "実務場面で判断できる研修に改善できました。", "fail": "知識が定着せず、再発リスクが残りました。"}, {"place": "採用面接", "icon": "🌟", "title": "インターン学生から鋭い質問", "desc": "学生から『この病院のDXや働き方改革は本気ですか？』と聞かれました。", "choices": {"A": "良いことだけを強調する", "B": "詳しいことは分からないと流す", "C": "実例と課題を率直に説明し、改善に参加できる魅力を伝える"}, "correct": "C", "success": "誠実で前向きな組織として印象づけられました。", "fail": "実態が見えず、採用広報として弱い印象になりました。"}, {"place": "人事課", "icon": "🗓️", "title": "勤務表への不満が増加", "desc": "特定職員に夜勤や遅番が偏っているとの声があります。", "choices": {"A": "勤務実績を確認し、公平性と現場事情を踏まえて調整", "B": "不満を言う人に我慢してもらう", "C": "所属長に丸投げする"}, "correct": "A", "success": "データと対話をもとに、公平性のある調整につなげました。", "fail": "不満や離職リスクが高まります。"}, {"place": "人事課", "icon": "🧑‍⚕️", "title": "資格職の採用応募が少ない", "desc": "看護師・薬剤師などの応募が伸び悩んでいます。", "choices": {"A": "求人票だけ更新する", "B": "現場の魅力・教育体制・働き方を整理して発信", "C": "採用時期が来るまで待つ"}, "correct": "B", "success": "応募者に伝わる採用広報へ改善できました。", "fail": "人材確保の競争で不利になります。"}, {"place": "相談室", "icon": "🧠", "title": "メンタル不調の相談", "desc": "職員から眠れない、出勤がつらいとの相談がありました。", "choices": {"A": "気合いで乗り切るよう励ます", "B": "産業医・相談窓口・所属調整につなぎ、記録する", "C": "本人が言うまで何もしない"}, "correct": "B", "success": "早期支援につなげ、悪化予防と安全配慮ができました。", "fail": "不調の悪化や安全配慮義務の問題につながります。"}, {"place": "研修室", "icon": "🆕", "title": "新規採用者が業務で孤立", "desc": "配属後、新人が誰に相談してよいか分からず困っています。", "choices": {"A": "メンター・相談先・振り返り面談を設定", "B": "自分で覚えるものとして放置", "C": "ミスが起きたら指導する"}, "correct": "A", "success": "早期離職を防ぎ、安心して学べる環境を作れました。", "fail": "孤立やミス、離職リスクが高まります。"}, {"place": "人事課", "icon": "⚖️", "title": "ハラスメント相談", "desc": "職員から上司の発言について相談がありました。", "choices": {"A": "相談内容を軽く扱う", "B": "双方をすぐ同席させて話し合わせる", "C": "相談者保護、記録、規程に沿った確認を進める"}, "correct": "C", "success": "相談者の安全と公正な確認手順を守れました。", "fail": "二次被害や組織不信につながる可能性があります。"}, {"place": "採用説明会", "icon": "🎤", "title": "学生が病院事務の仕事を地味だと思っている", "desc": "説明会で学生の反応が薄く、病院事務の魅力が伝わっていません。", "choices": {"A": "経営・DX・地域医療を支える実例を体験型で見せる", "B": "待遇だけを説明する", "C": "例年通りの説明資料を読む"}, "correct": "A", "success": "病院事務の実践性と成長機会を伝えられました。", "fail": "学生の印象に残らず、口コミ化しにくくなります。"}, {"place": "人事課", "icon": "📊", "title": "残業時間が一部部署に集中", "desc": "月次集計で特定部署の残業が突出しています。", "choices": {"A": "忙しい部署だから仕方ないとする", "B": "業務量・人員配置・繁忙要因を分析し、対策を検討", "C": "残業申請を厳しくする"}, "correct": "B", "success": "原因を踏まえた配置・業務改善につなげられました。", "fail": "表面的な抑制となり、サービス残業や疲弊につながります。"}]}};
let currentDeptKey = null;
let currentStages = [];
let current = 0;
let score = 0;
let active = false;
let locked = false;
function el(id) { return document.getElementById(id); }
function shuffleArray(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function selectDepartment(key) {
  currentDeptKey = key;
  currentStages = shuffleArray(departments[key].stages);
  current = 0; score = 0;
  el("departmentName").innerText = departments[key].name;
  el("stageTotal").innerText = currentStages.length;
  setStage();
}
function setStage() {
  const dept = departments[currentDeptKey];
  const s = currentStages[current];
  const scene = el("scene");
  scene.className = "scene " + dept.scene;
  el("runnerBody").innerText = dept.runner;
  el("stageNo").innerText = current + 1;
  el("score").innerText = score;
  el("statusText").innerText = "判断中";
  el("placeSign").innerText = s.place;
  el("eventIcon").innerText = s.icon;
  el("eventTitle").innerText = s.title;
  el("eventDesc").innerText = s.desc;
  el("choiceAText").innerText = s.choices.A;
  el("choiceBText").innerText = s.choices.B;
  el("choiceCText").innerText = s.choices.C;
  el("messageBox").style.display = "none";
  el("gameOver").style.display = "none";
  el("gameClear").style.display = "none";
  scene.classList.remove("running", "active", "flashGood", "flashBad");
  void scene.offsetWidth;
  scene.classList.add("active", "running");
  active = true; locked = false;
}
function restartDepartment() {
  if (!currentDeptKey) return;
  currentStages = shuffleArray(departments[currentDeptKey].stages);
  current = 0; score = 0; setStage();
}
function backToDepartmentSelect() {
  currentDeptKey = null; currentStages = []; current = 0; score = 0; active = false; locked = false;
  el("departmentName").innerText = "未選択"; el("stageNo").innerText = "0"; el("stageTotal").innerText = "0"; el("score").innerText = "0"; el("statusText").innerText = "部署選択中";
  el("placeSign").innerText = "部署を選択"; el("eventIcon").innerText = "🏥"; el("eventTitle").innerText = "部署を選択してください"; el("eventDesc").innerText = "上のボタンから部署を選ぶとゲームが始まります。";
  el("messageText").innerText = "部署を選択してください。"; el("messageBox").style.display = "block"; el("gameOver").style.display = "none"; el("gameClear").style.display = "none"; el("scene").className = "scene reception";
}
function jumpTo(choice) {
  if (!active || locked || !currentDeptKey) return;
  locked = true;
  const s = currentStages[current];
  const runner = el("runner");
  runner.classList.remove("jumpA", "jumpB", "jumpC");
  void runner.offsetWidth;
  runner.classList.add("jump" + choice);
  setTimeout(() => {
    if (choice === s.correct) {
      score += 100;
      el("score").innerText = score;
      el("statusText").innerText = "正解";
      el("messageText").innerText = s.success;
      el("messageBox").style.display = "block";
      el("scene").classList.add("flashGood");
      setTimeout(() => {
        current += 1;
        if (current >= currentStages.length) {
          active = false;
          el("finalScore").innerText = score;
          el("clearMessage").innerText = departments[currentDeptKey].name + "ステージをクリアしました。";
          el("gameClear").style.display = "block";
          el("statusText").innerText = "クリア";
        } else {
          setStage();
        }
      }, 1300);
    } else {
      active = false;
      el("statusText").innerText = "アウト";
      el("gameOverReason").innerText = s.fail + " 正解は「" + s.choices[s.correct] + "」でした。";
      el("scene").classList.add("flashBad");
      setTimeout(() => { el("gameOver").style.display = "block"; }, 700);
    }
  }, 720);
}
document.addEventListener("keydown", function(e) {
  const k = e.key.toUpperCase();
  if (["A","B","C"].includes(k)) jumpTo(k);
});
</script>
"""

components.html(GAME_HTML, height=900, scrolling=False)

st.subheader("教材としての狙い")
st.markdown("""
- 部署ごとに起こりやすい院内トラブルを体験する
- その場しのぎではなく、組織として安全な初動を選ぶ
- 受付・総務・医事・経営企画・人事の役割をゲームで理解する
- 正解／不正解を通じて、報告・共有・記録・患者安全の重要性を学ぶ
""")

st.info("選択肢はゲーム画面内のA/B/Cボタンとして押せます。キーボードのA/B/Cでも操作できます。")
