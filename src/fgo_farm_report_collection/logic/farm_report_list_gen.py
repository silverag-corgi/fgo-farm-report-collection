import os
import re
from datetime import date, datetime, timedelta
from logging import Logger
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_by_col_year(
        col_year: str
    ) -> None:
    
    '''ロジック(年指定)実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告一覧生成(年指定)を開始します。')
        
        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f'{col_year:02}-{(index+1):02}'
            
            # 周回報告一覧生成ロジックの実行
            do_logic_by_col_year_month(
                    col_year_month
                )
        
        pyl.log_inf(lg, f'周回報告一覧生成(年指定)を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_by_col_year_month(
        col_year_month: str
    ) -> None:
    
    '''ロジック(年月指定)実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告一覧生成(年月指定)を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # 収集年月が未来の場合
        today: date = datetime.today().date()
        col_first_date: date = datetime.strptime(col_year_month + '-01', '%Y-%m-%d').date()
        first_date_of_this_month: date = pyl.get_first_date_of_this_month(today)
        if col_first_date > first_date_of_this_month:
            pyl.log_inf(lg, f'収集年月が未来です。(col_year_month:{col_year_month})')
        else:
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
            generate_list: bool = True
            if list_gen_start_date is None or list_gen_end_date is None:
                generate_list = False
                pyl.log_inf(lg, f'周回報告一覧は最新です。({col_year_month})')
            else:
                if list_gen_start_date > list_gen_end_date:
                    generate_list = False
                    pyl.log_inf(lg, f'周回報告一覧は最新です。({col_year_month})')
                else:
                    generate_list = True
                    pyl.log_inf(lg, f'周回報告一覧を生成します。({list_gen_start_date}～{list_gen_end_date})')
            
            # 周回報告一覧ファイルの生成
            if generate_list == True:
                pyl.log_inf(lg, f'周回報告一覧ファイル：{farm_report_list_file_path}')
                __generate_farm_report_list_file(
                        list_gen_start_date,
                        list_gen_end_date,
                        farm_report_list_file_path
                    )
        
        pyl.log_inf(lg, f'周回報告一覧生成(年月指定)を終了します。')
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
        lg = pyl.get_logger(__name__)
        
        # 収集年月の周回報告一覧ファイルの存在有無チェック
        has_farm_report_list: bool = os.path.isfile(farm_report_list_file_path)
        
        # 周回報告一覧生成開始日付の生成
        list_gen_start_date: Optional[date] = None
        if has_farm_report_list == True:
            farm_report_list_df: pd.DataFrame = \
                pandas_util.read_farm_report_list_file(farm_report_list_file_path)
            
            posting_date_of_last_line_datetime: Any = \
                farm_report_list_df[const_util.FARM_REPORT_LIST_HEADER[1]].tail(1).item()
            posting_date_of_last_line: date = \
                pd.Timestamp(posting_date_of_last_line_datetime).date()
            
            if posting_date_of_last_line != \
                pyl.get_last_date_of_this_month(posting_date_of_last_line):
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
        if list_gen_start_date is not None \
            and col_first_date == first_date_of_this_month:
            list_gen_end_date = today + timedelta(days=-1)
        elif list_gen_start_date is not None \
            and col_first_date != first_date_of_this_month:
            list_gen_end_date = pyl.get_last_date_of_this_month(list_gen_start_date)
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
        lg = pyl.get_logger(__name__)
        
        # 周回報告一覧データフレームの初期化
        farm_report_list_df: pd.DataFrame = \
            pd.DataFrame(columns=const_util.FARM_REPORT_LIST_HEADER)
        
        # 開始日付から終了日付までの繰り返し
        if list_gen_start_date is not None and list_gen_end_date is not None:
            list_gen_date: Optional[date] = None
            for list_gen_date in pyl.gen_date_range(list_gen_start_date, list_gen_end_date):
                # 周回報告サイトURLの生成
                farm_report_site_url: str = const_util.FARM_REPORT_SITE_URL.format(list_gen_date)
                pyl.log_inf(lg, farm_report_site_url)
                
                # 周回報告サイトからの応答の取得(周回報告サイトへの要求)
                response_from_farm_report_site: Response = requests.get(farm_report_site_url)
                if response_from_farm_report_site.status_code != requests.codes['ok']:
                    pyl.log_war(lg, f'周回報告サイトへのアクセスに失敗しました。' +
                                    f'(farm_report_site_url:{farm_report_site_url}, ' +
                                    f'status_code:{response_from_farm_report_site.status_code})')
                    return None
                
                # クエスト種別ごとの周回報告数の取得
                bs: BeautifulSoup = \
                    BeautifulSoup(response_from_farm_report_site.content, 'html.parser')
                num_of_farm_reports_list: ResultSet = bs.find_all(class_='subtitle')
                num_of_farm_reports_of_event_quest: int = \
                    __get_num_of_farm_reports(num_of_farm_reports_list[0].get_text())
                num_of_farm_reports_of_normal_quest: int = \
                    __get_num_of_farm_reports(num_of_farm_reports_list[1].get_text())
                
                # 周回報告一覧データフレームの取得(周回報告サイトの読み込み)
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
                            [farm_report_list_df, farm_report_list_dfs_by_html[0]],
                            ignore_index=True
                        )
                
                # 周回報告一覧(通常クエ)の取得
                if num_of_farm_reports_of_event_quest == 0 \
                    and num_of_farm_reports_of_normal_quest > 0:
                    farm_report_list_dfs_by_html[0].set_axis(
                        const_util.FARM_REPORT_LIST_HEADER_RAW, axis='columns', inplace=True)
                    farm_report_list_dfs_by_html[0].insert(
                        0, const_util.FARM_REPORT_LIST_HEADER[0], '通常クエ')
                    farm_report_list_df = pd.concat(
                            [farm_report_list_df, farm_report_list_dfs_by_html[0]],
                            ignore_index=True
                        )
                elif num_of_farm_reports_of_event_quest > 0 \
                    and num_of_farm_reports_of_normal_quest > 0:
                    farm_report_list_dfs_by_html[1].set_axis(
                        const_util.FARM_REPORT_LIST_HEADER_RAW, axis='columns', inplace=True)
                    farm_report_list_dfs_by_html[1].insert(
                        0, const_util.FARM_REPORT_LIST_HEADER[0], '通常クエ')
                    farm_report_list_df = pd.concat(
                            [farm_report_list_df, farm_report_list_dfs_by_html[1]],
                            ignore_index=True
                        )
        
        # 周回報告一覧データフレームの保存
        pyl.log_inf(lg, f'周回報告一覧(追加分先頭n行)：\n{farm_report_list_df.head(5)}')
        pyl.log_inf(lg, f'周回報告一覧(追加分末尾n行)：\n{farm_report_list_df.tail(5)}')
        pandas_util.save_farm_report_list_df(farm_report_list_df, farm_report_list_file_path)
    except Exception as e:
        raise(e)
    
    return None


def __get_num_of_farm_reports(sub_title: str) -> int:
    '''周回報告数取得'''
    
    try:
        matched_result_of_event_quest = re.match('イベント \\((.*)\\)', sub_title)
        matched_result_of_normal_quest = re.match('恒常フリークエスト \\((.*)\\)', sub_title)
        
        num_of_farm_reports: int = 0
        if matched_result_of_event_quest is not None:
            num_of_farm_reports = int(matched_result_of_event_quest.group(1))
        elif matched_result_of_normal_quest is not None:
            num_of_farm_reports = int(matched_result_of_normal_quest.group(1))
    except Exception as e:
        raise(e)
    
    return num_of_farm_reports
