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
    # for feat, val in enumerate(CTG_features):
    #     if not CTG_features[feat][val].isdigit():
    #         CTG_features.replace(val, np.nan)


    # cc_ctg = {}
    # for key in CTG_features.keys():
    #     if not key == extra_feature:
    #         cc_ctg[key] = [val for val in CTG_features[key] if not pd.isnull(val)]

    c_ctg = {key: [val for val in CTG_features[key] if not pd.isna(val)] for key in CTG_features.keys() if
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
    CTG_features = CTG_features.replace('--', np.nan)

    c_ctg = rm_ext_and_nan(CTG_features, extra_feature)
    for key in c_ctg.keys():
        p_hist = np.histogram(c_ctg[key], 100, density=True)
        val = pd.DataFrame(CTG_features[key])
        idx_na = val.index[val[key].isna()].tolist()
        for i in idx_na:
            val.loc[i] = np.random.choice(c_ctg[key], p = p_hist)
        c_cdf[key] = val

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------

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
