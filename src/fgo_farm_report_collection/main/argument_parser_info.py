import argparse
import textwrap
from typing import Final

from fgo_farm_report_collection.main.sub_commands import (
    farm_report_gen_result_merge,
    farm_report_individual_summary_gen,
    farm_report_list_gen,
    farm_report_total_summary_gen,
)

ARGUMENT_PARSER_INFO_DICT: Final[dict] = {
    "description": textwrap.dedent(
        """\
        fgo-farm-report-collection (FGO周回報告収集)
        FGOの周回報告を収集・集計し、csvファイルやxlsxファイルに保存します。
        """
    ),
    "formatter_class": argparse.RawTextHelpFormatter,
    "exit_on_error": True,
    "arguments": [
        {
            "name": ["-d", "--use_debug_mode"],
            "action": "store_true",
            "default": False,
            "help": "デバッグモード使用有無",
        },
    ],
    "subcommands": {
        "title": "sub_commands",
        "required": True,
        "commands": [
            {
                "name": ["gen-list"],
                "help": textwrap.dedent(
                    """\
                    - 機能名
                        - 周回報告一覧生成
                    - 概要
                        - 周回報告一覧ファイルを生成します
                    - 生成ファイル
                        - 周回報告一覧ファイル
                            - ./dest/farm_report_list/[収集年月].csv
                    - コマンド例
                        - poetry run fgo gen-list -y 2021
                        - poetry run fgo gen-list -m 2021-01
                    """  # noqa: E501
                ),
                "func": farm_report_list_gen.generate_farm_report_list,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-y", "--col_year"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB(1つのみ必須)] 収集年(yyyy形式)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-m", "--col_year_month"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB(1つのみ必須)] 収集年月(yyyy-mm形式)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                ],
            },
            {
                "name": ["gen-tot"],
                "help": textwrap.dedent(
                    """\
                    - 機能名
                        - 周回報告全体概要生成
                    - 概要
                        - 事前に任意で周回報告一覧ファイルを生成します
                        - 周回報告一覧ファイルを基に周回報告全体概要ファイルを生成します
                    - 生成ファイル
                        - 周回報告一覧ファイル
                            - ./dest/farm_report_list/[収集年月].csv
                        - 周回報告年間ユーザ全体概要ファイル
                            - ./dest/farm_report_total_summary/yearly_user/[収集年]_[クエスト種別]_[最低周回数].csv
                        - 周回報告年間クエスト全体概要ファイル
                            - ./dest/farm_report_total_summary/yearly_quest/[収集年]_[クエスト種別]_[最低周回数].csv
                        - 周回報告月間ユーザ全体概要ファイル
                            - ./dest/farm_report_total_summary/monthly_user/[収集年月]_[クエスト種別]_[最低周回数].csv
                        - 周回報告月間クエスト全体概要ファイル
                            - ./dest/farm_report_total_summary/monthly_quest/[収集年月]_[クエスト種別]_[最低周回数].csv
                    - コマンド例
                        - poetry run fgo gen-tot -y 2021 -yu -a 100 -u
                        - poetry run fgo gen-tot -y 2021 -yq -a 100
                        - poetry run fgo gen-tot -y 2021 -mu -a 100 -u
                        - poetry run fgo gen-tot -y 2021 -mq -a 100
                        - poetry run fgo gen-tot -m 2021-01 -mu -a 100 -u
                        - poetry run fgo gen-tot -m 2021-01 -mq -a 100
                    """  # noqa: E501
                ),
                "func": farm_report_total_summary_gen.generate_farm_report_total_summary,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-y", "--col_year"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 収集年(yyyy形式)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-m", "--col_year_month"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 収集年月(yyyy-mm形式)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    # グループB2(1つのみ必須)
                    {
                        "name": ["-yu", "--generate_yearly_user_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB2(1つのみ必須)] 周回報告年間ユーザ全体概要生成要否
                                - 収集年を指定した場合にのみ、周回報告年間ユーザ全体概要を生成します
                                - 収集年月を指定した場合はエラーになります
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b2",
                    },
                    {
                        "name": ["-yq", "--generate_yearly_quest_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB2(1つのみ必須)] 周回報告年間クエスト全体概要生成要否
                                - 収集年を指定した場合にのみ、周回報告年間クエスト全体概要を生成します
                                - 収集年月を指定した場合はエラーになります
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b2",
                    },
                    {
                        "name": ["-mu", "--generate_monthly_user_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB2(1つのみ必須)] 周回報告月間ユーザ全体概要生成要否
                                - 周回報告月間ユーザ全体概要を生成します
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b2",
                    },
                    {
                        "name": ["-mq", "--generate_monthly_quest_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB2(1つのみ必須)] 周回報告月間クエスト全体概要生成要否
                                - 周回報告月間クエスト全体概要を生成します
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b2",
                    },
                    # グループB3(1つのみ必須)
                    {
                        "name": ["-a", "--min_num_of_all_quest"],
                        "type": int,
                        "help": textwrap.dedent(
                            """\
                            - [グループB3(1つのみ必須)] 最低周回数(全て)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b3",
                    },
                    {
                        "name": ["-n", "--min_num_of_normal_quest"],
                        "type": int,
                        "help": textwrap.dedent(
                            """\
                            - [グループB3(1つのみ必須)] 最低周回数(通常クエ)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b3",
                    },
                    {
                        "name": ["-e", "--min_num_of_event_quest"],
                        "type": int,
                        "help": textwrap.dedent(
                            """\
                            - [グループB3(1つのみ必須)] 最低周回数(イベクエ)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b3",
                    },
                    {
                        "name": ["-b", "--min_num_of_quest_by_batch"],
                        "type": int,
                        "help": textwrap.dedent(
                            """\
                            - [グループB3(1つのみ必須)] 最低周回数(3種類一括)
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b3",
                    },
                    # グループC(任意)
                    {
                        "name": ["-l", "--generate_list"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] 周回報告一覧生成要否
                                - 指定した場合は一覧を生成します
                                - 指定しない場合は生成せずに既存の一覧のみを使用します
                            """  # noqa: E501
                        ),
                        # "group": "optional_group_c",
                    },
                    {
                        "name": ["-u", "--output_user_name"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] ユーザ名出力要否
                                - 指定した場合は周回報告ユーザ全体概要ファイルにユーザ名を出力します
                            """  # noqa: E501
                        ),
                        # "group": "optional_group_c",
                    },
                ],
            },
            {
                "name": ["gen-ind"],
                "help": textwrap.dedent(
                    """\
                    - 機能名
                        - 周回報告個人概要生成
                    - 概要
                        - 事前に任意で周回報告一覧ファイルを生成します
                        - 周回報告一覧ファイルを基に周回報告個人概要ファイルを生成します
                    - 生成ファイル
                        - 周回報告一覧ファイル
                            - ./dest/farm_report_list/[収集年月].csv
                        - 周回報告個人概要ファイル
                            - ./dest/farm_report_individual_summary/[収集年]_[ユーザID].csv
                    - コマンド例
                        - poetry run fgo gen-ind 2021 silverag_corgi
                    """  # noqa: E501
                ),
                "func": farm_report_individual_summary_gen.generate_farm_report_individual_summary,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループA(必須)
                    {
                        "name": ["col_year"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] 収集年(yyyy形式)
                            """  # noqa: E501
                        ),
                    },
                    {
                        "name": ["user_id"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] ユーザID
                            """  # noqa: E501
                        ),
                    },
                    # グループC(任意)
                    {
                        "name": ["-l", "--generate_list"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] 周回報告一覧生成要否
                                - 指定した場合は一覧を生成します
                                - 指定しない場合は生成せずに既存の一覧のみを使用します
                            """  # noqa: E501
                        ),
                    },
                ],
            },
            {
                "name": ["merge"],
                "help": textwrap.dedent(
                    """\
                    - 機能名
                        - 周回報告生成結果マージ
                    - 概要
                        - 生成結果をExcelファイル(マージ結果ファイル)にマージします
                    - 生成ファイル
                        - 周回報告一覧マージ結果ファイル
                            - ./dest/merge_result/周回報告一覧.xlsx
                        - 周回報告年間ユーザ全体概要マージ結果ファイル
                            - ./dest/merge_result/周回報告年間ユーザ全体概要.xlsx
                        - 周回報告年間クエスト全体概要マージ結果ファイル
                            - ./dest/merge_result/周回報告年間クエスト全体概要.xlsx
                        - 周回報告月間ユーザ全体概要マージ結果ファイル
                            - ./dest/merge_result/周回報告ユーザ全体概要.xlsx
                        - 周回報告月間クエスト全体概要マージ結果ファイル
                            - ./dest/merge_result/周回報告クエスト全体概要.xlsx
                        - 周回報告個人概要マージ結果ファイル
                            - ./dest/merge_result/周回報告個人概要.xlsx
                    - コマンド例
                        - poetry run fgo merge -l
                        - poetry run fgo merge -yu
                        - poetry run fgo merge -yq
                        - poetry run fgo merge -mu
                        - poetry run fgo merge -mq
                        - poetry run fgo merge -i
                    """  # noqa: E501
                ),
                "func": farm_report_gen_result_merge.merge_farm_report_gen_result,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-l", "--merge_list"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告一覧マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-yu", "--merge_yearly_user_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告年間ユーザ全体概要マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-yq", "--merge_yearly_quest_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告年間クエスト全体概要マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-mu", "--merge_monthly_user_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告月間ユーザ全体概要マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-mq", "--merge_monthly_quest_total_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告月間クエスト全体概要マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    {
                        "name": ["-i", "--merge_individual_summary"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 周回報告個人概要マージ要否
                            """  # noqa: E501
                        ),
                        "exclusive_group": "exclusive_group_b1",
                    },
                    # グループC(任意)
                    {
                        "name": ["-a", "--append_sheet"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] シート追加要否
                                - 指定した場合は既存のシートは変更せず、新規のシートのみを追加します
                                - 指定しない場合は全てのシートを上書きします
                            """  # noqa: E501
                        ),
                    },
                ],
            },
        ],
    },
}
