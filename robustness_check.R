library(readxl)
library(dplyr)
library(plm)
library(lmtest)
library(sandwich)
library(clubSandwich)
library(imputeTS)
library(fdrtool)

wd = ""
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

# Robustness Check apa saja yang bisa dilakukan
# 1. Pakai TWFE bobot.
# 2. Pakai Heterogenous Effect berdasarkan grup persentil pertanian.
# 3. Pakai Placebo Test. Perform the placebo test multiple times (e.g., 100 or 1,000 iterations) by reshuffling the rainfall data and re-estimating the model.
# Interpretasi Hasil Placebo Test:
# a. If the placebo test consistently shows no significant relationship between the randomized rainfall and inflation, 
# a. this suggests that your initial finding (no significant relationship between actual rainfall and inflation) is likely to be robust.
# b. If, however, the placebo test shows significant relationships in some cases, it would imply that the null result in your main analysis could be 
# b. due to specific data characteristics or model issues, and you may need to re-examine the model's assumptions.

#================================================================TWFE BOBOT==========================================================================#
composite_tw = plm(composite_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                   data=data_panel_trend,
                   index=c('kode_bps', 'tahun'),
                   model='within',
                   effect = 'twoway',
                   weights = bobot)

composite_tw_se = coef_test(composite_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

food_tw = plm(food_diff ~ curah_hujan_diff + temperature_diff + log_pdrb + share_pertanian + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
              data=data_panel_trend,
              index=c('kode_bps', 'tahun'),
              model='within',
              effect = 'twoway',
              weights = bobot)

food_tw_se = coef_test(food_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

processed_food_tw = plm(processed_food_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                        data=data_panel_trend,
                        index=c('kode_bps', 'tahun'),
                        model='within',
                        effect = 'twoway',
                        weights = bobot)

processed_food_tw_se = coef_test(processed_food_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

housing_tw = plm(housing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                 data=data_panel_trend,
                 index=c('kode_bps', 'tahun'),
                 model='within',
                 effect = 'twoway',
                 weights = bobot)

housing_tw_se = coef_test(housing_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

clothing_tw = plm(clothing_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                  data=data_panel_trend,
                  index=c('kode_bps', 'tahun'),
                  model='within',
                  effect = 'twoway',
                  weights = bobot)
clothing_tw_se = coef_test(clothing_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

health_tw = plm(health_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                data=data_panel_trend,
                index=c('kode_bps', 'tahun'),
                model='within',
                effect = 'twoway',
                weights = bobot)
health_tw_se = coef_test(health_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

education_recreation_sport_tw = plm(education_recreation_sport_diff ~ curah_hujan_diff + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                                    data=data_panel_trend,
                                    index=c('kode_bps', 'tahun'),
                                    model='within',
                                    effect = 'twoway',
                                    weights = bobot)
education_recreation_sport_tw_se = coef_test(education_recreation_sport_tw, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")$SE

library(stargazer)
stargazer(composite_tw, food_tw, processed_food_tw, housing_tw,
          se=list(composite_tw_se, food_tw_se, processed_food_tw_se, housing_tw_se), 
          type = 'html',
          out = 'Laporan/Robustness Check/TWFE Bobot/Tabel Robustness Check Regresi Fixed Effect Part 1 tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))

stargazer(clothing_tw, health_tw, education_recreation_sport_tw,
          se=list(clothing_tw_se, health_tw_se, education_recreation_sport_tw_se), 
          type = 'html',
          out = 'Laporan/Robustness Check/TWFE Bobot/Tabel Robustness Check Regresi Fixed Effect Part 2 tex.html', no.space = TRUE, align = TRUE,
          omit.stat=c("LL","ser","f"))


#================================================================TWFE PLACEBO==========================================================================#

# Set up the placebo test with multiple iterations
set.seed(123)  # For reproducibility

# Define number of iterations
num_iterations = 100

# Create a vector to store the p-values for the placebo rainfall variable
p_values = numeric(num_iterations)

# Perform the placebo test 1,000 times
for (i in 1:num_iterations) {
  
  # Shuffle the rainfall data to create a placebo rainfall variable
  data_panel_trend$curah_hujan_diff_placebo = sample(data_panel_trend$curah_hujan_diff)
  
  # Fit the placebo regression model
  model_placebo <- plm(education_recreation_sport_diff ~ curah_hujan_diff_placebo + temperature_diff + share_pertanian + log_pdrb + share_industri + deflator_pertanian_growth + deflator_industri_growth + inflasi_lag1,
                       data=data_panel_trend,
                       index=c('kode_bps', 'tahun'),
                       model='within',
                       effect = 'twoway')
  coef_test_placebo = coef_test(model_placebo, vcov = "CR1", cluster = data_panel_trend$kode_bps, test = "naive-t")
  
  # Extract the p-value for the placebo rainfall variable and store it
  p_values[i] <- coef_test_placebo["curah_hujan_diff_placebo", "p_t"]
}

# Analyze the distribution of p-values
# Check how many times the placebo rainfall was found significant (e.g., p < 0.05)
significant_count <- sum(p_values < 0.05)

# Print the number of significant placebo tests
cat("Number of significant placebo tests (p < 0.05) after 100 iterations:", significant_count, "\n")

# Plot the distribution of p-values
hist(p_values, main = "p-values from Placebo Tests Education, Recreation & Sport", xlab = "p-value", breaks = 20)



