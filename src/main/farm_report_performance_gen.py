import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Optional

import python_lib_for_me as mylib
from src.logic import farm_report_performance_gen
from src.util import *


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、周回報告一覧ファイルと周回報告実績ファイルを生成する。
    
    Args:
        -
    
    Args on cmd line:
        col_year (str)               : [必須] 収集年(yyyy形式)
        user_id (str)                : [必須] ユーザID(Twitter)
        should_generate_list (bool)  : [任意] 周回報告一覧生成要否
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/farm_report_list_[収集年月].csv
        周回報告実績ファイル: ./dest/farm_report_performance/farm_report_performance_[収集年]_[ユーザID].csv
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 実行コマンド表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        lg.info(f'実行コマンド：{sys.argv}')
        
        # 引数取得＆検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # 周回報告実績生成ロジックの実行
        mylib.measure_proc_time(farm_report_performance_gen.do_logic)(
                args.col_year,
                args.user_id,
                bool(args.should_generate_list)
            )
    except Exception as e:
        if lg is not None:
            lg.exception('', exc_info=True)
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_msg: str = ''
        
        # 必須の引数
        help_msg = '収集年(yyyy形式)'
        parser.add_argument('col_year', help=help_msg)
        help_msg = 'ユーザID(Twitter)'
        parser.add_argument('user_id', help=help_msg)
        
        # 任意の引数
        help_msg = '周回報告一覧生成要否\n' + \
            '指定した場合は一覧を生成するが、指定しなかった場合は生成せずに既存の一覧のみを使用する。'
        parser.add_argument('-l', '--should_generate_list', help=help_msg, action='store_true')
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 検証：収集年が年(yyyy形式)であること
        try:
            datetime.strptime(args.col_year, '%Y')
        except ValueError:
            lg.info(f'収集年が年(yyyy形式)ではありません。(col_year:{args.col_year})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
