import pandas as pd

from src.util import const_util


def read_farm_report_list_file(
        farm_report_list_file_path: str
    ) -> pd.DataFrame:
    
    '''周回報告一覧ファイル読み込み'''
    
    farm_report_list_df: pd.DataFrame = pd.read_csv(
            farm_report_list_file_path,
            header=None,
            names=const_util.FARM_REPORT_LIST_HEADER,
            index_col=None,
            parse_dates=[const_util.FARM_REPORT_LIST_HEADER[1]],
            encoding=const_util.ENCODING
        )
    
    return farm_report_list_df


def save_farm_report_list_data_frame(
        farm_report_list_df: pd.DataFrame,
        farm_report_list_file_path: str
    ) -> None:
    
    '''周回報告一覧データフレーム保存'''
    
    farm_report_list_df.to_csv(
            farm_report_list_file_path,
            header=False,
            index=False,
            mode='a',
            encoding=const_util.ENCODING
        )
    
    return None


def save_farm_report_performance_data_frame(
        farm_report_performance_df: pd.DataFrame,
        farm_report_performance_file_path: str
    ) -> None:
    
    '''周回報告実績データフレーム保存'''
    
    farm_report_performance_df.to_csv(
            farm_report_performance_file_path,
            header=True,
            index=False,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None


def save_farm_report_summary_data_frame(
        farm_report_summary_df: pd.DataFrame,
        farm_report_summary_file_path: str
    ) -> None:
    
    '''周回報告概要データフレーム保存'''
    
    farm_report_summary_df.to_csv(
            farm_report_summary_file_path,
            header=False,
            index=True,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None
