import glob
import os
from datetime import datetime
from logging import Logger
from typing import Final, Optional, Union

import openpyxl
import pandas as pd
import python_lib_for_me as pyl
from styleframe import StyleFrame, Styler, utils

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_that_merge_list(
        append_sheet: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告一覧マージを開始します。')
        
        # 周回報告一覧ファイルパスの取得
        gen_result_file_paths: list[str] = __get_gen_result_file_paths(
            const_util.FARM_REPORT_LIST_FILE_PATH)
        
        # 周回報告一覧ファイルの件数が0件の場合
        if len(gen_result_file_paths) == 0:
            pyl.log_war(lg, f'周回報告一覧ファイルの件数が0件です。' +
                            f'(gen_result_file_paths:{gen_result_file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_sheet,
                        const_util.FARM_REPORT_LIST_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告一覧マージ結果ファイルへの出力
                for gen_result_file_path in reversed(gen_result_file_paths):
                    # 周回報告一覧データフレームの取得
                    pyl.log_inf(lg, f'周回報告一覧ファイルパス：{gen_result_file_path}')
                    gen_result_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
                        gen_result_file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # 書式設定の適用
                    gen_result_sf: StyleFrame = __apply_formatting_of_gen_result(
                            gen_result_df,
                            {
                                const_util.FARM_REPORT_LIST_HEADER[0]: 20,
                                const_util.FARM_REPORT_LIST_HEADER[1]: 20,
                                const_util.FARM_REPORT_LIST_HEADER[2]: 14,
                                const_util.FARM_REPORT_LIST_HEADER[3]: 25,
                                const_util.FARM_REPORT_LIST_HEADER[4]: 20,
                                const_util.FARM_REPORT_LIST_HEADER[5]: 10,
                                const_util.FARM_REPORT_LIST_HEADER[6]: 200,
                            }
                        )
                    
                    # シート名の生成
                    sheet_name: str = pyl.generate_file_name(gen_result_file_path)
                    
                    # シート説明スタイルフレームの生成
                    sheet_description_sfs: list[StyleFrame] = __generate_sheet_description_sfs(
                            '月ごとの周回報告一覧',
                            const_util.FARM_REPORT_LIST_HEADER,
                            sheet_name
                        )
                    
                    # 周回報告一覧スタイルフレームの保存
                    pandas_util.save_gen_result_sf(
                            sheet_description_sfs,
                            gen_result_sf,
                            excel_writer,
                            sheet_name,
                            columns_and_rows_to_freeze='A4',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告一覧マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        # マージ結果ファイルのセルの結合
        __merge_cells_of_merge_result_file(
                const_util.FARM_REPORT_LIST_MERGE_RESULT_FILE_PATH,
                ['A1:G1', 'A2:G2']
            )
        
        pyl.log_inf(lg, f'周回報告マージ結果ファイルパス：' +
                        f'{const_util.FARM_REPORT_LIST_MERGE_RESULT_FILE_PATH}')
        pyl.log_inf(lg, f'周回報告一覧マージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_usr_tot_sum(
        append_sheet: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告ユーザ全体概要マージを開始します。')
        
        # 周回報告ユーザ全体概要ファイルパスの取得
        gen_result_file_paths: list[str] = __get_gen_result_file_paths(
            const_util.FARM_REPORT_USER_TOTAL_SUMMARY_FILE_PATH)
        
        # 周回報告ユーザ全体概要ファイルの件数が0件の場合
        if len(gen_result_file_paths) == 0:
            pyl.log_war(lg, f'周回報告ユーザ全体概要ファイルの件数が0件です。' +
                            f'(gen_result_file_paths:{gen_result_file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_sheet,
                        const_util.FARM_REPORT_USER_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告ユーザ全体概要マージ結果ファイルへの出力
                for gen_result_file_path in reversed(gen_result_file_paths):
                    # 周回報告ユーザ全体概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告ユーザ全体概要ファイルパス：{gen_result_file_path}')
                    gen_result_df: pd.DataFrame = pandas_util.read_farm_report_usr_tot_sum_file(
                        gen_result_file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # 書式設定の適用
                    gen_result_sf: StyleFrame = __apply_formatting_of_gen_result(
                            gen_result_df,
                            {
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[0]: 20,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[1]: 20,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[2]: 10,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[3]: 10,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[4]: 13,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[5]: 13,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[6]: 13,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[7]: 13,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[8]: 15,
                            }
                        )
                    
                    # シート名の生成
                    sheet_name: str = pyl.generate_file_name(gen_result_file_path)
                    
                    # シート説明スタイルフレームの生成
                    sheet_description_sfs: list[StyleFrame] = __generate_sheet_description_sfs(
                            '月およびクエスト種別ごとの周回数(ユーザ編)',
                            const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER,
                            sheet_name
                        )
                    
                    # 周回報告ユーザ全体概要スタイルフレームの保存
                    pandas_util.save_gen_result_sf(
                            sheet_description_sfs,
                            gen_result_sf,
                            excel_writer,
                            sheet_name,
                            columns_and_rows_to_freeze='A4',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告ユーザ全体概要マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        # マージ結果ファイルのセルの結合
        __merge_cells_of_merge_result_file(
                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH,
                ['A1:I1', 'A2:I2']
            )
        
        pyl.log_inf(lg, f'周回報告マージ結果ファイルパス：' +
                        f'{const_util.FARM_REPORT_USER_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH}')
        pyl.log_inf(lg, f'周回報告ユーザ全体概要マージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_qst_tot_sum(
        append_sheet: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告クエスト全体概要マージを開始します。')
        
        # 周回報告クエスト全体概要ファイルパスの取得
        gen_result_file_paths: list[str] = __get_gen_result_file_paths(
            const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_FILE_PATH)
        
        # 周回報告クエスト全体概要ファイルの件数が0件の場合
        if len(gen_result_file_paths) == 0:
            pyl.log_war(lg, f'周回報告クエスト全体概要ファイルの件数が0件です。' +
                            f'(gen_result_file_paths:{gen_result_file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_sheet,
                        const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告クエスト全体概要マージ結果ファイルへの出力
                for gen_result_file_path in reversed(gen_result_file_paths):
                    # 周回報告クエスト全体概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告クエスト全体概要ファイルパス：{gen_result_file_path}')
                    gen_result_df: pd.DataFrame = pandas_util.read_farm_report_qst_tot_sum_file(
                        gen_result_file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # 書式設定の適用
                    gen_result_sf: StyleFrame = __apply_formatting_of_gen_result(
                            gen_result_df,
                            {
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[0]: 20,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[1]: 20,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[2]: 10,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[3]: 10,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[4]: 13,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[5]: 13,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[6]: 13,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[7]: 13,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[8]: 15,
                            }
                        )
                    
                    # シート名の生成
                    sheet_name: str = pyl.generate_file_name(gen_result_file_path)
                    
                    # シート説明スタイルフレームの生成
                    sheet_description_sfs: list[StyleFrame] = __generate_sheet_description_sfs(
                            '月およびクエスト種別ごとの周回数(クエスト編)',
                            const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER,
                            sheet_name
                        )
                    
                    # 周回報告クエスト全体概要スタイルフレームの保存
                    pandas_util.save_gen_result_sf(
                            sheet_description_sfs,
                            gen_result_sf,
                            excel_writer,
                            sheet_name,
                            columns_and_rows_to_freeze='A4',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告クエスト全体概要マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        # マージ結果ファイルのセルの結合
        __merge_cells_of_merge_result_file(
                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH,
                ['A1:I1', 'A2:I2']
            )
        
        pyl.log_inf(lg, f'周回報告マージ結果ファイルパス：' +
                        f'{const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH}')
        pyl.log_inf(lg, f'周回報告クエスト全体概要マージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_ind_sum(
        append_sheet: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告個人概要マージを開始します。')
        
        # 周回報告個人概要ファイルパスの取得
        gen_result_file_paths: list[str] = __get_gen_result_file_paths(
            const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH)
        
        # 周回報告個人概要ファイルの件数が0件の場合
        if len(gen_result_file_paths) == 0:
            pyl.log_war(lg, f'周回報告個人概要ファイルの件数が0件です。' +
                            f'(gen_result_file_paths:{gen_result_file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_sheet,
                        const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告個人概要マージ結果ファイルへの出力
                for gen_result_file_path in reversed(gen_result_file_paths):
                    # 周回報告個人概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告個人概要ファイルパス：{gen_result_file_path}')
                    gen_result_df: pd.DataFrame = pandas_util.read_farm_report_ind_sum_file(
                        gen_result_file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # 書式設定の適用
                    gen_result_sf: StyleFrame = __apply_formatting_of_gen_result(
                            gen_result_df,
                            {
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[0]: 10,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[1]: 17,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[2]: 17,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[3]: 17,
                            }
                        )
                    
                    # シート名の生成
                    sheet_name: str = pyl.generate_file_name(gen_result_file_path)
                    
                    # シート説明スタイルフレームの生成
                    sheet_description_sfs: list[StyleFrame] = __generate_sheet_description_sfs(
                            '年およびユーザごとの周回数',
                            const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER,
                            sheet_name
                        )
                    
                    # 周回報告個人概要スタイルフレームの保存
                    pandas_util.save_gen_result_sf(
                            sheet_description_sfs,
                            gen_result_sf,
                            excel_writer,
                            sheet_name,
                            columns_and_rows_to_freeze='A4',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告個人概要ファイルの書き込みに失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        # マージ結果ファイルのセルの結合
        __merge_cells_of_merge_result_file(
                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_MERGE_RESULT_FILE_PATH,
                ['A1:D1', 'A2:D2']
            )
        
        pyl.log_inf(lg, f'周回報告マージ結果ファイルパス：' +
                        f'{const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_MERGE_RESULT_FILE_PATH}')
        pyl.log_inf(lg, f'周回報告個人概要マージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __get_gen_result_file_paths(gen_result_file_path: str) -> list[str]:
    
    '''生成結果ファイルパス(複数)生成'''
    
    gen_result_file_dir: str = os.path.dirname(gen_result_file_path)
    gen_result_file_ext: str = os.path.splitext(gen_result_file_path)[1]
    gen_result_file_path_with_wildcard: str = gen_result_file_dir + '/*' + gen_result_file_ext
    gen_result_file_paths: list[str] = glob.glob(gen_result_file_path_with_wildcard)
    
    return gen_result_file_paths


def __generate_excel_writer(
        append_sheet: bool,
        merge_result_file_path: str
    ) -> Optional[pd.ExcelWriter]:
    
    '''Excelライター生成'''
    
    excel_writer: Optional[pd.ExcelWriter] = None
    
    if append_sheet == True and os.path.isfile(merge_result_file_path) == True:
        excel_writer = StyleFrame.ExcelWriter(
                merge_result_file_path,
                mode='a',
                if_sheet_exists='replace',  # overlay not working
            )
    else:
        excel_writer = StyleFrame.ExcelWriter(
                merge_result_file_path,
                mode='w',
            )
    
    return excel_writer


def __apply_formatting_of_gen_result(
        gen_result_df: pd.DataFrame,
        col_width_dict: dict[str, Union[int, float]] = {}
    ) -> StyleFrame:
    
    '''書式設定適用(生成結果)'''
    
    DATETIME_FORMAT: Final[str] = 'YYYY-MM-DD HH:MM:SS'
    
    # デフォルトのスタイルの適用
    default_style: Styler = Styler(
            bg_color=None,
            bold=False,
            font=const_util.FONT_NAME,
            font_size=const_util.FONT_SIZE,
            number_format=utils.number_formats.thousands_comma_sep,
            horizontal_alignment=utils.horizontal_alignments.general,
            wrap_text=False,
            shrink_to_fit=False,
            date_time_format=DATETIME_FORMAT,
        )
    gen_result_sf: StyleFrame = StyleFrame(gen_result_df, default_style)
    
    # ヘッダのスタイルの適用
    header_style: Styler = Styler(
            bg_color=utils.colors.grey,
            bold=True,
            font=const_util.FONT_NAME,
            font_size=const_util.FONT_SIZE,
            number_format=utils.number_formats.general,
            horizontal_alignment=utils.horizontal_alignments.center,
            wrap_text=True,
            shrink_to_fit=False,
            date_time_format=DATETIME_FORMAT,
        )
    gen_result_sf.apply_headers_style(header_style)
    
    # 列の幅の適用
    gen_result_sf.set_column_width_dict(col_width_dict)
    
    # 行の高さの適用
    row_indexes: tuple = gen_result_sf.row_indexes
    if len(row_indexes) == 1:
        gen_result_sf.set_row_height_dict({
                row_indexes[0]: 30,
            })
    else:
        gen_result_sf.set_row_height_dict({
                row_indexes[0]: 30,
                row_indexes[1:]: 20,
            })
    
    return gen_result_sf


def __apply_formatting_of_sheet_description(
        sheet_description_df: pd.DataFrame,
        col_width_dict: dict[str, Union[int, float]] = {},
        is_update_datetime_col: bool = False
    ) -> StyleFrame:
    
    '''書式設定適用(シート説明)'''
    
    DATETIME_FORMAT: Final[str] = 'YYYY-MM-DD HH:MM:SS'
    
    # デフォルトのスタイルの適用
    default_style: Styler = Styler(
            bg_color=None,
            bold=False,
            font=const_util.FONT_NAME,
            font_size=const_util.FONT_SIZE,
            number_format=utils.number_formats.general,
            horizontal_alignment=(utils.horizontal_alignments.general
                                    if is_update_datetime_col == False
                                    else utils.horizontal_alignments.right),
            wrap_text=False,
            shrink_to_fit=False if is_update_datetime_col == False else True,
            date_time_format=DATETIME_FORMAT,
        )
    sheet_description_sf: StyleFrame = StyleFrame(sheet_description_df, default_style)
    
    # 列の幅の適用
    sheet_description_sf.set_column_width_dict(col_width_dict)
    
    # 行の高さの適用
    row_indexes: tuple = sheet_description_sf.row_indexes
    sheet_description_sf.set_row_height_dict({
            row_indexes[:len(row_indexes) - 1]: 20,
        })
    
    return sheet_description_sf


def __generate_sheet_description_sfs(
        sheet_description: str,
        gen_result_header: list[str],
        sheet_name: str
    ) -> list[StyleFrame]:
    
    '''シート説明スタイルフレーム生成'''
    
    sheet_description_sfs: list[StyleFrame] = []
    
    # シート説明01データフレームの生成
    sheet_description_col_num: int = 0
    sheet_description_01_df: pd.DataFrame = \
        pd.DataFrame({f'col_{sheet_description_col_num}': [sheet_description, sheet_name]})
    for _ in range(len(gen_result_header) - 1):
        sheet_description_col_num = sheet_description_col_num + 1
        sheet_description_01_df[f'col_{sheet_description_col_num}'] = ''
    
    # シート説明01の書式設定の適用
    sheet_description_01_sf: StyleFrame = __apply_formatting_of_sheet_description(
        sheet_description_01_df, is_update_datetime_col=False)
    
    # 更新日時の取得
    update_datetime: datetime = datetime.now()
    update_date: str = update_datetime.strftime('%Y-%m-%d')
    update_time: str = update_datetime.strftime('%H:%M:%S')
    
    # シート説明02データフレームの生成
    sheet_description_col_num = sheet_description_col_num + 1
    sheet_description_02_df: pd.DataFrame = \
        pd.DataFrame({f'col_{sheet_description_col_num}': [update_date, update_time]})
    
    # シート説明02の書式設定の適用
    sheet_description_02_sf: StyleFrame = __apply_formatting_of_sheet_description(
        sheet_description_02_df, is_update_datetime_col=True)
    
    # シート説明スタイルフレームへの追加
    sheet_description_sfs.append(sheet_description_01_sf)
    sheet_description_sfs.append(sheet_description_02_sf)
    
    return sheet_description_sfs


def __merge_cells_of_merge_result_file(
        merge_result_file_path: str,
        ranges: list[str]
    ) -> None:
    
    '''セル結合(マージ結果ファイル)'''
    
    merge_result_wb: openpyxl.Workbook = openpyxl.load_workbook(merge_result_file_path)
    
    for sheet_name in merge_result_wb.sheetnames:
        for range in ranges:
            merge_result_wb[sheet_name].merge_cells(range)  # type: ignore
    
    merge_result_wb.save(merge_result_file_path)
    
    return None
