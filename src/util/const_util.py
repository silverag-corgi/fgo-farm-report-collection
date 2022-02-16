from typing import Final

FARM_REPORT_LIST_FILE_PATH:                 Final[str] = './dest/farm_report_list/farm_report_list_{0}.csv'
FARM_REPORT_TOTAL_SUMMARY_FILE_PATH:        Final[str] = './dest/farm_report_total_summary/farm_report_total_summary_{0}_{1}_{2}.csv'
FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH:   Final[str] = './dest/farm_report_individual_summary/farm_report_individual_summary_{0}_{1}.csv'

FARM_REPORT_SITE_URL: Final[str] = 'https://fgojunks.max747.org/harvest/contents/date/{0}.html'
USER_INFO_SITE_URL:   Final[str] = 'https://twpro.jp/{0}'

FARM_REPORT_LIST_HEADER:                Final[list[str]] = \
    ['quest_kind', 'posting_date', 'user_id', 'quest_place', 'num_of_farms', 'material']
FARM_REPORT_LIST_HEADER_RAW:            Final[list[str]] = \
    FARM_REPORT_LIST_HEADER[1:6]
FARM_REPORT_TOTAL_SUMMARY_HEADER:       Final[list[str]] = \
    ['user_id', 'user_name', 'num_of_farms']
FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER:  Final[list[str]] = \
    ['posting_month', 'num_of_farms_for_normal', 'num_of_farms_for_event', 'num_of_farms_for_all']

ENCODING: Final[str] = 'utf8'

QUEST_KINDS: Final[list[str]] = ['全て', '通常クエ', 'イベクエ']

NUM_OF_MONTHS: Final[int] = 12
