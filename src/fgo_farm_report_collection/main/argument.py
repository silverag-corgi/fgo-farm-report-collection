import argparse
from abc import ABCMeta
from datetime import datetime
from typing import Optional

import python_lib_for_me as pyl


class FarmReportAbstractBaseArg(metaclass=ABCMeta):
    """周回報告抽象基底引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        self.__use_debug_mode: bool = arg_namespace.use_debug_mode
        return None

    @property
    def use_debug_mode(self) -> bool:
        return self.__use_debug_mode


class FarmReportListArg(FarmReportAbstractBaseArg):
    """周回報告一覧引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__col_year: Optional[str] = arg_namespace.col_year
        self.__col_year_month: Optional[str] = arg_namespace.col_year_month
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：収集年が年(yyyy形式)であるか、もしくは収集年月が年月(yyyy-mm形式)であること
            if self.col_year is not None:
                try:
                    datetime.strptime(self.col_year, "%Y")
                except ValueError as e:
                    raise pyl.ArgumentValidationError(f"収集年が年(yyyy形式)ではありません。(col_year:{self.col_year})")
            elif self.col_year_month is not None:
                try:
                    datetime.strptime(self.col_year_month, "%Y-%m")
                except ValueError as e:
                    raise pyl.ArgumentValidationError(
                        f"収集年月が年月(yyyy-mm形式)ではありません。(col_year_month:{self.col_year_month})"
                    )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
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
        self.__generate_yearly_user_total_summary: bool = arg_namespace.generate_yearly_user_total_summary
        self.__generate_yearly_quest_total_summary: bool = arg_namespace.generate_yearly_quest_total_summary
        self.__generate_monthly_user_total_summary: bool = arg_namespace.generate_monthly_user_total_summary
        self.__generate_monthly_quest_total_summary: bool = arg_namespace.generate_monthly_quest_total_summary
        # グループB3(1つのみ必須)
        self.__min_num_of_all_quest: Optional[int] = arg_namespace.min_num_of_all_quest
        self.__min_num_of_normal_quest: Optional[int] = arg_namespace.min_num_of_normal_quest
        self.__min_num_of_event_quest: Optional[int] = arg_namespace.min_num_of_event_quest
        self.__min_num_of_quest_by_batch: Optional[int] = arg_namespace.min_num_of_quest_by_batch
        # グループC(任意)
        self.__generate_list: bool = arg_namespace.generate_list
        self.__output_user_name: bool = arg_namespace.output_user_name
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数検証
            super().__validate_arg()

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：周回報告年間ユーザ全体概要生成要否、もしくは、周回報告年間クエスト全体概要生成要否が真の場合は、
            # 収集年が指定されていること
            if (
                self.generate_yearly_user_total_summary is True or self.generate_yearly_quest_total_summary is True
            ) and self.col_year is None:
                raise pyl.ArgumentValidationError(
                    f"収集年が指定されていません。(col_year:{self.col_year}, col_year_month:{self.col_year_month})"
                )

            # 検証：最低周回数のいずれかが0以上であること
            if self.min_num_of_all_quest is not None and not (self.min_num_of_all_quest >= 0):
                raise pyl.ArgumentValidationError(
                    f"最低周回数(全て)が0以上ではありません。(min_num_of_all_quest:{self.min_num_of_all_quest})"
                )
            elif self.min_num_of_normal_quest is not None and not (self.min_num_of_normal_quest >= 0):
                raise pyl.ArgumentValidationError(
                    f"最低周回数(通常クエ)が0以上ではありません。(min_num_of_normal_quest:{self.min_num_of_normal_quest})"
                )
            elif self.min_num_of_event_quest is not None and not (self.min_num_of_event_quest >= 0):
                raise pyl.ArgumentValidationError(
                    f"最低周回数(イベクエ)が0以上ではありません。(min_num_of_event_quest:{self.min_num_of_event_quest})"
                )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        return (
            self.__generate_yearly_user_total_summary is True
            or self.__generate_yearly_quest_total_summary is True
            or self.__generate_monthly_user_total_summary is True
            or self.__generate_monthly_quest_total_summary is True
        ) and (
            self.__min_num_of_all_quest is not None
            or self.__min_num_of_normal_quest is not None
            or self.__min_num_of_event_quest is not None
            or self.__min_num_of_quest_by_batch is not None
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


class FarmReportIndividualSummaryArg(FarmReportAbstractBaseArg):
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
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：収集年が年(yyyy形式)であること
            try:
                datetime.strptime(self.col_year, "%Y")
            except ValueError:
                raise pyl.ArgumentValidationError(f"収集年が年(yyyy形式)ではありません。(col_year:{self.col_year})")

            # 検証：ユーザIDが4文字以上であること
            if not (len(self.user_id) >= 4):
                raise pyl.ArgumentValidationError(f"ユーザIDが4文字以上ではありません。(user_id:{self.user_id})")
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
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


class FarmReportGenResultArg(FarmReportAbstractBaseArg):
    """周回報告生成結果引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__merge_list: bool = arg_namespace.merge_list
        self.__merge_yearly_user_total_summary: bool = arg_namespace.merge_yearly_user_total_summary
        self.__merge_yearly_quest_total_summary: bool = arg_namespace.merge_yearly_quest_total_summary
        self.__merge_monthly_user_total_summary: bool = arg_namespace.merge_monthly_user_total_summary
        self.__merge_monthly_quest_total_summary: bool = arg_namespace.merge_monthly_quest_total_summary
        self.__merge_individual_summary: bool = arg_namespace.merge_individual_summary
        # グループC(任意)
        self.__append_sheet: bool = arg_namespace.append_sheet
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：なし
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
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
