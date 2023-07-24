###################################################################
#Comparison of AB Test and Conversion of Bidding Methods
###################################################################

#Preparing and Analyzing Data
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
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.expand_frame_repr', False)

dfc = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/Measurement_Problems/ABTesti/ab_testing.xlsx", sheet_name="Control Group")
dft = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/Measurement_Problems/ABTesti/ab_testing.xlsx", sheet_name="Test Group")

dfc.head()
dft.head()

dfc.describe().T
dft.describe().T


#Combining the control and test group using the concat method after analysis
dfc.columns = ["Impression_c", "Click_c", "Purchase_c", "Earning_c"]
df = pd.concat([dfc, dft], axis=1)
df.head()

#Defining the A/B Test Hypothesis
#H0 : M1 = M2 (There is no difference in the mean purchases of the control and test groups.)
#H1 : M1!= M2 (There is difference in the mean purchases of the control and test groups.)

#Analyze purchase (gain) averages for the control and test group
df["Purchase_c"].mean() #550.8940587702316
df["Purchase"].mean() #582.1060966484677

#It seems that there is a difference according to the averages, but we can test whether this difference is by chance or not with A / B tests.

#Performing Hypothesis Testing
#Normality Assumption and Variance Homogeneity

# H0: The assumption of normal distribution is provided.
# H1: The assumption of normal distribution is not provided.

#shapiro: used to test the assumption of normality.
test_stat, pvalue = shapiro(df["Purchase_c"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9773, p-value = 0.5891 -> p > 0.05, normal distribution

test_stat, pvalue = shapiro(df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541 -> p > 0.05, normal distribution

############################
# Variance Homogeneity Assumption
############################

# H0: Variances are Homogeneous
# H1: Variances are not Homogeneous

#levene: tests the assumption of homogeneity of variance.
test_stat, pvalue = levene(df["Purchase_c"],
                           df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 2.6393, p-value = 0.1083 -> p > 0.05, bu nedenle H0 kabul edilir. yani varyanslar homojendir


#Independent two-sample t-test (parametric test) if assumptions are met

test_stat, pvalue = ttest_ind(df["Purchase_c"],
                              df["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = -0.9416, p-value = 0.3493 -> p > 0.05,  H0 accepted. (There is no difference in the mean purchases of the control and test groups.)

#according to test result
#p value is greater than 0.05. In this case, H0 is accepted and we have to say that there is no statistically significant
#difference between the purchasing averages. The means in the data were randomly high in the test data.