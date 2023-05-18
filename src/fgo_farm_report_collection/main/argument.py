import argparse
from typing import Optional


class FarmReportBaseArg:
    """周回報告基本引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        self.__use_debug_mode: bool = arg_namespace.use_debug_mode
        return None

    @property
    def use_debug_mode(self) -> bool:
        return self.__use_debug_mode


class FarmReportListArg(FarmReportBaseArg):
    """周回報告一覧引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__col_year: Optional[str] = arg_namespace.col_year
        self.__col_year_month: Optional[str] = arg_namespace.col_year_month
        return None

    def is_specified(self) -> bool:
        return self.__col_year is not None or self.__col_year_month is not None

    @property
    def col_year(self) -> Optional[str]:
        return self.__col_year

    @property
    def col_year_month(self) -> Optional[str]:
        return self.__col_year_month


class FarmReportTotalSummaryArg(FarmReportListArg):
    """周回報告全体概要引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB2(1つのみ必須)
        self.__generate_yearly_user_total_summary: bool = (
            arg_namespace.generate_yearly_user_total_summary
        )
        self.__generate_yearly_quest_total_summary: bool = (
            arg_namespace.generate_yearly_quest_total_summary
        )
        self.__generate_monthly_user_total_summary: bool = (
            arg_namespace.generate_monthly_user_total_summary
        )
        self.__generate_monthly_quest_total_summary: bool = (
            arg_namespace.generate_monthly_quest_total_summary
        )
        # グループB3(1つのみ必須)
        self.__min_num_of_all_quest: Optional[int] = arg_namespace.min_num_of_all_quest
        self.__min_num_of_normal_quest: Optional[int] = arg_namespace.min_num_of_normal_quest
        self.__min_num_of_event_quest: Optional[int] = arg_namespace.min_num_of_event_quest
        self.__min_num_of_quest_by_batch: Optional[int] = arg_namespace.min_num_of_quest_by_batch
        # グループC(任意)
        self.__generate_list: bool = arg_namespace.generate_list
        self.__output_user_name: bool = arg_namespace.output_user_name
        return None

    def is_specified(self) -> bool:
        return super().is_specified() and (
            (
                self.__generate_yearly_user_total_summary is True
                or self.__generate_yearly_quest_total_summary is True
                or self.__generate_monthly_user_total_summary is True
                or self.__generate_monthly_quest_total_summary is True
            )
            and (
                self.__min_num_of_all_quest is not None
                or self.__min_num_of_normal_quest is not None
                or self.__min_num_of_event_quest is not None
                or self.__min_num_of_quest_by_batch is not None
            )
        )

    @property
    def generate_yearly_user_total_summary(self) -> bool:
        return self.__generate_yearly_user_total_summary

    @property
    def generate_yearly_quest_total_summary(self) -> bool:
        return self.__generate_yearly_quest_total_summary

    @property
    def generate_monthly_user_total_summary(self) -> bool:
        return self.__generate_monthly_user_total_summary

    @property
    def generate_monthly_quest_total_summary(self) -> bool:
        return self.__generate_monthly_quest_total_summary

    @property
    def min_num_of_all_quest(self) -> Optional[int]:
        return self.__min_num_of_all_quest

    @property
    def min_num_of_normal_quest(self) -> Optional[int]:
        return self.__min_num_of_normal_quest

    @property
    def min_num_of_event_quest(self) -> Optional[int]:
        return self.__min_num_of_event_quest

    @property
    def min_num_of_quest_by_batch(self) -> Optional[int]:
        return self.__min_num_of_quest_by_batch

    @property
    def generate_list(self) -> bool:
        return self.__generate_list

    @property
    def output_user_name(self) -> bool:
        return self.__output_user_name


class FarmReportIndividualSummaryArg(FarmReportBaseArg):
    """周回報告個人概要引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループA(必須)
        self.__col_year: str = arg_namespace.col_year
        self.__user_id: str = arg_namespace.user_id
        # グループC(任意)
        self.__generate_list: bool = arg_namespace.generate_list
        return None

    def is_specified(self) -> bool:
        return (self.__col_year is not None) and (self.__user_id is not None)

    @property
    def col_year(self) -> str:
        return self.__col_year

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def generate_list(self) -> bool:
        return self.__generate_list


class FarmReportGenResultArg(FarmReportBaseArg):
    """周回報告生成結果引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__merge_list: bool = arg_namespace.merge_list
        self.__merge_yearly_user_total_summary: bool = arg_namespace.merge_yearly_user_total_summary
        self.__merge_yearly_quest_total_summary: bool = (
            arg_namespace.merge_yearly_quest_total_summary
        )
        self.__merge_monthly_user_total_summary: bool = (
            arg_namespace.merge_monthly_user_total_summary
        )
        self.__merge_monthly_quest_total_summary: bool = (
            arg_namespace.merge_monthly_quest_total_summary
        )
        self.__merge_individual_summary: bool = arg_namespace.merge_individual_summary
        # グループC(任意)
        self.__append_sheet: bool = arg_namespace.append_sheet
        return None

    def is_specified(self) -> bool:
        return (
            self.__merge_list is True
            or self.__merge_yearly_user_total_summary is True
            or self.__merge_yearly_quest_total_summary is True
            or self.__merge_monthly_user_total_summary is True
            or self.__merge_monthly_quest_total_summary is True
            or self.__merge_individual_summary is True
        )

    @property
    def merge_list(self) -> bool:
        return self.__merge_list

    @property
    def merge_yearly_user_total_summary(self) -> bool:
        return self.__merge_yearly_user_total_summary

    @property
    def merge_yearly_quest_total_summary(self) -> bool:
        return self.__merge_yearly_quest_total_summary

    @property
    def merge_monthly_user_total_summary(self) -> bool:
        return self.__merge_monthly_user_total_summary

    @property
    def merge_monthly_quest_total_summary(self) -> bool:
        return self.__merge_monthly_quest_total_summary

    @property
    def merge_individual_summary(self) -> bool:
        return self.__merge_individual_summary

    @property
    def append_sheet(self) -> bool:
        return self.__append_sheet
