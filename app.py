import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_excel("datasets.xlsx", sheet_name="Worksheet")

with st.sidebar:
    st.title('Tugas Sesi 10')
    st.write('1. 240434006 - Fahri Prawirakusuma')
    st.write('2. 240434001 - Fauzan Naufal Nur Ramadhani')


with st.container():
    st.subheader("Perbandingan Jumlah Diperiksa dan Melanggar")
    filter, noFilter = st.tabs(["Filter", "Tanpa Filter"])

    with filter:
        # Perbandingan per wilayah dengan filter slider
        filtered_data = data[data['status_pemeriksaan'].isin(['Diperiksa', 'Melanggar'])]

        selected_year = st.selectbox(
            "Pilih Tahun",
            options=filtered_data['tahun'].unique(),
            index=0
        )

        threshold_value = st.slider(
            "Filter Jumlah Kendaraan (≥)",
            min_value=int(filtered_data['jumlah'].min()),
            max_value=int(filtered_data['jumlah'].max()),
            value=int(filtered_data['jumlah'].min()),
            step=100
        )

        filtered = filtered_data[
            (filtered_data['tahun'] == selected_year) & 
            (filtered_data['jumlah'] >= threshold_value)
        ]

        fig2 = px.bar(
            filtered,
            x='wilayah_bptd',
            y='jumlah',
            color='status_pemeriksaan',
            barmode='group',
            labels={'jumlah': 'Jumlah Kendaraan', 'wilayah_bptd': 'Wilayah BPTD'},
            title=f"Data Pemeriksaan Tahun {selected_year} (Jumlah ≥ {threshold_value})"
        )

        st.plotly_chart(fig2)
        # end perbandingan per wilayah filter


    with noFilter:
        # Perbandingan per wilayah
        diperiksa = data[data['status_pemeriksaan'] == 'Diperiksa']
        melanggar = data[data['status_pemeriksaan'] == 'Melanggar']

        comparison = pd.merge(
            diperiksa[['wilayah_bptd', 'jumlah']], 
            melanggar[['wilayah_bptd', 'jumlah']], 
            on='wilayah_bptd', 
            how='inner', 
            suffixes=('_diperiksa', '_melanggar')
        )

        comparison_melt = comparison.melt(
            id_vars="wilayah_bptd", 
            value_vars=["jumlah_diperiksa", "jumlah_melanggar"], 
            var_name="Status", 
            value_name="Jumlah"
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=comparison_melt, x="wilayah_bptd", y="Jumlah", hue="Status", ax=ax)
        ax.set_title('Perbandingan Jumlah Diperiksa dan Melanggar per Wilayah')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.tight_layout()
        st.pyplot(fig)
        # end per wilayah

    # Perbandingan Persen
    st.subheader("Perbandingan Dalam Persen")

    sns.set_theme(style="whitegrid")

    persen = data[data['satuan'] == 'Persen']

    g = sns.catplot(
        data=persen, kind="bar",
        x=persen['wilayah_bptd'], y=persen['jumlah'], hue=persen['tahun'],
        errorbar="sd", palette="dark", alpha=.6, height=6, aspect=2
    )
    g.despine(left=True)
    g.set_xticklabels(rotation=90)
    g.set_axis_labels("", "Persen")
    g.legend.set_title("")

    st.pyplot(g.fig)
    # end persen
    
    # Pesan
    with st.expander("Buat Pesan"):
        pesan = st.text_area('Pesan')
        if st.button('Simpan'):
            st.write('Pesan: ', pesan)
    # end pesan