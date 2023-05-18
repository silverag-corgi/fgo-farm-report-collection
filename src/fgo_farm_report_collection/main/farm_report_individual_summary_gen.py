import argparse
from datetime import datetime
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_individual_summary_gen
from fgo_farm_report_collection.main import argument


def generate_farm_report_individual_summary(arg_namespace: argparse.Namespace) -> None:
    """
    周回報告個人概要生成

    Summary:
        引数を検証して問題ない場合、周回報告一覧ファイルを基に周回報告個人概要ファイルを生成する。

        また、事前に任意で周回報告一覧ファイルを生成する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数の検証
        arg: argument.FarmReportIndividualSummaryArg = argument.FarmReportIndividualSummaryArg(
            arg_namespace
        )
        __validate_arg(arg)

        # ロジック(周回報告個人概要生成)の実行
        pyl.measure_proc_time(
            farm_report_individual_summary_gen.do_logic,
        )(
            arg.col_year,
            arg.user_id,
            arg.generate_list,
        )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.FarmReportIndividualSummaryArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：収集年が年(yyyy形式)であること
        try:
            datetime.strptime(arg.col_year, "%Y")
        except ValueError:
            raise pyl.ArgumentValidationError(f"収集年が年(yyyy形式)ではありません。(col_year:{arg.col_year})")

        # 検証：ユーザIDが4文字以上であること
        if not (len(arg.user_id) >= 4):
            raise pyl.ArgumentValidationError(f"ユーザIDが4文字以上ではありません。(user_id:{arg.user_id})")
    except Exception as e:
        raise (e)

    return None
