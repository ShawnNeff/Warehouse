import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("./assets/Reliable-Parts_Logo.webp", width=230)
with col2:
    st.title("Shawn Neff", anchor=False)
    st.write(
        "Jr. Data Analyst, assisting enterprises by supporting data-driven decision-making."
    )

    if st.button("✉ Contact Me"):
        show_contact_form()

# --- EXPERIENCE  & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - Bachlor's in computer science
    - Strong hands-on experience and knowledge in python and Excel
    - Excellent team-player and displaying a strong sense of initiative on tasks
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python, Pandas, SQL, VBA, C#, HTML5, CSS, JavaScript
    - Data Visualization: PowerBi, MS Excel, Plotly
    - Databases: Postgres, MongoDB, MySQL
    """
)
