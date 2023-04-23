import os
from datetime import date, datetime
from enum import IntEnum, auto
from logging import Logger
from typing import Optional

import numpy as np
import pandas as pd
import python_lib_for_me as pyl
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pandas.core.groupby.generic import DataFrameGroupBy
from requests.models import Response

from fgo_farm_report_collection.util import const_util, pandas_util


class EnumOfProc(IntEnum):
    GENERATE_YEARLY_USER_TOTAL_SUMMARY = auto()
    GENERATE_YEARLY_QUEST_TOTAL_SUMMARY = auto()
    GENERATE_MONTHLY_USER_TOTAL_SUMMARY = auto()
    GENERATE_MONTHLY_QUEST_TOTAL_SUMMARY = auto()


def do_logic_that_generate_yearly_tot_sum_by_col_year(
    col_year: str,
    enum_of_proc: EnumOfProc,
    min_num_of_farms: int,
    quest_kinds: list[str],
    output_user_name: bool = False,
) -> None:
    """ロジック(周回報告年間全体概要生成(年指定))実行"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"周回報告年間全体概要生成(年指定)を開始します。")

        # 収集年月の生成
        col_year_months: list[str] = [
            f"{col_year:04}-{(index+1):02}" for index in range(const_util.NUM_OF_MONTHS)
        ]

        # ロジック(周回報告全体概要生成(共通))の実行
        __do_logic_that_generate_tot_sum(
            col_year, col_year_months, enum_of_proc, min_num_of_farms, quest_kinds, output_user_name
        )
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"周回報告年間全体概要生成(年指定)を終了します。")

    return None


def do_logic_that_generate_monthly_tot_sum_by_col_year(
    col_year: str,
    enum_of_proc: EnumOfProc,
    min_num_of_farms: int,
    quest_kinds: list[str],
    output_user_name: bool = False,
) -> None:
    """ロジック(周回報告月間全体概要生成(年指定))実行"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"周回報告月間全体概要生成(年指定)を開始します。")

        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f"{col_year:04}-{(index+1):02}"

            # ロジック(周回報告全体概要生成(共通))の実行
            __do_logic_that_generate_tot_sum(
                col_year_month,
                [col_year_month],
                enum_of_proc,
                min_num_of_farms,
                quest_kinds,
                output_user_name,
            )
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"周回報告月間全体概要生成(年指定)を終了します。")

    return None


