import os
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen
from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic(
        col_year: str,
        user_id: str,
        generate_list: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告個人概要生成を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # 周回報告個人概要データフレームの初期化
        farm_report_ind_sum_df: pd.DataFrame = pd.DataFrame(
                index=range(const_util.NUM_OF_MONTHS),
                columns=const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER
            )
        farm_report_ind_sum_df.fillna(0, inplace=True)
        
        # 指定したユーザの周回数の集計
        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f'{col_year:02}-{(index+1):02}'
            
            # 周回報告一覧ファイルパスの生成
            farm_report_list_file_path: str = \
                const_util.FARM_REPORT_LIST_FILE_PATH.format(col_year_month)
            
            # 周回報告個人概要更新の判定
            update_ind_sum: bool = True
            if generate_list == True:
                # 周回報告一覧生成ロジックの実行
                pyl.measure_proc_time(
                    farm_report_list_gen.do_logic_by_col_year_month)(col_year_month)
                
                # 周回報告一覧ファイルの存在有無チェック
                if os.path.isfile(farm_report_list_file_path) == False:
                    update_ind_sum = False
            else:
                update_ind_sum = False
            
            # 周回報告個人概要データフレームの更新
            farm_report_ind_sum_df.at[
                index, const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[0]] = col_year_month
            if update_ind_sum == True:
                __update_farm_report_ind_sum_df(
                        farm_report_list_file_path,
                        user_id,
                        farm_report_ind_sum_df,
                        index
                    )
        
        # 周回報告個人概要ファイルパスの生成
        farm_report_ind_sum_file_path: str = \
            const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH.format(col_year, user_id)
        
        # 周回報告個人概要データフレームの保存
        pyl.log_inf(lg, f'周回報告個人概要：\n{farm_report_ind_sum_df}')
        pandas_util.save_farm_report_ind_sum_df(
            farm_report_ind_sum_df, farm_report_ind_sum_file_path)
        
        pyl.log_inf(lg, f'周回報告個人概要生成を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __update_farm_report_ind_sum_df(
        farm_report_list_file_path: str,
        user_id: str,
        farm_report_ind_sum_df: pd.DataFrame,
        index: int
    ) -> None:
    
    '''周回報告個人概要データフレーム更新'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        
        # 周回報告一覧データフレームの取得(周回報告一覧ファイルの読み込み)
        farm_report_list_df: pd.DataFrame = \
                pandas_util.read_farm_report_list_file(farm_report_list_file_path)
        
        # ユーザID、クエスト種別による抽出
        df_by_user_id: pd.DataFrame = \
            farm_report_list_df.query(
                f'{const_util.FARM_REPORT_LIST_HEADER[2]}.str.match("^{user_id}$")')
        df_by_user_id_and_normal_quest: pd.DataFrame = \
            df_by_user_id.query(
                f'{const_util.FARM_REPORT_LIST_HEADER[0]}.str.match("{const_util.QUEST_KINDS[1]}")')
        df_by_user_id_and_event_quest: pd.DataFrame = \
            df_by_user_id.query(
                f'{const_util.FARM_REPORT_LIST_HEADER[0]}.str.match("{const_util.QUEST_KINDS[2]}")')
        
        # 周回数の更新
        farm_report_ind_sum_df.at[index, const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[1]] = \
            df_by_user_id_and_normal_quest[const_util.FARM_REPORT_LIST_HEADER[4]].sum()
        farm_report_ind_sum_df.at[index, const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[2]] = \
            df_by_user_id_and_event_quest[const_util.FARM_REPORT_LIST_HEADER[4]].sum()
        farm_report_ind_sum_df.at[index, const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[3]] = \
            df_by_user_id[const_util.FARM_REPORT_LIST_HEADER[4]].sum()
    except Exception as e:
        raise(e)
    
    return None
