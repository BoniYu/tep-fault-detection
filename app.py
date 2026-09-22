import streamlit as st

st.title("TEP Fault Detection")
st.write("Hello! If you can see this, Streamlit is working.")

reactor_temp = st.number_input("Reactor temperature", value=120.4)

st.write(f"You entered: {reactor_temp}")