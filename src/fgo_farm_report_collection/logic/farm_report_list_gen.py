import json
import os
from datetime import date, datetime, timedelta
from logging import Logger
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import requests

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_that_generate_list_by_col_year(
        col_year: str
    ) -> None:
    
    '''ロジック(周回報告一覧生成(年指定))実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告一覧生成(年指定)を開始します。')
        
        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f'{col_year:04}-{(index+1):02}'
            
            # 周回報告一覧生成ロジックの実行
            do_logic_that_generate_list_by_col_year_month(
                    col_year_month
                )
        
        pyl.log_inf(lg, f'周回報告一覧生成(年指定)を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_generate_list_by_col_year_month(
        col_year_month: str
    ) -> None:
    
    '''ロジック(周回報告一覧生成(年月指定))実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
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
            
            # 周回報告一覧ファイルの存在有無チェック
            has_farm_report_list: bool = os.path.isfile(farm_report_list_file_path)
            
            # 周回報告一覧生成開始日付の設定
            list_gen_start_date: Optional[date] = __generate_list_gen_start_date(
                has_farm_report_list, farm_report_list_file_path, col_first_date)
            
            # 周回報告一覧生成終了日付の設定
            list_gen_end_date: Optional[date] = __generate_list_gen_end_date(
                list_gen_start_date, col_first_date, first_date_of_this_month, today)
            
            # 周回報告一覧生成要否の判定
            generate_list: bool = True
            if list_gen_start_date is None or list_gen_end_date is None:
                generate_list = False
                pyl.log_inf(lg, f'周回報告一覧は最新です。(col_year_month:{col_year_month})')
            else:
                if list_gen_start_date > list_gen_end_date:
                    generate_list = False
                    pyl.log_inf(lg, f'周回報告一覧は最新です。(col_year_month:{col_year_month})')
                else:
                    generate_list = True
                    pyl.log_inf(lg, f'周回報告一覧を生成します。' +
                                    f'(col_year_month:{list_gen_start_date}～{list_gen_end_date})')
            
            # 周回報告一覧ファイルの生成
            if generate_list == True:
                pyl.log_inf(lg, f'周回報告一覧ファイル：{farm_report_list_file_path}')
                __generate_farm_report_list_file(
                        list_gen_start_date,
                        list_gen_end_date,
                        farm_report_list_file_path,
                        has_farm_report_list
                    )
        
        pyl.log_inf(lg, f'周回報告一覧生成(年月指定)を終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __generate_list_gen_start_date(
        has_farm_report_list: bool,
        farm_report_list_file_path: str,
        col_first_date: date
    ) -> Optional[date]:
    
    '''周回報告一覧生成開始日付生成'''
    
    lg: Optional[Logger] = None
    
    try:
        list_gen_start_date: Optional[date] = None
        if has_farm_report_list == True:
            farm_report_list_df: pd.DataFrame = \
                pandas_util.read_farm_report_list_file(farm_report_list_file_path)
            
            post_date_of_last_line_datetime: Any = \
                farm_report_list_df[const_util.FARM_REPORT_LIST_HEADER[1]].tail(1).item()
            post_date_of_last_line: date = \
                pd.Timestamp(post_date_of_last_line_datetime).date()
            
            if post_date_of_last_line != \
                pyl.get_last_date_of_this_month(post_date_of_last_line):
                list_gen_start_date = post_date_of_last_line + timedelta(days=1)
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
        farm_report_list_file_path: str,
        has_farm_report_list: bool
    ) -> None:
    
    '''周回報告一覧ファイル生成'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 周回報告一覧データフレームの初期化
        farm_report_list_df: pd.DataFrame = pd.DataFrame(columns=const_util.FARM_REPORT_LIST_HEADER)
        
        # 周回報告一覧データフレームへの格納
        if list_gen_start_date is not None and list_gen_end_date is not None:
            list_gen_date: Optional[date] = None
            for list_gen_date in pyl.gen_date_range(list_gen_start_date, list_gen_end_date):
                # 周回報告サイトURLの生成
                farm_report_site_url: str = const_util.FARM_REPORT_SITE_URL.format(list_gen_date)
                pyl.log_inf(lg, f'周回報告サイトURL：{farm_report_site_url}')
                
                # 周回報告サイトからの周回報告の取得
                farm_report_site_response = requests.get(farm_report_site_url)
                farm_reports: dict[Any, Any] = json.loads(farm_report_site_response.text)
                
                # 周回報告データフレームの格納
                for farm_report in farm_reports:
                    farm_report_df = pd.DataFrame(
                            [[
                                (const_util.QUEST_KINDS[1]
                                    if bool(farm_report['freequest']) == True
                                    else const_util.QUEST_KINDS[2]),
                                pyl.convert_timestamp_to_jst(
                                    farm_report['timestamp'], '%Y-%m-%dT%H:%M:%S%z'),
                                farm_report['reporter'],
                                farm_report['chapter'] + ' ' + farm_report['place'],
                                farm_report['runcount'],
                                ', '.join(['{0}: {1}'.format(key, value)
                                            for key, value in farm_report['items'].items()]),
                            ]],
                            columns=const_util.FARM_REPORT_LIST_HEADER
                        )
                    farm_report_list_df = \
                        pd.concat([farm_report_list_df, farm_report_df], ignore_index=True)
        
        # 周回報告一覧データフレームの保存
        pyl.log_inf(lg, f'周回報告一覧(追加分先頭n行)：\n{farm_report_list_df.head(5)}')
        pyl.log_inf(lg, f'周回報告一覧(追加分末尾n行)：\n{farm_report_list_df.tail(5)}')
        pandas_util.save_farm_report_list_df(
            farm_report_list_df, farm_report_list_file_path, has_farm_report_list)
    except Exception as e:
        raise(e)
    
    return None
