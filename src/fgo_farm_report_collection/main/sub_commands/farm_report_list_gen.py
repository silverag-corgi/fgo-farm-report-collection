import argparse
from datetime import datetime
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen
from fgo_farm_report_collection.main import argument


def generate_farm_report_list(arg_namespace: argparse.Namespace) -> None:
    """
    周回報告一覧生成

    Summary:
        引数を検証して問題ない場合、周回報告一覧ファイルを生成する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.FarmReportListArg = argument.FarmReportListArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)

        # 引数の検証
        __validate_arg(arg)

        # ロジック(周回報告一覧生成)の実行
        if arg.col_year is not None:
            pyl.measure_proc_time(
                farm_report_list_gen.do_logic_that_generate_list_by_col_year,
            )(
                arg.use_debug_mode,
                arg.col_year,
            )
        elif arg.col_year_month is not None:
            pyl.measure_proc_time(
                farm_report_list_gen.do_logic_that_generate_list_by_col_year_month,
            )(
                arg.use_debug_mode,
                arg.col_year_month,
            )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.FarmReportListArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：収集年が年(yyyy形式)であるか、もしくは収集年月が年月(yyyy-mm形式)であること
        if arg.col_year is not None:
            try:
                datetime.strptime(arg.col_year, "%Y")
            except ValueError as e:
                raise pyl.ArgumentValidationError(f"収集年が年(yyyy形式)ではありません。(col_year:{arg.col_year})")
        elif arg.col_year_month is not None:
            try:
                datetime.strptime(arg.col_year_month, "%Y-%m")
            except ValueError as e:
                raise pyl.ArgumentValidationError(
                    f"収集年月が年月(yyyy-mm形式)ではありません。(col_year_month:{arg.col_year_month})"
                )
    except Exception as e:
        raise (e)

    return None
