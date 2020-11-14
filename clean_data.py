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
    # replace all non alphanumeric character to nan:
    CTG_clean_features = CTG_features.replace(regex=r'\D', value=np.nan)

    # create a dictionary without nan values:
    c_ctg = rm_ext_and_nan(CTG_features, extra_feature)
    for key in c_ctg.keys():
        # # calculate the probability of each element
        # p = []
        # p += [(c_ctg[key].count(val) / len(c_ctg[key])) for val in c_ctg[key]]
        p_dict = {val: (c_ctg[key].count(val) / len(c_ctg[key])) for val in c_ctg[key]}

        # find all nan values and replace then randomly:
        val = CTG_clean_features[key].to_list()
        idx_na = []
        idx_na += [i for i in range(len(val)) if pd.isna(val[i])]
        for i in idx_na:
            val[i] = np.random.choice(np.fromiter(p_dict.keys(), dtype=float),
                                      p=np.fromiter(p_dict.values(), dtype=float))
        c_cdf[key] = val

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    d_summary = {}
    for key in c_feat.keys():
        dict_temp = {}
        values_arr = c_feat[key].to_numpy()
        dict_temp["min"] = np.min(values_arr)
        dict_temp["Q1"] = np.quantile(values_arr, 0.25)
        dict_temp["median"] = np.median(values_arr)
        dict_temp["Q3"] = np.quantile(values_arr, 0.75)
        dict_temp["max"] = np.max(values_arr)

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

    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)


######## Debug
import os
directory = r'C:\Users\hadas\Documents\OneDrive - Technion\semester_7\Machine learning in healthcare\Hw\HW1'
CTG_dataset_filname = os.path.join(directory, 'messed_CTG.xls')
CTG_dataset = pd.read_excel(CTG_dataset_filname, sheet_name='Raw Data').iloc[1:,:]
CTG_features = CTG_dataset[['LB', 'AC', 'FM', 'UC', 'DL', 'DS', 'DR', 'DP', 'ASTV', 'MSTV', 'ALTV', 'MLTV',
                            'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode', 'Mean', 'Median', 'Variance', 'Tendency']]
extra_feature = 'DR'
CTG_morph = CTG_dataset[['CLASS']]
fetal_state = CTG_dataset[['NSP']]
