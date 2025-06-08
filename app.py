import streamlit as st

home = st.Page(
    page='home.py',
    title='Company to User',
    icon='📦',
    default=True
)

home2 = st.Page(
    page='home2.py',
    title='User to Company',
    icon='📦',
)



pg = st.navigation({
    "Menu": [home,home2]
})


pg.run()