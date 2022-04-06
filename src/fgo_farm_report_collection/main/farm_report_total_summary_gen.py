import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Callable, Optional

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
        col_year (str)                      : [グループB1][1つのみ必須] 収集年(yyyy形式)
        col_year_month (str)                : [グループB1][1つのみ必須] 収集年月(yyyy-mm形式)
        generate_user_total_summary (bool)  : [グループB2][1つのみ必須] 周回報告ユーザ全体概要生成要否
        generate_quest_total_summary (bool) : [グループB2][1つのみ必須] 周回報告クエスト全体概要生成要否
        min_num_of_all_quest (int)          : [グループB3][1つのみ必須] 最低周回数(全て)
        min_num_of_normal_quest (int)       : [グループB3][1つのみ必須] 最低周回数(通常クエ)
        min_num_of_event_quest (int)        : [グループB3][1つのみ必須] 最低周回数(イベクエ)
        min_num_of_quest_by_batch (int)     : [グループB3][1つのみ必須] 最低周回数(3種類一括)
        generate_list (bool)                : [グループC][任意] 周回報告一覧生成要否
        output_user_name (bool)             : [グループC][任意] ユーザ名出力要否
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/[収集年月].csv
        周回報告ユーザ全体概要ファイル: ./dest/farm_report_total_summary/user/[収集年月]_[クエスト種別]_[最低周回数].csv
        周回報告クエスト全体概要ファイル: ./dest/farm_report_total_summary/quest/[収集年月]_[クエスト種別]_[最低周回数].csv
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
            if args.col_year is not None:
                pyl.measure_proc_time(
                    farm_report_list_gen.do_logic_that_generate_list_by_col_year)(
                            args.col_year
                        )
            elif args.col_year_month is not None:
                pyl.measure_proc_time(
                    farm_report_list_gen.do_logic_that_generate_list_by_col_year_month)(
                            args.col_year_month
                        )
        
        # ロジック(周回報告全体概要生成)の実行
        if args.col_year is not None:
            if args.min_num_of_quest_by_batch is None:
                __do_individual_processing(
                        (farm_report_total_summary_gen.
                            do_logic_that_generate_tot_sum_by_col_year),
                        args
                    )
            else:
                __do_batch_processing(
                        (farm_report_total_summary_gen.
                            do_logic_that_generate_tot_sum_by_col_year),
                        args
                    )
        elif args.col_year_month is not None:
            if args.min_num_of_quest_by_batch is None:
                __do_individual_processing(
                        (farm_report_total_summary_gen.
                            do_logic_that_generate_tot_sum_by_col_year_month),
                        args
                    )
            else:
                __do_batch_processing(
                        (farm_report_total_summary_gen.
                            do_logic_that_generate_tot_sum_by_col_year_month),
                        args
                    )
    except KeyboardInterrupt as e:
        if lg is not None:
            pyl.log_inf(lg, f'処理を中断しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
        return 1
    
    return 0


def __do_individual_processing(function_object: Callable, args: argparse.Namespace) -> None:
    
    '''個別処理実行'''
    
    pyl.measure_proc_time(function_object)(
            args.col_year if args.col_year is not None else args.col_year_month,
            (farm_report_total_summary_gen.EnumOfProc.GENERATE_USER_TOTAL_SUMMARY
                if bool(args.generate_user_total_summary) == True
                else farm_report_total_summary_gen.EnumOfProc.GENERATE_QUEST_TOTAL_SUMMARY),
            (int(args.min_num_of_all_quest)
                if args.min_num_of_all_quest is not None
                else int(args.min_num_of_normal_quest)
                if args.min_num_of_normal_quest is not None
                else int(args.min_num_of_event_quest)),
            (const_util.QUEST_KINDS[0]
                if args.min_num_of_all_quest is not None
                else const_util.QUEST_KINDS[1]
                if args.min_num_of_normal_quest is not None
                else const_util.QUEST_KINDS[2]),
            bool(args.output_user_name)
        )
    
    return None


def __do_batch_processing(function_object: Callable, args: argparse.Namespace) -> None:
    
    '''一括処理実行'''
    
    pyl.measure_proc_time(function_object)(
            args.col_year if args.col_year is not None else args.col_year_month,
            (farm_report_total_summary_gen.EnumOfProc.GENERATE_USER_TOTAL_SUMMARY
                if bool(args.generate_user_total_summary) == True
                else farm_report_total_summary_gen.EnumOfProc.GENERATE_QUEST_TOTAL_SUMMARY),
            int(args.min_num_of_quest_by_batch),
            const_util.QUEST_KINDS[0],
            bool(args.output_user_name)
        )
    pyl.measure_proc_time(function_object)(
            args.col_year if args.col_year is not None else args.col_year_month,
            (farm_report_total_summary_gen.EnumOfProc.GENERATE_USER_TOTAL_SUMMARY
                if bool(args.generate_user_total_summary) == True
                else farm_report_total_summary_gen.EnumOfProc.GENERATE_QUEST_TOTAL_SUMMARY),
            int(args.min_num_of_quest_by_batch),
            const_util.QUEST_KINDS[1],
            args.output_user_name
        )
    pyl.measure_proc_time(function_object)(
            args.col_year if args.col_year is not None else args.col_year_month,
            (farm_report_total_summary_gen.EnumOfProc.GENERATE_USER_TOTAL_SUMMARY
                if bool(args.generate_user_total_summary) == True
                else farm_report_total_summary_gen.EnumOfProc.GENERATE_QUEST_TOTAL_SUMMARY),
            int(args.min_num_of_quest_by_batch),
            const_util.QUEST_KINDS[2],
            args.output_user_name
        )
    
    return None


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
        
        # グループB1の引数(1つのみ必須な引数)
        arg_group_b1: argparse._ArgumentGroup = parser.add_argument_group(
            'Group B1 - only one required arguments',
            '1つのみ必須な引数\n収集する年月を指定します')
        mutually_exclusive_group_b1: argparse._MutuallyExclusiveGroup = \
            arg_group_b1.add_mutually_exclusive_group(required=True)
        help_ = '収集年(yyyy形式)'
        mutually_exclusive_group_b1.add_argument('-y', '--col_year', type=str, help=help_)
        help_ = '収集年月(yyyy-mm形式)'
        mutually_exclusive_group_b1.add_argument('-m', '--col_year_month', type=str, help=help_)
        
        # グループB2の引数(1つのみ必須な引数)
        arg_group_b2: argparse._ArgumentGroup = parser.add_argument_group(
            'Group B2 - only one required arguments',
            '1つのみ必須な引数\n処理を指定します')
        mutually_exclusive_group_b2: argparse._MutuallyExclusiveGroup = \
            arg_group_b2.add_mutually_exclusive_group(required=True)
        help_ = '周回報告{0}全体概要生成要否\n' + \
                '周回報告{0}全体概要を生成します'
        mutually_exclusive_group_b2.add_argument(
            '-u', '--generate_user_total_summary', action='store_true', help=help_.format('ユーザ'))
        mutually_exclusive_group_b2.add_argument(
            '-q', '--generate_quest_total_summary', action='store_true', help=help_.format('クエスト'))
        
        # グループB3の引数(1つのみ必須な引数)
        arg_group_b3: argparse._ArgumentGroup = parser.add_argument_group(
            'Group B3 - only one required arguments',
            '1つのみ必須な引数\n収集する最低周回数を指定します')
        mutually_exclusive_group_b3: argparse._MutuallyExclusiveGroup = \
            arg_group_b3.add_mutually_exclusive_group(required=True)
        help_ = '最低周回数({0})'
        mutually_exclusive_group_b3.add_argument(
            '-a', '--min_num_of_all_quest', type=int, help=help_.format('全て'))
        mutually_exclusive_group_b3.add_argument(
            '-n', '--min_num_of_normal_quest', type=int, help=help_.format('通常クエ'))
        mutually_exclusive_group_b3.add_argument(
            '-e', '--min_num_of_event_quest', type=int, help=help_.format('イベクエ'))
        mutually_exclusive_group_b3.add_argument(
            '-b', '--min_num_of_quest_by_batch', type=int, help=help_.format('3種類一括'))
        
        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            'Group C - optional arguments', '任意の引数')
        help_ = '周回報告一覧生成要否\n' + \
                '指定した場合は一覧を生成します\n' + \
                '指定しない場合は生成せずに既存の一覧のみを使用します'
        arg_group_c.add_argument('-l', '--generate_list', action='store_true', help=help_)
        help_ = 'ユーザ名出力要否\n' + \
                '指定した場合は周回報告ユーザ全体概要ファイルにユーザ名を出力します'
        arg_group_c.add_argument('-un', '--output_user_name', action='store_true', help=help_)
        
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
