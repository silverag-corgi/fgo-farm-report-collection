import os
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl

from fgo_farm_report_collection.logic import farm_report_list_gen
from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_that_generate_ind_sum(
    use_debug_mode: bool,
    col_year: str,
    user_id: str,
    generate_list: bool,
) -> None:
    """ロジック(周回報告個人概要生成)実行"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)
        clg.log_inf(f"ロジック(周回報告個人概要生成)実行を開始します。")

        # Pandasオプション設定
        pd.set_option("display.unicode.east_asian_width", True)

        # 周回報告個人概要データフレームの初期化
        farm_report_ind_sum_df: pd.DataFrame = pd.DataFrame(
            index=range(const_util.NUM_OF_MONTHS), columns=const_util.FARM_REPORT_IND_SUM_HEADER
        )
        farm_report_ind_sum_df.fillna(0, inplace=True)

        # 指定したユーザの周回数の集計
        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f"{col_year:04}-{(index+1):02}"

            # 周回報告一覧ファイルパスの生成
            farm_report_list_file_path: str = const_util.FARM_REPORT_LIST_FILE_PATH.format(
                col_year_month
            )

            # 周回報告個人概要更新の判定
            update_ind_sum: bool = True
            if generate_list is True:
                # ロジック(周回報告一覧生成)の実行
                pyl.measure_proc_time(
                    farm_report_list_gen.do_logic_that_generate_list_by_col_year_month,
                )(
                    col_year_month,
                )

                # 周回報告一覧ファイルの存在有無チェック
                if os.path.isfile(farm_report_list_file_path) is False:
                    update_ind_sum = False
            else:
                if os.path.isfile(farm_report_list_file_path) is False:
                    update_ind_sum = False

            # 周回報告個人概要データフレームの更新
            farm_report_ind_sum_df.at[
                index, const_util.FARM_REPORT_IND_SUM_HEADER[0]
            ] = col_year_month
            if update_ind_sum is True:
                __update_farm_report_ind_sum_df(
                    use_debug_mode,
                    farm_report_list_file_path,
                    user_id,
                    farm_report_ind_sum_df,
                    index,
                )

        # 周回報告個人概要ファイルパスの生成
        farm_report_ind_sum_file_path: str = const_util.FARM_REPORT_IND_SUM_FILE_PATH.format(
            col_year, user_id
        )

        # 周回報告個人概要データフレームの保存
        pandas_util.save_farm_report_ind_sum_df(
            use_debug_mode, farm_report_ind_sum_df, farm_report_ind_sum_file_path
        )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"ロジック(周回報告個人概要生成)実行を終了します。")

    return None


def __update_farm_report_ind_sum_df(
    use_debug_mode: bool,
    farm_report_list_file_path: str,
    user_id: str,
    farm_report_ind_sum_df: pd.DataFrame,
    index: int,
) -> None:
    """周回報告個人概要データフレーム更新"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)

        # 周回報告一覧データフレームの取得(周回報告一覧ファイルの読み込み)
        farm_report_list_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
            use_debug_mode, farm_report_list_file_path
        )

        # ユーザID、クエスト種別による抽出
        user_id = f"{user_id: <15}"
        df_by_user_id: pd.DataFrame = farm_report_list_df.query(
            f"{const_util.FARM_REPORT_LIST_HEADER[1]}.str.match('^{user_id}$')"
        )
        df_by_user_id_and_normal_quest: pd.DataFrame = df_by_user_id.query(
            f"{const_util.FARM_REPORT_LIST_HEADER[2]}.str.match('{const_util.QUEST_KINDS[1]}')"
        )
        df_by_user_id_and_event_quest: pd.DataFrame = df_by_user_id.query(
            f"{const_util.FARM_REPORT_LIST_HEADER[2]}.str.match('{const_util.QUEST_KINDS[2]}')"
        )

        # 周回数の更新
        farm_report_ind_sum_df.at[
            index, const_util.FARM_REPORT_IND_SUM_HEADER[1]
        ] = df_by_user_id_and_normal_quest[const_util.FARM_REPORT_LIST_HEADER[5]].sum()
        farm_report_ind_sum_df.at[
            index, const_util.FARM_REPORT_IND_SUM_HEADER[2]
        ] = df_by_user_id_and_event_quest[const_util.FARM_REPORT_LIST_HEADER[5]].sum()
        farm_report_ind_sum_df.at[index, const_util.FARM_REPORT_IND_SUM_HEADER[3]] = df_by_user_id[
            const_util.FARM_REPORT_LIST_HEADER[5]
        ].sum()
    except Exception as e:
        raise (e)

    return None
