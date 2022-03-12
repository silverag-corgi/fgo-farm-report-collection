import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、周回報告一覧ファイルを生成する。
    
    Args:
        -
    
    Args on cmd line:
        col_year (str)          : [いずれかが必須] 収集年(yyyy形式)
        col_year_month (str)    : [いずれかが必須] 収集年月(yyyy-mm形式)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/farm_report_list_[収集年月].csv
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 実行コマンドの表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        pyl.log_inf(lg, f'実行コマンド：{sys.argv}')
        
        # 引数の取得・検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # ロジック(周回報告一覧生成)の実行
        if args.col_year is not None:
            pyl.measure_proc_time(farm_report_list_gen.do_logic_by_col_year)(
                    args.col_year
                )
        elif args.col_year_month is not None:
            pyl.measure_proc_time(farm_report_list_gen.do_logic_by_col_year_month)(
                    args.col_year_month
                )
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
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
        
        # グループで1つのみ必須の引数
        group: argparse._MutuallyExclusiveGroup = \
            parser.add_mutually_exclusive_group(required=True)
        help_msg = '{0}\nグループで1つのみ必須'
        group.add_argument(
            '-y', '--col_year', type=str, help=help_msg.format('収集年(yyyy形式)'))
        group.add_argument(
            '-m', '--col_year_month', type=str, help=help_msg.format('収集年月(yyyy-mm形式)'))
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 検証：収集年が年(yyyy形式)であるか、もしくは収集年月が年月(yyyy-mm形式)であること
        if args.col_year is not None:
            try:
                datetime.strptime(args.col_year, '%Y')
            except ValueError:
                pyl.log_war(lg, f'収集年が年(yyyy形式)ではありません。(col_year:{args.col_year})')
                return False
        elif args.col_year_month is not None:
            try:
                datetime.strptime(args.col_year_month, '%Y-%m')
            except ValueError:
                pyl.log_war(lg, f'収集年月が年月(yyyy-mm形式)ではありません。(col_year_month:{args.col_year_month})')
                return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
