import argparse
from datetime import datetime
from typing import Callable, Optional

import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen, farm_report_total_summary_gen
from fgo_farm_report_collection.main import argument
from fgo_farm_report_collection.util import const_util


def generate_farm_report_total_summary(arg_namespace: argparse.Namespace) -> None:
    """
    周回報告全体概要生成

    Summary:
        引数を検証して問題ない場合、周回報告一覧ファイルを基に周回報告全体概要ファイルを生成する。

        また、事前に任意で周回報告一覧ファイルを生成する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.FarmReportTotalSummaryArg = argument.FarmReportTotalSummaryArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"周回報告全体概要生成を開始します。")

        # 引数の検証
        __validate_arg(arg)

        # ロジック(周回報告一覧生成)の実行
        if arg.generate_list is True:
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

        # 関数オブジェクトの取得
        function_object: Optional[Callable] = None
        if arg.col_year is not None:
            if (
                arg.generate_yearly_user_total_summary is True
                or arg.generate_yearly_quest_total_summary is True
            ):
                function_object = (
                    farm_report_total_summary_gen
                ).do_logic_that_generate_yearly_tot_sum_by_col_year
            elif (
                arg.generate_monthly_user_total_summary is True
                or arg.generate_monthly_quest_total_summary is True
            ):
                function_object = (
                    farm_report_total_summary_gen
                ).do_logic_that_generate_monthly_tot_sum_by_col_year
        elif arg.col_year_month is not None:
            if (
                arg.generate_monthly_user_total_summary is True
                or arg.generate_monthly_quest_total_summary is True
            ):
                function_object = (
                    farm_report_total_summary_gen
                ).do_logic_that_generate_monthly_tot_sum_by_col_year_month

        # ロジック(周回報告全体概要生成)の実行
        if function_object is not None:
            pyl.measure_proc_time(function_object)(
                (arg.use_debug_mode),
                (arg.col_year if arg.col_year is not None else arg.col_year_month),
                (
                    (farm_report_total_summary_gen).EnumOfProc.GENERATE_YEARLY_USER_TOTAL_SUMMARY
                    if arg.generate_yearly_user_total_summary is True
                    else (
                        farm_report_total_summary_gen
                    ).EnumOfProc.GENERATE_YEARLY_QUEST_TOTAL_SUMMARY
                    if arg.generate_yearly_quest_total_summary is True
                    else (
                        farm_report_total_summary_gen
                    ).EnumOfProc.GENERATE_MONTHLY_USER_TOTAL_SUMMARY
                    if arg.generate_monthly_user_total_summary is True
                    else (
                        farm_report_total_summary_gen
                    ).EnumOfProc.GENERATE_MONTHLY_QUEST_TOTAL_SUMMARY
                ),
                (
                    arg.min_num_of_all_quest
                    if arg.min_num_of_all_quest is not None
                    else arg.min_num_of_normal_quest
                    if arg.min_num_of_normal_quest is not None
                    else arg.min_num_of_event_quest
                    if arg.min_num_of_event_quest is not None
                    else arg.min_num_of_quest_by_batch
                ),
                (
                    [const_util.QUEST_KINDS[0]]
                    if arg.min_num_of_all_quest is not None
                    else [const_util.QUEST_KINDS[1]]
                    if arg.min_num_of_normal_quest is not None
                    else [const_util.QUEST_KINDS[2]]
                    if arg.min_num_of_event_quest is not None
                    else const_util.QUEST_KINDS
                ),
                (arg.output_user_name),
            )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"周回報告全体概要生成を終了します。")

    return None


def __validate_arg(arg: argument.FarmReportTotalSummaryArg) -> None:
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
            except ValueError:
                raise pyl.ArgumentValidationError(f"収集年が年(yyyy形式)ではありません。(col_year:{arg.col_year})")
        elif arg.col_year_month is not None:
            try:
                datetime.strptime(arg.col_year_month, "%Y-%m")
            except ValueError:
                raise pyl.ArgumentValidationError(
                    f"収集年月が年月(yyyy-mm形式)ではありません。(col_year_month:{arg.col_year_month})"
                )

        # 検証：周回報告年間ユーザ全体概要生成要否、もしくは、周回報告年間クエスト全体概要生成要否が真の場合は、
        # 収集年が指定されていること
        if (
            arg.generate_yearly_user_total_summary is True
            or arg.generate_yearly_quest_total_summary is True
        ) and arg.col_year is None:
            raise pyl.ArgumentValidationError(
                f"収集年が指定されていません。(col_year:{arg.col_year}, col_year_month:{arg.col_year_month})"
            )

        # 検証：最低周回数のいずれかが0以上であること
        if arg.min_num_of_all_quest is not None and not (arg.min_num_of_all_quest >= 0):
            raise pyl.ArgumentValidationError(
                f"最低周回数(全て)が0以上ではありません。(min_num_of_all_quest:{arg.min_num_of_all_quest})"
            )
        elif arg.min_num_of_normal_quest is not None and not (arg.min_num_of_normal_quest >= 0):
            raise pyl.ArgumentValidationError(
                f"最低周回数(通常クエ)が0以上ではありません。(min_num_of_normal_quest:{arg.min_num_of_normal_quest})"
            )
        elif arg.min_num_of_event_quest is not None and not (arg.min_num_of_event_quest >= 0):
            raise pyl.ArgumentValidationError(
                f"最低周回数(イベクエ)が0以上ではありません。(min_num_of_event_quest:{arg.min_num_of_event_quest})"
            )
    except Exception as e:
        raise (e)

    return None
