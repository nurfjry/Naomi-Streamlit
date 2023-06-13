import streamlit as st
import numpy as np
import scipy.stats as stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.title('✨ Selamat Datang ✨')
analysis_type = st.sidebar.selectbox('Pilih Analisis 🌞', ('Uji Varians Dua Populasi', 'Uji Bartlett', 'Uji Satu Arah ANOVA', 'Uji LSD', 'Korelasi', 'Regresi'))

if analysis_type == 'Uji Varians Dua Populasi':
    st.sidebar.subheader('Uji Varians Dua Populasi')
    sample1 = st.sidebar.text_input('Sampel A (pakai koma untuk spasi)', '1, 2, 3, 4, 5')
    sample2 = st.sidebar.text_input('Sampel B (pakai koma untuk spasi)', '2, 4, 6, 8, 10')
    alpha_var = st.sidebar.slider('Taraf Signifikansi', 0.01, 0.10, 0.05, 0.01)

    sample1_array = np.array(list(map(float, sample1.split(','))))
    sample2_array = np.array(list(map(float, sample2.split(','))))

    _, p_value_var = stats.bartlett(sample1_array, sample2_array)

    st.header('Uji Varians Dua Populasi')
    st.write('**H0**: Varians A  sama dengan Varians B')
    st.write('**H1**: Varians A tidak sama dengan Varians B')
    st.write('---')
    st.write('**Keputusan**: ', 'Tolak H0' if p_value_var < alpha_var else 'Gagal tolak H0')
    st.write('**P-value**: ', p_value_var)

#Uji Bartlett
elif analysis_type == 'Uji Bartlett':
    st.sidebar.subheader('Uji Bartlett')
    sample1_bartlett = st.sidebar.text_input('Sampel A (pakai koma untuk spasi)', '1, 2, 3, 4, 5', key='bartlett_sample1')
    sample2_bartlett = st.sidebar.text_input('Sampel B (pakai koma untuk spasi)', '2, 4, 6, 8, 10', key='bartlett_sample2')
    alpha_bartlett = st.sidebar.slider('Taraf Signifikansi', 0.01, 0.10, 0.05, 0.01, key='bartlett_alpha')

    sample1_bartlett_array = np.array(list(map(float, sample1_bartlett.split(','))))
    sample2_bartlett_array = np.array(list(map(float, sample2_bartlett.split(','))))
    
    _, p_value_bartlett = stats.bartlett(sample1_bartlett_array, sample2_bartlett_array)

    st.header('Uji Bartlett')
    st.write('**H0**: Varians dari semua sampel sama')
    st.write('**H1**: Setidaknya ada salah satu varians sampel yang berbeda')
    st.write('---')
    st.write('**Keputusan**: ', 'Tolak H0' if p_value_bartlett < alpha_bartlett else 'Gagal tolak H0')
    st.write('**P-value**: ', p_value_bartlett)

#One Way ANOVA
elif analysis_type == 'Uji Satu Arah ANOVA':
    st.sidebar.subheader('Uji Satu Arah ANOVA')
    groups = st.sidebar.text_input('Kelompok (pakai koma untuk spasi)', 'Kelompok A, Kelompok B, Kelompok C')
    sample1_anova = st.sidebar.text_input('Sampel A (pakai koma untuk spasi)', '1, 2, 3, 4, 5', key='anova_sample1')
    sample2_anova = st.sidebar.text_input('Sampel B (pakai koma untuk spasi)', '2, 4, 6, 8, 10', key='anova_sample2')
    sample3_anova = st.sidebar.text_input('Sampel C (pakai koma untuk spasi)', '3, 6, 9, 12, 15', key='anova_sample3')
    alpha_anova = st.sidebar.slider('Taraf Signifikansi', 0.01, 0.10, 0.05, 0.01, key='anova_alpha')

    groups_list = groups.split(',')
    samples_anova = [np.array(list(map(float, sample.split(',')))) for sample in [sample1_anova, sample2_anova, sample3_anova]]

    _, p_value_anova = stats.f_oneway(*samples_anova)

    st.header('Uji Satu Arah ANOVA')
    st.write('**H0**: Rata-rata semua kelompok sama')
    st.write('**H1**: Setidaknya ada satu rata-rata kelompok yang berbeda')
    st.write('---')
    st.write('**Keputusan**: ', 'Tolak H0' if p_value_anova < alpha_anova else 'Gagal tolak H0')
    st.write('**P-value**: ', p_value_anova)

