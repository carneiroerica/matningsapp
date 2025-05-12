import streamlit as st
import pandas as pd

# Läs in CSV-filen med semikolon som separator
df = pd.read_csv("koordinater.csv", sep=';')  # Assuming CSV uses semicolon

# Ladda Excel-filen
@st.cache_data
def load_data():
    return pd.read_excel("Matningsdata.xlsx")

excel_df = load_data()  # Excel file loaded separately, not overwriting df

# Debug: Skriv ut hela DataFrame innan borttagning
st.write("Data före borttagning:", excel_df)

# Ta bort sista raden baserat på radindex (om den är sista raden)
excel_df = excel_df[:-1]

# Ta bort den sista raden om den innehåller "Fakturtotal (kr)"
# Säkerställ att inga mellanslag är kvar genom att använda strip()
excel_df = excel_df[excel_df["DP (TPAB)"].str.strip() != "Fakturtotal (kr)"]

# Debug: Skriv ut DataFrame efter borttagning
st.write("Data efter borttagning:", excel_df)

st.title("Kostnadsfördelning för mätning per DP")

# Input för totalkostnaden
total_kostnad = st.number_input("Ange totalkostnad (kr):", min_value=0.0, step=1000.0)

if total_kostnad > 0:
    # Kontrollera att 'Andel' kolumn finns
    if "Andel" in excel_df.columns:
        # Räkna om kostnadsandel
        excel_df["Beräknad kostnad"] = excel_df["Andel"] * total_kostnad

        # Visa tabellen
        st.subheader("Fördelning per DP")
        st.dataframe(excel_df[["DP (TPAB)", "Månadsvisa rör", "Kvartalsvisa rör", "Årsmätningar", "Andel", "Beräknad kostnad"]].rename(columns={
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

        excel_data = to_excel(excel_df[["DP (TPAB)", "Andel", "Beräknad kostnad"]])
        st.download_button(label="Ladda ner resultat som Excel",
                           data=excel_data,
                           file_name="kostnadsfordelning.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("Kolumnen 'Andel' finns inte i Excel-filen.")
else:
    st.info("Ange totalbeloppet från fakturan för att beräkna fördelningen.")
