import pandas as pd

from fgo_farm_report_collection.util import const_util


def read_farm_report_list_file(
        farm_report_list_file_path: str
    ) -> pd.DataFrame:
    
    '''周回報告一覧ファイル読み込み'''
    
    farm_report_list_df: pd.DataFrame = pd.read_csv(
            farm_report_list_file_path,
            header=None,
            names=const_util.FARM_REPORT_LIST_HEADER,
            index_col=None,
            skiprows=1,
            parse_dates=[const_util.FARM_REPORT_LIST_HEADER[0]],
            encoding=const_util.ENCODING
        )
    
    return farm_report_list_df


def save_farm_report_list_df(
        farm_report_list_df: pd.DataFrame,
        farm_report_list_file_path: str,
        has_farm_report_list: bool
    ) -> None:
    
    '''周回報告一覧データフレーム保存'''
    
    farm_report_list_df.to_csv(
            farm_report_list_file_path,
            header=(has_farm_report_list == False),
            index=False,
            mode='a',
            encoding=const_util.ENCODING
        )
    
    return None


def save_farm_report_ind_sum_df(
        farm_report_ind_sum_df: pd.DataFrame,
        farm_report_ind_sum_file_path: str
    ) -> None:
    
    '''周回報告個人概要データフレーム保存'''
    
    farm_report_ind_sum_df.to_csv(
            farm_report_ind_sum_file_path,
            header=True,
            index=False,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None


def save_farm_report_tot_sum_df(
        farm_report_tot_sum_df: pd.DataFrame,
        farm_report_tot_sum_file_path: str
    ) -> None:
    
    '''周回報告全体概要データフレーム保存'''
    
    farm_report_tot_sum_df.to_csv(
            farm_report_tot_sum_file_path,
            header=True,
            index=True,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None