#LSD
elif analysis_type == 'Uji LSD':
    st.sidebar.subheader('Uji LSD (Post ANOVA)')
    df_data = {
        'Group': ['Kelompok A'] * 5 + ['Kelompok B'] * 5 + ['Kelompok C'] * 5,
        'Values': [1, 2, 3, 4, 5, 2, 4, 6, 8, 10, 3, 6, 9, 12, 15]
    }
    df = pd.DataFrame(df_data)
    selected_group = st.sidebar.selectbox('Pilih satu kelompok untuk dianalisis', df['Group'].unique())

    group_selected = df[df['Group'] == selected_group]
    group_selected_values = group_selected['Values'].values
    mean_selected_group = group_selected_values.mean()
    n_selected_group = len(group_selected_values)
    std_error_selected_group = group_selected_values.std() / np.sqrt(n_selected_group)
    alpha_anova = st.sidebar.slider('Taraf Signifikansi', 0.01, 0.10, 0.05, 0.01, key='anova_alpha')
    lsd = stats.t.ppf(1 - alpha_anova / 2, len(df['Group'].unique()) * (n_selected_group - 1))
    lsd_value = lsd * std_error_selected_group

    st.header('Uji LSD (Post ANOVA)')
    st.write(f'**Kelompok**: {selected_group}')
    st.write(f'**Rata-rata**: {mean_selected_group}')
    st.write(f'**Jumlah pengamatan**: {n_selected_group}')
    st.write(f'**Standar error**: {std_error_selected_group}')
    st.write(f'**Nilai LSD**: {lsd_value}')

#Korelasi
elif analysis_type == 'Korelasi':
    st.sidebar.subheader('Korelasi')
    correlation_data = st.sidebar.text_input('Korelasi Data (pakai koma untuk spasi)', '1, 2, 3, 4, 5, 2, 4, 6, 8, 10', key='correlation_data')
    alpha_corr = st.sidebar.slider('Taraf Signifikansi', 0.01, 0.10, 0.05, 0.01, key='corr_alpha')

    correlation_data_array = np.array(list(map(float, correlation_data.split(','))))

    corr_coef, p_value_corr = stats.pearsonr(correlation_data_array[::2], correlation_data_array[1::2])

    st.header('Korelasi')
    st.write('**H0**: Tidak ada korelasi antara kedua variabel')
    st.write('**H1**: Ada korelasi antara kedua variabel')
    st.write('---')
    st.write('**Koefisien Korelasi**: ', corr_coef)
    st.write('**P-value**: ', p_value_corr)

#Regresi
elif analysis_type == 'Regresi':
    st.sidebar.subheader('Regresi')
    regression_x = st.sidebar.text_input('X (pakai koma untuk spasi)', '1, 2, 3, 4, 5', key='regression_x')
    regression_y = st.sidebar.text_input('Y (pakai koma untuk spasi)', '2, 4, 6, 8, 10', key='regression_y')

    regression_x_array = np.array(list(map(float, regression_x.split(','))))
    regression_y_array = np.array(list(map(float, regression_y.split(','))))

    slope, intercept, r_value, p_value, std_err = stats.linregress(regression_x_array, regression_y_array)

    st.header('Regresi')
    st.write('**Model Regresi**: Y = {}X + {}'.format(slope, intercept))
    st.write('**R-squared**: ', r_value ** 2)
    st.write('**P-value**: ', p_value)
    st.write('**Standar Error**: ', std_err)

    #scatterplot
    fig, ax = plt.subplots()
    sns.scatterplot(x=regression_x_array, y=regression_y_array, ax=ax)
    ax.plot(regression_x_array, intercept + slope * regression_x_array, color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Regression')
    st.pyplot(fig)

# Varians Dua Pop
if analysis_type == 'Uji Varians Dua Populasi':
    st.sidebar.subheader('Uji Varians Dua Populasi')
    # ... Rest of the code ...

# Uji Bartlett
elif analysis_type == 'Uji Bartlett':
    st.sidebar.subheader('Uji Bartlett')
    # ... Rest of the code ...

# One Way ANOVA
elif analysis_type == 'Uji Satu Arah ANOVA':
    st.sidebar.subheader('Uji Satu Arah ANOVA')
    # ... Rest of the code ...

# LSD
elif analysis_type == 'Uji LSD':
    st.sidebar.subheader('Uji LSD (Post ANOVA)')
    # ... Rest of the code ...

# Korelasi
elif analysis_type == 'Korelasi':
    st.sidebar.subheader('Korelasi')
    # ... Rest of the code ...

# Regresi
elif analysis_type == 'Regresi':
    st.sidebar.subheader('Regresi')
    # ... Rest of the code ...

# Function to execute analysis and display results
def run_analysis():
    if analysis_type == 'Uji Varians Dua Populasi':
        # ... Code for Uji Varians Dua Populasi ...
        pass

    elif analysis_type == 'Uji Bartlett':
        # ... Code for Uji Bartlett ...
        pass

    elif analysis_type == 'Uji Satu Arah ANOVA':
        # ... Code for Uji Satu Arah ANOVA ...
        pass

    elif analysis_type == 'Uji LSD':
        # ... Code for Uji LSD ...
        pass

    elif analysis_type == 'Korelasi':
        # ... Code for Korelasi ...
        pass

    elif analysis_type == 'Regresi':
        # ... Code for Regresi ...
        pass

# Run analysis on button click in sidebar
if st.sidebar.button('Lihat Hasil'):
    run_analysis()