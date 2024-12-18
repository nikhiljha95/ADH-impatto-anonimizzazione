import streamlit as st
import json

def reset_session_state():
    """Reset all session state variables to their initial state."""
    for key in st.session_state.keys():
        del st.session_state[key]

def main():
    # Set page title
    st.title("Linee guida per anonimizzazione dei dati")

    warnings = json.loads(open('messages.json').read())
    
    # Initialize session state for tracking questions and answers
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 'q1'
        st.session_state.answers = {}
        st.session_state.warnings = {}
    
    # Question flow dictionary
    questions = json.loads(open('./logic-tree.json').read())
    
    if len(st.session_state.answers) > 0:
        for q, answer in st.session_state.answers.items():
            
            st.write(f"{questions[q]['text']} - {answer}")

            # Messagges in any
            if st.session_state.warnings[q] in warnings:
                st.warning(warnings[st.session_state.warnings[q]])

    # Display current question
    if st.session_state.current_question in questions:
        current_q = questions[st.session_state.current_question]
        st.write(current_q['text'])

        cols = st.columns(len(current_q['opts']))
        for i, option in enumerate(current_q['opts']):
            with cols[i]:
                if st.button(current_q['opts'][i]):
                    st.session_state.answers[st.session_state.current_question] = current_q['opts'][i]
                    st.session_state.warnings[st.session_state.current_question] = current_q['opts_warnings'][i]
                    st.session_state.current_question = current_q['opts_next'][i]
                    st.rerun()
    
    # End of questionnaire
    if st.session_state.current_question == 'end':
        st.success("Questionario completato!")   
    
    if st.session_state.current_question == 'todo':
        st.warning("Ramo ancora non implementato.")
    
    # Reset button
    st.markdown("---")
    if st.button('Ricomincia'):
        reset_session_state()
        st.rerun()

if __name__ == "__main__":
    main()