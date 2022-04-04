from typing import Final

FARM_REPORT_LIST_FILE_PATH: Final[str] = \
    './dest/farm_report_list/{0}.csv'
FARM_REPORT_USER_TOTAL_SUMMARY_FILE_PATH: Final[str] = \
    './dest/farm_report_total_summary/user/{0}_{1}_{2}周以上.csv'
FARM_REPORT_QUEST_TOTAL_SUMMARY_FILE_PATH: Final[str] = \
    './dest/farm_report_total_summary/quest/{0}_{1}_{2}周以上.csv'
FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH: Final[str] = \
    './dest/farm_report_individual_summary/{0}_{1}.csv'

FARM_REPORT_LIST_MERGE_RESULT_FILE_PATH: Final[str] = \
    './dest/merge_result/周回報告一覧.xlsx'
FARM_REPORT_USER_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH: Final[str] = \
    './dest/merge_result/周回報告ユーザ全体概要.xlsx'
FARM_REPORT_QUEST_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH: Final[str] = \
    './dest/merge_result/周回報告クエスト全体概要.xlsx'
FARM_REPORT_INDIVIDUAL_SUMMARY_MERGE_RESULT_FILE_PATH: Final[str] = \
    './dest/merge_result/周回報告個人概要.xlsx'

FARM_REPORT_SITE_URL: Final[str] = \
    'https://fgojunks.max747.org/harvest/contents/date/{0}.json'
USER_INFO_SITE_URL: Final[str] = \
    'https://twpro.jp/{0}'

FARM_REPORT_LIST_HEADER: Final[list[str]] = \
    [
        '投稿日時',
        'ユーザID',
        'クエスト種別',
        '章名',
        '座標名',
        '周回数',
        '素材'
    ]
FARM_REPORT_USER_TOTAL_SUMMARY_HEADER: Final[list[str]] = \
    [
        'ユーザID',
        'ユーザ名',
        '周回数',
        '報告数',
        '周回数／報告'
    ]
FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER: Final[list[str]] = \
    [
        '章名',
        '座標名',
        '周回数',
        '報告数',
        '周回数／報告'
    ]
FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER: Final[list[str]] = \
    [
        '投稿月',
        '周回数(通常)',
        '周回数(イベント)',
        '周回数(全て)'
    ]

ENCODING: Final[str] = 'utf8'

QUEST_KINDS: Final[list[str]] = \
    [
        '全て',
        '通常クエ',
        'イベクエ'
    ]

NUM_OF_MONTHS: Final[int] = 12

FONT_NAME: Final[str] = 'Meiryo UI'
FONT_SIZE: Final[int] = 10
