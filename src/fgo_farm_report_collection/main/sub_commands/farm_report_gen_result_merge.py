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
        # 引数の取得
        arg: argument.FarmReportGenResultArg = argument.FarmReportGenResultArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"周回報告生成結果マージを開始します。")

        # ロジック(周回報告生成結果マージ)の実行
        if arg.merge_list is True:
            farm_report_gen_result_merge.do_logic_that_merge_list(
                arg.use_debug_mode,
                arg.append_sheet,
            )
        elif arg.merge_yearly_user_total_summary is True:
            farm_report_gen_result_merge.do_logic_that_merge_yearly_usr_tot_sum(
                arg.use_debug_mode,
                arg.append_sheet,
            )
        elif arg.merge_yearly_quest_total_summary is True:
            farm_report_gen_result_merge.do_logic_that_merge_yearly_qst_tot_sum(
                arg.use_debug_mode,
                arg.append_sheet,
            )
        elif arg.merge_monthly_user_total_summary is True:
            farm_report_gen_result_merge.do_logic_that_merge_monthly_usr_tot_sum(
                arg.use_debug_mode,
                arg.append_sheet,
            )
        elif arg.merge_monthly_quest_total_summary is True:
            farm_report_gen_result_merge.do_logic_that_merge_monthly_qst_tot_sum(
                arg.use_debug_mode,
                arg.append_sheet,
            )
        elif arg.merge_individual_summary is True:
            farm_report_gen_result_merge.do_logic_that_merge_ind_sum(
                arg.use_debug_mode,
                arg.append_sheet,
            )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"周回報告生成結果マージを終了します。")

    return None
