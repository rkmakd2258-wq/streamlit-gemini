import streamlit as st
from google import genai

def main():
    st.title('노인 복지 채팅')

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 채팅 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("질문을 입력하세요"):
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.write(prompt)
        # 사용자 메시지 저장
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gemini AI 응답 생성
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        with st.chat_message("assistant"):
            # 로딩 스피너 표시
            with st.spinner('AI가 응답을 생성하고 있습니다...'):
                # AI 설정과 함께 컨텍스트 생성
                system_prompt = "어르신들 대상의 서비스니까 친절하고 살갑게 대답해줘. 그리고 대답은 알기 쉬운 용어를 써서 말해줘. 유저 질문이 노인 복지 관련 내용이 아니면, 노인 복지 내용만 질문하도록 해줘."
                full_prompt = f"{system_prompt}\n\n사용자: {prompt}"
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                st.write(response.text)
                # AI 응답 저장
                st.session_state.messages.append({"role": "assistant", "content": response.text})

if __name__ == "__main__":
    main()




