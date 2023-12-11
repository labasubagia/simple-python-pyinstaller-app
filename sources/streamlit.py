import streamlit as st
from calc import add2

st.title('Add 2 Val app v1.0.5')

n1 = st.number_input('Insert 1st number', step=1)
n2 = st.number_input('Insert 2nd number', step=1)

st.text(f'result {add2(n1, n2)}')