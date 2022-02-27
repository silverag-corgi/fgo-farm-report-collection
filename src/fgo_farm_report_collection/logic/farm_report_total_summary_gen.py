import os
from datetime import date, datetime
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic(
        col_year_month: str,
        min_num_of_farms: int,
        quest_kind: str,
        should_output_user_name: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告全体概要生成を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # 収集年月が未来の場合
        today: date = datetime.today().date()
        col_first_date: date = datetime.strptime(col_year_month + '-01', '%Y-%m-%d').date()
        first_date_of_this_month: date = pyl.get_first_date_of_this_month(today)
        if col_first_date > first_date_of_this_month:
            pyl.log_inf(lg, f'収集年月が未来です。(col_year_month:{col_year_month})')
        else:
            # 周回報告一覧ファイルパス、周回報告全体概要ファイルパスの生成
            farm_report_list_file_path: str = \
                const_util.FARM_REPORT_LIST_FILE_PATH.format(col_year_month)
            farm_report_tot_sum_file_path: str = \
                const_util.FARM_REPORT_TOTAL_SUMMARY_FILE_PATH.format(
                    col_year_month, quest_kind, f'{min_num_of_farms}周以上')
            
            # 周回報告一覧ファイルが存在しない場合
            if os.path.isfile(farm_report_list_file_path) == False:
                pyl.log_inf(lg, f'周回報告一覧ファイルが存在しません。' +
                                f'(farm_report_list_file_path:{farm_report_list_file_path})')
            else:
                # 周回報告全体概要ファイルの生成
                pyl.log_inf(lg, f'周回報告全体概要ファイル：{farm_report_tot_sum_file_path}')
                __generate_farm_report_tot_sum_file(
                        farm_report_list_file_path,
                        quest_kind,
                        min_num_of_farms,
                        farm_report_tot_sum_file_path,
                        should_output_user_name
                    )
        
        pyl.log_inf(lg, f'周回報告全体概要生成を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __generate_farm_report_tot_sum_file(
        farm_report_list_file_path: str,
        quest_kind: str,
        min_num_of_farms: int,
        farm_report_tot_sum_file_path: str,
        should_output_user_name: bool
    ) -> None:
    
    '''周回報告全体概要ファイル生成'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        
        # 周回報告一覧データフレームの取得(周回報告一覧ファイルの読み込み)
        farm_report_list_df: pd.DataFrame = \
            pandas_util.read_farm_report_list_file(farm_report_list_file_path)
        
        if quest_kind in const_util.QUEST_KINDS:
            # クエスト種別による抽出
            farm_report_tot_sum_df: pd.DataFrame
            if quest_kind in const_util.QUEST_KINDS[1:3]:
                farm_report_tot_sum_df = farm_report_list_df.query(
                    f'{const_util.FARM_REPORT_LIST_HEADER[0]}.str.match("{quest_kind}")')
            else:
                farm_report_tot_sum_df = farm_report_list_df
        
            # 投稿者による集計
            farm_report_tot_sum_df = farm_report_tot_sum_df.groupby(
                const_util.FARM_REPORT_LIST_HEADER[2]).sum()
            
            # 周回数による降順ソート
            farm_report_tot_sum_df.sort_values(
                const_util.FARM_REPORT_LIST_HEADER[4], ascending=False, inplace=True)
            
            # 周回数による抽出
            farm_report_tot_sum_df.query(
                f'{const_util.FARM_REPORT_LIST_HEADER[4]} >= {min_num_of_farms}', inplace=True)
            
            # 列(ユーザ名)の追加
            farm_report_tot_sum_df.insert(
                0, const_util.FARM_REPORT_TOTAL_SUMMARY_HEADER[1], '-')
            
            # ユーザ名の設定
            if should_output_user_name == True:
                pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
                for index, _ in farm_report_tot_sum_df.iterrows():
                    try:
                        user_site_info_url: str = const_util.USER_INFO_SITE_URL.format(index)
                        response_for_bs: Response = requests.get(user_site_info_url)
                        bs: BeautifulSoup = BeautifulSoup(response_for_bs.content, 'html.parser')
                        user_name_list: ResultSet = bs.find_all(class_='name')
                        farm_report_tot_sum_df.at[
                            index, const_util.FARM_REPORT_TOTAL_SUMMARY_HEADER[1]] = \
                                user_name_list[0].get_text()
                        pyl.log_deb(lg, f'ユーザ名の設定に成功しました。(user_id:{index})')
                    except Exception as e:
                        pyl.log_war(lg, f'ユーザ名の設定に失敗しました。' +
                                        f'アカウントが削除されている可能性があります。(user_id:{index})')
            
            # 周回報告全体概要データフレームの保存
            pyl.log_inf(lg, f'周回報告全体概要(先頭n行)：\n{farm_report_tot_sum_df.head(5)}')
            pyl.log_inf(lg, f'周回報告全体概要(末尾n行)：\n{farm_report_tot_sum_df.tail(5)}')
            pandas_util.save_farm_report_tot_sum_df(
                farm_report_tot_sum_df, farm_report_tot_sum_file_path)
    except Exception as e:
        raise(e)
    
    return None
