ID,Latitud,Longitud
1,18.09267,59.426156
2,18.0927,59.4262
3,18.0926,59.4261
4,18.09265,59.42615
5,18.09268,59.42618
import streamlit as st
import pandas as pd

# Ladda Excel-filen
@st.cache_data
def load_data():
    return pd.read_excel("Matningsdata.xlsx")

df = load_data()

st.title("Kostnadsfördelning för mätning per DP")

# Input för totalkostnaden
total_kostnad = st.number_input("Ange totalkostnad (kr):", min_value=0.0, step=1000.0)

if total_kostnad > 0:
    # Räkna om kostnadsandel
    df["Beräknad kostnad"] = df["Andel"] * total_kostnad

    # Visa tabellen
    st.subheader("Fördelning per DP")
    st.dataframe(df[["DP (TPAB)", "Månadsvisa rör", "Kvartalsvisa rör", "Årsmätningar", "Andel", "Beräknad kostnad"]].rename(columns={
        "DP (TPAB)": "DP",
        "Månadsvisa rör": "Månadsrör",
        "Kvartalsvisa rör": "Kvartalsrör",
        "Årsmätningar": "Årsmätningar",
        "Andel": "Andel",
        "Beräknad kostnad": "Kostnad (kr)"
    }))

    # Ladda ner resultatet som Excel
    @st.cache_data
    def to_excel(dataframe):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Fördelning')
        output.seek(0)
        return output

    excel_data = to_excel(df[["DP (TPAB)", "Andel", "Beräknad kostnad"]])
    st.download_button(label="Ladda ner resultat som Excel",
                       data=excel_data,
                       file_name="kostnadsfordelning.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Ange en totalkostnad för att se fördelningen.")
