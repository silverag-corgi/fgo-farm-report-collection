import json
import os
from datetime import date, datetime, timedelta
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import requests
from requests import Response

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_that_generate_list_by_col_year(
    use_debug_mode: bool,
    col_year: str,
) -> None:
    """ロジック(周回報告一覧生成(年指定))実行"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)
        clg.log_inf(f"周回報告一覧生成(年指定)を開始します。")

        for index in range(const_util.NUM_OF_MONTHS):
            # 収集年月の生成
            col_year_month: str = f"{col_year:04}-{(index+1):02}"

            # 周回報告一覧生成ロジックの実行
            do_logic_that_generate_list_by_col_year_month(use_debug_mode, col_year_month)
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"周回報告一覧生成(年指定)を終了します。")

    return None


def do_logic_that_generate_list_by_col_year_month(
    use_debug_mode: bool,
    col_year_month: str,
) -> None:
    """ロジック(周回報告一覧生成(年月指定))実行"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)
        clg.log_inf(f"周回報告一覧生成(年月指定)を開始します。")

        # Pandasオプション設定
        pd.set_option("display.unicode.east_asian_width", True)

        # 収集年月が未来の場合
        today: date = datetime.today().date()
        col_first_date: date = datetime.strptime(col_year_month + "-01", "%Y-%m-%d").date()
        first_date_of_this_month: date = pyl.get_first_date_of_this_month(today)
        if col_first_date > first_date_of_this_month:
            clg.log_inf(f"収集年月が未来です。(col_year_month:{col_year_month})")
        else:
            # 周回報告一覧ファイルパスの生成
            farm_report_list_file_path: str = const_util.FARM_REPORT_LIST_FILE_PATH.format(
                col_year_month
            )

            # 周回報告一覧ファイルの存在有無チェック
            has_farm_report_list: bool = os.path.isfile(farm_report_list_file_path)

            # 周回報告一覧生成開始日付の設定
            list_gen_start_date: Optional[date] = __generate_list_gen_start_date(
                use_debug_mode, has_farm_report_list, farm_report_list_file_path, col_first_date
            )

            # 周回報告一覧生成終了日付の設定
            list_gen_end_date: Optional[date] = __generate_list_gen_end_date(
                use_debug_mode, list_gen_start_date, col_first_date, first_date_of_this_month, today
            )

            # 周回報告一覧生成要否の判定
            generate_list: bool = True
            if list_gen_start_date is None or list_gen_end_date is None:
                generate_list = False
                clg.log_inf(f"周回報告一覧は最新です。(col_year_month:{col_year_month})")
            else:
                if list_gen_start_date > list_gen_end_date:
                    generate_list = False
                    clg.log_inf(f"周回報告一覧は最新です。(col_year_month:{col_year_month})")
                else:
                    generate_list = True
                    clg.log_inf(
                        f"周回報告一覧を生成します。(col_year_month:{list_gen_start_date}～{list_gen_end_date})"
                    )

            # 周回報告一覧ファイルの生成
            if generate_list is True:
                __generate_farm_report_list_file(
                    use_debug_mode,
                    list_gen_start_date,
                    list_gen_end_date,
                    farm_report_list_file_path,
                    has_farm_report_list,
                )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"周回報告一覧生成(年月指定)を終了します。")

    return None


def __generate_list_gen_start_date(
    use_debug_mode: bool,
    has_farm_report_list: bool,
    farm_report_list_file_path: str,
    col_first_date: date,
) -> Optional[date]:
    """周回報告一覧生成開始日付生成"""

    try:
        list_gen_start_date: Optional[date] = None
        if has_farm_report_list is True:
            farm_report_list_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
                use_debug_mode, farm_report_list_file_path
            )

            post_datetime_of_last_line_timestamp: pd.Timestamp = (
                farm_report_list_df[const_util.FARM_REPORT_LIST_HEADER[0]].tail(1).item()
            )
            post_datetime_of_last_line_date: date = pd.to_datetime(
                post_datetime_of_last_line_timestamp
            ).date()

            if post_datetime_of_last_line_date != pyl.get_last_date_of_this_month(
                post_datetime_of_last_line_date
            ):
                list_gen_start_date = post_datetime_of_last_line_date + timedelta(days=1)
            else:
                list_gen_start_date = None
        else:
            list_gen_start_date = col_first_date
    except Exception as e:
        raise (e)

    return list_gen_start_date


