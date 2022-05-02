#Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.

# Görev 1: Veriyi Hazırlama ve Analiz Etme
#  Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


df_control = pd.read_excel("/Users/eminebozkurt/Desktop/vbo/Week4/hw1/ab_testing.xlsx", sheet_name="Control Group")
df_control.head()
df_control.shape
df_control.info()


df_test = pd.read_excel("/Users/eminebozkurt/Desktop/vbo/Week4/hw1/ab_testing.xlsx", sheet_name="Test Group")
df_test.head()
df_test.shape
df_test.info()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
df_control.head()
df_control["Purchase"].value_counts().sum()
df_control.describe().T

df_test.head()
df_test["Purchase"].value_counts().sum()
df_test.describe().T

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
df_control["Group"] = "Control_Group"
df_test["Group"] = "Test_Group"
pd.concat([df_control, df_test], axis=0, ignore_index=True)

# Görev 2: A/B Testinin Hipotezinin Tanımlanması
# Adım 1: Hipotezi tanımlayınız.
# H0 : M1 = M2() (Average bidding'in maximum bidding'ten tıklanma anlamında, istatiksel olarak birbirlerinden anlamlı farkları yoktur.)
# H1 : M1!= M2() (... vardır.)


# Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.
df_control.head()
df_control["Purchase"].mean() # 550.8940587702316
df_test["Purchase"].mean() # 582.1060966484675
df_control["Purchase"].describe().T


# Görev 3: Hipotez Testinin Gerçekleştirilmesi

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.

# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? Elde edilen p-value değerlerini yorumlayınız.
df_control.head()

test_stat, pvalue = shapiro(df_control[(df_control["Group"] == "Control_Group")]["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891 > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = shapiro(df_test[(df_test["Group"] == "Test_Group")]["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541 > 0.05 H0 REDDEDİLEMEZ
# ikisi için de normallik varsayımı sağlanır.


# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını
# Purchase değişkeni üzerinden test ediniz. Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.


test_stat, pvalue = levene(df_control.loc[df_control["Group"] == "Control_Group", "Purchase"],
                           df_test.loc[df_test["Group"] == "Test_Group", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083 > 0.05 H0 REDDEDİLEMEZ
# Varyanslar homojendir.


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Bizimkinde varsayımlar sağlanıyor. Bağımsız iki örneklem t testini seçeceğiz.


test_stat, pvalue = ttest_ind(df_control.loc[df_control["Group"] == "Control_Group", "Purchase"],
                              df_test.loc[df_test["Group"] == "Test_Group", "Purchase"],
                              equal_var=True)


print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493 > 0.05 H0 REDDEDILEMEZ.


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları
# arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# p-value = 0.3493 > 0.05 H0 REDDEDILEMEZ satın alma sayılarında istatiski olarak anlamlı bir farklılık yoktur.

# Görev 4: Sonuçların Analizi
# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
# Bağımsız iki örneklem t testini kullandım çünkü normallik varsayımı sağlanıyordu ve varyanslar homojendir.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
# Average bidding maximum bidding'le benzer olduğu için average bidding başarısızdır.
