# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    # regular expressions \D = replace all non 0-9 character; this is equivalent to the class [^0-9]
    # regex = Whether to interpret to_replace and/or value as regular expressions.
    CTG_clean_features = CTG_features.replace(regex=r'\D', value=np.nan)
    c_ctg = {key: [val for val in CTG_clean_features[key] if not pd.isna(val)] for key in CTG_clean_features.keys() if
             not key == extra_feature}

    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    # replace all non-numeric character to nan:
    CTG_clean_features = CTG_features.replace(regex=r'\D', value=np.nan)

    # create a dictionary without nan values:
    c_ctg = rm_ext_and_nan(CTG_features, extra_feature)

    # create a dictionary with random values (from relevant distribution p) instead of NaN
    for key in c_ctg.keys():
        # # calculate the probability of each element
        p_dict = {val: (c_ctg[key].count(val) / len(c_ctg[key])) for val in c_ctg[key]}

        # find all nan values' indexes and replace them randomly:
        val = CTG_clean_features[key].to_list()
        idx_na = []
        idx_na += [i for i in range(len(val)) if pd.isna(val[i])]
        for i in idx_na:
            # np.fromiter converts dict keys/vals into iterable array
            val[i] = np.random.choice(np.fromiter(p_dict.keys(), dtype=float),
                                      p=np.fromiter(p_dict.values(), dtype=float))

        # insert key and vals to dict
        c_cdf[key] = val

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dictionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    d_summary = {}

    # calculating each key description as dict
    for key in c_feat.keys():
        dict_temp = {}
        values_arr = c_feat[key].to_numpy()
        dict_temp["min"] = np.min(values_arr)
        dict_temp["Q1"] = np.quantile(values_arr, 0.25)
        dict_temp["median"] = np.median(values_arr)
        dict_temp["Q3"] = np.quantile(values_arr, 0.75)
        dict_temp["max"] = np.max(values_arr)

        # insert key description (dict) to d_summary (dict)
        d_summary[key] = dict_temp
    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    for key in c_feat.keys():
        # Calculating Upper/Lower Whiskers (UW/LW)
        Q1 = d_summary[key]['Q1']
        Q3 = d_summary[key]['Q3']
        LW = Q1 - 1.5 * (Q3 - Q1)
        UW = Q3 + 1.5 * (Q3 - Q1)

        # insert val if within whiskers, rest are replaced with NaN
        temp_val = [val if LW < val < UW else np.nan for val in c_feat[key]]

        # create dict without outliers
        c_no_outlier[key] = temp_val

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    filt_feature = [val for val in c_cdf[feature] if val < thresh]
    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat

    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    # create function to normalized/standardized according to each mode:
    def StandardizationScaling(value, key, d_statistics):
        standard_val = (value - d_statistics[key]['mean']) / d_statistics[key]["std"]
        return standard_val

    def MinMaxScaling(value, key, d_statistics):
        standard_val = (value - d_statistics[key]['min']) / (d_statistics[key]['max'] - d_statistics[key]['min'])
        return standard_val

    def MeanNormalization(value, key, d_statistics):
        standard_val = (value - d_statistics[key]['mean']) / (d_statistics[key]['max'] - d_statistics[key]['min'])
        return standard_val

    # get statistic:
    d_statistics = CTG_features.describe()

    # create dictionary for the scaling val:
    nsd_res = {}
    if mode == 'none':
        nsd_res = {key: [val for val in CTG_features[key]]
                   for key in CTG_features.keys()}
    if mode == 'mean':
        nsd_res = {key: [MeanNormalization(val, key, d_statistics) for val in CTG_features[key]]
                   for key in CTG_features.keys()}
    if mode == 'standard':
        nsd_res = {key: [StandardizationScaling(val, key, d_statistics) for val in CTG_features[key]]
                   for key in CTG_features.keys()}

    if mode == 'MinMax':
        nsd_res = {key: [MinMaxScaling(val, key, d_statistics) for val in CTG_features[key]]
                   for key in CTG_features.keys()}

    # plot histogram
    if flag:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle(selected_feat[0])

        first_feat = CTG_features[selected_feat[0]]  # Histogram Before scaling for 1st selected feature
        ax1.hist(first_feat, bins=100)
        ax1.set(xlabel='Histogram ' + selected_feat[0], ylabel='Count')
        ax1.set_title('before ' + mode + ' scaling')

        first_feat_new = nsd_res[selected_feat[0]]  # Histogram After scaling for 1st selected feature
        ax2.hist(first_feat_new, bins=100)
        ax2.set(xlabel='Histogram ' + selected_feat[0], ylabel='Count')
        ax2.set_title('after ' + mode + ' scaling')

        fig2, (ax3, ax4) = plt.subplots(1, 2)
        fig2.suptitle(selected_feat[1])

        second_feat = CTG_features[selected_feat[1]]  # Histogram Before scaling for 2nd selected feature
        ax3.hist(second_feat, bins=100)
        ax3.set(xlabel='Histogram ' + selected_feat[1], ylabel='Count')
        ax3.set_title('before ' + mode + ' scaling')

        second_feat_new = nsd_res[selected_feat[1]]   # Histogram After scaling for 2nd selected feature
        ax4.hist(second_feat_new, bins=100)
        ax4.set(xlabel='Histogram ' + selected_feat[1], ylabel='Count')
        ax4.set_title('after ' + mode + ' scaling')

        plt.show()
    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)


######## Debug
import os

# directory = r'C:\Users\hadas\Documents\OneDrive - Technion\semester_7\Machine learning in healthcare\Hw\HW1'
directory = r'C:\Users\Nathan\PycharmProjects\ML_in_Healthcare_Winter2021\HW1'
CTG_dataset_filname = os.path.join(directory, 'messed_CTG.xls')
CTG_dataset = pd.read_excel(CTG_dataset_filname, sheet_name='Raw Data').iloc[1:, :]
CTG_features = CTG_dataset[['LB', 'AC', 'FM', 'UC', 'DL', 'DS', 'DR', 'DP', 'ASTV', 'MSTV', 'ALTV', 'MLTV',
                            'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode', 'Mean', 'Median', 'Variance', 'Tendency']]
extra_feature = 'DR'
CTG_morph = CTG_dataset[['CLASS']]
fetal_state = CTG_dataset[['NSP']]
