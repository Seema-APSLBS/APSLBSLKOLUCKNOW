iimport streamlit as st

st.title("My new app")
st.write("Hello! We are creating a web app")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)

if st.button("Submit"):
    if name.strip():
        st.write(f"Hello, {name}! Welcome to Streamlit.")
        st.write(f"Your age is {int(age)}")
    else:
        st.warning("Please enter your name before submitting.")

