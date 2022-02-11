import os
import re
from datetime import date, datetime, timedelta
from logging import Logger
from typing import Final, Optional

import pandas as pd
import python_lib_for_me as mylib
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response
from src.util import const_util, pandas_util


def do_logic(
        col_year_month: str
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        lg.info(f'周回報告一覧生成を開始します。')
        
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
            # 周回報告一覧ファイルパスの生成
            farm_report_list_file_path: str = \
                const_util.FARM_REPORT_LIST_FILE_PATH.format(col_year_month)
            
            # 周回報告一覧生成開始日付の設定
            list_gen_start_date: Optional[date] = __generate_list_gen_start_date(
                farm_report_list_file_path, col_first_date)
            
            # 周回報告一覧生成終了日付の設定
            list_gen_end_date: Optional[date] = __generate_list_gen_end_date(
                list_gen_start_date, col_first_date, first_date_of_this_month, today)
            
            # 周回報告一覧生成要否の判定
            if list_gen_start_date is None or list_gen_end_date is None:
                should_generate = False
                lg.info(f'周回報告一覧は最新です。({col_year_month})')
            else:
                if list_gen_start_date > list_gen_end_date:
                    should_generate = False
                    lg.info(f'周回報告一覧は最新です。({col_year_month})')
                else:
                    should_generate = True
                    lg.info(f'周回報告一覧を生成します。({list_gen_start_date}～{list_gen_end_date})')
            
            # 周回報告一覧ファイルの生成
            if should_generate == True:
                lg.info(f'周回報告一覧ファイル：{farm_report_list_file_path}')
                __generate_farm_report_list_file(
                        list_gen_start_date,
                        list_gen_end_date,
                        farm_report_list_file_path
                    )
        
        lg.info(f'周回報告一覧生成を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __generate_list_gen_start_date(
        farm_report_list_file_path: str,
        col_first_date: date
    ) -> Optional[date]:
    
    '''周回報告一覧生成開始日付生成'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 収集年月の周回報告一覧ファイルの存在有無チェック
        has_farm_report_list: bool = os.path.isfile(farm_report_list_file_path)
        
        # 周回報告一覧生成開始日付の生成
        list_gen_start_date: Optional[date] = None
        if has_farm_report_list == True:
            farm_report_list_df: pd.DataFrame = \
                pandas_util.read_farm_report_list_file(farm_report_list_file_path)
            
            posting_date_of_last_line_timestamp: pd.Timestamp = pd.Timestamp(
                farm_report_list_df[const_util.FARM_REPORT_LIST_HEADER[1]].tail(1).item())
            posting_date_of_last_line: date = posting_date_of_last_line_timestamp.date()
            
            if posting_date_of_last_line != \
                mylib.get_last_date_of_this_month(posting_date_of_last_line):
                list_gen_start_date = posting_date_of_last_line + timedelta(days=1)
            else:
                list_gen_start_date = None
        else:
            list_gen_start_date = col_first_date
    except Exception as e:
        raise(e)
    
    return list_gen_start_date


def __generate_list_gen_end_date(
        list_gen_start_date: Optional[date],
        col_first_date: date,
        first_date_of_this_month: date,
        today: date
    ) -> Optional[date]:
    
    '''周回報告一覧生成終了日付生成'''
    
    try:
        list_gen_end_date: Optional[date] = None
        if list_gen_start_date != None \
            and col_first_date == first_date_of_this_month:
            list_gen_end_date = today + timedelta(days=-1)
        elif list_gen_start_date != None \
            and col_first_date != first_date_of_this_month:
            list_gen_end_date = mylib.get_last_date_of_this_month(list_gen_start_date)
    except Exception as e:
        raise(e)
    
    return list_gen_end_date


def __generate_farm_report_list_file(
        list_gen_start_date: Optional[date],
        list_gen_end_date: Optional[date],
        farm_report_list_file_path: str
    ) -> None:
    
    '''周回報告一覧ファイル生成'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 周回報告一覧データフレームの初期化
        farm_report_list_df: pd.DataFrame = \
            pd.DataFrame(columns=const_util.FARM_REPORT_LIST_HEADER)
        
        # 開始日付から終了日付までの繰り返し
        if list_gen_start_date is not None and list_gen_end_date is not None:
            list_gen_date: Optional[date] = None
            for list_gen_date in mylib.gen_date_range(list_gen_start_date, list_gen_end_date):
                # 周回報告サイトURLの生成
                farm_report_site_url: str = const_util.FARM_REPORT_SITE_URL.format(list_gen_date)
                lg.info(farm_report_site_url)
                
                # クエスト種別ごとの周回報告数の取得
                response_for_bs: Response = requests.get(farm_report_site_url)
                bs: BeautifulSoup = BeautifulSoup(response_for_bs.content, 'html.parser')
                num_of_farm_reports_list: ResultSet = bs.find_all(class_='subtitle')
                num_of_farm_reports_of_event_quest: int = \
                    __get_num_of_farm_reports(num_of_farm_reports_list[0].get_text())
                num_of_farm_reports_of_normal_quest: int = \
                    __get_num_of_farm_reports(num_of_farm_reports_list[1].get_text())
                
                # 周回報告一覧データフレームの取得
                farm_report_list_dfs_by_html: list[pd.DataFrame] = pd.read_html(
                        farm_report_site_url,
                        index_col=None,
                        parse_dates=[0]
                    )
                
                # 周回報告一覧(イベクエ)の取得
                if num_of_farm_reports_of_event_quest > 0:
                    farm_report_list_dfs_by_html[0].set_axis(
                        const_util.FARM_REPORT_LIST_HEADER_RAW, axis='columns', inplace=True)
                    farm_report_list_dfs_by_html[0].insert(
                        0, const_util.FARM_REPORT_LIST_HEADER[0], 'イベクエ')
                    farm_report_list_df = pd.concat(
                            [farm_report_list_df, farm_report_list_dfs_by_html[0]]
                        )
                
                # 周回報告一覧(通常クエ)の取得
                if num_of_farm_reports_of_event_quest == 0 \
                    and num_of_farm_reports_of_normal_quest > 0:
                    farm_report_list_dfs_by_html[0].set_axis(
                        const_util.FARM_REPORT_LIST_HEADER_RAW, axis='columns', inplace=True)
                    farm_report_list_dfs_by_html[0].insert(
                        0, const_util.FARM_REPORT_LIST_HEADER[0], '通常クエ')
                    farm_report_list_df = pd.concat(
                            [farm_report_list_df, farm_report_list_dfs_by_html[0]]
                        )
                elif num_of_farm_reports_of_event_quest > 0 \
                    and num_of_farm_reports_of_normal_quest > 0:
                    farm_report_list_dfs_by_html[1].set_axis(
                        const_util.FARM_REPORT_LIST_HEADER_RAW, axis='columns', inplace=True)
                    farm_report_list_dfs_by_html[1].insert(
                        0, const_util.FARM_REPORT_LIST_HEADER[0], '通常クエ')
                    farm_report_list_df = pd.concat(
                            [farm_report_list_df, farm_report_list_dfs_by_html[1]]
                        )
        
        # 周回報告一覧データフレームの保存
        farm_report_list_df.reset_index(drop=True, inplace=True)
        lg.info(f'周回報告一覧(追加分先頭n行)\n{farm_report_list_df.head(5)}')
        lg.info(f'周回報告一覧(追加分末尾n行)\n{farm_report_list_df.tail(5)}')
        pandas_util.save_farm_report_list_data_frame(
            farm_report_list_df, farm_report_list_file_path)
    except Exception as e:
        raise(e)
    
    return None


def __get_num_of_farm_reports(sub_title: str) -> int:
    '''周回報告数取得'''
    
    try:
        matched_result_of_event_quest = re.match('イベント \\((.*)\\)', sub_title)
        matched_result_of_normal_quest = re.match('恒常フリークエスト \\((.*)\\)', sub_title)
        
        if matched_result_of_event_quest is not None:
            num_of_farm_reports: int = int(matched_result_of_event_quest.group(1))
        elif matched_result_of_normal_quest is not None:
            num_of_farm_reports: int = int(matched_result_of_normal_quest.group(1))
        else:
            num_of_farm_reports: int = 0
    except Exception as e:
        raise(e)
    
    return num_of_farm_reports
