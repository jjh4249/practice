import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="수질오염-건강영향 분석 대시보드",
    page_icon="🌊",
    layout="wide",
)

# -----------------------------------
# Global style
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont,
                 "Malgun Gothic", "맑은 고딕", Arial, sans-serif !important;
}

/* 전체 배경 */
.stApp { background: #f0f4f8; }

/* 사이드바 */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b4b 0%, #1a4a7a 100%) !important;
}
section[data-testid="stSidebar"] * { color: #e8f0fe !important; }
section[data-testid="stSidebar"] .stRadio label { color: #e8f0fe !important; }

/* 컨테이너 */
.block-container { padding: 2rem 2.5rem; }

/* 헤더 */
.dashboard-header {
    background: linear-gradient(135deg, #0d2b4b 0%, #1565c0 60%, #0288d1 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    color: white;
}
.dashboard-header h1 { color: white !important; font-size: 1.7rem; margin: 0 0 0.4rem 0; }
.dashboard-header p { color: #b3d4f5; margin: 0; font-size: 0.9rem; }

/* KPI 카드 */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border-left: 5px solid #1565c0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
.kpi-card .kpi-label { font-size: 0.78rem; color: #6b7a8d; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card .kpi-value { font-size: 2rem; font-weight: 700; color: #0d2b4b; line-height: 1.2; }
.kpi-card .kpi-sub { font-size: 0.82rem; color: #1565c0; margin-top: 0.2rem; }

/* 섹션 헤더 */
.section-header {
    display: flex; align-items: center; gap: 0.6rem;
    font-size: 1.15rem; font-weight: 700; color: #0d2b4b;
    border-bottom: 2px solid #e3eaf3;
    padding-bottom: 0.6rem; margin: 1.6rem 0 1rem 0;
}

/* 차트 카드 */
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 1.2rem;
}

/* 인사이트 박스 */
.insight-box {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f7ff 100%);
    border: 1px solid #b3d4f5;
    border-left: 4px solid #1565c0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #1a2a3a;
    line-height: 1.6;
}
.insight-box b { color: #0d2b4b; }

/* 경고/강조 박스 */
.warn-box {
    background: linear-gradient(135deg, #fff8e1 0%, #fffde7 100%);
    border: 1px solid #ffe082;
    border-left: 4px solid #f9a825;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #4a3800;
    line-height: 1.6;
}

/* 가설 배지 */
.badge-support {
    background: #e8f5e9; color: #2e7d32;
    border: 1px solid #a5d6a7;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.8rem; font-weight: 600;
    display: inline-block;
}
.badge-partial {
    background: #fff8e1; color: #f57f17;
    border: 1px solid #ffe082;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.8rem; font-weight: 600;
    display: inline-block;
}

/* 정책 카드 */
.policy-card {
    background: white; border-radius: 12px;
    padding: 1.2rem 1.4rem;
    border-left: 4px solid #0288d1;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    margin-bottom: 0.9rem;
}
.policy-card h4 { color: #0d2b4b; margin: 0 0 0.4rem 0; font-size: 0.95rem; }
.policy-card p { color: #4a5568; margin: 0; font-size: 0.85rem; line-height: 1.6; }

/* 관측 지점 범례 */
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; margin: 4px 0; }
.dot-nakdong { width: 12px; height: 12px; background: #e53935; border-radius: 50%; display: inline-block; }
.dot-bukhan { width: 12px; height: 12px; background: #1e88e5; border-radius: 50%; display: inline-block; }

/* Streamlit 기본 요소 override */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)

# ===================================
# 공통 색상 팔레트
# ===================================
COLORS = {
    "낙동강": "#e53935",
    "북한강": "#1e88e5",
    "accent": "#0d2b4b",
    "light": "#f0f4f8",
}
FONT = "Noto Sans KR, Malgun Gothic, Arial, sans-serif"

def layout(fig, height=460, margin=None):
    m = margin or dict(l=20, r=20, t=50, b=20)
    fig.update_layout(
        height=height, margin=m,
        font=dict(family=FONT, size=12),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#e3eaf3", borderwidth=1),
    )
    return fig

# ===================================
# 데이터
# ===================================
water_quality_df = pd.DataFrame({
    "지표": ["BOD", "COD", "DO", "T-N", "T-P", "클로로필-a", "납(Pb)", "카드뮴(Cd)", "비소(As)"],
    "단위": ["mg/L", "mg/L", "mg/L", "mg/L", "mg/L", "μg/L", "μg/L", "μg/L", "μg/L"],
    "낙동강": [4.00, 8.31, 7.59, 3.50, 0.13, 51.83, 2.21, 0.17, 2.65],
    "북한강": [1.67, 3.54, 9.20, 1.55, 0.04, 16.16, 0.61, 0.05, 0.83],
    "배율": [2.4, 2.3, 0.8, 2.3, 3.3, 3.2, 3.6, 3.4, 3.2],
    "분류": ["수질", "수질", "수질", "영양염류", "영양염류", "조류", "중금속", "중금속", "중금속"],
})

health_df = pd.DataFrame({
    "질환": ["아토피 피부염", "소화기 질환", "내분비계 질환"],
    "낙동강": [110.56, 66.48, 35.64],
    "북한강": [90.12, 31.40, 16.52],
    "배율": [1.23, 2.12, 2.16],
})

correlation_df = pd.DataFrame({
    "변수 관계": [
        "BOD ↔ 소화기 질환",
        "DO ↔ 소화기 질환",
        "납 ↔ 내분비계 질환",
        "카드뮴 ↔ 내분비계 질환",
        "비소 ↔ 내분비계 질환",
        "클로로필-a ↔ 아토피 피부염",
    ],
    "상관계수 r": [0.985, -0.968, 0.982, 0.980, 0.979, 0.859],
    "유의성": ["p<0.001"] * 6,
    "방향": ["양(+)", "음(-)", "양(+)", "양(+)", "양(+)", "양(+)"],
})

scenario_df = pd.DataFrame({
    "시나리오": ["A", "B", "C", "D"],
    "오염 감소 조건": ["BOD 20% 감소", "중금속 30% 감소", "클로로필-a 25% 감소", "A+B+C 복합 감축"],
    "예상 효과": ["소화기 질환 12~18% 감소", "내분비계 질환 10~15% 감소", "아토피 6~10% 감소", "소화기 15%, 내분비 12%, 아토피 8% 감소"],
    "주요 수혜 지역": ["낙동강 중·하류", "낙동강 공단 인근", "녹조 다발 지역", "전체 유역"],
    "아토피 감소율": [0, 0, 8, 8],
    "소화기 감소율": [15, 0, 0, 15],
    "내분비 감소율": [0, 13, 0, 12],
})

# 관측 지점 (낙동강 25개, 북한강 25개)
np.random.seed(42)
observation_points = pd.DataFrame({
    "이름": ([f"낙동강 지점{i+1}" for i in range(25)] + [f"북한강 지점{i+1}" for i in range(25)]),
    "유역": (["낙동강"] * 25 + ["북한강"] * 25),
    "lat": (
        np.random.uniform(35.1, 36.8, 25).tolist() +
        np.random.uniform(37.4, 38.2, 25).tolist()
    ),
    "lon": (
        np.random.uniform(127.5, 129.0, 25).tolist() +
        np.random.uniform(127.2, 128.0, 25).tolist()
    ),
    "BOD": (
        np.random.normal(4.0, 0.4, 25).tolist() +
        np.random.normal(1.67, 0.2, 25).tolist()
    ),
    "중금속지수": (
        np.random.normal(2.2, 0.3, 25).tolist() +
        np.random.normal(0.61, 0.1, 25).tolist()
    ),
})

current_policy_df = pd.DataFrame({
    "정책명": ["수질오염총량관리제", "물환경측정망 운영", "조류경보제", "통합물관리 정책", "배출시설 관리"],
    "핵심 내용": [
        "유역별 목표수질을 설정하고 오염물질 배출총량 관리",
        "하천·호소 수질을 정기적으로 측정하고 수질 변동 감시",
        "클로로필-a 등 지표 기반 조류 발생 단계별 경보 발령",
        "수량·수질·수생태를 유역 단위로 통합 관리",
        "오염원 배출기준 관리 및 처리시설 운영 효율 개선",
    ],
    "한계": [
        "건강영향 데이터와 직접 연계가 부족함",
        "실시간 대응보다 사후 모니터링 중심",
        "사전예방보다 발생 이후 대응 성격이 강함",
        "실행 주체 간 협업과 데이터 연계가 제한적",
        "비점오염원·중금속 복합오염 대응에 한계",
    ],
    "실행 가능성": ["★★★★", "★★★", "★★★★", "★★", "★★★"],
})

# ===================================
# 사이드바
# ===================================
with st.sidebar:
    st.markdown("## 🌊 분석 메뉴")
    page = st.radio(
        "",
        ["📋 연구 개요", "🗺️ 수질 비교 & 지도", "🏥 건강 영향", "📊 상관관계 분석", "📜 정책 시나리오"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**📂 데이터 출처**")
    st.caption("보건환경정책연구원 (2026)\n낙동강·북한강 유역 수질오염과\n피부·내분비계 질환 상관관계 분석 보고서")
    st.markdown("---")
    st.markdown("**📅 연구 기간**")
    st.caption("2023~2025년 5~9월")
    st.markdown("**📍 관측 지점**")
    st.caption("총 50개 (유역별 25개)")

# ===================================
# 메인 헤더
# ===================================
st.markdown("""
<div class="dashboard-header">
  <h1>🌊 낙동강·북한강 유역 수질오염과 건강영향 분석 대시보드</h1>
  <p>보건환경정책연구원 | 수생태계 미량 화학물질과 피부·내분비계 질환 상관관계 분석 및 정책 제안</p>
</div>
""", unsafe_allow_html=True)

# ===================================
# PAGE 1: 연구 개요
# ===================================
if page == "📋 연구 개요":

    # KPI 카드
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("관측 지점", "50", "유역별 각 25개"),
        ("연구 기간", "3년", "2023 ~ 2025"),
        ("분석 변수", "16개", "수질·건강·기상"),
        ("가설 지지율", "100%", "3개 가설 모두 지지"),
    ]
    for col, (label, val, sub) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    # 가설 검증 결과
    st.markdown('<div class="section-header">🔬 가설 검증 결과</div>', unsafe_allow_html=True)
    hyp_data = [
        ("가설 1", "낙동강 유역은 북한강보다 수질오염 수준이 높고 질병 방문 횟수도 더 높다", "지지", "badge-support"),
        ("가설 2", "유기물 오염·영양염류 농도가 높을수록 소화기 질환 방문 횟수가 증가한다", "강하게 지지", "badge-support"),
        ("가설 3", "중금속 농도가 높을수록 내분비계 질환 방문 횟수가 증가한다", "강하게 지지", "badge-support"),
    ]
    for h, content, result, cls in hyp_data:
        st.markdown(f"""
        <div class="policy-card">
          <h4>{h} &nbsp; <span class="{cls}">{result}</span></h4>
          <p>{content}</p>
        </div>""", unsafe_allow_html=True)

    # 핵심 수치 요약
    st.markdown('<div class="section-header">📈 핵심 수치 요약</div>', unsafe_allow_html=True)

    # 레이더 차트 (오염도 비교)
    categories = ["BOD", "COD", "T-N", "T-P", "클로로필-a", "납(Pb)"]
    nakdong_vals = [4.00, 8.31, 3.50, 0.13*100, 51.83/10, 2.21]  # 스케일 조정
    bukhan_vals  = [1.67, 3.54, 1.55, 0.04*100, 16.16/10, 0.61]

    # 정규화 (0~1)
    max_vals = [max(a, b) for a, b in zip(nakdong_vals, bukhan_vals)]
    n_norm = [v/m for v, m in zip(nakdong_vals, max_vals)]
    b_norm = [v/m for v, m in zip(bukhan_vals, max_vals)]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=n_norm + [n_norm[0]], theta=categories + [categories[0]],
        fill='toself', name='낙동강', line_color=COLORS["낙동강"], fillcolor='rgba(229,57,53,0.25)'))
    fig_radar.add_trace(go.Scatterpolar(r=b_norm + [b_norm[0]], theta=categories + [categories[0]],
        fill='toself', name='북한강', line_color=COLORS["북한강"], fillcolor='rgba(30,136,229,0.25)'))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True, height=380, title="오염도 상대 비교 (정규화)",
        font=dict(family=FONT), paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=20),
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        # 배율 비교 수평 바
        ratio_df = water_quality_df[["지표", "배율", "분류"]].copy()
        color_map = {"수질": "#1e88e5", "영양염류": "#43a047", "조류": "#fb8c00", "중금속": "#e53935"}
        fig_ratio = px.bar(ratio_df, x="배율", y="지표", orientation='h', color="분류",
                           color_discrete_map=color_map,
                           title="낙동강/북한강 오염 배율",
                           text="배율")
        fig_ratio.update_traces(texttemplate="%{text:.1f}x", textposition='outside')
        fig_ratio.add_vline(x=1, line_dash="dash", line_color="gray", annotation_text="기준(1x)")
        layout(fig_ratio, height=380)
        fig_ratio.update_layout(xaxis_title="배율 (낙동강 ÷ 북한강)", yaxis_title="")
        st.plotly_chart(fig_ratio, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    💡 <b>핵심 인사이트</b>: 낙동강 유역은 모든 오염 지표에서 북한강 대비 2~4배 높은 수준을 보이며,
    특히 <b>중금속(납 3.6배, 카드뮴 3.4배, 비소 3.2배)</b>과 <b>클로로필-a(3.2배)</b>의 격차가 두드러진다.
    소화기·내분비계 질환 방문 횟수는 낙동강 유역에서 약 2배 이상 높게 나타났다.
    </div>""", unsafe_allow_html=True)

# ===================================
# PAGE 2: 수질 비교 & 지도
# ===================================
elif page == "🗺️ 수질 비교 & 지도":

    st.markdown('<div class="section-header">🗺️ 관측 지점 분포 지도</div>', unsafe_allow_html=True)

    map_tab1, map_tab2 = st.tabs(["📍 관측 지점 분포", "🌡️ BOD 농도 분포"])

    with map_tab1:
        fig_map = px.scatter_mapbox(
            observation_points,
            lat="lat", lon="lon",
            color="유역",
            color_discrete_map={"낙동강": "#e53935", "북한강": "#1e88e5"},
            hover_name="이름",
            hover_data={"BOD": ":.2f", "중금속지수": ":.2f", "lat": False, "lon": False},
            size_max=12,
            zoom=6.0,
            center={"lat": 36.5, "lon": 128.0},
            mapbox_style="carto-positron",
            title="낙동강·북한강 유역 관측 지점 분포 (총 50개)",
            height=500,
        )
        fig_map.update_traces(marker=dict(size=10, opacity=0.85))
        fig_map.update_layout(
            font=dict(family=FONT),
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(title="유역", x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with map_tab2:
        observation_points["BOD_clipped"] = observation_points["BOD"].clip(lower=0.5)
        fig_map2 = px.scatter_mapbox(
            observation_points,
            lat="lat", lon="lon",
            color="BOD_clipped",
            color_continuous_scale=["#1e88e5", "#ffee58", "#e53935"],
            size="BOD_clipped",
            size_max=16,
            hover_name="이름",
            hover_data={"BOD": ":.2f", "유역": True, "lat": False, "lon": False, "BOD_clipped": False},
            zoom=6.0,
            center={"lat": 36.5, "lon": 128.0},
            mapbox_style="carto-positron",
            title="관측 지점별 BOD 농도 (mg/L)",
            height=500,
            labels={"BOD_clipped": "BOD (mg/L)"},
        )
        fig_map2.update_layout(
            font=dict(family=FONT),
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(title="BOD<br>(mg/L)"),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_map2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    📍 <b>지도 해설</b>: 낙동강 유역 관측 지점은 경상북도~경상남도 일대(북위 35.1°~36.8°),
    북한강 유역은 강원도~경기도 일대(북위 37.4°~38.2°)에 각 25개씩 배치되었다.
    BOD 농도는 낙동강 중·하류 구간에서 뚜렷하게 높게 나타난다.
    </div>""", unsafe_allow_html=True)

    # 수질 비교 차트
    st.markdown('<div class="section-header">💧 유역별 수질 지표 비교</div>', unsafe_allow_html=True)

    col_sel = st.selectbox("분류 선택", ["전체", "수질", "영양염류", "조류", "중금속"])
    df_filt = water_quality_df if col_sel == "전체" else water_quality_df[water_quality_df["분류"] == col_sel]

    chart_df = df_filt.melt(id_vars=["지표", "단위", "분류"], value_vars=["낙동강", "북한강"],
                             var_name="유역", value_name="값")
    fig_bar = px.bar(chart_df, x="지표", y="값", color="유역", barmode="group",
                     color_discrete_map={"낙동강": COLORS["낙동강"], "북한강": COLORS["북한강"]},
                     text_auto=".2f",
                     title=f"유역별 수질 지표 평균 비교 ({col_sel})")
    fig_bar.update_traces(textposition='outside', textfont_size=10)
    layout(fig_bar, height=420)
    fig_bar.update_layout(xaxis_title="", yaxis_title="농도", bargap=0.25)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 수질 히트맵 (정규화)
    st.markdown('<div class="section-header">🔥 오염 강도 히트맵</div>', unsafe_allow_html=True)
    pivot = water_quality_df.set_index("지표")[["낙동강", "북한강"]]
    # 각 지표를 행 최대값으로 정규화
    pivot_norm = pivot.div(pivot.max(axis=1), axis=0)

    fig_heat = px.imshow(pivot_norm.T, color_continuous_scale="RdYlBu_r",
                         title="오염 강도 히트맵 (행 최대값 대비 정규화)",
                         text_auto=".2f", aspect="auto")
    layout(fig_heat, height=220)
    fig_heat.update_layout(coloraxis_colorbar=dict(title="상대 강도"), xaxis_title="", yaxis_title="")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 원자료</div>', unsafe_allow_html=True)
    st.dataframe(
        water_quality_df[["지표", "단위", "낙동강", "북한강", "배율", "분류"]],
        use_container_width=True, hide_index=True,
    )

# ===================================
# PAGE 3: 건강 영향
# ===================================
elif page == "🏥 건강 영향":

    st.markdown('<div class="section-header">🏥 유역별 질환 방문 횟수 비교</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        health_melt = health_df.melt(id_vars=["질환"], value_vars=["낙동강", "북한강"],
                                      var_name="유역", value_name="방문 횟수")
        fig_health = px.bar(health_melt, x="질환", y="방문 횟수", color="유역", barmode="group",
                            color_discrete_map={"낙동강": COLORS["낙동강"], "북한강": COLORS["북한강"]},
                            text_auto=".1f",
                            title="질환별 의료기관 방문 횟수 평균 (회)")
        fig_health.update_traces(textposition='outside')
        layout(fig_health, height=400)
        fig_health.update_layout(xaxis_title="", yaxis_title="방문 횟수 (회)")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_health, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # 배율 게이지 카드
        for _, row in health_df.iterrows():
            color = "#e53935" if row["배율"] > 2 else "#fb8c00"
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:{color}">
              <div class="kpi-label">{row['질환']}</div>
              <div class="kpi-value" style="color:{color}">{row['배율']:.1f}x</div>
              <div class="kpi-sub">낙동강 ÷ 북한강 | 낙동강 {row['낙동강']:.0f}회 vs 북한강 {row['북한강']:.0f}회</div>
            </div>""", unsafe_allow_html=True)

    # 누적 가로 바
    st.markdown('<div class="section-header">📊 질환별 유역 비중 비교</div>', unsafe_allow_html=True)

    fig_ratio2 = go.Figure()
    for i, row in health_df.iterrows():
        total = row["낙동강"] + row["북한강"]
        fig_ratio2.add_trace(go.Bar(
            name="낙동강", x=[row["낙동강"] / total * 100], y=[row["질환"]],
            orientation='h', marker_color=COLORS["낙동강"],
            text=f"낙동강 {row['낙동강'] / total * 100:.0f}%",
            textposition='inside', showlegend=(i == 0),
        ))
        fig_ratio2.add_trace(go.Bar(
            name="북한강", x=[row["북한강"] / total * 100], y=[row["질환"]],
            orientation='h', marker_color=COLORS["북한강"],
            text=f"북한강 {row['북한강'] / total * 100:.0f}%",
            textposition='inside', showlegend=(i == 0),
        ))
    fig_ratio2.update_layout(barmode='stack', height=280,
                              xaxis_title="비중 (%)", yaxis_title="",
                              font=dict(family=FONT), paper_bgcolor="white", plot_bgcolor="white",
                              margin=dict(l=20, r=20, t=40, b=20),
                              title="질환별 유역 비중 (%)  ← 낙동강이 클수록 오염 연관성↑")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_ratio2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 건강 지표 summary box
    st.markdown("""
    <div class="insight-box">
    🏥 <b>해석</b>:
    소화기 질환(2.1배)과 내분비계 질환(2.2배)은 수질오염 수준의 차이와 유사한 배율로 낙동강에서 높게 나타난다.
    반면 아토피 피부염(1.2배)은 기온·습도 등 기상 요인의 복합 작용이 크므로 수질 단독 요인으로 설명하기 어렵다.
    </div>
    <div class="warn-box">
    ⚠️ <b>주의</b>: 본 데이터는 시뮬레이션 기반이며, 생활 습관·소득 수준·의료 접근성 등
    교란 변수를 통제한 추가 역학 연구가 필요하다.
    </div>""", unsafe_allow_html=True)

# ===================================
# PAGE 4: 상관관계 분석
# ===================================
elif page == "📊 상관관계 분석":

    st.markdown('<div class="section-header">📊 상관계수 개요</div>', unsafe_allow_html=True)

    # 상관계수 워터폴 스타일 바
    corr_sorted = correlation_df.sort_values("상관계수 r", key=abs, ascending=True)
    colors = [COLORS["낙동강"] if v > 0 else COLORS["북한강"] for v in corr_sorted["상관계수 r"]]
    fig_corr = go.Figure(go.Bar(
        x=corr_sorted["상관계수 r"],
        y=corr_sorted["변수 관계"],
        orientation='h',
        marker_color=colors,
        text=[f"r = {v:.3f}" for v in corr_sorted["상관계수 r"]],
        textposition='outside',
    ))
    fig_corr.add_vline(x=0, line_color="black", line_width=1)
    layout(fig_corr, height=380)
    fig_corr.update_layout(
        title="주요 변수 간 피어슨 상관계수 (p<0.001)",
        xaxis=dict(range=[-1.1, 1.1], title="상관계수 r"),
        yaxis_title="",
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 산점도 시뮬레이션
    st.markdown('<div class="section-header">🔍 주요 관계 산점도 시뮬레이션</div>', unsafe_allow_html=True)

    selected_rel = st.selectbox("관계 선택", correlation_df["변수 관계"].tolist())
    sel_row = correlation_df[correlation_df["변수 관계"] == selected_rel].iloc[0]
    r = sel_row["상관계수 r"]

    # 시뮬레이션 데이터 생성
    np.random.seed(7)
    n_n, n_b = 25, 25

    def sim_data(r, x_mean, x_std, y_mean, y_std, n):
        x = np.random.normal(x_mean, x_std, n)
        noise = np.random.normal(0, 1, n)
        y = y_mean + y_std * (r * (x - x_mean) / x_std + np.sqrt(1 - r**2) * noise)
        return x, y

    rel_params = {
        "BOD ↔ 소화기 질환":         (4.0, 0.35,  66.5, 4.5, 1.67, 0.2,  31.4, 2.0),
        "DO ↔ 소화기 질환":           (7.6, 0.4,   66.5, 4.5, 9.2,  0.35, 31.4, 2.0),
        "납 ↔ 내분비계 질환":          (2.2, 0.3,   35.6, 3.0, 0.61, 0.1,  16.5, 1.5),
        "카드뮴 ↔ 내분비계 질환":     (0.17,0.02,  35.6, 3.0, 0.05, 0.01, 16.5, 1.5),
        "비소 ↔ 내분비계 질환":        (2.65,0.3,   35.6, 3.0, 0.83, 0.1,  16.5, 1.5),
        "클로로필-a ↔ 아토피 피부염": (51.8,4.0,  110.6, 5.0,16.2,  2.0,  90.1, 4.5),
    }
    params = rel_params[selected_rel]
    x_n, y_n = sim_data(r, params[0], params[1], params[2], params[3], n_n)
    x_b, y_b = sim_data(r, params[4], params[5], params[6], params[7], n_b)

    parts = selected_rel.split(" ↔ ")
    xlab, ylab = parts[0].strip(), parts[1].strip()

    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(x=x_n, y=y_n, mode='markers', name='낙동강',
        marker=dict(color=COLORS["낙동강"], size=9, opacity=0.75)))
    fig_scatter.add_trace(go.Scatter(x=x_b, y=y_b, mode='markers', name='북한강',
        marker=dict(color=COLORS["북한강"], size=9, opacity=0.75)))

    # 전체 회귀선
    all_x = np.concatenate([x_n, x_b])
    all_y = np.concatenate([y_n, y_b])
    m, b_coef = np.polyfit(all_x, all_y, 1)
    x_line = np.linspace(all_x.min(), all_x.max(), 100)
    fig_scatter.add_trace(go.Scatter(x=x_line, y=m * x_line + b_coef, mode='lines',
        name=f'회귀선 (r={r:.3f})', line=dict(color='gray', dash='dash', width=2)))

    layout(fig_scatter, height=420)
    fig_scatter.update_layout(
        title=f"{xlab} vs {ylab}  |  r = {r:.3f}, p < 0.001",
        xaxis_title=xlab, yaxis_title=ylab,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 해석 카드
    abs_r = abs(r)
    strength = "매우 강한" if abs_r >= 0.9 else "강한" if abs_r >= 0.7 else "중간"
    direction = "양의" if r > 0 else "음의"
    st.markdown(f"""
    <div class="insight-box">
    📊 <b>해석</b>: {xlab}와 {ylab} 간에는 <b>{strength} {direction} 상관관계(r = {r:.3f})</b>가 확인된다 (p &lt; 0.001).
    이는 {xlab} 수준이 높아질수록 {ylab}{'이' if direction == '양의' else '은'} {'증가' if r > 0 else '감소'}하는 경향이 통계적으로 유의미함을 의미한다.
    </div>""", unsafe_allow_html=True)

    # 상관관계 전체 테이블
    st.markdown('<div class="section-header">📋 전체 상관관계 요약</div>', unsafe_allow_html=True)
    st.dataframe(correlation_df, use_container_width=True, hide_index=True)

    # R² 바
    st.markdown('<div class="section-header">📐 설명력 (R²) 비교</div>', unsafe_allow_html=True)
    r2_df = correlation_df.copy()
    r2_df["R²"] = r2_df["상관계수 r"] ** 2
    fig_r2 = px.bar(r2_df, x="변수 관계", y="R²", text_auto=".3f",
                    color="R²", color_continuous_scale="Blues",
                    title="변수 관계별 설명력 R² (1에 가까울수록 강한 설명력)")
    fig_r2.update_traces(textposition='outside')
    layout(fig_r2, height=380)
    fig_r2.update_layout(xaxis_title="", yaxis_range=[0, 1.1],
                          coloraxis_showscale=False)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_r2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================
# PAGE 5: 정책 시나리오
# ===================================
elif page == "📜 정책 시나리오":

    tab1, tab2 = st.tabs(["🏛️ 현행 정책", "🚀 개선 시나리오"])

    with tab1:
        st.markdown('<div class="section-header">🏛️ 현재 시행 중인 주요 정책</div>', unsafe_allow_html=True)

        for _, row in current_policy_df.iterrows():
            st.markdown(f"""
            <div class="policy-card">
              <h4>{row['정책명']} &nbsp; <span style="color:#888;font-size:0.85rem">{row['실행 가능성']}</span></h4>
              <p>✅ {row['핵심 내용']}<br>⚠️ <i>{row['한계']}</i></p>
            </div>""", unsafe_allow_html=True)

        # 실행 가능성 시각화
        st.markdown('<div class="section-header">📊 정책 실행 가능성 비교</div>', unsafe_allow_html=True)
        feasibility_map = {"★★★★": 4, "★★★": 3, "★★": 2, "★": 1}
        current_policy_df["실행점수"] = current_policy_df["실행 가능성"].map(feasibility_map)
        fig_feas = px.bar(current_policy_df, x="정책명", y="실행점수",
                          color="실행점수", color_continuous_scale="Blues",
                          text="실행 가능성", title="정책별 실행 가능성 (4점 만점)")
        fig_feas.update_traces(textposition='outside')
        layout(fig_feas, height=360)
        fig_feas.update_layout(yaxis_range=[0, 5], yaxis_title="실행 점수",
                                coloraxis_showscale=False, xaxis_title="")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_feas, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-header">🚀 오염 저감 시나리오 분석</div>', unsafe_allow_html=True)

        # 시나리오 전체 비교
        sc_melt = scenario_df.melt(
            id_vars=["시나리오"], value_vars=["아토피 감소율", "소화기 감소율", "내분비 감소율"],
            var_name="질환", value_name="감소율 (%)"
        )
        label_map = {"아토피 감소율": "아토피 피부염", "소화기 감소율": "소화기 질환", "내분비 감소율": "내분비계 질환"}
        sc_melt["질환"] = sc_melt["질환"].map(label_map)

        fig_sc = px.bar(sc_melt, x="시나리오", y="감소율 (%)", color="질환", barmode="group",
                        color_discrete_map={
                            "아토피 피부염": "#fb8c00",
                            "소화기 질환": "#1e88e5",
                            "내분비계 질환": "#e53935",
                        },
                        text_auto=".0f",
                        title="시나리오별 질환 기대 감소율 (%)")
        fig_sc.update_traces(textposition='outside')
        layout(fig_sc, height=400)
        fig_sc.update_layout(yaxis_title="감소율 (%)", yaxis_range=[0, 20])
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_sc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 시나리오 선택 상세
        st.markdown('<div class="section-header">🔍 시나리오 상세 분석</div>', unsafe_allow_html=True)
        sel_sc = st.select_slider("시나리오 선택", options=["A", "B", "C", "D"])
        sc_row = scenario_df[scenario_df["시나리오"] == sel_sc].iloc[0]

        col1, col2 = st.columns([1.2, 0.8])
        with col1:
            st.markdown(f"""
            <div class="policy-card" style="border-left-color:#0d2b4b">
              <h4>시나리오 {sel_sc}: {sc_row['오염 감소 조건']}</h4>
              <p>
                🎯 <b>예상 효과</b>: {sc_row['예상 효과']}<br>
                📍 <b>주요 수혜 지역</b>: {sc_row['주요 수혜 지역']}<br><br>
                📉 아토피 감소율: <b>{sc_row['아토피 감소율']}%</b><br>
                📉 소화기 감소율: <b>{sc_row['소화기 감소율']}%</b><br>
                📉 내분비계 감소율: <b>{sc_row['내분비 감소율']}%</b>
              </p>
            </div>""", unsafe_allow_html=True)

            # 의료비 절감 추정
            base_visits = {"아토피": 110.56, "소화기": 66.48, "내분비": 35.64}
            cost_per_visit = {"아토피": 80000, "소화기": 60000, "내분비": 120000}
            population = 3_000_000  # 낙동강 인근 인구 추정
            total_saving = (
                base_visits["아토피"] * sc_row["아토피 감소율"] / 100 * cost_per_visit["아토피"] +
                base_visits["소화기"] * sc_row["소화기 감소율"] / 100 * cost_per_visit["소화기"] +
                base_visits["내분비"] * sc_row["내분비 감소율"] / 100 * cost_per_visit["내분비"]
            ) * population / 1e8  # 억 원

            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:#2e7d32;margin-top:1rem">
              <div class="kpi-label">💰 연간 의료비 절감 추정 (낙동강 유역)</div>
              <div class="kpi-value" style="color:#2e7d32">{total_saving:.0f}억 원</div>
              <div class="kpi-sub">인구 300만 명 기준 시뮬레이션 추정치</div>
            </div>""", unsafe_allow_html=True)

        with col2:
            vals = [sc_row["아토피 감소율"], sc_row["소화기 감소율"], sc_row["내분비 감소율"]]
            labels_pie = ["아토피 피부염", "소화기 질환", "내분비계 질환"]
            non_zero = [(l, v) for l, v in zip(labels_pie, vals) if v > 0]

            if non_zero:
                fig_pie = go.Figure(go.Pie(
                    labels=[x[0] for x in non_zero],
                    values=[x[1] for x in non_zero],
                    hole=0.5,
                    marker_colors=["#fb8c00", "#1e88e5", "#e53935"][:len(non_zero)],
                ))
                fig_pie.update_traces(textinfo="percent+label", textfont_size=12)
                fig_pie.update_layout(
                    title=f"시나리오 {sel_sc} 기대 효과 구성",
                    height=320, font=dict(family=FONT),
                    paper_bgcolor="white", margin=dict(l=10, r=10, t=50, b=10),
                    showlegend=False,
                )
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_pie, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("이 시나리오는 단독 효과가 없습니다. 시나리오 D를 선택해 복합 효과를 확인하세요.")

        # 단기·중기·장기 정책 로드맵
        st.markdown('<div class="section-header">🗓️ 정책 로드맵</div>', unsafe_allow_html=True)
        roadmap = [
            ("단기 (1~2년)", "#1e88e5", [
                "총량관리 항목 확대 (납·카드뮴·비소·클로로필-a 추가)",
                "수질-건강 통합 모니터링 시스템 구축 (환경부-복지부 공동)",
                "조류 사전 경보 강화 (ML 기반 예측 모델 도입)",
                "낙동강 자동 측정망 10개소 추가 설치",
            ]),
            ("중기 (3~5년)", "#43a047", [
                "중금속 집중관리구역 지정 및 저감 시설 의무화",
                "유역 단위 건강영향평가 제도 도입",
                "건강 취약지역 무상 의료 지원 프로그램",
                "영양염류 저감 농업 인센티브 제공",
            ]),
            ("장기 (5년 이상)", "#e53935", [
                "유역 단위 통합 거버넌스 법제화",
                "수환경 건강영향 예방 및 관리에 관한 법률 제정",
                "탄소중립 연계 수질 관리 로드맵 수립",
            ]),
        ]
        for period, color, items in roadmap:
            items_html = "".join([f"<li>{it}</li>" for it in items])
            st.markdown(f"""
            <div class="policy-card" style="border-left-color:{color}">
              <h4 style="color:{color}">{period}</h4>
              <ul style="margin:0;padding-left:1.2rem;color:#4a5568;font-size:0.85rem;line-height:1.8">
                {items_html}
              </ul>
            </div>""", unsafe_allow_html=True)
