import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="은퇴 자금 계산기", page_icon="💰", layout="centered")

def format_krw(amount_won):
    """원 단위 금액을 억, 만 원 단위 문자열로 변환"""
    eok = int(amount_won // 100000000)
    man = int((amount_won % 100000000) // 10000)
    
    result = []
    if eok > 0:
        result.append(f"{eok}억")
    if man > 0:
        result.append(f"{man:,}만")
    
    return " ".join(result) + " 원" if result else "0 원"

st.title("💰 복리 은퇴 자금 계산기")
st.markdown("매월 적립식 투자의 복리 효과를 상세 단위(억, 만 원)로 확인하세요.")

# 사이드바 입력 폼
with st.sidebar:
    st.header("투자 조건 입력")
    monthly_investment_man = st.number_input("매월 적립액 (만 원)", min_value=0, value=90, step=10)
    years = st.slider("투자 기간 (년)", min_value=1, max_value=50, value=23)
    annual_return_rate = st.number_input("연평균 수익률 (%)", min_value=0.0, value=20.0, step=1.0)

# 계산 로직
monthly_investment = monthly_investment_man * 10000
months = years * 12
monthly_rate = annual_return_rate / 100 / 12

principals = []
totals = []
current_total = 0

for i in range(1, months + 1):
    current_total = (current_total + monthly_investment) * (1 + monthly_rate)
    if i % 12 == 0:
        principals.append(monthly_investment * i)
        totals.append(current_total)

final_amount = totals[-1] if totals else 0
total_principal = monthly_investment * months
total_interest = final_amount - total_principal

# 결과 요약 표시
st.subheader("📌 최종 예상 결과")
st.success(f"### 은퇴 시 예상 자산: **{format_krw(final_amount)}**")

col1, col2 = st.columns(2)
with col1:
    st.metric("총 투자 원금", format_krw(total_principal))
with col2:
    st.metric("누적 이자 수익", format_krw(total_interest))

st.divider()

# 연도별 자산 성장 추이 (백만 원 단위 차트)
st.subheader("📈 연도별 자산 성장 추이 (단위: 백만 원)")
chart_data = pd.DataFrame({
    "년도": range(1, years + 1),
    "투자 원금": [p / 1000000 for p in principals],
    "예상 자산": [t / 1000000 for t in totals]
}).set_index("년도")

st.line_chart(chart_data)

# 상세 데이터 표
if st.checkbox("연도별 상세 금액 보기"):
    df_details = pd.DataFrame({
        "년도": [f"{y}년차" for y in range(1, years + 1)],
        "누적 원금": [format_krw(p) for p in principals],
        "예상 자산": [format_krw(t) for t in totals]
    })
    st.table(df_details)
