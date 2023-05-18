import argparse
from typing import Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_gen_result_merge
from fgo_farm_report_collection.main import argument


def merge_farm_report_gen_result(arg_namespace: argparse.Namespace) -> None:
    """
    周回報告生成結果マージ

    Summary:
        引数を検証して問題ない場合、生成結果をExcelファイル(マージ結果ファイル)にマージする。

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
        arg: argument.FarmReportGenResultArg = argument.FarmReportGenResultArg(arg_namespace)
        __validate_arg(arg)

        # ロジック(周回報告生成結果マージ)の実行
        if bool(arg.merge_list) is True:
            farm_report_gen_result_merge.do_logic_that_merge_list(
                arg.append_sheet,
            )
        elif bool(arg.merge_yearly_user_total_summary) is True:
            farm_report_gen_result_merge.do_logic_that_merge_yearly_usr_tot_sum(
                arg.append_sheet,
            )
        elif bool(arg.merge_yearly_quest_total_summary) is True:
            farm_report_gen_result_merge.do_logic_that_merge_yearly_qst_tot_sum(
                arg.append_sheet,
            )
        elif bool(arg.merge_monthly_user_total_summary) is True:
            farm_report_gen_result_merge.do_logic_that_merge_monthly_usr_tot_sum(
                arg.append_sheet,
            )
        elif bool(arg.merge_monthly_quest_total_summary) is True:
            farm_report_gen_result_merge.do_logic_that_merge_monthly_qst_tot_sum(
                arg.append_sheet,
            )
        elif bool(arg.merge_individual_summary) is True:
            farm_report_gen_result_merge.do_logic_that_merge_ind_sum(
                arg.append_sheet,
            )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.FarmReportGenResultArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：なし
    except Exception as e:
        raise (e)

    return None
