# Panel fixed effect

library(readxl)
library(dplyr)
library(imputeTS)

wd = ''
setwd(wd)

data_panel_median = read_excel('Data/panel data long 2012=100 Dummy median.xlsx')
data_cs_median = read_excel('Data/cross section data 2012=100 Dummy median.xlsx')

data_panel_trend = read_excel('Data/panel data long 2012=100 Dummy trend.xlsx')
data_cs_trend = read_excel('Data/cross section data 2012=100 Dummy trend.xlsx')


# Create new variable of each weight for each sub index
data_panel_trend$food_weight = 0.1885
data_panel_trend$processed_food_weight = 0.1619
data_panel_trend$housing_weight = 0.2537
data_panel_trend$clothing_weight = 0.0725
data_panel_trend$health_weight = 0.0473
data_panel_trend$education_recreation_sport_weight = 0.0846
data_panel_trend$transportation_communication_finance_weight = 0.1915

data_panel_trend$dummy_kota = factor(data_panel_trend$dummy_kota)
data_panel_trend$percentile_group_pertanian = factor(data_panel_trend$percentile_group_pertanian)

data_panel_trend = data_panel_trend %>%
  group_by(kode_bps) %>%
  mutate(inflasi_lag1 = na_interpolation(inflasi_lag1, option = "linear"))

# Fixed Effect
library(plm)
library(lmtest)
library(sandwich)
library(clubSandwich)

composite_ind = plm(composite_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                   data=data_panel_trend,
                   index=c('kode_bps', 'tahun'),
                   model='within',
                   effect = 'individual')
composite_ind_se = coef_test(composite_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

composite_tw = plm(composite_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                   data=data_panel_trend,
                  index=c('kode_bps', 'tahun'),
                  model='within',
                  effect = 'twoway')

composite_tw_se = coef_test(composite_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

food_ind = plm(food_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
              data=data_panel_trend,
              index=c('kode_bps', 'tahun'),
              model='within',
              effect = 'individual')
food_ind_se = coef_test(food_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

food_tw = plm(food_diff ~ curah_hujan_diff + temperature_diff + log_pdrb + share_pertanian + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
              data=data_panel_trend,
              index=c('kode_bps', 'tahun'),
              model='within',
              effect = 'twoway')
food_tw_se = coef_test(food_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

processed_food_ind = plm(processed_food_diff ~ curah_hujan_diff+ temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                        data=data_panel_trend,
                        index=c('kode_bps', 'tahun'),
                        model='within',
                        effect = 'individual')
processed_food_ind_se = coef_test(processed_food_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

processed_food_tw = plm(processed_food_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                       data=data_panel_trend,
                       index=c('kode_bps', 'tahun'),
                       model='within',
                       effect = 'twoway')
processed_food_tw_se = coef_test(processed_food_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

housing_ind = plm(housing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                 data=data_panel_trend,
                 index=c('kode_bps', 'tahun'),
                 model='within',
                 effect = 'individual')
housing_ind_se = coef_test(housing_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

housing_tw = plm(housing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                data=data_panel_trend,
                index=c('kode_bps', 'tahun'),
                model='within',
                effect = 'twoway')
housing_tw_se = coef_test(housing_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

clothing_ind = plm(clothing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                  data=data_panel_trend,
                  index=c('kode_bps', 'tahun'),
                  model='within',
                  effect = 'individual')
clothing_ind_se = coef_test(clothing_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

clothing_tw = plm(clothing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                  data=data_panel_trend,
                  index=c('kode_bps', 'tahun'),
                  model='within',
                  effect = 'twoway')
clothing_tw_se = coef_test(clothing_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

health_ind = plm(health_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                 data=data_panel_trend,
                   index=c('kode_bps', 'tahun'),
                   model='within',
                   effect = 'individual')
health_ind_se = coef_test(health_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

health_tw = plm(health_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                  data=data_panel_trend,
                  index=c('kode_bps', 'tahun'),
                  model='within',
                  effect = 'twoway')
health_tw_se = coef_test(health_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

#Education
education_recreation_sport_ind = plm(education_recreation_sport_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                                          data=data_panel_trend,
                                          index=c('kode_bps', 'tahun'),
                                          model='within',
                                          effect = 'individual')
education_recreation_sport_ind_se = coef_test(education_recreation_sport_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

education_recreation_sport_tw = plm(education_recreation_sport_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                                         data=data_panel_trend,
                                         index=c('kode_bps', 'tahun'),
                                         model='within',
                                         effect = 'twoway')
education_recreation_sport_tw_se = coef_test(education_recreation_sport_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

#Transportation
transportation_communication_finance_ind = plm(transportation_communication_finance_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                                               data=data_panel_trend,
                                               index=c('kode_bps', 'tahun'),
                                               model='within',
                                               effect = 'individual')
transportation_communication_finance_ind_se = coef_test(transportation_communication_finance_ind, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

transportation_communication_finance_tw = plm(transportation_communication_finance_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                                              data=data_panel_trend,
                                              index=c('kode_bps', 'tahun'),
                                              model='within',
                                              effect = 'twoway')
transportation_communication_finance_tw_se = coef_test(transportation_communication_finance_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE



library(stargazer)
stargazer(composite_ind, composite_tw, food_ind, food_tw, 
          se=list(composite_ind_se, composite_tw_se, food_ind_se, food_tw_se), 
          type = 'html',
          out = 'Laporan/Individual and Twoway/Tabel Regresi Fixed Effect Part 1 tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))

stargazer(processed_food_ind, processed_food_tw, housing_ind, housing_tw,
          se=list(processed_food_ind_se, processed_food_tw_se, housing_ind_se, housing_tw_se), 
          type = 'html',
          out = 'Laporan/Individual and Twoway/Tabel Regresi Fixed Effect Part 2 tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))

stargazer(clothing_ind, clothing_tw, health_ind, health_tw,
          se=list(clothing_ind_se, clothing_tw_se, health_ind_se, health_tw_se), 
          type = 'html',
          out = 'Laporan/Individual and Twoway/Tabel Regresi Fixed Effect Part 3 tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))

stargazer(education_recreation_sport_ind, education_recreation_sport_tw,
          se=list(education_recreation_sport_ind_se, education_recreation_sport_tw_se), 
          type = 'html',
          out = 'Laporan/Individual and Twoway/Tabel Regresi Fixed Effect Part 4 education tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))

stargazer(transportation_communication_finance_ind, transportation_communication_finance_tw,
          se=list(transportation_communication_finance_ind_se, transportation_communication_finance_tw_se), 
          type = 'html',
          out = 'Laporan/Individual and Twoway/Tabel Regresi Fixed Effect Part 4 transportation tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))



# Descriptive statistics for panel data
library(xtsum)
pdata_trend = pdata.frame(data_panel_trend, index = c("kab_kota", "tahun"), drop.index = TRUE)

pdata_trend_selected = pdata_trend[, ]

pdata_sum = xtsum(pdata_trend, variables = c('composite_diff', 'food_diff', 'processed_food_diff', 'housing_diff',
                                             'clothing_diff', 'curah_hujan_diff', 
                                             'temperature_diff', 'share_pertanian', 'log_pdrb', 'share_industri', 
                                             'deflator_pertanian_growth', 'deflator_industri_growth', 'inflasi_lag1'),
                  return.data.frame = TRUE)

library(writexl)
write_xlsx(pdata_sum, 'Laporan/Individual and Twoway/Tabel Statistik Deskriptif.xlsx')













