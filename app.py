import streamlit as st
import pandas as pd
import os

# Load CSV file
df_coords = pd.read_csv("koordinater.csv")

st.title("Kostnadsfördelning för mätning per DP")

# Load Excel file with caching
file_path = "Matningsdata.xlsx"
last_modified = os.path.getmtime(file_path)

@st.cache_data
def load_data(file_path, last_modified):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df

df = load_data(file_path, last_modified)

# Input for total cost
total_kostnad = st.number_input("Ange totalkostnad (kr):", min_value=0.0, step=1000.0)

if total_kostnad > 0:
    if "Andel" not in df.columns:
        st.error("Kolumnen 'Andel' saknas i Excel-filen!")
    else:
        df["Beräknad kostnad"] = df["Andel"] * total_kostnad

        # Show only the table after cost is entered
        st.subheader("Fördelning per DP")
        st.dataframe(df[[
            "DP (TPAB)", "Månadsvisa rör", "Kvartalsvisa rör", "Årsmätningar", "Andel", "Beräknad kostnad"
        ]].rename(columns={
            "DP (TPAB)": "DP",
            "Månadsvisa rör": "Månadsrör",
            "Kvartalsvisa rör": "Kvartalsrör",
            "Årsmätningar": "Årsmätningar",
            "Andel": "Andel",
            "Beräknad kostnad": "Kostnad (kr)"
        }))

        @st.cache_data
        def to_excel(dataframe):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Fördelning')
            output.seek(0)
            return output

        excel_data = to_excel(df[["DP (TPAB)", "Andel", "Beräknad kostnad"]])
        st.download_button(
            label="Ladda ner resultat som Excel",
            data=excel_data,
            file_name="kostnadsfordelning.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Ange en totalkostnad för att se fördelningen.")
