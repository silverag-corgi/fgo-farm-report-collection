import argparse
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
        # 引数の取得
        arg: argument.FarmReportIndividualSummaryArg = argument.FarmReportIndividualSummaryArg(
            arg_namespace
        )

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"周回報告個人概要生成を開始します。")

        # ロジック(周回報告個人概要生成)の実行
        pyl.measure_proc_time(
            farm_report_individual_summary_gen.do_logic_that_generate_ind_sum,
        )(
            arg.col_year,
            arg.user_id,
            generate_list=arg.generate_list,
            use_debug_mode=arg.use_debug_mode,
        )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"周回報告個人概要生成を終了します。")

    return None