def do_logic_that_generate_monthly_tot_sum_by_col_year_month(
    col_year_month: str,
    enum_of_proc: EnumOfProc,
    min_num_of_farms: int,
    quest_kinds: list[str],
    output_user_name: bool = False,
) -> None:
    """ロジック(周回報告月間全体概要生成(年月指定))実行"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"周回報告月間全体概要生成(年月指定)を開始します。")

        # ロジック(周回報告全体概要生成(共通))の実行
        __do_logic_that_generate_tot_sum(
            col_year_month,
            [col_year_month],
            enum_of_proc,
            min_num_of_farms,
            quest_kinds,
            output_user_name,
        )
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"周回報告月間全体概要生成(年月指定)を終了します。")

    return None


def __do_logic_that_generate_tot_sum(
    col_year_month_for_file_path: str,
    col_year_months: list[str],
    enum_of_proc: EnumOfProc,
    min_num_of_farms: int,
    quest_kinds: list[str],
    output_user_name: bool = False,
) -> None:
    """ロジック(周回報告全体概要生成(共通))実行"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"周回報告全体概要生成(共通)を開始します。")

        # Pandasオプション設定
        pd.set_option("display.unicode.east_asian_width", True)

        # 周回報告一覧ファイルパス(複数)の生成
        farm_report_list_file_paths: list[str] = []
        for col_year_month in col_year_months:
            # 初日(収集年月、今月)の取得
            first_date_of_col_year_month: date = datetime.strptime(
                col_year_month + "-01", "%Y-%m-%d"
            ).date()
            today: date = datetime.today().date()
            first_date_of_this_month: date = pyl.get_first_date_of_this_month(today)

            # 周回報告一覧ファイルパスの追加
            if first_date_of_col_year_month > first_date_of_this_month:
                pyl.log_inf(lg, f"収集年月が未来です。(col_year_month:{col_year_month})")
            else:
                farm_report_list_file_path: str = const_util.FARM_REPORT_LIST_FILE_PATH.format(
                    col_year_month
                )
                farm_report_list_file_paths.append(farm_report_list_file_path)

        for quest_kind in quest_kinds:
            # 周回報告全体概要ファイルパスの生成
            farm_report_tot_sum_file_path: str = ""
            if enum_of_proc == EnumOfProc.GENERATE_YEARLY_USER_TOTAL_SUMMARY:
                farm_report_tot_sum_file_path = (
                    const_util.FARM_REPORT_YEARLY_USR_TOT_SUM_FILE_PATH.format(
                        col_year_month_for_file_path, quest_kind, min_num_of_farms
                    )
                )
            elif enum_of_proc == EnumOfProc.GENERATE_YEARLY_QUEST_TOTAL_SUMMARY:
                farm_report_tot_sum_file_path = (
                    const_util.FARM_REPORT_YEARLY_QST_TOT_SUM_FILE_PATH.format(
                        col_year_month_for_file_path, quest_kind, min_num_of_farms
                    )
                )
            elif enum_of_proc == EnumOfProc.GENERATE_MONTHLY_USER_TOTAL_SUMMARY:
                farm_report_tot_sum_file_path = (
                    const_util.FARM_REPORT_MONTHLY_USR_TOT_SUM_FILE_PATH.format(
                        col_year_month_for_file_path, quest_kind, min_num_of_farms
                    )
                )
            elif enum_of_proc == EnumOfProc.GENERATE_MONTHLY_QUEST_TOTAL_SUMMARY:
                farm_report_tot_sum_file_path = (
                    const_util.FARM_REPORT_MONTHLY_QST_TOT_SUM_FILE_PATH.format(
                        col_year_month_for_file_path, quest_kind, min_num_of_farms
                    )
                )

            # 周回報告全体概要ファイルの生成
            if enum_of_proc == EnumOfProc.GENERATE_YEARLY_USER_TOTAL_SUMMARY:
                __generate_farm_report_usr_tot_sum_file(
                    farm_report_list_file_paths,
                    quest_kind,
                    min_num_of_farms,
                    farm_report_tot_sum_file_path,
                    output_user_name,
                )
            elif enum_of_proc == EnumOfProc.GENERATE_YEARLY_QUEST_TOTAL_SUMMARY:
                __generate_farm_report_qst_tot_sum_file(
                    farm_report_list_file_paths,
                    quest_kind,
                    min_num_of_farms,
                    farm_report_tot_sum_file_path,
                )
            elif enum_of_proc == EnumOfProc.GENERATE_MONTHLY_USER_TOTAL_SUMMARY:
                __generate_farm_report_usr_tot_sum_file(
                    farm_report_list_file_paths,
                    quest_kind,
                    min_num_of_farms,
                    farm_report_tot_sum_file_path,
                    output_user_name,
                )
            elif enum_of_proc == EnumOfProc.GENERATE_MONTHLY_QUEST_TOTAL_SUMMARY:
                __generate_farm_report_qst_tot_sum_file(
                    farm_report_list_file_paths,
                    quest_kind,
                    min_num_of_farms,
                    farm_report_tot_sum_file_path,
                )
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"周回報告全体概要生成(共通)を終了します。")

    return None


