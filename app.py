import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="院内トラブル即応 横スクロールゲーム",
    layout="wide",
)

st.title("院内トラブル即応シミュレーション：横スクロール版")
st.caption("イベントに遭遇したら、ジャンプで正しい対応を選ぶインターン向けゲーム")

GAME_HTML = r"""
<div id="gameRoot">
  <div class="hud">
    <div class="hud-title">🏥 院内トラブル即応ランナー</div>
    <div class="hud-box">ステージ: <span id="stageNo">1</span>/<span id="stageTotal">6</span></div>
    <div class="hud-box">スコア: <span id="score">0</span></div>
    <div class="hud-box">状態: <span id="statusText">待機中</span></div>
  </div>

  <div id="scene" class="scene lobby">
    <div class="parallax back"></div>
    <div class="parallax mid"></div>

    <div class="sign" id="placeSign">総合受付</div>
    <div class="eventCard" id="eventCard">
      <div class="eventIcon" id="eventIcon">⚠️</div>
      <div>
        <div class="eventTitle" id="eventTitle">イベント発生</div>
        <div class="eventDesc" id="eventDesc">スタートを押してください。</div>
      </div>
    </div>

    <div class="runner" id="runner">
      <div class="runnerShadow"></div>
      <div class="runnerBody">👩‍💼</div>
    </div>

    <div class="choice choiceA" id="choiceA">
      <div class="choiceKey">A</div>
      <div class="choiceText" id="choiceAText"></div>
    </div>

    <div class="choice choiceB" id="choiceB">
      <div class="choiceKey">B</div>
      <div class="choiceText" id="choiceBText"></div>
    </div>

    <div class="choice choiceC" id="choiceC">
      <div class="choiceKey">C</div>
      <div class="choiceText" id="choiceCText"></div>
    </div>

    <div class="ground"></div>
    <div class="message" id="messageBox">
      <div id="messageText">スタートを押すとゲームが始まります。</div>
      <button onclick="startGame()">スタート</button>
    </div>

    <div class="gameOver" id="gameOver">
      <h2>アウト！</h2>
      <p id="gameOverReason"></p>
      <button onclick="restartGame()">最初からやり直す</button>
    </div>

    <div class="gameClear" id="gameClear">
      <h2>クリア！</h2>
      <p>全イベントを適切に対応できました。</p>
      <p>最終スコア: <span id="finalScore"></span></p>
      <button onclick="restartGame()">もう一度プレイ</button>
    </div>
  </div>

  <div class="controls">
    <button onclick="jumpTo('A')">Aへジャンプ</button>
    <button onclick="jumpTo('B')">Bへジャンプ</button>
    <button onclick="jumpTo('C')">Cへジャンプ</button>
    <button onclick="restartGame()">リセット</button>
  </div>

  <div class="help">
    操作：画面下のボタン、またはキーボードの <b>A / B / C</b> で選択。正解なら横スクロールで次の場所へ進み、不正解ならアウトです。
  </div>
</div>

<style>
#gameRoot {
  font-family: "Yu Gothic", "Meiryo", system-ui, sans-serif;
  color: #0f172a;
}
.hud {
  display: flex;
  gap: 12px;
  align-items: center;
  margin: 8px 0 12px 0;
  flex-wrap: wrap;
}
.hud-title {
  font-size: 22px;
  font-weight: 900;
  padding: 8px 14px;
  border-radius: 999px;
  background: linear-gradient(135deg, #dbeafe, #eef2ff);
  border: 1px solid #bfdbfe;
}
.hud-box {
  font-weight: 800;
  padding: 8px 12px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  box-shadow: 0 4px 12px rgba(15,23,42,.08);
}
.scene {
  position: relative;
  height: 620px;
  overflow: hidden;
  border-radius: 24px;
  border: 2px solid #cbd5e1;
  box-shadow: 0 20px 40px rgba(15,23,42,.12);
  background: linear-gradient(#bfdbfe, #eff6ff 42%, #f8fafc 42%);
}
.scene.lobby { --accent:#3b82f6; --bg1:#dbeafe; --bg2:#eff6ff; }
.scene.system { --accent:#6366f1; --bg1:#e0e7ff; --bg2:#f5f3ff; }
.scene.waiting { --accent:#f97316; --bg1:#ffedd5; --bg2:#fff7ed; }
.scene.emergency { --accent:#dc2626; --bg1:#fee2e2; --bg2:#fff1f2; }
.scene.privacy { --accent:#8b5cf6; --bg1:#ede9fe; --bg2:#faf5ff; }
.scene.clearzone { --accent:#16a34a; --bg1:#dcfce7; --bg2:#f0fdf4; }

.parallax {
  position: absolute;
  inset: 0;
  background-repeat: repeat-x;
  opacity: .9;
}
.parallax.back {
  background:
    linear-gradient(var(--bg1), var(--bg2));
}
.parallax.mid {
  background-image:
    linear-gradient(90deg, transparent 0 30px, rgba(255,255,255,.85) 30px 120px, transparent 120px 180px),
    linear-gradient(90deg, transparent 0 60px, rgba(15,23,42,.10) 60px 64px, transparent 64px 180px);
  background-size: 260px 180px, 260px 180px;
  background-position: 0 180px, 0 180px;
  animation: scrollBg 18s linear infinite;
}
.scene.running .parallax.mid { animation-duration: 6s; }
.sign {
  position: absolute;
  left: 32px;
  top: 28px;
  font-size: 24px;
  font-weight: 900;
  color: white;
  background: var(--accent);
  border-radius: 999px;
  padding: 10px 18px;
  box-shadow: 0 10px 20px rgba(15,23,42,.16);
  z-index: 5;
}
.eventCard {
  position: absolute;
  left: 50%;
  top: 42px;
  transform: translateX(-50%);
  width: 620px;
  min-height: 92px;
  background: rgba(255,255,255,.95);
  border: 3px solid var(--accent);
  border-radius: 22px;
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 14px 18px;
  box-shadow: 0 16px 34px rgba(15,23,42,.16);
  z-index: 10;
}
.eventIcon {
  font-size: 42px;
  animation: warningPulse .8s infinite alternate;
}
.eventTitle {
  font-size: 22px;
  font-weight: 900;
}
.eventDesc {
  font-size: 14px;
  line-height: 1.55;
  color: #334155;
}
.runner {
  position: absolute;
  left: 120px;
  bottom: 95px;
  width: 78px;
  height: 96px;
  z-index: 20;
}
.runnerBody {
  position: absolute;
  font-size: 64px;
  left: 0;
  top: 0;
  filter: drop-shadow(0 10px 12px rgba(15,23,42,.22));
  animation: runBob .45s infinite alternate;
}
.runnerShadow {
  position: absolute;
  width: 72px;
  height: 16px;
  left: 3px;
  bottom: 0;
  background: rgba(15,23,42,.18);
  border-radius: 50%;
  filter: blur(1px);
}
.runner.jumpA, .runner.jumpB, .runner.jumpC {
  animation: jumpArc .72s ease-out forwards;
}
.choice {
  position: absolute;
  right: -360px;
  width: 300px;
  min-height: 82px;
  background: white;
  border: 3px solid var(--accent);
  border-radius: 20px;
  padding: 12px 14px 12px 54px;
  box-sizing: border-box;
  z-index: 12;
  box-shadow: 0 16px 28px rgba(15,23,42,.14);
}
.choiceA { top: 210px; }
.choiceB { top: 330px; }
.choiceC { top: 450px; }
.scene.active .choice {
  animation: choicesIn 1.2s ease forwards;
}
.scene.running .choice {
  animation: choicesMove 4.8s linear forwards;
}
.choiceKey {
  position: absolute;
  left: 12px;
  top: 16px;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: var(--accent);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 900;
}
.choiceText {
  font-weight: 800;
  font-size: 14px;
  line-height: 1.45;
}
.ground {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 92px;
  background:
    linear-gradient(90deg, rgba(255,255,255,.35) 0 30px, transparent 30px 70px),
    linear-gradient(#64748b, #334155);
  background-size: 120px 100%;
  animation: scrollGround 1.2s linear infinite;
}
.message {
  position: absolute;
  left: 50%;
  bottom: 122px;
  transform: translateX(-50%);
  background: rgba(255,255,255,.96);
  border: 2px solid #cbd5e1;
  border-radius: 18px;
  padding: 14px 18px;
  text-align: center;
  width: 620px;
  z-index: 50;
  box-shadow: 0 16px 32px rgba(15,23,42,.18);
}
.message button, .gameOver button, .gameClear button, .controls button {
  border: 0;
  border-radius: 999px;
  padding: 10px 16px;
  font-weight: 900;
  background: #2563eb;
  color: white;
  cursor: pointer;
  margin: 6px;
}
.gameOver, .gameClear {
  display: none;
  position: absolute;
  inset: 80px 12% auto 12%;
  min-height: 240px;
  background: white;
  border-radius: 24px;
  text-align: center;
  z-index: 80;
  padding: 28px;
  box-shadow: 0 22px 50px rgba(15,23,42,.28);
}
.gameOver { border: 5px solid #dc2626; }
.gameClear { border: 5px solid #16a34a; }
.gameOver h2 { color: #dc2626; font-size: 42px; }
.gameClear h2 { color: #16a34a; font-size: 42px; }
.controls {
  margin-top: 12px;
  text-align: center;
}
.help {
  margin-top: 10px;
  padding: 10px 14px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

@keyframes scrollBg {
  from { background-position: 0 180px, 0 180px; }
  to { background-position: -520px 180px, -520px 180px; }
}
@keyframes scrollGround {
  from { background-position: 0 0, 0 0; }
  to { background-position: -120px 0, 0 0; }
}
@keyframes warningPulse {
  from { transform: scale(1) rotate(-4deg); }
  to { transform: scale(1.15) rotate(5deg); }
}
@keyframes runBob {
  from { transform: translateY(0) rotate(-3deg); }
  to { transform: translateY(-8px) rotate(4deg); }
}
@keyframes choicesIn {
  to { right: 80px; }
}
@keyframes choicesMove {
  from { right: 80px; }
  to { right: 66%; }
}
@keyframes jumpArc {
  0% { bottom: 95px; transform: translateX(0) scale(1); }
  45% { bottom: 260px; transform: translateX(280px) scale(1.15); }
  100% { bottom: 95px; transform: translateX(555px) scale(1); }
}
.flashGood {
  animation: goodFlash .7s ease 2;
}
.flashBad {
  animation: badShake .5s ease 2;
}
@keyframes goodFlash {
  0%, 100% { box-shadow: inset 0 0 0 0 rgba(22,163,74,0); }
  50% { box-shadow: inset 0 0 0 999px rgba(22,163,74,.18); }
}
@keyframes badShake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-12px); }
  40% { transform: translateX(12px); }
  60% { transform: translateX(-8px); }
  80% { transform: translateX(8px); }
}
</style>

<script>
const stages = [
  {
    place: "総合受付",
    scene: "lobby",
    icon: "💻",
    title: "電子カルテ・受付システム停止",
    desc: "朝の受付直後、電子カルテと受付システムが停止。待合には患者が増えています。",
    choices: {
      A: "紙運用へ切替＋情報システム連絡＋患者説明",
      B: "復旧するまで受付を止める",
      C: "各窓口が現場判断でばらばらに対応"
    },
    correct: "A",
    success: "BCPに沿って診療継続。患者説明もでき、混乱を抑えました。",
    fail: "受付が混乱し、患者不満と診療遅延が拡大しました。"
  },
  {
    place: "外来待合",
    scene: "waiting",
    icon: "🗣️",
    title: "待ち時間への強いクレーム",
    desc: "患者が大きな声で怒っています。周囲の患者も不安そうに見ています。",
    choices: {
      A: "個別スペースへ案内＋傾聴＋見通し説明",
      B: "順番なので待つようその場で説明",
      C: "すぐ診察順を早める"
    },
    correct: "A",
    success: "待合全体への波及を抑え、患者の不満を受け止められました。",
    fail: "不公平感や二次クレームが生じ、待合全体の緊張が高まりました。"
  },
  {
    place: "救急入口",
    scene: "emergency",
    icon: "🚑",
    title: "救急搬送が同時に2件到着",
    desc: "胸痛患者と転倒患者が同時に到着。外来も混雑しています。",
    choices: {
      A: "救急看護師へ即時共有＋外来へ遅延説明＋導線分離",
      B: "受付職員だけで救急情報を整理",
      C: "外来患者への説明を後回し"
    },
    correct: "A",
    success: "救急対応と外来説明を分け、混乱を最小限にできました。",
    fail: "優先順位判断や外来説明が遅れ、安全性と信頼度が低下しました。"
  },
  {
    place: "検査フロア",
    scene: "privacy",
    icon: "🔎",
    title: "検査待ち患者が見当たらない",
    desc: "検査室から患者未到着の連絡。高齢で認知機能低下の可能性があります。",
    choices: {
      A: "関係部署へ共有＋最終確認場所を追跡＋安全確認",
      B: "すぐ院内放送で呼び出す",
      C: "検査室にもう少し待つよう伝える"
    },
    correct: "A",
    success: "移動経路を追跡し、安全に発見できました。",
    fail: "発見が遅れ、患者安全や個人情報配慮に課題が残りました。"
  },
  {
    place: "代表電話",
    scene: "system",
    icon: "📞",
    title: "報道機関から突然の問い合わせ",
    desc: "救急受入問題について、報道機関から代表電話に問い合わせが入りました。",
    choices: {
      A: "広報・管理者へ集約＋記録を残す",
      B: "電話を受けた職員が分かる範囲で説明",
      C: "忙しいので折り返しせず放置"
    },
    correct: "A",
    success: "情報を一本化し、組織対応として適切なルートに乗せました。",
    fail: "組織見解と異なる説明や対応遅れのリスクが生じました。"
  },
  {
    place: "会計・書類窓口",
    scene: "privacy",
    icon: "🪪",
    title: "患者情報を別患者へ渡しそうになる",
    desc: "同姓同名に近い患者。書類を渡す直前に本人確認が不十分かもしれないと気づきました。",
    choices: {
      A: "氏名＋生年月日等で再確認し、書類を照合",
      B: "急いでいるためそのまま渡す",
      C: "名前だけ再確認して渡す"
    },
    correct: "A",
    success: "誤交付を防止。ヒヤリハットとして再発防止につなげました。",
    fail: "個人情報インシデントのリスクが高まりました。"
  }
];

let current = 0;
let score = 0;
let active = false;
let locked = false;

function el(id) { return document.getElementById(id); }

function setStage() {
  const s = stages[current];
  const scene = el("scene");
  scene.className = "scene " + s.scene;
  el("stageNo").innerText = current + 1;
  el("stageTotal").innerText = stages.length;
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

function startGame() {
  current = 0;
  score = 0;
  setStage();
}

function restartGame() {
  current = 0;
  score = 0;
  active = false;
  locked = false;
  el("score").innerText = 0;
  el("stageNo").innerText = 1;
  el("statusText").innerText = "待機中";
  el("gameOver").style.display = "none";
  el("gameClear").style.display = "none";
  el("messageBox").style.display = "block";
  el("messageText").innerText = "スタートを押すとゲームが始まります。";
  el("scene").className = "scene lobby";
}

function jumpTo(choice) {
  if (!active || locked) return;
  locked = true;

  const s = stages[current];
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
        if (current >= stages.length) {
          active = false;
          el("finalScore").innerText = score;
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

components.html(GAME_HTML, height=820, scrolling=False)

st.subheader("教材としての狙い")
st.markdown(
    """
- 突発イベントに対して、**最初の一手**を考える
- 「正解っぽいが危ない対応」と「組織として安全な対応」の違いを学ぶ
- 受付・医事・救急・情報システム・広報など、部署横断の連携を体験する
- ゲーム後に「なぜその選択が良いのか」を振り返る
"""
)

st.info("この横スクロール版は、Streamlit内にHTML/CSS/JavaScriptを埋め込んで動かしています。GitHub/Streamlit Cloudでも追加ライブラリなしで動きます。")
