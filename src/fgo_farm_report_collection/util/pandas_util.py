import os
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
from styleframe import StyleFrame

from fgo_farm_report_collection.util import const_util


def save_farm_report_list_df(
        farm_report_list_df: pd.DataFrame,
        farm_report_list_file_path: str,
        has_farm_report_list: bool
    ) -> None:
    
    '''周回報告一覧データフレーム保存'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # インデックスのリセット
        farm_report_list_df.reset_index(drop=True)
        
        # 周回報告全体概要データフレームのログ出力
        pyl.log_inf(lg, f'周回報告一覧(追加分先頭n行)：\n{farm_report_list_df.head(5)}')
        pyl.log_inf(lg, f'周回報告一覧(追加分末尾n行)：\n{farm_report_list_df.tail(5)}')
        pyl.log_inf(lg, f'周回報告一覧ファイルパス：\n{farm_report_list_file_path}')
        
        # 周回報告全体概要データフレームの保存
        farm_report_list_df.to_csv(
                farm_report_list_file_path,
                header=(has_farm_report_list == False),
                index=False,
                mode='a',
                encoding=const_util.ENCODING
            )
    except Exception as e:
        raise(e)
    
    return None


def read_farm_report_list_file(
        farm_report_list_file_path: str,
        reset_index_from_one: bool = False,
        move_index_to_column: bool = False
    ) -> pd.DataFrame:
    
    '''周回報告一覧ファイル読み込み'''
    
    farm_report_list_df: pd.DataFrame = pd.read_csv(
            farm_report_list_file_path,
            header=None,
            names=const_util.FARM_REPORT_LIST_HEADER,
            index_col=None,
            skiprows=1,
            parse_dates=[const_util.FARM_REPORT_LIST_HEADER[0]],
            thousands=',',
            encoding=const_util.ENCODING
        )
    
    if reset_index_from_one == True:
        farm_report_list_df.index = farm_report_list_df.index + 1
    
    if move_index_to_column == True:
        farm_report_list_df.reset_index(inplace=True)
        farm_report_list_df.rename(columns={'index': 'No'}, inplace=True)
    
    return farm_report_list_df


def save_farm_report_usr_tot_sum_df(
        farm_report_usr_tot_sum_df: pd.DataFrame,
        farm_report_usr_tot_sum_file_path: str
    ) -> None:
    
    '''周回報告ユーザ全体概要データフレーム保存'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # インデックスのリセット
        farm_report_usr_tot_sum_df.reset_index(inplace=True)
        
        # 周回報告ユーザ全体概要データフレームのログ出力
        pyl.log_inf(lg, f'周回報告ユーザ全体概要(先頭n行)：\n{farm_report_usr_tot_sum_df.head(5)}')
        pyl.log_inf(lg, f'周回報告ユーザ全体概要(末尾n行)：\n{farm_report_usr_tot_sum_df.tail(5)}')
        pyl.log_inf(lg, f'周回報告ユーザ全体概要ファイルパス：\n{farm_report_usr_tot_sum_file_path}')
        
        # 周回報告ユーザ全体概要データフレームの保存
        farm_report_usr_tot_sum_df.to_csv(
                farm_report_usr_tot_sum_file_path,
                header=True,
                index=False,
                mode='w',
                encoding=const_util.ENCODING
            )
    except Exception as e:
        raise(e)
    
    return None


def read_farm_report_usr_tot_sum_file(
        farm_report_usr_tot_sum_file_path: str,
        reset_index_from_one: bool = False,
        move_index_to_column: bool = False
    ) -> pd.DataFrame:
    
    '''周回報告ユーザ全体概要ファイル読み込み'''
    
    farm_report_usr_tot_sum_df: pd.DataFrame = pd.read_csv(
            farm_report_usr_tot_sum_file_path,
            header=None,
            names=const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER,
            index_col=None,
            skiprows=1,
            thousands=',',
            encoding=const_util.ENCODING
        )
    
    if reset_index_from_one == True:
        farm_report_usr_tot_sum_df.index = farm_report_usr_tot_sum_df.index + 1
    
    if move_index_to_column == True:
        farm_report_usr_tot_sum_df.reset_index(inplace=True)
        farm_report_usr_tot_sum_df.rename(columns={'index': 'No'}, inplace=True)
    
    return farm_report_usr_tot_sum_df


