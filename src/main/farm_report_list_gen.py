import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Optional

import python_lib_for_me
from src.logic import *
from src.util import *


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、周回報告一覧ファイルを生成する。
    
    Args:
        -
    
    Args on cmd line:
        col_year_month (str): [必須] 収集年月(yyyy-mm形式)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/farm_report_list_[収集年月].csv
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = python_lib_for_me.get_logger(__name__)
        
        # 実行コマンド表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        lg.info(f'実行コマンド：{sys.argv}')
        
        # 引数取得＆検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # 周回報告一覧生成ロジックの実行
        mylib.measure_proc_time(farm_report_list_gen.do_logic)(
                args.col_year_month
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
        help_msg = '収集年月(yyyy-mm形式)'
        parser.add_argument('col_year_month', help=help_msg)
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = python_lib_for_me.get_logger(__name__)
        
        # 検証：収集年月が年月(yyyy-mm形式)であること
        try:
            datetime.strptime(args.col_year_month, '%Y-%m')
        except ValueError:
            lg.info(f'収集年月が年月(yyyy-mm形式)ではありません。(col_year_month:{args.col_year_month})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
