import math
import secrets
import string
import streamlit as st

def calculate_security_metrics(password, pool_size):
    length = len(password)
    
    entropy_bits = round(length * math.log2(pool_size)) if length > 0 and pool_size > 0 else 0
    
    human_shortcuts = ["123", "abc", "qwe", "asd", "pass", "admin", "th", "he", "er"]
    risk_matches = sum(1 for pattern in human_shortcuts if pattern in password.lower())
    
    if entropy_bits < 45 or risk_matches > 0:
        status = "🔴 Vulnerable"
        desc = "This password contains predictable human typing patterns or is too short. A basic script could crack it instantly."
    elif entropy_bits < 72:
        status = "🟡 Moderate"
        desc = "Decent baseline strength, but increasing the character length or adding symbols will close the hacking window."
    else:
        status = "🟢 Excellent"
        desc = "This password shows excellent mathematical randomness and is resistant to common pattern-matching attacks."
    
    return {
        "bits": entropy_bits,
        "risks": risk_matches,
        "status": status,
        "desc": desc,
        "length": length
    }

def generate_random_password():
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    password = ''.join(secrets.choice(all_characters) for _ in range(16))
    return password, len(all_characters)

def main():
    st.set_page_config(page_title="PASS_CHECKER", page_icon="🛡️", layout="centered")
    
    st.markdown("""
        <style>
            @import url('https://googleapis.com');

            * {
                font-family: 'Poppins';
            }

            html, body, [data-testid="stAppViewContainer"] {
                color: #ffffff;
                background:##34282C;
            }

            [data-testid="stMetric"] {
                background-color: #282C35; 
                border: 1px solid #1e293b;  
                border-radius: 14px;            
                padding: 16px;                           
                box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.4); 
            }

            [data-testid="stMetricLabel"] {
                font-size: 18px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #FFD700;
            }

            [data-testid="stMetricValue"] {
                font-size: 19px;
                font-weight: 700;
                color: #ffffff;
            }
            
            div.stButton > button {
                background-color: #B8860B; 
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                font-size: 18px;
                font-weight: 600;
                padding: 10px 0px;
                text-transform: uppercase;
                letter-spacing: 0.025em;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
                transition: background-color 0.15s, transform 0.1s;
            }
                
            [data-testid="stAlert"], 
            [data-testid="stAlert"] > div, 
            div[role="alert"] {
                background-color:#282C35; 
                color: #ffffff;             
                border: 1px solid #1e293b;  
                border-radius: 14px;        
                box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.4);
                font-size: 18px;
            }
            
            [data-testid="stAlert"] p, 
            [data-testid="stAlert"] span, 
            [data-testid="stAlert"] strong {
                color: #ffffff;             
                font-family: 'Poppins';
                font-size: 18px;
            }
            
            [data-testid="stAlert"] svg {
                color: #6366f1;
            }

            [data-testid="stColumn"] p strong {
                color: #ffffff;
                font-weight: 600;
                font-size: 20px;
            }

            div[data-testid="stCaptionContainer"] p,
            div[data-testid="stCaptionContainer"] span,
            div[data-testid="stCaptionContainer"] {
                color: #ffffff;
                font-weight: 500; 
                opacity: 0.95;  
                font-family: poppins;  
                font-size: 18px;
                line-height: 1.45;
            }

            [data-testid="stTextInput"] div[data-baseweb="input"] {
                background-color: transparent;
                border: 2px solid #ffffff;
                border-radius: 8px;
            }
            [data-testid="stTextInput"] input {
                color: #ffffff;
                caret-color: #ffffff;
            }
            [data-testid="stTextInput"] input::placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
            }
            [data-testid="InputInstructions"] {
                display: none !important;
            }
          
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color:#FFffff; font-size: 30px; font-family: Poppins;'>Password Analyzer and Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #ffffff, font-family: Poppins;'>Testing machine randomness vs. predictable human typing habits.</p>", unsafe_allow_html=True)
    st.write("---")

    if "current_password" not in st.session_state:
        st.session_state.current_password = ""
    if "current_pool" not in st.session_state:
        st.session_state.current_pool = 72
    if "source" not in st.session_state:
        st.session_state.source = "Manual Input"

    column_left, column_right = st.columns(2)
    
    with column_left:
        st.markdown("**Live Password Analyzer**")
        st.caption("Type a password profile manually below to test keyboard shortcuts.")
        user_input = st.text_input(
            "Input Field Box", 
            label_visibility="collapsed", 
            placeholder="Type custom string and press 'Enter'...", 
            type="password",
            key="manual_password_input" 
        )        
        if user_input:
            st.session_state.current_password = user_input
            st.session_state.source = "Manual Input"
            
            estimated_pool = 26
            if any(c.isupper() for c in user_input): estimated_pool += 26
            if any(c.isdigit() for c in user_input): estimated_pool += 10
            if any(c in string.punctuation for c in user_input): estimated_pool += 20
            st.session_state.current_pool = estimated_pool
        elif st.session_state.source == "Manual Input":
            st.session_state.current_password = ""
    
    with column_right:
        st.markdown("**Secure Password Generator**")
        st.caption("Deploy a secure machine-generated string using random code loops.")
        click_generate = st.button("Generate Secure Key +", use_container_width=True)
        
        if click_generate:
            machine_password, machine_pool = generate_random_password()
            st.session_state.current_password = machine_password
            st.session_state.current_pool = machine_pool
            st.session_state.source = "Machine Stream"
    
    if st.session_state.current_password:
        if st.session_state.source == "Machine Stream":
            st.code(st.session_state.current_password, language="text")
            
        report = calculate_security_metrics(st.session_state.current_password, st.session_state.current_pool)
        st.write("---")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(label="Password Length", value=f"{report['length']} chars")
            
        with metric_col2:
            st.metric(label="Entropy Strength", value=f"{report['bits']} Bits")
            
        with metric_col3:
            st.metric(label="Pattern Matches", value=f"{report['risks']} Found")
            
        st.write(" ") 

        st.info(f"**Security Rating:** {report['status']}\n\n{report['desc']}")

if __name__ == "__main__":
    main()
