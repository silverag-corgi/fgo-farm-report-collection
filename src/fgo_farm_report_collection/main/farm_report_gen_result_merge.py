import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_gen_result_merge


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、生成結果をExcelファイル(マージ結果ファイル)にマージする。
    
    Args:
        -
    
    Args on cmd line:
        merge_list (bool)                   : [グループB1][1つのみ必須] 周回報告一覧マージ要否
        merge_user_total_summary (bool)     : [グループB1][1つのみ必須] 周回報告ユーザ全体概要マージ要否
        merge_quest_total_summary (bool)    : [グループB1][1つのみ必須] 周回報告クエスト全体概要マージ要否
        merge_individual_summary (bool)     : [グループB1][1つのみ必須] 周回報告個人概要マージ要否
        append_sheet (bool)                 : [グループC][任意] シート追加要否
    
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
        
        # ロジック(周回報告生成結果マージ)の実行
        if bool(args.merge_list) == True:
            farm_report_gen_result_merge.do_logic_that_merge_list(
                    args.append_sheet
                )
        elif bool(args.merge_user_total_summary) == True:
            farm_report_gen_result_merge.do_logic_that_merge_usr_tot_sum(
                    args.append_sheet
                )
        elif bool(args.merge_quest_total_summary) == True:
            farm_report_gen_result_merge.do_logic_that_merge_qst_tot_sum(
                    args.append_sheet
                )
        elif bool(args.merge_individual_summary) == True:
            farm_report_gen_result_merge.do_logic_that_merge_ind_sum(
                    args.append_sheet
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
                description='周回報告生成結果マージ\n' +
                            '生成結果をExcelファイルにマージします',
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
        help_ = '周回報告一覧マージ要否'
        mutually_exclusive_group_b.add_argument(
            '-l', '--merge_list', action='store_true', help=help_)
        help_ = '周回報告ユーザ全体概要マージ要否'
        mutually_exclusive_group_b.add_argument(
            '-u', '--merge_user_total_summary', action='store_true', help=help_)
        help_ = '周回報告クエスト全体概要マージ要否'
        mutually_exclusive_group_b.add_argument(
            '-q', '--merge_quest_total_summary', action='store_true', help=help_)
        help_ = '周回報告個人概要マージ要否'
        mutually_exclusive_group_b.add_argument(
            '-i', '--merge_individual_summary', action='store_true', help=help_)
        
        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            'Group C - optional arguments', '任意の引数')
        help_ = 'シート追加要否\n' + \
                '指定した場合は既存のシートは変更せず、新規のシートのみを追加します\n' + \
                '指定しない場合は全てのシートを上書きします'
        arg_group_c.add_argument('-a', '--append_sheet', action='store_true', help=help_)
        
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
