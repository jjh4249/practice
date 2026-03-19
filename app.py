import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Water Health Policy Dashboard",
    page_icon="💧",
    layout="wide",
)

# -----------------------------
# Data (rough prototype based on the report summary)
# -----------------------------
water_quality = pd.DataFrame({
    "Indicator": ["BOD", "COD", "T-N", "T-P", "Chl-a", "Pb", "Cd", "As"],
    "Nakdong_vs_Bukhan_Ratio": [2.4, 2.3, 2.3, 3.3, 3.2, 3.6, 3.4, 3.2],
    "Category": ["Organic", "Organic", "Nutrient", "Nutrient", "Algae", "Heavy Metal", "Heavy Metal", "Heavy Metal"]
})

health_visits = pd.DataFrame({
    "Disease": ["Gastrointestinal", "Endocrine", "Atopy"],
    "Nakdong_vs_Bukhan_Ratio": [2.1, 2.2, 1.2]
})

correlation = pd.DataFrame({
    "Pair": [
        "BOD - Gastrointestinal",
        "DO - Gastrointestinal",
        "Pb - Endocrine",
        "Cd - Endocrine",
        "As - Endocrine",
        "Chl-a - Atopy"
    ],
    "r": [0.985, -0.968, 0.982, 0.980, 0.979, 0.859]
})

scenario = pd.DataFrame({
    "Policy": [
        "Organic pollution reduction",
        "Heavy metal management",
        "Algae early warning",
        "Integrated watershed monitoring"
    ],
    "Estimated Health Benefit (%)": [18, 15, 9, 12]
})

# -----------------------------
# Helpers
# -----------------------------
def bar_chart(df, x_col, y_col, title, xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

def horizontal_bar(df, x_col, y_col, title, xlabel=""):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(df[y_col], df[x_col])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    plt.tight_layout()
    st.pyplot(fig)

# -----------------------------
# App
# -----------------------------
st.title("수질-건강 연계 정책 대시보드")
st.caption("보고서 기반 러프 프로토타입 · Streamlit MVP")

with st.sidebar:
    st.header("탐색 메뉴")
    section = st.radio(
        "섹션 선택",
        ["개요", "수질 비교", "건강 영향", "상관관계", "정책 시나리오", "원문 요약"]
    )

st.markdown(
    """
    이 앱은 업로드된 정책 보고서의 핵심 내용을 빠르게 시각화하기 위한 초기 버전입니다.
    실제 운영용으로 확장할 때는 원본 데이터 연동, 지도 시각화, 시계열 분석, 다운로드 기능을 추가하면 됩니다.
    """
)

if section == "개요":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("핵심 비교 유역", "낙동강 vs 북한강")
    c2.metric("대표 수질지표", "BOD 2.4배")
    c3.metric("대표 건강지표", "내분비 2.2배")
    c4.metric("핵심 메시지", "수질 + 보건 통합관리")

    st.subheader("핵심 메시지")
    st.write("""
    - 낙동강은 북한강 대비 유기물, 영양염류, 조류, 중금속 지표가 전반적으로 더 높게 나타남
    - 소화기 및 내분비계 질환 방문도 더 높게 나타남
    - 수질관리는 환경정책만이 아니라 공중보건 정책과 통합해서 접근할 필요가 있음
    """)

    st.subheader("빠른 비교")
    bar_chart(
        health_visits,
        "Disease",
        "Nakdong_vs_Bukhan_Ratio",
        "질환 방문 상대비교",
        ylabel="Ratio"
    )

elif section == "수질 비교":
    st.subheader("수질오염 지표 비교")
    selected_category = st.selectbox(
        "카테고리 필터",
        ["All"] + sorted(water_quality["Category"].unique().tolist())
    )
    view_df = water_quality.copy()
    if selected_category != "All":
        view_df = view_df[view_df["Category"] == selected_category]

    st.dataframe(view_df, use_container_width=True)

    bar_chart(
        view_df,
        "Indicator",
        "Nakdong_vs_Bukhan_Ratio",
        "낙동강 / 북한강 수질지표 비율",
        ylabel="Ratio"
    )

    st.info("값이 1보다 크면 낙동강 지표가 북한강보다 높다는 뜻입니다.")

elif section == "건강 영향":
    st.subheader("건강영향 비교")
    st.dataframe(health_visits, use_container_width=True)

    bar_chart(
        health_visits,
        "Disease",
        "Nakdong_vs_Bukhan_Ratio",
        "낙동강 / 북한강 질환 방문 비율",
        ylabel="Ratio"
    )

    st.markdown("**해석 포인트**")
    st.write("""
    - 소화기 질환과 내분비계 질환에서 차이가 상대적으로 크게 나타남
    - 아토피는 차이가 있으나 상대적으로 완만함
    """)

elif section == "상관관계":
    st.subheader("수질지표-질환 상관관계")
    st.dataframe(correlation, use_container_width=True)

    horizontal_bar(
        correlation.sort_values("r"),
        "r",
        "Pair",
        "상관계수(r) 비교",
        xlabel="Correlation coefficient"
    )

    st.warning("""
    상관관계는 인과관계와 동일하지 않습니다.
    실제 정책 판단에는 교란변수 통제와 추가 역학분석이 필요합니다.
    """)

elif section == "정책 시나리오":
    st.subheader("정책 시나리오")
    st.dataframe(scenario, use_container_width=True)

    bar_chart(
        scenario,
        "Policy",
        "Estimated Health Benefit (%)",
        "정책별 예상 건강개선 효과",
        ylabel="Estimated benefit (%)"
    )

    st.markdown("**정책 방향 예시**")
    st.write("""
    1. 단기: 총량관리 항목 확대, 조류 사전경보 강화, 집중 측정망 보강  
    2. 중기: 중금속 관리구역 지정, 유역 단위 건강영향평가 도입  
    3. 장기: 수질-공중보건 통합관리 법제화
    """)

elif section == "원문 요약":
    st.subheader("보고서 요약")
    st.write("""
    이 보고서는 낙동강과 북한강의 수질 차이를 비교하고, 그 차이가 주민 건강에 미칠 수 있는 영향을
    분석한 정책 보고서입니다. 낙동강은 북한강보다 BOD, COD, T-N, T-P, 클로로필-a, 중금속 농도가
    전반적으로 높게 나타났고, 소화기 및 내분비계 질환 방문도 더 높았습니다.

    특히 BOD와 소화기 질환, 납·카드뮴·비소와 내분비계 질환, 클로로필-a와 아토피 간의 상관성이
    강하게 나타났다는 점이 핵심입니다. 따라서 수질관리를 단순한 환경관리 차원이 아니라
    보건정책과 통합된 관점으로 확장해야 한다는 정책적 시사점을 제시합니다.
    """)

    st.markdown("**한계**")
    st.write("""
    - 가상 시뮬레이션 데이터 기반
    - 교란변수 통제가 제한적
    - 실제 정책 적용 전 추가 검증 필요
    """)

st.divider()
st.caption("Next step: CSV 연동, 지도 추가, 시계열 데이터 추가, 다운로드 리포트 기능 확장")
