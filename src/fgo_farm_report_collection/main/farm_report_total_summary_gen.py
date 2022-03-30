import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen, farm_report_total_summary_gen
from fgo_farm_report_collection.util import const_util


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、周回報告一覧ファイルを基に周回報告全体概要ファイルを生成する。
        
        任意で周回報告一覧ファイルを生成する。
    
    Args:
        -
    
    Args on cmd line:
        col_year_month (str)            : [グループA][必須] 収集年月(yyyy-mm形式)
        min_num_of_all_quest (int)      : [グループB][1つのみ必須] 最低周回数(全て)
        min_num_of_normal_quest (int)   : [グループB][1つのみ必須] 最低周回数(通常クエ)
        min_num_of_event_quest (int)    : [グループB][1つのみ必須] 最低周回数(イベクエ)
        generate_list (bool)            : [グループC][任意] 周回報告一覧生成要否
        output_user_name (bool)         : [グループC][任意] ユーザ名出力要否
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/[収集年月].csv
        周回報告全体概要ファイル: ./dest/farm_report_total_summary/[収集年月]_[クエスト種別]_[最低周回数].csv
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
        if bool(args.generate_list) == True:
            pyl.measure_proc_time(
                farm_report_list_gen.do_logic_that_generate_list_by_col_year_month)(
                        args.col_year_month
                    )
        
        # ロジック(周回報告全体概要生成)の実行
        if args.min_num_of_all_quest is not None:
            pyl.measure_proc_time(farm_report_total_summary_gen.do_logic)(
                    args.col_year_month,
                    int(args.min_num_of_all_quest),
                    const_util.QUEST_KINDS[0],
                    args.output_user_name
                )
        elif args.min_num_of_normal_quest is not None:
            pyl.measure_proc_time(farm_report_total_summary_gen.do_logic)(
                    args.col_year_month,
                    int(args.min_num_of_normal_quest),
                    const_util.QUEST_KINDS[1],
                    args.output_user_name
                )
        elif args.min_num_of_event_quest is not None:
            pyl.measure_proc_time(farm_report_total_summary_gen.do_logic)(
                    args.col_year_month,
                    int(args.min_num_of_event_quest),
                    const_util.QUEST_KINDS[2],
                    args.output_user_name
                )
    except KeyboardInterrupt as e:
        if lg is not None:
            pyl.log_inf(lg, f'処理を中断しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
                description='周回報告全体概要生成\n' +
                            '周回報告一覧ファイルを基に周回報告全体概要ファイルを生成します\n' +
                            '任意で周回報告一覧ファイルを生成します',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_: str = ''
        
        # グループAの引数(全て必須な引数)
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'Group A - all required arguments', '全て必須な引数')
        help_ = '収集年月(yyyy-mm形式)'
        arg_group_a.add_argument('col_year_month', help=help_)
        
        # グループBの引数(1つのみ必須な引数)
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            'Group B - only one required arguments',
            '1つのみ必須な引数\n収集する最低周回数を指定します')
        mutually_exclusive_group_b: argparse._MutuallyExclusiveGroup = \
            arg_group_b.add_mutually_exclusive_group(required=True)
        help_ = '最低周回数({0})'
        mutually_exclusive_group_b.add_argument(
            '-a', '--min_num_of_all_quest', type=int, help=help_.format('全て'))
        mutually_exclusive_group_b.add_argument(
            '-n', '--min_num_of_normal_quest', type=int, help=help_.format('通常クエ'))
        mutually_exclusive_group_b.add_argument(
            '-e', '--min_num_of_event_quest', type=int, help=help_.format('イベクエ'))
        
        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            'Group C - optional arguments', '任意の引数')
        help_ = '周回報告一覧生成要否\n' + \
                '指定した場合は一覧を生成します\n' + \
                '指定しない場合は生成せずに既存の一覧のみを使用します'
        arg_group_c.add_argument('-l', '--generate_list', action='store_true', help=help_)
        help_ = 'ユーザ名出力要否\n' + \
                '指定した場合は周回報告概要ファイルにユーザ名を出力します'
        arg_group_c.add_argument('-u', '--output_user_name', action='store_true', help=help_)
        
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
        
        # 検証：収集年月が年月(yyyy-mm形式)であること
        try:
            datetime.strptime(args.col_year_month, '%Y-%m')
        except ValueError:
            pyl.log_war(lg, f'収集年月が年月(yyyy-mm形式)ではありません。' +
                            f'(col_year_month:{args.col_year_month})')
            return False
        
        # 検証：最低周回数のいずれかが0以上であること
        if args.min_num_of_all_quest is not None \
            and not (args.min_num_of_all_quest >= 0):
            pyl.log_war(lg, f'最低周回数(全て)が0以上ではありません。' +
                            f'(min_num_of_all_quest:{args.min_num_of_all_quest})')
            return False
        elif args.min_num_of_normal_quest is not None \
            and not (args.min_num_of_normal_quest >= 0):
            pyl.log_war(lg, f'最低周回数(通常クエ)が0以上ではありません。' +
                            f'(min_num_of_normal_quest:{args.min_num_of_normal_quest})')
            return False
        elif args.min_num_of_event_quest is not None \
            and not (args.min_num_of_event_quest >= 0):
            pyl.log_war(lg, f'最低周回数(イベクエ)が0以上ではありません。' +
                            f'(min_num_of_event_quest:{args.min_num_of_event_quest})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
