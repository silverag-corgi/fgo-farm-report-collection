from typing import Final

FARM_REPORT_LIST_FILE_PATH: Final[str] = \
    './dest/farm_report_list/{0}.csv'
FARM_REPORT_TOTAL_SUMMARY_FILE_PATH: Final[str] = \
    './dest/farm_report_total_summary/{0}_{1}_{2}.csv'
FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH: Final[str] = \
    './dest/farm_report_individual_summary/{0}_{1}.csv'

FARM_REPORT_SITE_URL: Final[str] = \
    'https://fgojunks.max747.org/harvest/contents/date/{0}.json'
USER_INFO_SITE_URL: Final[str] = \
    'https://twpro.jp/{0}'

FARM_REPORT_LIST_HEADER: Final[list[str]] = \
    [
        'quest_kind',
        'post_date',
        'user_id',
        'quest_place',
        'num_of_farms',
        'materials'
    ]
FARM_REPORT_TOTAL_SUMMARY_HEADER: Final[list[str]] = \
    [
        'user_id',
        'user_name',
        'num_of_farms'
    ]
FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER: Final[list[str]] = \
    [
        'post_month',
        'num_of_farms_for_normal',
        'num_of_farms_for_event',
        'num_of_farms_for_all'
    ]

ENCODING: Final[str] = 'utf8'

QUEST_KINDS: Final[list[str]] = \
    [
        '全て',
        '通常クエ',
        'イベクエ'
    ]

NUM_OF_MONTHS: Final[int] = 12
