"""
Merging id bps dan 82 kota kabupaten, serta merapikan data simreg bappenas
@author: Fawdy
"""

import pandas as pd

id_bps = pd.read_excel('Data/Kode dan Nama Wilayah BPS.xlsx')
kota_82 = pd.read_excel('Data/Nama 82 Kabupaten Kota dan ID BPS Terpilih untuk Paper.xlsx')

kota_82['kota_low'] = kota_82['kab_kota'].str.lower()
id_bps['kota_low'] = id_bps['wilayah'].str.lower()
id_bps_merge = id_bps.drop('wilayah', axis=1)

merge_df = pd.merge(id_bps_merge, kota_82,
                    on='kota_low',
                    how='right')

merge_df.to_excel('Data/82 Kota dan ID BPS.xlsx', index=False)


# Collecting Data From Simreg Bappenas
id_bps_82 = pd.read_excel('Data/82 Kota dan ID BPS.xlsx')['kode_bps']
id_bps_82_list = list(id_bps_82)
id_bps_82_str = [str(i) for i in id_bps_82_list]

def cleaning_data(tahun, kode_kk, tipe_pdrb):
    # tahun: str, contoh 2016
    # kode_kk: list berisi str, contoh kode_kepri
    
    # tahun = '2016'
    # kode_kk = kode_analisis_prov
    # tipe_pdrb = 'ADHK' atau 'ADHB'
    
    pdrb = pd.read_excel(f'Data/PDRB/PDRB Lapangan Usaha Kab Kota Dalam Milyar Seluruh Indonesia {tipe_pdrb} tahun {tahun}.xlsx')

    lapangan_usaha = list(pdrb.iloc[0,6:])
    index_kk = list(pdrb[pdrb['Unnamed: 4'].isin(kode_kk)].index)
    
    if '9999' in kode_kk:
        index_kk.sort(reverse=True)
    
    nama_kk = list(pdrb['Unnamed: 5'].iloc[index_kk])
    pdrb_kk = pdrb.iloc[index_kk, 6:]
    
    # pdrb_kk = pdrb.iloc[index_kk[0]:(index_kk[-1]+1), 6:]
    
    pdrb_kk.columns = lapangan_usaha
    pdrb_kk['Nama Kab/Kota'] = nama_kk
    pdrb_kk_melt = pd.melt(pdrb_kk, id_vars=['Nama Kab/Kota'], value_vars=lapangan_usaha)
    
    pdrb_kk_melt.columns = ['Nama Kab/Kota', 'Lapangan Usaha', f'Nilai PDRB {tahun}']
    pdrb_kk_melt[f'Nilai PDRB {tahun}'] = pdrb_kk_melt[f'Nilai PDRB {tahun}'].astype(float)
    
    dict_result_cleaning = {
        'PDRB DF':pdrb_kk_melt,
        'Lapangan Usaha': lapangan_usaha
        }
    return dict_result_cleaning


def creating_wide_df(list_tahun, kode_kk_cd, tipe_pdrb_cd):
    # list_tahun: list, berisi list tahun dari tahun awal sampai tahun akhir
    # kode_kk: list berisi str, contoh kode_kepri
    
    # list_tahun = ['2016', '2019', '2020']
    # kode_kk_cd = kode_sulsel
    # tipe_pdrb = 'ADHK' atau 'ADHB'
    
    for t in list_tahun:
        pdrb_t = cleaning_data(t, kode_kk_cd, tipe_pdrb_cd)['PDRB DF']
        
        if t==list_tahun[0]:
            pdrb_merge = cleaning_data(list_tahun[0], kode_kk_cd, tipe_pdrb_cd)['PDRB DF']
        else:
            pdrb_merge = pd.merge(pdrb_merge, pdrb_t,
                                  on=['Nama Kab/Kota', 'Lapangan Usaha'],
                                  how='inner')
    return pdrb_merge

tahun_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
pdrb_wide = creating_wide_df(tahun_list, id_bps_82_str, 'ADHB')
lapangan_usaha = list(pdrb_wide['Lapangan Usaha'].unique())
indeks_terpilih = [0, 2, 11, 12, 14]
lu_selected = [lapangan_usaha[i] for i in indeks_terpilih]

filtered_pdrb = pdrb_wide[pdrb_wide['Lapangan Usaha'].isin(lu_selected)]
new_columns = [filtered_pdrb.columns[0]] + [filtered_pdrb.columns[1]] + tahun_list
filtered_pdrb.columns = new_columns

# Converting from wide to long

for l in lu_selected:
    test_pdrb = filtered_pdrb[filtered_pdrb['Lapangan Usaha']==l]
    
    for t in tahun_list:
        t_int = int(t)
        
        pdrb_slice = test_pdrb[['Nama Kab/Kota', t]]
        pdrb_slice['Tahun'] = t_int
        pdrb_slice.rename(columns = {t:l}, inplace = True) 
        
        if t_int==2010:
            pdrb_long = pdrb_slice
        else:
            pdrb_long = pd.concat([pdrb_long, pdrb_slice])
    
    if l==lu_selected[0]:
        pdrb_merge = pdrb_long
    else:
        pdrb_merge = pd.merge(pdrb_merge, pdrb_long,
                              on=('Nama Kab/Kota', 'Tahun'),
                              how='inner')

pdrb_merge.columns = ['kab_kota', 'pdrb_total', 'tahun',
                      'industri', 'pariwisata', 'perdagangan', 'pertanian']
pdrb_merge = pdrb_merge[['kab_kota', 'tahun', 'pdrb_total',
                         'industri', 'pariwisata', 'perdagangan', 'pertanian']]

pdrb_merge.to_excel('Data/PDRB/PDRB Lapangan Usaha ADHB 2010 2019 82 Kab Kota.xlsx', index=False)


