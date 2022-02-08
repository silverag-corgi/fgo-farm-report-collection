from datetime import date, datetime, timedelta
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as mylib
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response
from src.util import *


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
        lg = mylib.get_logger(__name__)
        lg.info(f'周回報告概要生成を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # 実行要否の判定
        today: date = datetime.today().date()
        col_first_date: date = datetime.strptime(col_year_month + '-01', '%Y-%m-%d').date()
        first_date_of_this_month: date = mylib.get_first_date_of_this_month(today)
        if col_first_date <= first_date_of_this_month:
            should_execute = True
        else:
            should_execute = False
            lg.info(f'収集年月が未来です。(col_year_month:{col_year_month})')
        
        if should_execute == True:
            # 周回報告一覧ファイルパス、周回報告概要ファイルパスの生成
            farm_report_list_file_path: str = \
                const_util.FARM_REPORT_LIST_FILE_PATH.format(col_year_month)
            farm_report_summary_file_path: str = \
                const_util.FARM_REPORT_SUMMARY_FILE_PATH.format(col_year_month, quest_kind, f'{min_num_of_farms}周以上')
            
            # 周回報告概要ファイルの生成
            lg.info(f'周回報告概要ファイル：{farm_report_summary_file_path}')
            __generate_farm_report_summary(
                    farm_report_list_file_path,
                    quest_kind,
                    min_num_of_farms,
                    farm_report_summary_file_path,
                    should_output_user_name
                )
        
        lg.info(f'周回報告概要生成を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __generate_farm_report_summary(
        farm_report_list_file_path: str,
        quest_kind: str,
        min_num_of_farms: int,
        farm_report_summary_file_path: str,
        should_output_user_name: bool
    ) -> None:
    
    '''周回報告概要ファイル生成'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 周回報告一覧ファイルの読み込み
        farm_report_list_data_frame: pd.DataFrame = pd.read_csv(
                farm_report_list_file_path,
                header=None,
                names=const_util.FARM_REPORT_LIST_HEADER,
                index_col=None,
                parse_dates=[const_util.FARM_REPORT_LIST_HEADER[1]],
                encoding=const_util.ENCODING
            )
        
        if quest_kind in const_util.QUEST_KINDS:
            # クエスト種別による抽出
            if quest_kind in const_util.QUEST_KINDS[1:3]:
                farm_report_summary_data_frame: pd.DataFrame = farm_report_list_data_frame.query(
                    f'{const_util.FARM_REPORT_LIST_HEADER[0]}.str.match("{quest_kind}")')
            else:
                farm_report_summary_data_frame: pd.DataFrame = farm_report_list_data_frame
        
            # 投稿者による集計
            farm_report_summary_data_frame = farm_report_summary_data_frame.groupby(
                const_util.FARM_REPORT_LIST_HEADER[2]).sum()
            
            # 周回数による降順ソート
            farm_report_summary_data_frame.sort_values(
                const_util.FARM_REPORT_LIST_HEADER[4], ascending=False, inplace=True)
            
            # 周回数による抽出
            farm_report_summary_data_frame.query(
                f'{const_util.FARM_REPORT_LIST_HEADER[4]} >= {min_num_of_farms}', inplace=True)
            
            # 列(ユーザ名)の追加
            farm_report_summary_data_frame.insert(
                0, const_util.FARM_REPORT_SUMMARY_HEADER[1], '-')
            
            # ユーザ名の設定
            if should_output_user_name == True:
                for index, row in farm_report_summary_data_frame.iterrows():
                    try:
                        user_site_info_url: str = USER_INFO_SITE_URL.format(index)
                        response_for_bs: Response = requests.get(user_site_info_url)
                        bs: BeautifulSoup = BeautifulSoup(response_for_bs.content, 'html.parser')
                        user_name_list: ResultSet = bs.find_all(class_='name')
                        farm_report_summary_data_frame.at[
                            index, const_util.FARM_REPORT_SUMMARY_HEADER[1]] = \
                                user_name_list[0].get_text()
                        lg.debug(f'ユーザ名の設定に成功しました。(user_id:{index})')
                    except Exception as e:
                        lg.warning(f'ユーザ名の設定に失敗しました。アカウントが削除されている可能性があります。(user_id:{index})')
            
            # 周回報告概要ファイルの保存
            lg.info(f'\n{farm_report_summary_data_frame}')
            farm_report_summary_data_frame.to_csv(
                    farm_report_summary_file_path,
                    header=False,
                    index=True,
                    mode='w',
                    encoding=const_util.ENCODING
                )
    except Exception as e:
        raise(e)
    
    return None
