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
    colors = {
        'sunny': ('#eaf9ff', '#f9f1d8'),
        'rainy': ('#dbe9fb', '#a5c9f7'),
        'storm': ('#1c2431', '#3c4b66'),
        'magic': ('#f8e9ff', '#d5b8ff')
    }
    bg, accent = colors.get(weather, colors['sunny'])

    style = f"""
    <style>
    .stApp {{
        background: linear-gradient(140deg, {bg}, {accent});
        color: #1b2044;
        min-height: 100vh;
    }}
    .stButton>button {{
        background: linear-gradient(120deg, #ff8c00, #ff1a75); 
        color: white; 
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #fff;
    }}
    .stProgress>div>div {{
        background: #ff9900;
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

    if random.random() < 0.25:
        st.session_state.hp = max(0, st.session_state.hp - damage)
        st.session_state.message = f'熱血教官：沒錯！你被怪獸反擊了，扣{damage}點 HP！⚔️'
    else:
        st.session_state.message = '熱血教官：超強一擊！繼續保持震撼力！💥'

    st.session_state.scene = random.choice(['古老遺跡', '暗影山谷', '精靈湖畔', '龍之巢穴'])

    if st.session_state.hp == 0:
        st.session_state.game_over = True
        st.session_state.message = '熱血教官：哇！你被打倒了，但別灰心，下次更猛！💪'


# 遊戲循環與畫面
refresh_timer()
update_weather()
set_fantasy_css(st.session_state.weather)

st.markdown(f"### 場景：{st.session_state.scene}  |  天氣：{st.session_state.weather.title()}")

col1, col2 = st.columns(2)
col1.metric("分數", st.session_state.score)
col1.metric("HP", f"{st.session_state.hp}/{MAX_HP}")
col2.metric("剩餘時間", f"{st.session_state.time_left}s")
col2.progress(st.session_state.time_left / TOTAL_TIME)

st.markdown(f"**{st.session_state.message}**")

if not st.session_state.game_over:
    if st.button('🗡️ 熱血點擊攻擊'):    
        hit_action()
        refresh_timer()
        update_weather()

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

st.markdown('---')
st.info('💡 請在終端機輸入 `streamlit run app.py` 來啟動遊戲預覽。')

