import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_gen_files_merge


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、生成されたファイルをExcelファイルにマージする。
    
    Args:
        -
    
    Args on cmd line:
        merge_list_files (bool)                 : [グループB1][1つのみ必須] 周回報告一覧ファイルマージ要否
        merge_user_total_summary_files (bool)   : [グループB1][1つのみ必須] 周回報告ユーザ全体概要ファイルマージ要否
        merge_quest_total_summary_files (bool)  : [グループB1][1つのみ必須] 周回報告クエスト全体概要ファイルマージ要否
        merge_individual_summary_files (bool)   : [グループB1][1つのみ必須] 周回報告個人概要ファイルマージ要否
        append_generated_file (bool)            : [グループC][任意] マージ結果追記要否
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        周回報告一覧マージ結果ファイル: ./dest/merge_result/farm_report_list.xlsx
        周回報告ユーザ全体概要マージ結果ファイル: ./dest/merge_result/farm_report_user_total_summary.xlsx
        周回報告クエスト全体概要マージ結果ファイル: ./dest/merge_result/farm_report_quest_total_summary.xlsx
        周回報告個人概要マージ結果ファイル: ./dest/merge_result/farm_report_individual_summary.xlsx
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
        
        # ロジック(周回報告生成ファイルマージ)の実行
        if bool(args.merge_list_files) == True:
            farm_report_gen_files_merge.do_logic_that_merge_farm_report_list_files(
                    args.append_generated_file
                )
        elif bool(args.merge_user_total_summary_files) == True:
            farm_report_gen_files_merge.do_logic_that_merge_farm_report_usr_tot_sum_files(
                    args.append_generated_file
                )
        elif bool(args.merge_quest_total_summary_files) == True:
            farm_report_gen_files_merge.do_logic_that_merge_farm_report_qst_tot_sum_files(
                    args.append_generated_file
                )
        elif bool(args.merge_individual_summary_files) == True:
            farm_report_gen_files_merge.do_logic_that_merge_farm_report_ind_sum_files(
                    args.append_generated_file
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
                description='周回報告生成ファイルマージ\n' +
                            '生成されたファイルをExcelファイルにマージします',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_: str = ''
        
        # グループBの引数(1つのみ必須な引数)
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            'Group B - only one required arguments',
            '1つのみ必須な引数\n処理を指定します')
        mutually_exclusive_group_b: argparse._MutuallyExclusiveGroup = \
            arg_group_b.add_mutually_exclusive_group(required=True)
        help_ = '周回報告一覧ファイルマージ要否'
        mutually_exclusive_group_b.add_argument(
            '-l', '--merge_list_files', action='store_true', help=help_)
        help_ = '周回報告ユーザ全体概要ファイルマージ要否'
        mutually_exclusive_group_b.add_argument(
            '-u', '--merge_user_total_summary_files', action='store_true', help=help_)
        help_ = '周回報告クエスト全体概要ファイルマージ要否'
        mutually_exclusive_group_b.add_argument(
            '-q', '--merge_quest_total_summary_files', action='store_true', help=help_)
        help_ = '周回報告個人概要ファイルマージ要否'
        mutually_exclusive_group_b.add_argument(
            '-i', '--merge_individual_summary_files', action='store_true', help=help_)
        
        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            'Group C - optional arguments', '任意の引数')
        help_ = '生成ファイル追記要否\n' + \
                '指定した場合は生成ファイルをシート単位で追記します\n' + \
                '指定しない場合は生成ファイルを上書きします'
        arg_group_c.add_argument('-a', '--append_generated_file', action='store_true', help=help_)
        
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
        
        # 検証：なし
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
