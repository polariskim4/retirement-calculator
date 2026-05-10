import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="은퇴 자금 계산기", page_icon="💰", layout="centered")

st.title("💰 복리 은퇴 자금 계산기")
st.markdown("매월 꾸준히 적립식으로 투자할 때, 복리 효과를 통해 은퇴 시점에 모이는 자산을 계산하고 시각화합니다.")

# 사이드바 입력 폼
with st.sidebar:
    st.header("투자 조건 입력")
    monthly_investment = st.number_input("매월 적립액 (원)", min_value=0, value=900000, step=50000, format="%d")
    years = st.slider("투자 기간 (년)", min_value=1, max_value=50, value=23)
    annual_return_rate = st.number_input("연평균 수익률 (%)", min_value=0.0, value=20.0, step=1.0)

# 계산 로직 (매월 말 적립 기준)
months = years * 12
monthly_rate = annual_return_rate / 100 / 12

principals = []
totals = []
current_total = 0

for i in range(1, months + 1):
    current_total = (current_total + monthly_investment) * (1 + monthly_rate)
    
    # 1년 단위로 차트용 데이터 저장
    if i % 12 == 0:
        principals.append(monthly_investment * i)
        totals.append(current_total)

total_principal = monthly_investment * months
final_amount = totals[-1] if totals else 0
total_interest = final_amount - total_principal

# 결과 요약 표시
st.subheader("계산 결과 요약")
col1, col2, col3 = st.columns(3)
col1.metric("총 투자 원금", f"{total_principal:,.0f} 원")
col2.metric("누적 이자", f"{total_interest:,.0f} 원")
col3.metric("최종 예상 금액", f"{final_amount:,.0f} 원")

st.divider()

# 연도별 자산 성장 추이 차트
st.subheader("📈 연도별 자산 성장 추이")
chart_data = pd.DataFrame({
    "년도": range(1, years + 1),
    "총 투자 원금": principals,
    "최종 예상 금액": totals
}).set_index("년도")

st.line_chart(chart_data)
