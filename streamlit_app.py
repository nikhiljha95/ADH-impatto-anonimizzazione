import streamlit as st

def reset_session_state():
    """Reset all session state variables to their initial state."""
    for key in st.session_state.keys():
        del st.session_state[key]

def main():
    # Set page title
    st.title("Linee guida per anonimizzazione dei dati")
    
    # Initialize session state for tracking questions and answers
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 'q1'
        st.session_state.answers = {}
    
    # Question flow dictionary
    questions = {
        'q1': {
            'text': 'Che *adversary model* prevedi?',
            'opts': ['Malicious', 'Honest-but-curious'],
            'opts_next': ['malicious', 'todo']
        },

        'malicious': {
            'text': 'Quante dimensioni ha il tuo dataset?',
            'opts': ['Tante (10+)', 'Poche (10-)'],
            'opts_next': ['curse-of-dimensionality', 'quanti-tipi-dato']
        },

        'quanti-tipi-dato': {
            'text': 'Ci sono tipi diversi di dato?',
            'opts': ['Sì', 'No'],
            'opts_next': ['todo', 'todo']
        },
        
    }
    
    if len(st.session_state.answers) > 0:
        for q, answer in st.session_state.answers.items():
            st.write(f"{questions[q]['text']} - {answer}")

    # Display current question
    if st.session_state.current_question in questions:
        current_q = questions[st.session_state.current_question]
        st.write(current_q['text'])
        
        # Yes/No buttons
        #col1, col2 = st.columns(2)
        #with col1:
        #    if st.button(questions[st.session_state.current_question]['opt1']):
        #        # Store the answer
        #        st.session_state.answers[st.session_state.current_question] = questions[st.session_state.current_question]['opt1']
        #        # Move to next question based on 'yes' path
        #        st.session_state.current_question = current_q['opt1_next']
        #        st.rerun()
        #
        #with col2:
        #    if st.button(questions[st.session_state.current_question]['opt2']):
        #        # Store the answer
        #        st.session_state.answers[st.session_state.current_question] = questions[st.session_state.current_question]['opt2']
        #        # Move to next question based on 'no' path
        #        st.session_state.current_question = current_q['opt2_next']
        #        st.rerun()

        cols = st.columns(len(current_q['opts']))
        for i, option in enumerate(current_q['opts']):
            with cols[i]:
                if st.button(current_q['opts'][i]):
                    st.session_state.answers[st.session_state.current_question] = current_q['opts'][i]
                    st.session_state.current_question = current_q['opts_next'][i]
                    print(current_q)
                    st.rerun()
    
    # End of questionnaire
    if st.session_state.current_question == 'end':
        st.success("Questionario completato!")

    # Messagges
    if st.session_state.current_question == 'curse-of-dimensionality':
        st.warning("Se hai tante colonne (es. più di 10), il tuo dataset è soggetto alla ***curse of dimensionality***. È praticamente impossibile proteggere le righe. Suggeriamo di ridurre i requisiti di privacy.")
    if st.session_state.current_question == 'todo':
        st.warning("Ramo ancora non implementato.")
    
    # Reset button
    st.markdown("---")
    if st.button('Ricomincia'):
        reset_session_state()
        st.rerun()

if __name__ == "__main__":
    main()