def __generate_list_gen_end_date(
    use_debug_mode: bool,
    list_gen_start_date: Optional[date],
    col_first_date: date,
    first_date_of_this_month: date,
    today: date,
) -> Optional[date]:
    """周回報告一覧生成終了日付生成"""

    try:
        list_gen_end_date: Optional[date] = None
        if list_gen_start_date is not None and col_first_date == first_date_of_this_month:
            list_gen_end_date = today + timedelta(days=-1)
        elif list_gen_start_date is not None and col_first_date != first_date_of_this_month:
            list_gen_end_date = pyl.get_last_date_of_this_month(list_gen_start_date)
    except Exception as e:
        raise (e)

    return list_gen_end_date


def __generate_farm_report_list_file(
    use_debug_mode: bool,
    list_gen_start_date: Optional[date],
    list_gen_end_date: Optional[date],
    farm_report_list_file_path: str,
    has_farm_report_list: bool,
) -> None:
    """周回報告一覧ファイル生成"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)

        # 周回報告一覧データフレームの初期化
        farm_report_list_df: pd.DataFrame = pd.DataFrame(columns=const_util.FARM_REPORT_LIST_HEADER)

        # 周回報告一覧データフレームへの格納
        if list_gen_start_date is not None and list_gen_end_date is not None:
            list_gen_date: Optional[date] = None
            for list_gen_date in pyl.gen_date_range(list_gen_start_date, list_gen_end_date):
                # 周回報告サイトURLの生成
                farm_report_site_url: str = const_util.FARM_REPORT_SITE_URL.format(list_gen_date)
                clg.log_inf(f"周回報告サイトURL：{farm_report_site_url}")

                # 周回報告サイトからの周回報告の取得
                farm_report_site_response: Response = requests.get(farm_report_site_url)
                if farm_report_site_response.status_code != requests.codes["ok"]:
                    clg.log_wrn(
                        f"周回報告サイトへのアクセスに失敗しました。"
                        + f"(farm_report_site_url:{farm_report_site_url}, "
                        + f"status_code:{farm_report_site_response.status_code})"
                    )
                    continue
                farm_reports: dict[Any, Any] = json.loads(farm_report_site_response.text)

                # 周回報告データフレームの格納
                for farm_report in farm_reports:
                    farm_report_df = pd.DataFrame(
                        [
                            [
                                pyl.convert_timestamp_to_jst(
                                    farm_report["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
                                ),
                                f"{farm_report['reporter']: <15}",
                                (
                                    const_util.QUEST_KINDS[1]
                                    if bool(farm_report["freequest"]) is True
                                    else const_util.QUEST_KINDS[2]
                                ),
                                farm_report["chapter"],
                                farm_report["place"],
                                farm_report["runcount"],
                                ", ".join(
                                    [
                                        "{0}: {1}".format(key, value)
                                        for key, value in farm_report["items"].items()
                                    ]
                                ),
                            ]
                        ],
                        columns=const_util.FARM_REPORT_LIST_HEADER,
                    )
                    farm_report_list_df = pd.concat(
                        [farm_report_list_df, farm_report_df], ignore_index=True
                    )

            # 投稿日による昇順ソート
            farm_report_list_df.sort_values(
                const_util.FARM_REPORT_LIST_HEADER[0], ascending=True, inplace=True
            )

        # 周回報告一覧データフレームの保存
        if len(farm_report_list_df) > 0:
            pandas_util.save_farm_report_list_df(
                use_debug_mode,
                farm_report_list_df,
                farm_report_list_file_path,
                has_farm_report_list,
            )
    except Exception as e:
        raise (e)

    return None
