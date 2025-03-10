import streamlit as st

# Sidrubrik
st.title("Faktureringsberäknare")

# Användaren matar in ett fakturabelopp
belopp = st.number_input("Ange totalt fakturabelopp:", min_value=0.0, step=100.0)

# Beräkning och visning av resultat
if belopp > 0:
    tpab = belopp * 0.82
    täby_kommun = belopp * 0.09
    riksbyggen = belopp * 0.06
    wallenstam = belopp * 0.03

    st.write(f"### Uppdelning av fakturabeloppet:")
    st.write(f"**TPAB:** {tpab:.2f} kr")
    st.write(f"**Täby Kommun:** {täby_kommun:.2f} kr")
    st.write(f"**Riksbyggen:** {riksbyggen:.2f} kr")
    st.write(f"**Wallenstam:** {wallenstam:.2f} kr")
