import argparse
import os
import sys
from datetime import datetime
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_individual_summary_gen


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、周回報告一覧ファイルを基に周回報告個人概要ファイルを生成する。

        任意で周回報告一覧ファイルを生成する。

    Args:
        -

    Args on cmd line:
        col_year (str)          : [グループA][必須] 収集年(yyyy形式)
        user_id (str)           : [グループA][必須] ユーザID
        generate_list (bool)    : [グループC][任意] 周回報告一覧生成要否

    Returns:
        int: 終了コード(0：正常、1：異常)

    Destinations:
        周回報告一覧ファイル: ./dest/farm_report_list/[収集年月].csv
        周回報告個人概要ファイル: ./dest/farm_report_individual_summary/[収集年]_[ユーザID].csv
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 実行コマンドの表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        clg.log_inf(f"実行コマンド：{sys.argv}")

        # 引数の取得・検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) is False:
            return 1

        # ロジック(周回報告個人概要生成)の実行
        pyl.measure_proc_time(
            farm_report_individual_summary_gen.do_logic,
        )(
            args.col_year,
            args.user_id,
            bool(args.generate_list),
        )
    except KeyboardInterrupt as e:
        if clg is not None:
            clg.log_inf(f"処理を中断しました。")
    except Exception as e:
        if clg is not None:
            clg.log_exc("")
        return 1

    return 0


def __get_args() -> argparse.Namespace:
    """引数取得"""

    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
            description="周回報告個人概要生成\n"
            + "周回報告一覧ファイルを基に周回報告個人概要ファイルを生成します\n"
            + "任意で周回報告一覧ファイルを生成します",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループAの引数(全て必須な引数)
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            "Group A - all required arguments",
            "全て必須な引数",
        )
        help_ = "収集年(yyyy形式)"
        arg_group_a.add_argument(
            "col_year",
            help=help_,
        )
        help_ = "ユーザID"
        arg_group_a.add_argument(
            "user_id",
            help=help_,
        )

        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            "Group C - optional arguments",
            "任意の引数",
        )
        help_ = "周回報告一覧生成要否\n" + "指定した場合は一覧を生成します\n" + "指定しない場合は生成せずに既存の一覧のみを使用します"
        arg_group_c.add_argument(
            "-l",
            "--generate_list",
            help=help_,
            action="store_true",
        )

        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise (e)

    return args


def __validate_args(args: argparse.Namespace) -> bool:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 検証：収集年が年(yyyy形式)であること
        try:
            datetime.strptime(args.col_year, "%Y")
        except ValueError:
            clg.log_err(f"収集年が年(yyyy形式)ではありません。(col_year:{args.col_year})")
            return False

        # 検証：ユーザIDが4文字以上であること
        if not (len(args.user_id) >= 4):
            clg.log_err(f"ユーザIDが4文字以上ではありません。(user_id:{args.user_id})")
            return False
    except Exception as e:
        raise (e)

    return True


if __name__ == "__main__":
    sys.exit(main())
