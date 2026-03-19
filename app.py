import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="수질오염-건강영향 분석 대시보드",
    page_icon="🌊",
    layout="wide",
)

# -----------------------------------
# Font / style fix for Korean text
# -----------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
                     "Malgun Gothic", "맑은 고딕", "Noto Sans CJK KR",
                     "Noto Sans KR", "Nanum Gothic", Arial, sans-serif !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-weight: 700 !important;
    }

    .metric-card {
        padding: 16px;
        border-radius: 12px;
        background: #f7f7f9;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }

    .policy-card {
        padding: 18px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #dbe2ea;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------
# Data
# -----------------------------------
water_quality_df = pd.DataFrame({
    "지표": ["BOD", "COD", "DO", "T-N", "T-P", "클로로필-a", "납 Pb", "카드뮴 Cd", "비소 As"],
    "단위": ["mg/L", "mg/L", "mg/L", "mg/L", "mg/L", "μg/L", "μg/L", "μg/L", "μg/L"],
    "낙동강": [4.00, 8.31, 7.59, 3.50, 0.13, 51.83, 2.21, 0.17, 2.65],
    "북한강": [1.67, 3.54, 9.20, 1.55, 0.04, 16.16, 0.61, 0.05, 0.83],
})

health_df = pd.DataFrame({
    "질환": ["아토피 피부염", "소화기 질환", "내분비계 질환"],
    "낙동강": [110.56, 66.48, 35.64],
    "북한강": [90.12, 31.40, 16.52],
})

hypothesis_df = pd.DataFrame({
    "가설": ["가설 1", "가설 2", "가설 3"],
    "내용": [
        "낙동강 유역은 북한강 유역보다 수질오염 수준이 높고 질병 방문 횟수도 더 높다",
        "유기물 오염·영양염류 농도가 높을수록 소화기 질환 방문 횟수가 증가한다",
        "중금속 농도가 높을수록 내분비계 질환 방문 횟수가 증가한다",
    ],
    "결과": ["지지", "강하게 지지", "강하게 지지"],
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
    "유의성": ["p < 0.001"] * 6,
})

scenario_df = pd.DataFrame({
    "시나리오": ["A", "B", "C", "D"],
    "오염 감소 조건": [
        "BOD 20% 감소",
        "중금속 30% 감소",
        "클로로필-a 25% 감소",
        "A+B+C 복합 감축"
    ],
    "예상 효과": [
        "소화기 질환 12~18% 감소",
        "내분비계 질환 10~15% 감소",
        "아토피 6~10% 감소",
        "소화기 15%, 내분비 12%, 아토피 8% 감소"
    ],
    "주요 수혜 지역": [
        "낙동강 중·하류",
        "낙동강 공단 인근",
        "녹조 다발 지역",
        "전체 유역"
    ]
})

# 현황 정책 데이터 추가
current_policy_df = pd.DataFrame({
    "정책명": [
        "수질오염총량관리제",
        "물환경측정망 운영",
        "조류경보제",
        "통합물관리 정책",
        "배출시설 및 공공하수처리장 관리"
    ],
    "핵심 내용": [
        "유역별 목표수질을 설정하고 오염물질 배출총량을 관리",
        "하천·호소 수질을 정기적으로 측정하고 수질 변동을 감시",
        "클로로필-a 등 지표를 기반으로 조류 발생 단계별 경보 발령",
        "수량·수질·수생태를 유역 단위로 통합 관리",
        "오염원 배출기준 관리 및 처리시설 운영 효율 개선"
    ],
    "한계": [
        "건강영향 데이터와 직접 연계가 부족함",
        "실시간 대응보다 사후 모니터링 중심",
        "사전예방보다 발생 이후 대응 성격이 강함",
        "실행 주체 간 협업과 데이터 연계가 아직 제한적",
        "비점오염원·중금속 복합오염 대응에는 한계가 있음"
    ]
})

# -----------------------------------
# Helpers
# -----------------------------------
def make_grouped_bar(df: pd.DataFrame, category_col: str, title: str):
    chart_df = df.melt(
        id_vars=[category_col],
        value_vars=["낙동강", "북한강"],
        var_name="유역",
        value_name="값"
    )
    fig = px.bar(
        chart_df,
        x=category_col,
        y="값",
        color="유역",
        barmode="group",
        title=title,
        text_auto=".2f"
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title="값",
        legend_title="유역",
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", '
                   '"Malgun Gothic", "맑은 고딕", "Noto Sans KR", Arial, sans-serif'
        ),
        height=480,
    )
    return fig

def make_correlation_bar(df: pd.DataFrame, title: str):
    fig = px.bar(
        df,
        x="변수 관계",
        y="상관계수 r",
        title=title,
        text_auto=".3f"
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title="상관계수 r",
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", '
                   '"Malgun Gothic", "맑은 고딕", "Noto Sans KR", Arial, sans-serif'
        ),
        height=480,
    )
    return fig

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.title("분석 메뉴")
page = st.sidebar.radio(
    "이동",
    ["개요", "수질 비교", "건강영향", "상관관계", "정책 시나리오"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**데이터 출처**")
st.sidebar.caption("업로드된 보고서 기반 요약 대시보드")

# -----------------------------------
# Main
# -----------------------------------
st.title("낙동강·북한강 유역 수질오염과 건강영향 분석 대시보드")
st.caption("보고서 기반 러프 버전 Streamlit 앱")

if page == "개요":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("관측 지점 수", "50개", "유역별 각 25개")
    with col2:
        st.metric("연구 기간", "2023~2025", "5~9월 기준")
    with col3:
        st.metric("주요 분석 대상", "수질 + 건강", "상관·회귀·시나리오")

    st.markdown("### 연구 목적")
    st.write(
        """
        본 대시보드는 낙동강과 북한강 유역의 수질오염 수준과
        피부·소화기·내분비계 질환 방문 현황 간의 관계를
        직관적으로 확인하기 위한 시각화 앱이다.
        """
    )

    st.markdown("### 가설 검증 결과")
    st.dataframe(hypothesis_df, use_container_width=True, hide_index=True)

    st.markdown("### 핵심 요약")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="metric-card">
            <b>오염 수준</b><br>
            낙동강 유역은 BOD, COD, T-N, T-P, 중금속, 클로로필-a 모두에서
            북한강보다 높은 평균값을 보였다.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="metric-card">
            <b>건강영향</b><br>
            소화기 질환과 내분비계 질환 방문 횟수는 낙동강 유역에서
            더 높게 나타났다.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "수질 비교":
    st.subheader("유역별 주요 수질 지표 비교")
    st.plotly_chart(
        make_grouped_bar(
            water_quality_df.iloc[:6],
            "지표",
            "유역별 주요 수질 지표 평균 비교"
        ),
        use_container_width=True
    )

    st.markdown("### 중금속 비교")
    st.plotly_chart(
        make_grouped_bar(
            water_quality_df.iloc[6:],
            "지표",
            "유역별 중금속 농도 평균 비교"
        ),
        use_container_width=True
    )

    st.markdown("### 원자료")
    st.dataframe(water_quality_df, use_container_width=True, hide_index=True)

elif page == "건강영향":
    st.subheader("유역별 질환 방문 횟수 비교")
    st.plotly_chart(
        make_grouped_bar(
            health_df,
            "질환",
            "유역별 질환 방문 횟수 평균 비교"
        ),
        use_container_width=True
    )

    st.markdown("### 질환별 평균값")
    st.dataframe(health_df, use_container_width=True, hide_index=True)

    st.markdown("### 해석")
    st.write(
        """
        - 소화기 질환: 낙동강 유역이 북한강보다 약 2.1배 높음  
        - 내분비계 질환: 낙동강 유역이 북한강보다 약 2.2배 높음  
        - 아토피 피부염: 차이는 있으나 상대적으로 격차는 작음
        """
    )

elif page == "상관관계":
    st.subheader("주요 변수 간 상관관계")
    st.plotly_chart(
        make_correlation_bar(
            correlation_df,
            "수질·중금속·질환 변수 간 상관계수"
        ),
        use_container_width=True
    )

    st.dataframe(correlation_df, use_container_width=True, hide_index=True)

    selected_relation = st.selectbox(
        "관심 관계 선택",
        correlation_df["변수 관계"].tolist()
    )

    selected_row = correlation_df[correlation_df["변수 관계"] == selected_relation].iloc[0]

    st.markdown("### 선택 결과")
    st.write(f"**변수 관계:** {selected_row['변수 관계']}")
    st.write(f"**상관계수 r:** {selected_row['상관계수 r']}")
    st.write(f"**유의성:** {selected_row['유의성']}")

elif page == "정책 시나리오":
    st.subheader("현황 정책 및 개선 시나리오")

    tab1, tab2 = st.tabs(["현황 정책", "개선 시나리오"])

    with tab1:
        st.markdown("### 현재 시행 중인 주요 정책")
        st.dataframe(current_policy_df, use_container_width=True, hide_index=True)

        st.markdown("### 정책 해설")
        st.markdown(
            """
            <div class="policy-card">
            <b>1. 수질오염총량관리제</b><br>
            유역 단위로 목표수질을 설정하고 오염부하량을 관리하는 제도다.
            다만 수질 기준 충족 여부 중심이라 건강영향과 직접 연결한 평가는 부족하다.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="policy-card">
            <b>2. 물환경측정망 운영</b><br>
            정기 측정을 통해 하천과 호소의 수질 변화를 파악하는 데 효과적이다.
            하지만 실시간 예측과 선제 대응 기능은 상대적으로 약하다.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="policy-card">
            <b>3. 조류경보제</b><br>
            녹조 발생 시 경보를 발령해 대응을 유도하는 제도다.
            다만 경보 이전 단계의 예방 관리와 건강위험 조기 차단 측면은 강화가 필요하다.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="policy-card">
            <b>4. 종합 평가</b><br>
            현재 정책들은 수질 관리 체계 자체는 갖추고 있지만,
            수질 데이터와 지역 주민 건강 데이터를 통합해 해석하는 구조는 아직 미흡하다.
            따라서 향후에는 '오염 관리' 중심에서 '건강영향 예방'까지 확장할 필요가 있다.
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown("### 오염 저감 시나리오별 기대 효과")
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)

        st.markdown("### 제안 정책 방향")
        st.write(
            """
            1. 총량관리 항목 확대  
            2. 수질-건강 통합 모니터링 시스템 구축  
            3. 조류 사전 예측 모델 도입  
            4. 낙동강 자동 측정망 보강  
            5. 중금속 집중관리구역 지정
            """
        )

        st.markdown("### 시나리오 해석")
        selected_scenario = st.selectbox(
            "시나리오 선택",
            scenario_df["시나리오"].tolist()
        )

        selected_scenario_row = scenario_df[scenario_df["시나리오"] == selected_scenario].iloc[0]

        st.markdown(
            f"""
            <div class="policy-card">
            <b>선택한 시나리오: {selected_scenario_row['시나리오']}</b><br><br>
            <b>오염 감소 조건</b>: {selected_scenario_row['오염 감소 조건']}<br>
            <b>예상 효과</b>: {selected_scenario_row['예상 효과']}<br>
            <b>주요 수혜 지역</b>: {selected_scenario_row['주요 수혜 지역']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 실행 포인트")
    st.info(
        "현재 버전은 보고서 요약 시각화용 러프 앱이다. "
        "다음 단계에서는 현황 정책-개선안 비교 차트, 지역별 정책 적용 지도, "
        "정책 우선순위 평가 기능을 추가하면 더 완성도 있는 대시보드가 된다."
    )