def save_farm_report_qst_tot_sum_df(
        farm_report_qst_tot_sum_df: pd.DataFrame,
        farm_report_qst_tot_sum_file_path: str
    ) -> None:
    
    '''周回報告クエスト全体概要データフレーム保存'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # インデックスのリセット
        farm_report_qst_tot_sum_df.reset_index(inplace=True)
        
        # 周回報告クエスト全体概要データフレームのログ出力
        pyl.log_inf(lg, f'周回報告クエスト全体概要(先頭n行)：\n{farm_report_qst_tot_sum_df.head(5)}')
        pyl.log_inf(lg, f'周回報告クエスト全体概要(末尾n行)：\n{farm_report_qst_tot_sum_df.tail(5)}')
        pyl.log_inf(lg, f'周回報告クエスト全体概要ファイルパス：\n{farm_report_qst_tot_sum_file_path}')
        
        # 周回報告クエスト全体概要データフレームの保存
        farm_report_qst_tot_sum_df.to_csv(
                farm_report_qst_tot_sum_file_path,
                header=True,
                index=False,
                mode='w',
                encoding=const_util.ENCODING
            )
    except Exception as e:
        raise(e)
    
    return None


def read_farm_report_qst_tot_sum_file(
        farm_report_qst_tot_sum_file_path: str,
        reset_index_from_one: bool = False,
        move_index_to_column: bool = False
    ) -> pd.DataFrame:
    
    '''周回報告クエスト全体概要ファイル読み込み'''
    
    farm_report_qst_tot_sum_df: pd.DataFrame = pd.read_csv(
            farm_report_qst_tot_sum_file_path,
            header=None,
            names=const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER,
            index_col=None,
            skiprows=1,
            thousands=',',
            encoding=const_util.ENCODING
        )
    
    if reset_index_from_one == True:
        farm_report_qst_tot_sum_df.index = farm_report_qst_tot_sum_df.index + 1
    
    if move_index_to_column == True:
        farm_report_qst_tot_sum_df.reset_index(inplace=True)
        farm_report_qst_tot_sum_df.rename(columns={'index': 'No'}, inplace=True)
    
    return farm_report_qst_tot_sum_df


def save_farm_report_ind_sum_df(
        farm_report_ind_sum_df: pd.DataFrame,
        farm_report_ind_sum_file_path: str
    ) -> None:
    
    '''周回報告個人概要データフレーム保存'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 周回報告全体概要データフレームのログ出力
        pyl.log_inf(lg, f'周回報告個人概要：\n{farm_report_ind_sum_df}')
        pyl.log_inf(lg, f'周回報告個人概要ファイルパス：\n{farm_report_ind_sum_file_path}')
        
        # 周回報告全体概要データフレームの保存
        farm_report_ind_sum_df.to_csv(
                farm_report_ind_sum_file_path,
                header=True,
                index=False,
                mode='w',
                encoding=const_util.ENCODING
            )
    except Exception as e:
        raise(e)
    
    return None


def read_farm_report_ind_sum_file(
        farm_report_ind_sum_file_path: str,
        reset_index_from_one: bool = False,
        move_index_to_column: bool = False
    ) -> pd.DataFrame:
    
    '''周回報告個人概要ファイル読み込み'''
    
    farm_report_ind_sum_df: pd.DataFrame = pd.read_csv(
            farm_report_ind_sum_file_path,
            header=None,
            names=const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER,
            index_col=None,
            skiprows=1,
            thousands=',',
            encoding=const_util.ENCODING
        )
    
    if reset_index_from_one == True:
        farm_report_ind_sum_df.index = farm_report_ind_sum_df.index + 1
    
    if move_index_to_column == True:
        farm_report_ind_sum_df.reset_index(inplace=True)
        farm_report_ind_sum_df.rename(columns={'index': 'No'}, inplace=True)
    
    return farm_report_ind_sum_df


def save_farm_report_sf(
        farm_report_sf: StyleFrame,
        excel_writer: Optional[pd.ExcelWriter],
        farm_report_file_path: str,
        row_to_add_filters: int = 0,
        columns_and_rows_to_freeze: str = 'B2'
    ) -> None:
    
    '''周回報告スタイルフレーム保存'''
    
    farm_report_sf.to_excel(
            excel_writer,  # type: ignore
            sheet_name=os.path.splitext(os.path.basename(farm_report_file_path))[0],
            row_to_add_filters=row_to_add_filters,
            columns_and_rows_to_freeze=columns_and_rows_to_freeze,
            index=False
        )
    
    return None
