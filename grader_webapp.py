import streamlit as st
import re

NUM_QUESTIONS = 45

# 공통 정답 (1~34번)
shared_answers = [
    1, 3, 2, 4, 2, 1, 2, 4, 1, 2,
    3, 4, 1, 2, 3, 4, 1, 2, 3, 4,
    1, 2, 3, 4, 1, 2, 3, 4, 1, 2,
    3, 4, 1, 2
]
# 화작/언매 Tail
hwajak_tail = [3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1]
eonmae_tail = [4, 3, 2, 1, 4, 3, 2, 1, 4, 3, 2]

# 문항별 오답 개수 계산
def get_wrong_count(user_part, correct_part):
    return sum(1 for u, c in zip(user_part, correct_part) if u != c)

# Streamlit UI
st.title("📘 수능 국어 채점기")
version = st.radio("시험 유형을 선택하세요:", options=["화작", "언매"])
user_input = st.text_input("답안을 45개 입력하세요. /n숫자 45자리만 인식하므로, 공백, 쉼표, 슬래시 등을 입력하셔도 됩니다.")

# 버전에 따른 전체 정답 구성
if version == '화작':
    correct_answers = shared_answers + hwajak_tail
else:
    correct_answers = shared_answers + eonmae_tail  # 언매 꼬리 연결

if user_input:
    digits = re.findall(r'[1-5]', user_input)
    if len(digits) != NUM_QUESTIONS:
        st.error(f"⚠️ 입력된 숫자 개수는 {len(digits)}개입니다. 정확히 {NUM_QUESTIONS}개를 입력해주세요.")
    else:
        user_answers = [int(d) for d in digits]
        mode = st.selectbox(
            "채점 방식 선택", [
                "1. 전체 오답 여부만 확인",
                "2. 과목별 오답 여부 확인",
                "3. 지문별 오답 여부 확인",
                "4. 정답 전체 확인"
            ]
        )
        show_wrong_count = st.checkbox("오답 개수 보기", value=False)

        if mode.startswith("1"):
            if user_answers == correct_answers:
                st.success("✅ 모든 문항의 정답이 맞습니다!")
            else:
                if show_wrong_count:
                    wrongs = get_wrong_count(user_answers, correct_answers)
                    st.error(f"❌ 오답이 포함되어 있습니다. ({wrongs}문항 오답)")
                else:
                    st.error("❌ 오답이 포함되어 있습니다.")

        elif mode.startswith("2"):
            st.subheader("📊 과목별 오답 여부")
            sections = {
                "독서": range(0, 17),
                "문학": range(17, 34),
                "화작": range(34, 45),
                "언매": range(34, 45)
            }
            for subject, idx in sections.items():
                if version == '화작' and subject == '언매':
                    continue
                if version == '언매' and subject == '화작':
                    continue
                u = [user_answers[i] for i in idx]
                c = [correct_answers[i] for i in idx]
                if u == c:
                    st.success(f"✅ {subject}: 모든 문항 정답")
                else:
                    if show_wrong_count:
                        st.error(f"❌ {subject}: 오답이 포함되어 있음 ({get_wrong_count(u, c)}문항 오답)")
                    else:
                        st.error(f"❌ {subject}: 오답이 포함되어 있음")

        elif mode.startswith("3"):
            st.subheader("📊 지문별 오답 여부 (예시)")
            reading = {
                "독서 지문 1": range(0, 5),
                "독서 지문 2": range(5, 9),
                "독서 지문 3": range(9, 13),
                "독서 지문 4": range(13, 17)
            }
            literature = {
                "문학 지문 1": range(17, 22),
                "문학 지문 2": range(22, 26),
                "문학 지문 3": range(26, 30),
                "문학 지문 4": range(30, 34)
            }
            for section in [reading, literature]:
                for name, idx in section.items():
                    u = [user_answers[i] for i in idx]
                    c = [correct_answers[i] for i in idx]
                    if u == c:
                        st.success(f"✅ {name}: 모든 문항 정답")
                    else:
                        if show_wrong_count:
                            st.error(f"❌ {name}: 오답이 포함되어 있음 ({get_wrong_count(u, c)}문항 오답)")
                        else:
                            st.error(f"❌ {name}: 오답이 포함되어 있음")

        elif mode.startswith("4"):
            st.subheader("📄 정답 전체 확인표")
            for i in range(NUM_QUESTIONS):
                mark = "✅" if user_answers[i] == correct_answers[i] else "❌"
                st.write(f"{i+1:2}번: 정답={correct_answers[i]}, 내답={user_answers[i]} {mark}")
