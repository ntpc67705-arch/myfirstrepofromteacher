import streamlit as st
import time
import random

# 設定網頁標題與版面
st.set_page_config(page_title="奇幻冒險 Clicker", layout="centered")
st.title("🛡️ 奇幻冒險：熱血教官 Clicker")

########################
# Fantasy 主題 CSS
########################

def set_fantasy_css(weather):
    # 固定淺藍風格背景
    style = f"""
    <style>
    .stApp {{
        background: #d8f0ff !important;
        background-image: none !important;
        color: #1b2044;
        min-height: 100vh;
    }}
    .stButton>button {{
        background: linear-gradient(120deg, #2f86f3, #59bcff);
        color: white;
        font-weight: bold;
        border-radius: 14px;
        border: 2px solid #85d0ff;
        box-shadow: 0 0 10px rgba(53, 126, 255, 0.35);
    }}
    .stProgress>div>div {{
        background: #316fd0;
    }}
    .card {{
        background: rgba(255,255,255,0.85);
        border: 1px solid #a8dcff;
        border-radius: 16px;
        padding: 14px;
        box-shadow: 0 0 16px rgba(33, 124, 255, 0.2);
        animation: pulse 1.2s ease-in-out infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-4px) scale(1.02); }}
        100% {{ transform: translateY(0) scale(1); }}
    }}
    .item-card {{
        background: rgba(218, 252, 255, 0.9);
        border: 1px dashed #57c6f7;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# 初始化遊戲狀態
TOTAL_TIME = 30
MAX_HP = 100

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'hp' not in st.session_state:
    st.session_state.hp = MAX_HP
if 'time_left' not in st.session_state:
    st.session_state.time_left = TOTAL_TIME
if 'start_ts' not in st.session_state:
    st.session_state.start_ts = time.time()
if 'weather' not in st.session_state:
    st.session_state.weather = 'sunny'
if 'message' not in st.session_state:
    st.session_state.message = '熱血教官：出發！瘋狂點擊，打爆敵人！🔥'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'scene' not in st.session_state:
    st.session_state.scene = '魔法森林'
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'next_level_score' not in st.session_state:
    st.session_state.next_level_score = 150
if 'items' not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = ['神秘藥水']
if 'play_sfx' not in st.session_state:
    st.session_state.play_sfx = ''

# 主要函式

def reset_game():
    st.session_state.score = 0
    st.session_state.hp = MAX_HP
    st.session_state.time_left = TOTAL_TIME
    st.session_state.start_ts = time.time()
    st.session_state.weather = 'sunny'
    st.session_state.message = '熱血教官：全速衝刺，這局必須贏！'
    st.session_state.game_over = False
    st.session_state.scene = '魔法森林'
    st.session_state.level = 1
    st.session_state.next_level_score = 150
    st.session_state.items = ['神秘藥水']
    st.session_state.play_sfx = ''


def play_sound(effect):
    if effect == 'hit':
        tone = 440
        duration = 0.08
    elif effect == 'level':
        tone = 880
        duration = 0.16
    elif effect == 'game_over':
        tone = 220
        duration = 0.25
    else:
        return

    script = f"""
    <script>
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContext();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'triangle';
    o.frequency.setValueAtTime({tone}, ctx.currentTime);
    g.gain.setValueAtTime(0.04, ctx.currentTime);
    o.connect(g);
    g.connect(ctx.destination);
    o.start();
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + {duration});
    o.stop(ctx.currentTime + {duration});
    </script>
    """
    st.markdown(script, unsafe_allow_html=True)


def refresh_timer():
    elapsed = time.time() - st.session_state.start_ts
    st.session_state.time_left = max(0, TOTAL_TIME - int(elapsed))
    if st.session_state.time_left == 0:
        st.session_state.game_over = True

def update_weather():
    if st.session_state.time_left > TOTAL_TIME * 0.7:
        st.session_state.weather = 'sunny'
    elif st.session_state.time_left > TOTAL_TIME * 0.3:
        st.session_state.weather = 'rainy'
    else:
        st.session_state.weather = 'storm'

    if random.random() < 0.15:
        st.session_state.weather = 'magic'

def hit_action():
    if st.session_state.game_over:
        return

    damage = random.randint(5, 15)
    st.session_state.score += random.randint(10, 25)
    st.session_state.hp = min(MAX_HP, st.session_state.hp + random.randint(0, 5))
    st.session_state.play_sfx = 'hit'

    if random.random() < 0.25:
        st.session_state.hp = max(0, st.session_state.hp - damage)
        st.session_state.message = f'熱血教官：沒錯！你被怪獸反擊了，扣{damage}點 HP！⚔️'
    else:
        st.session_state.message = '熱血教官：超強一擊！繼續保持震撼力！💥'

    st.session_state.scene = random.choice(['古老遺跡', '暗影山谷', '精靈湖畔', '龍之巢穴'])

    # 等級解鎖與道具系統
    if st.session_state.score >= st.session_state.next_level_score:
        st.session_state.level += 1
        st.session_state.next_level_score += 120
        st.session_state.message = f'熱血教官：太猛了！升級到等級 {st.session_state.level}！✨ 生命和力量提升！'
        st.session_state.hp = min(MAX_HP, st.session_state.hp + 12)
        st.session_state.items.append('超級恢復藥水')
        st.session_state.play_sfx = 'level'

    # 隨機道具掉落
    if random.random() < 0.3:
        drop = random.choice(['力量符文', '防禦護符', '快速卷軸'])
        if drop not in st.session_state.items:
            st.session_state.items.append(drop)
            st.session_state.message += f' 獲得新道具：{drop}！🎁'

    if st.session_state.hp == 0:
        st.session_state.game_over = True
        st.session_state.message = '熱血教官：哇！你被打倒了，但別灰心，下次更猛！💪'
        st.session_state.play_sfx = 'game_over'


# 遊戲循環與畫面
refresh_timer()
update_weather()
set_fantasy_css(st.session_state.weather)

st.markdown(f"### 場景：{st.session_state.scene}  |  天氣：{st.session_state.weather.title()}")

col1, col2 = st.columns(2)
col1.metric("分數", st.session_state.score)
col1.metric("HP", f"{st.session_state.hp}/{MAX_HP}")
col1.metric("等級", f"{st.session_state.level}")
col2.metric("剩餘時間", f"{st.session_state.time_left}s")
col2.progress(st.session_state.time_left / TOTAL_TIME)

st.markdown(f"<div class='card'><strong>{st.session_state.message}</strong></div>", unsafe_allow_html=True)

if not st.session_state.game_over:
    if st.button('🗡️ 熱血點擊攻擊'):    
        hit_action()
        refresh_timer()
        update_weather()

    # 道具使用
    items = st.session_state.get('items', [])
    if not isinstance(items, list):
        items = []
        st.session_state.items = items

    if items:
        st.markdown('### 🧾 你擁有的道具')
        for item in items:
            st.markdown(f'<div class="item-card">{item}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button('💖 恢復藥水') and '超級恢復藥水' in st.session_state.items:
            st.session_state.hp = min(MAX_HP, st.session_state.hp + 30)
            st.session_state.items.remove('超級恢復藥水')
            st.success('使用超級恢復藥水，HP +30！')

        if c2.button('🛡️ 防禦護符') and '防禦護符' in st.session_state.items:
            st.session_state.hp = min(MAX_HP, st.session_state.hp + 15)
            st.session_state.items.remove('防禦護符')
            st.success('使用防禦護符，守住傷害！')

        if c3.button('⚡ 加速卷軸') and '快速卷軸' in st.session_state.items:
            st.session_state.score += 35
            st.session_state.items.remove('快速卷軸')
            st.success('使用快速卷軸，瞬間獲得 +35 分！')

    st.write('🎯 快點擊，盡可能衝到最高分！')
    st.write('⏳ 這場比賽會在倒數結束時決定勝負')
else:
    result = '勝利' if st.session_state.hp > 0 else '失敗'
    if st.session_state.score >= 300 and st.session_state.hp > 0:
        st.success(f'🏆 你獲得 {result}! 最終分數：{st.session_state.score}，HP：{st.session_state.hp}')
    else:
        st.error(f'💥 遊戲結束（{result}）。最終分數：{st.session_state.score}，HP：{st.session_state.hp}')
    st.write('熱血教官：別放棄，重整旗鼓再來一次！')
    if st.button('🔁 再來一局'):
        reset_game()
        st.experimental_rerun()

# 透過 JS 播放音效
if st.session_state.play_sfx:
    play_sound(st.session_state.play_sfx)
    st.session_state.play_sfx = ''

st.markdown('---')
st.info('💡 請在終端機輸入 `streamlit run app.py` 來啟動遊戲預覽。')

