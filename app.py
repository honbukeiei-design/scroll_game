
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="院内トラブル即応シミュレーション", layout="wide")

st.title("院内トラブル即応シミュレーション：部署別ステージ版")
st.caption("受付・総務課・医事課・経営管理課・人事課で発生する突発イベントに即応する横スクロール型ゲーム")

GAME_HTML = """
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
    <button onclick="selectDepartment('management')">経営管理課</button>
    <button onclick="selectDepartment('hr')">人事課</button>
  </div>

  <div id="scene" class="scene reception">
    <div class="parallax back"></div>
    <div class="parallax mid"></div>
    <div class="sign" id="placeSign">部署を選択</div>

    <div class="eventCard">
      <div class="eventIcon" id="eventIcon">🏥</div>
      <div>
        <div class="eventTitle" id="eventTitle">部署を選択してください</div>
        <div class="eventDesc" id="eventDesc">上のボタンから部署を選ぶとゲームが始まります。</div>
      </div>
    </div>

    <div class="runner" id="runner">
      <div class="runnerShadow"></div>
      <div class="runnerBody" id="runnerBody">👩‍💼</div>
    </div>

    <button class="choiceButton choiceA" onclick="jumpTo('A')">
      <span class="choiceKey">A</span><span class="choiceText" id="choiceAText">A</span>
    </button>
    <button class="choiceButton choiceB" onclick="jumpTo('B')">
      <span class="choiceKey">B</span><span class="choiceText" id="choiceBText">B</span>
    </button>
    <button class="choiceButton choiceC" onclick="jumpTo('C')">
      <span class="choiceKey">C</span><span class="choiceText" id="choiceCText">C</span>
    </button>

    <div class="ground"></div>

    <div class="message" id="messageBox">
      <div id="messageText">部署を選択してください。</div>
    </div>

    <div class="gameOver" id="gameOver">
      <h2>アウト！</h2>
      <p id="gameOverReason"></p>
      <button onclick="restartDepartment()">同じ部署でもう一度</button>
      <button onclick="backToDepartmentSelect()">部署選択へ戻る</button>
    </div>

    <div class="gameClear" id="gameClear">
      <h2>クリア！</h2>
      <p id="clearMessage">全イベントを適切に対応できました。</p>
      <p>最終スコア: <span id="finalScore"></span></p>
      <button onclick="restartDepartment()">同じ部署でもう一度</button>
      <button onclick="backToDepartmentSelect()">部署選択へ戻る</button>
    </div>
  </div>

  <div class="help">
    操作：ゲーム画面内の <b>A/B/Cボタン</b> をクリック、またはキーボードの <b>A / B / C</b>。正解なら次へ進み、不正解ならアウトです。
  </div>
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
.parallax.mid {
  background-image:
    linear-gradient(90deg, transparent 0 30px, rgba(255,255,255,.88) 30px 120px, transparent 120px 180px),
    linear-gradient(90deg, transparent 0 60px, rgba(15,23,42,.10) 60px 64px, transparent 64px 180px);
  background-size: 260px 190px, 260px 190px;
  background-position: 0 190px, 0 190px;
  animation: scrollBg 18s linear infinite;
}
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
.choiceA { top: 220px; }
.choiceB { top: 350px; }
.choiceC { top: 480px; }
.scene.active .choiceButton { animation: choicesIn 1.2s ease forwards; }
.scene.running .choiceButton { animation: choicesMove 5.0s linear forwards; }
.choiceKey { position: absolute; left: 12px; top: 18px; width: 34px; height: 34px; border-radius: 999px; background: var(--accent); color: white; display: grid; place-items: center; font-weight: 900; }
.choiceText { font-weight: 900; font-size: 14px; line-height: 1.45; }
.ground { position: absolute; left: 0; right: 0; bottom: 0; height: 92px; background: linear-gradient(90deg, rgba(255,255,255,.35) 0 30px, transparent 30px 70px), linear-gradient(#64748b, #334155); background-size: 120px 100%; animation: scrollGround 1.2s linear infinite; }
.message { position: absolute; left: 50%; bottom: 122px; transform: translateX(-50%); background: rgba(255,255,255,.96); border: 2px solid #cbd5e1; border-radius: 18px; padding: 14px 18px; text-align: center; width: 650px; z-index: 50; box-shadow: 0 16px 32px rgba(15,23,42,.18); font-weight: 800; }
.gameOver, .gameClear { display: none; position: absolute; inset: 80px 12% auto 12%; min-height: 250px; background: white; border-radius: 24px; text-align: center; z-index: 80; padding: 28px; box-shadow: 0 22px 50px rgba(15,23,42,.28); }
.gameOver { border: 5px solid #dc2626; }
.gameClear { border: 5px solid #16a34a; }
.gameOver h2 { color: #dc2626; font-size: 42px; }
.gameClear h2 { color: #16a34a; font-size: 42px; }
.gameOver button, .gameClear button { border: 0; border-radius: 999px; padding: 10px 16px; font-weight: 900; background: #2563eb; color: white; cursor: pointer; margin: 6px; }
.help { margin-top: 10px; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; }

@keyframes scrollBg { from { background-position: 0 190px, 0 190px; } to { background-position: -520px 190px, -520px 190px; } }
@keyframes scrollGround { from { background-position: 0 0, 0 0; } to { background-position: -120px 0, 0 0; } }
@keyframes warningPulse { from { transform: scale(1) rotate(-4deg); } to { transform: scale(1.15) rotate(5deg); } }
@keyframes runBob { from { transform: translateY(0) rotate(-3deg); } to { transform: translateY(-8px) rotate(4deg); } }
@keyframes choicesIn { to { right: 70px; } }
@keyframes choicesMove { from { right: 70px; } to { right: 65%; } }
@keyframes jumpArc { 0% { bottom: 95px; transform: translateX(0) scale(1); } 45% { bottom: 270px; transform: translateX(290px) scale(1.15); } 100% { bottom: 95px; transform: translateX(565px) scale(1); } }
.flashGood { animation: goodFlash .7s ease 2; }
.flashBad { animation: badShake .5s ease 2; }
@keyframes goodFlash { 0%, 100% { box-shadow: inset 0 0 0 0 rgba(22,163,74,0); } 50% { box-shadow: inset 0 0 0 999px rgba(22,163,74,.18); } }
@keyframes badShake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-12px); } 40% { transform: translateX(12px); } 60% { transform: translateX(-8px); } 80% { transform: translateX(8px); } }
</style>

<script>
const departments = {
  reception: {
    name: "受付", scene: "reception", runner: "👩‍💼",
    stages: [
      { place: "総合受付", icon: "🤒", title: "発熱患者が通常受付に来院", desc: "予約なしの患者が発熱と咳を訴えています。待合には高齢患者もいます。", choices: { A: "通常受付で問診票を書いてもらう", B: "マスク着用・距離確保の上、発熱導線へ案内", C: "診療科が分からないのでその場で待機" }, correct: "B", success: "感染対策導線へ案内し、待合でのリスクを抑えました。", fail: "通常待合に滞留し、感染対策上のリスクが高まりました。" },
      { place: "受付カウンター", icon: "🪪", title: "保険証なし・財布も忘れた患者", desc: "軽症で歩行可能。保険証も現金もないと言っています。", choices: { A: "受診を断る", B: "医事相談へつなぎ、自費・後日精算等を説明", C: "何も確認せず通常受付へ通す" }, correct: "B", success: "診療機会を妨げず、未収リスクにも配慮できました。", fail: "説明不足により、会計トラブルや未収リスクが高まりました。" },
      { place: "外来待合", icon: "😡", title: "待ち時間への強いクレーム", desc: "患者が大きな声で怒っています。周囲の患者も不安そうです。", choices: { A: "個別スペースへ案内し、傾聴と見通し説明", B: "順番なのでその場で待つよう説明", C: "すぐ診察順を早める" }, correct: "A", success: "待合全体への波及を抑え、患者の不満を受け止められました。", fail: "不公平感や二次クレームが生じ、待合全体の緊張が高まりました。" }
    ]
  },
  general: {
    name: "総務課", scene: "general", runner: "🧑‍💼",
    stages: [
      { place: "総務課", icon: "⚡", title: "院内の一部で停電", desc: "外来棟の一部照明と複合機が停止。患者案内にも影響が出始めています。", choices: { A: "設備担当へ連絡し、影響範囲を把握して院内共有", B: "復旧まで各部署判断に任せる", C: "患者には説明せず通常運用" }, correct: "A", success: "影響範囲を把握し、混乱を抑えながら復旧対応に入れました。", fail: "部署ごとに情報がばらつき、問い合わせと混乱が増えました。" },
      { place: "代表電話", icon: "📞", title: "報道機関から突然の問い合わせ", desc: "救急受入問題について、代表電話に取材問い合わせが入りました。", choices: { A: "電話を受けた職員が分かる範囲で説明", B: "広報・管理者へ集約し、記録を残す", C: "忙しいので折り返しせず放置" }, correct: "B", success: "情報を一本化し、組織として適切な対応ルートに乗せました。", fail: "組織見解と異なる説明や対応遅れのリスクが生じました。" },
      { place: "施設管理", icon: "💧", title: "待合スペースで雨漏り", desc: "雨漏りで床が濡れ、患者が転倒しそうです。", choices: { A: "立入制限・清掃・設備連絡・代替導線を確保", B: "診療が忙しいので後で対応", C: "雑巾だけ置いて様子を見る" }, correct: "A", success: "転倒リスクを防ぎ、患者導線を安全に確保しました。", fail: "転倒事故や苦情につながるリスクが残りました。" }
    ]
  },
  medical: {
    name: "医事課", scene: "medical", runner: "👨‍💻",
    stages: [
      { place: "医事課", icon: "💻", title: "レセコン・受付システム停止", desc: "朝の受付直後、レセコンと受付システムが停止。待合には患者が増えています。", choices: { A: "紙運用へ切替＋情報システム連絡＋患者説明", B: "復旧するまで受付を止める", C: "各窓口が現場判断でばらばらに対応" }, correct: "A", success: "BCPに沿って診療継続。患者説明もでき、混乱を抑えました。", fail: "受付が混乱し、患者不満と診療遅延が拡大しました。" },
      { place: "会計窓口", icon: "💰", title: "会計で未収リスク発生", desc: "自費扱いの患者が支払い困難を申し出ています。", choices: { A: "相談窓口・分納等のルールに沿って説明し記録", B: "その場の雰囲気で免除する", C: "強い口調で即時支払いを求める" }, correct: "A", success: "患者対応と未収管理の両立ができました。", fail: "説明トラブルや会計処理の不整合が発生しました。" },
      { place: "書類窓口", icon: "🪪", title: "患者情報を別患者へ渡しそうになる", desc: "同姓同名に近い患者。書類を渡す直前に本人確認が不十分かもしれないと気づきました。", choices: { A: "氏名＋生年月日等で再確認し、書類を照合", B: "急いでいるためそのまま渡す", C: "名前だけ再確認して渡す" }, correct: "A", success: "誤交付を防止。ヒヤリハットとして再発防止につなげました。", fail: "個人情報インシデントのリスクが高まりました。" }
    ]
  },
  management: {
    name: "経営管理課", scene: "management", runner: "📊",
    stages: [
      { place: "経営管理課", icon: "📉", title: "月次収支が急激に悪化", desc: "入院単価低下と材料費増加で、月次収支が予算を大きく下回りました。", choices: { A: "診療科別・病棟別・DPC別に要因分析し改善案を整理", B: "とりあえず全体に経費削減を指示", C: "一時的なものとして放置" }, correct: "A", success: "要因を分解し、現場と共有できる改善テーマに落とし込めました。", fail: "原因不明のまま対策が空回りし、現場の納得感も低下しました。" },
      { place: "会議室", icon: "🏥", title: "病床利用率が低下", desc: "病床利用率が下がり、稼働病床のあり方が課題になっています。", choices: { A: "紹介経路・退院支援・病床機能をセットで分析", B: "すぐ病床削減だけを提案", C: "現場に患者を増やすよう依頼だけする" }, correct: "A", success: "病床稼働の構造を捉え、経営と地域医療の両面で検討できました。", fail: "単純な削減・増患指示となり、現場との溝が深まりました。" },
      { place: "企画会議", icon: "🤖", title: "AI導入提案が出た", desc: "AI問診や議事録要約の提案がありますが、費用対効果が不明です。", choices: { A: "小規模PoCで効果指標を決めて検証", B: "流行しているので全院一斉導入", C: "リスクがあるので全て禁止" }, correct: "A", success: "小さく試し、効果とリスクを見ながら展開する方針を作れました。", fail: "過剰投資または機会損失につながりました。" }
    ]
  },
  hr: {
    name: "人事課", scene: "hr", runner: "🧑‍🏫",
    stages: [
      { place: "人事課", icon: "😰", title: "若手職員から退職相談", desc: "入職2年目の職員が、業務負担と相談しづらさを理由に退職を迷っています。", choices: { A: "面談で状況把握し、所属長と支援策を調整", B: "本人の意思なので即退職手続きへ進める", C: "忙しい時期なので後回し" }, correct: "A", success: "本人の声を受け止め、組織的な支援につなげました。", fail: "離職防止の機会を逃し、職場課題も放置されました。" },
      { place: "研修室", icon: "📚", title: "個人情報研修の理解不足", desc: "ヒヤリハット後の確認で、個人情報の扱いに部署差があることが分かりました。", choices: { A: "事例型研修と確認テストで実務に近く学ばせる", B: "規程をメール送付して完了", C: "問題を起こした職員だけ注意" }, correct: "A", success: "実務場面で判断できる研修に改善できました。", fail: "知識が定着せず、再発リスクが残りました。" },
      { place: "採用面接", icon: "🌟", title: "インターン学生から鋭い質問", desc: "学生から『この病院のDXや働き方改革は本気ですか？』と聞かれました。", choices: { A: "実例と課題を率直に説明し、改善に参加できる魅力を伝える", B: "良いことだけを強調する", C: "詳しいことは分からないと流す" }, correct: "A", success: "誠実で前向きな組織として印象づけられました。", fail: "実態が見えず、採用広報として弱い印象になりました。" }
    ]
  }
};

let currentDeptKey = null;
let currentStages = [];
let current = 0;
let score = 0;
let active = false;
let locked = false;

function el(id) { return document.getElementById(id); }

function selectDepartment(key) {
  currentDeptKey = key;
  currentStages = departments[key].stages;
  current = 0;
  score = 0;
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
  active = true;
  locked = false;
}

function restartDepartment() {
  if (!currentDeptKey) return;
  current = 0;
  score = 0;
  setStage();
}

function backToDepartmentSelect() {
  currentDeptKey = null;
  currentStages = [];
  current = 0;
  score = 0;
  active = false;
  locked = false;
  el("departmentName").innerText = "未選択";
  el("stageNo").innerText = "0";
  el("stageTotal").innerText = "0";
  el("score").innerText = "0";
  el("statusText").innerText = "部署選択中";
  el("placeSign").innerText = "部署を選択";
  el("eventIcon").innerText = "🏥";
  el("eventTitle").innerText = "部署を選択してください";
  el("eventDesc").innerText = "上のボタンから部署を選ぶとゲームが始まります。";
  el("messageText").innerText = "部署を選択してください。";
  el("messageBox").style.display = "block";
  el("gameOver").style.display = "none";
  el("gameClear").style.display = "none";
  el("scene").className = "scene reception";
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
      setTimeout(() => {
        el("gameOver").style.display = "block";
      }, 700);
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
st.markdown("- 部署ごとに起こりやすい院内トラブルを体験する\\n- その場しのぎではなく、組織として安全な初動を選ぶ\\n- 受付・総務・医事・経営管理・人事の役割をゲームで理解する\\n- 正解／不正解を通じて、報告・共有・記録・患者安全の重要性を学ぶ")

st.info("選択肢はゲーム画面内のA/B/Cボタンとして押せます。キーボードのA/B/Cでも操作できます。")