def __generate_farm_report_usr_tot_sum_file(
    farm_report_list_file_paths: list[str],
    quest_kind: str,
    min_num_of_farms: int,
    farm_report_tot_sum_file_path: str,
    output_user_name: bool,
) -> None:
    """周回報告ユーザ全体概要ファイル生成"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)

        # 周回報告一覧データフレームの取得(周回報告一覧ファイルの読み込み)
        farm_report_list_df: pd.DataFrame = pd.DataFrame()
        for farm_report_list_file_path in farm_report_list_file_paths:
            if os.path.isfile(farm_report_list_file_path) is False:
                pyl.log_inf(
                    lg,
                    f"周回報告一覧ファイルが存在しません。(farm_report_list_file_path:{farm_report_list_file_path})",
                )
            else:
                farm_report_list_temp_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
                    farm_report_list_file_path
                )
                farm_report_list_df = pd.concat(
                    [farm_report_list_df, farm_report_list_temp_df], ignore_index=True
                )

        if len(farm_report_list_df) > 0 and quest_kind in const_util.QUEST_KINDS:
            # クエスト種別による抽出
            farm_report_list_df_by_quest_kind: pd.DataFrame
            if quest_kind in const_util.QUEST_KINDS[1:3]:
                farm_report_list_df_by_quest_kind = farm_report_list_df.query(
                    f"{const_util.FARM_REPORT_LIST_HEADER[2]}.str.match('{quest_kind}')"
                )
            else:
                farm_report_list_df_by_quest_kind = farm_report_list_df

            # 投稿者によるグループ化
            farm_report_list_df_group: DataFrameGroupBy = farm_report_list_df_by_quest_kind.groupby(
                const_util.FARM_REPORT_LIST_HEADER[1]
            )

            # 周回数と報告数の集計
            # TODO 変数`farm_report_tot_sum_series`の型を`pd.Series`から`pd.DataFrame`に変更する
            farm_report_tot_sum_series: pd.Series = farm_report_list_df_group[
                const_util.FARM_REPORT_LIST_HEADER[5]
            ].aggregate([np.sum, np.count_nonzero, min, max, np.median, np.mean, np.std])
            farm_report_tot_sum_df: pd.DataFrame = pd.DataFrame(farm_report_tot_sum_series).rename(
                columns={
                    "sum": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[2],
                    "count_nonzero": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[3],
                    "min": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[4],
                    "max": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[5],
                    "median": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[6],
                    "mean": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[7],
                    "std": const_util.FARM_REPORT_USR_TOT_SUM_HEADER[8],
                }
            )
            farm_report_tot_sum_df.fillna(0, inplace=True)

            # 周回数による降順ソート
            farm_report_tot_sum_df.sort_values(
                const_util.FARM_REPORT_USR_TOT_SUM_HEADER[2], ascending=False, inplace=True
            )

            # 周回数による抽出
            farm_report_tot_sum_df.query(
                f"{const_util.FARM_REPORT_USR_TOT_SUM_HEADER[2]} >= {min_num_of_farms}",
                inplace=True,
            )

            # 周回数の揃え
            # TODO 引数`func`を`cast(Any, pyl.round_half_up(data, 2))`に変更する
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_USR_TOT_SUM_HEADER[6]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_USR_TOT_SUM_HEADER[6]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_USR_TOT_SUM_HEADER[7]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_USR_TOT_SUM_HEADER[7]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_USR_TOT_SUM_HEADER[8]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_USR_TOT_SUM_HEADER[8]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )

            # 列(ユーザ名)の追加
            farm_report_tot_sum_df.insert(0, const_util.FARM_REPORT_USR_TOT_SUM_HEADER[1], "-")

            # ユーザ名の設定
            if output_user_name is True:
                pyl.log_inf(lg, f"時間がかかるため気長にお待ちください。")
                for user_id, _ in farm_report_tot_sum_df.iterrows():
                    try:
                        user_info_site_url: str = const_util.USER_INFO_SITE_URL.format(
                            str(user_id).strip()
                        )
                        user_info_site_response: Response = requests.get(user_info_site_url)
                        # TODO 引数`markup`を`cast(str, user_info_site_response.content)`に変更する
                        user_info_site_bs: BeautifulSoup = BeautifulSoup(
                            user_info_site_response.content,
                            "lxml",
                            from_encoding=const_util.ENCODING,
                        )
                        user_name_rs: ResultSet = user_info_site_bs.find_all(class_="name")
                        farm_report_tot_sum_df.at[
                            user_id, const_util.FARM_REPORT_USR_TOT_SUM_HEADER[1]
                        ] = user_name_rs[0].get_text()
                        pyl.log_deb(lg, f"ユーザ名の設定に成功しました。(user_id:{user_id})")
                    except Exception as e:
                        pyl.log_war(
                            lg,
                            f"ユーザ名の設定に失敗しました。アカウントが削除されている可能性があります。(user_id:{user_id})",
                        )

            # 周回報告ユーザ全体概要データフレームの保存
            pandas_util.save_farm_report_usr_tot_sum_df(
                farm_report_tot_sum_df, farm_report_tot_sum_file_path
            )
    except Exception as e:
        raise (e)

    return None


def __generate_farm_report_qst_tot_sum_file(
    farm_report_list_file_paths: list[str],
    quest_kind: str,
    min_num_of_farms: int,
    farm_report_tot_sum_file_path: str,
) -> None:
    """周回報告クエスト全体概要ファイル生成"""

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)

        # 周回報告一覧データフレームの取得(周回報告一覧ファイルの読み込み)
        farm_report_list_df: pd.DataFrame = pd.DataFrame()
        for farm_report_list_file_path in farm_report_list_file_paths:
            # 周回報告一覧ファイルの存在確認
            if os.path.isfile(farm_report_list_file_path) is False:
                pyl.log_inf(
                    lg,
                    f"周回報告一覧ファイルが存在しません。"
                    + f"(farm_report_list_file_path:{farm_report_list_file_path})",
                )
            else:
                farm_report_list_temp_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
                    farm_report_list_file_path
                )
                farm_report_list_df = pd.concat(
                    [farm_report_list_df, farm_report_list_temp_df], ignore_index=True
                )

        if len(farm_report_list_df) > 0 and quest_kind in const_util.QUEST_KINDS:
            # クエスト種別による抽出
            farm_report_list_df_by_quest_kind: pd.DataFrame
            if quest_kind in const_util.QUEST_KINDS[1:3]:
                farm_report_list_df_by_quest_kind = farm_report_list_df.query(
                    f"{const_util.FARM_REPORT_LIST_HEADER[2]}.str.match('{quest_kind}')"
                )
            else:
                farm_report_list_df_by_quest_kind = farm_report_list_df

            # 章名と座標名によるグループ化
            farm_report_list_df_group: DataFrameGroupBy = farm_report_list_df_by_quest_kind.groupby(
                [const_util.FARM_REPORT_LIST_HEADER[3], const_util.FARM_REPORT_LIST_HEADER[4]]
            )

            # 周回数と報告数の集計
            # TODO 変数`farm_report_tot_sum_series`の型を`pd.Series`から`pd.DataFrame`に変更する
            farm_report_tot_sum_series: pd.Series = farm_report_list_df_group[
                const_util.FARM_REPORT_LIST_HEADER[5]
            ].aggregate([np.sum, np.count_nonzero, min, max, np.median, np.mean, np.std])
            farm_report_tot_sum_df: pd.DataFrame = pd.DataFrame(farm_report_tot_sum_series).rename(
                columns={
                    "sum": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[2],
                    "count_nonzero": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[3],
                    "min": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[4],
                    "max": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[5],
                    "median": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[6],
                    "mean": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[7],
                    "std": const_util.FARM_REPORT_QST_TOT_SUM_HEADER[8],
                }
            )
            farm_report_tot_sum_df.fillna(0, inplace=True)

            # 周回数による降順ソート
            farm_report_tot_sum_df.sort_values(
                const_util.FARM_REPORT_QST_TOT_SUM_HEADER[2], ascending=False, inplace=True
            )

            # 周回数による抽出
            farm_report_tot_sum_df.query(
                f"{const_util.FARM_REPORT_QST_TOT_SUM_HEADER[2]} >= {min_num_of_farms}",
                inplace=True,
            )

            # 周回数の揃え
            # TODO 引数`func`を`cast(Any, pyl.round_half_up(data, 2))`に変更する
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_QST_TOT_SUM_HEADER[6]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_QST_TOT_SUM_HEADER[6]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_QST_TOT_SUM_HEADER[7]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_QST_TOT_SUM_HEADER[7]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )
            farm_report_tot_sum_df[
                const_util.FARM_REPORT_QST_TOT_SUM_HEADER[8]
            ] = farm_report_tot_sum_df[const_util.FARM_REPORT_QST_TOT_SUM_HEADER[8]].apply(
                lambda data: pyl.round_half_up(data, 2)
            )

            # 周回報告クエスト全体概要データフレームの保存
            pandas_util.save_farm_report_qst_tot_sum_df(
                farm_report_tot_sum_df, farm_report_tot_sum_file_path
            )
    except Exception as e:
        raise (e)

    return None
