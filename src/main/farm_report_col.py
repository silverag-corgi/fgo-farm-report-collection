import argparse
import os
import sys
from datetime import datetime
from logging import Logger
from typing import Optional

import python_lib_for_me
from src.logic import farm_report_col
from src.util import const_util


def main():
    '''メイン'''
    
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
        
        # 周回報告収集
        if args.min_num_of_all_quest is not None:
            farm_report_col.do_logic(
                    args.col_year_month,
                    args.min_num_of_all_quest,
                    const_util.QUEST_KINDS[0],
                    args.should_output_user_name
                )
        elif args.min_num_of_normal_quest is not None:
            farm_report_col.do_logic(
                    args.col_year_month,
                    args.min_num_of_normal_quest,
                    const_util.QUEST_KINDS[1],
                    args.should_output_user_name
                )
        elif args.min_num_of_event_quest is not None:
            farm_report_col.do_logic(
                    args.col_year_month,
                    args.min_num_of_event_quest,
                    const_util.QUEST_KINDS[2],
                    args.should_output_user_name
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
        
        # グループで1つのみ必須の引数
        group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
        help_msg = '最低周回数({0})\nグループで1つのみ必須'
        group.add_argument('-a', '--min_num_of_all_quest', type=int, help=help_msg.format('全て'))
        group.add_argument('-n', '--min_num_of_normal_quest', type=int, help=help_msg.format('通常クエ'))
        group.add_argument('-e', '--min_num_of_event_quest', type=int, help=help_msg.format('イベクエ'))
        
        # 任意の引数
        help_msg = 'ユーザ名出力要否'
        parser.add_argument('-u', '--should_output_user_name', help=help_msg, action='store_true')
        
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
        
        # 検証：最低周回数のいずれかが0以上であること
        if args.min_num_of_all_quest is not None \
            and args.min_num_of_all_quest < 0:
            lg.info(f'最低周回数(全て)が0以上ではありません。(min_num_of_all_quest:{args.min_num_of_all_quest})')
            return False
        elif args.min_num_of_normal_quest is not None \
            and args.min_num_of_normal_quest < 0:
            lg.info(f'最低周回数(通常クエ)が0以上ではありません。(min_num_of_normal_quest:{args.min_num_of_normal_quest})')
            return False
        elif args.min_num_of_event_quest is not None \
            and args.min_num_of_event_quest < 0:
            lg.info(f'最低周回数(イベクエ)が0以上ではありません。(min_num_of_event_quest:{args.min_num_of_event_quest})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())
