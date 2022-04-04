import glob
import os
from logging import Logger
from typing import Optional, Union

import pandas as pd
import python_lib_for_me as pyl
from styleframe import StyleFrame, Styler, utils

from fgo_farm_report_collection.util import const_util, pandas_util


def do_logic_that_merge_farm_report_list_files(
        append_generated_file: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告一覧ファイルマージを開始します。')
        
        # 周回報告一覧ファイルパスの取得
        file_paths: list[str] = __get_file_paths_from_file_path_with_wildcard(
            const_util.FARM_REPORT_LIST_FILE_PATH)
        
        # 周回報告一覧ファイルの件数が0件の場合
        if len(file_paths) == 0:
            pyl.log_war(lg, f'周回報告一覧ファイルの件数が0件です。(file_paths:{file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_generated_file,
                        const_util.FARM_REPORT_LIST_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告一覧マージ結果ファイルへの出力
                for file_path in reversed(file_paths):
                    # 周回報告一覧データフレームの取得
                    pyl.log_inf(lg, f'周回報告一覧ファイルパス：{file_path}')
                    farm_report_df: pd.DataFrame = pandas_util.read_farm_report_list_file(
                        file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # 書式設定の適用
                    farm_report_sf: StyleFrame = __apply_formatting(
                            farm_report_df,
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
                    
                    # 周回報告一覧スタイルフレームの保存
                    pandas_util.save_farm_report_sf(
                            farm_report_sf,
                            excel_writer,
                            file_path,
                            columns_and_rows_to_freeze='D2',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告一覧マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        pyl.log_inf(lg, f'周回報告一覧ファイルマージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_farm_report_usr_tot_sum_files(
        append_generated_file: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告ユーザ全体概要ファイルマージを開始します。')
        
        # 周回報告ユーザ全体概要ファイルパスの取得
        file_paths: list[str] = __get_file_paths_from_file_path_with_wildcard(
            const_util.FARM_REPORT_USER_TOTAL_SUMMARY_FILE_PATH)
        
        # 周回報告ユーザ全体概要ファイルの件数が0件の場合
        if len(file_paths) == 0:
            pyl.log_war(lg, f'周回報告ユーザ全体概要ファイルの件数が0件です。(file_paths:{file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_generated_file,
                        const_util.FARM_REPORT_USER_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告ユーザ全体概要マージ結果ファイルへの出力
                for file_path in reversed(file_paths):
                    # 周回報告ユーザ全体概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告ユーザ全体概要ファイルパス：{file_path}')
                    farm_report_df: pd.DataFrame = pandas_util.read_farm_report_usr_tot_sum_file(
                        file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # Excel書式設定の適用
                    farm_report_sf: StyleFrame = __apply_formatting(
                            farm_report_df,
                            {
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[0]: 20,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[1]: 20,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[2]: 10,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[3]: 10,
                                const_util.FARM_REPORT_USER_TOTAL_SUMMARY_HEADER[4]: 13,
                            }
                        )
                    
                    # 周回報告ユーザ全体概要スタイルフレームの保存
                    pandas_util.save_farm_report_sf(
                            farm_report_sf,
                            excel_writer,
                            file_path,
                            columns_and_rows_to_freeze='D2',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告ユーザ全体概要マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        pyl.log_inf(lg, f'周回報告ユーザ全体概要ファイルマージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_farm_report_qst_tot_sum_files(
        append_generated_file: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告クエスト全体概要ファイルマージを開始します。')
        
        # 周回報告クエスト全体概要ファイルパスの取得
        file_paths: list[str] = __get_file_paths_from_file_path_with_wildcard(
            const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_FILE_PATH)
        
        # 周回報告クエスト全体概要ファイルの件数が0件の場合
        if len(file_paths) == 0:
            pyl.log_war(lg, f'周回報告クエスト全体概要ファイルの件数が0件です。(file_paths:{file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_generated_file,
                        const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告クエスト全体概要マージ結果ファイルへの出力
                for file_path in reversed(file_paths):
                    # 周回報告クエスト全体概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告クエスト全体概要ファイルパス：{file_path}')
                    farm_report_df: pd.DataFrame = pandas_util.read_farm_report_qst_tot_sum_file(
                        file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # Excel書式設定の適用
                    farm_report_sf: StyleFrame = __apply_formatting(
                            farm_report_df,
                            {
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[0]: 20,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[1]: 20,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[2]: 10,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[3]: 10,
                                const_util.FARM_REPORT_QUEST_TOTAL_SUMMARY_HEADER[4]: 13,
                            }
                        )
                    
                    # 周回報告クエスト全体概要スタイルフレームの保存
                    pandas_util.save_farm_report_sf(
                            farm_report_sf,
                            excel_writer,
                            file_path,
                            columns_and_rows_to_freeze='D2',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告クエスト全体概要マージ結果ファイルへの出力に失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        pyl.log_inf(lg, f'周回報告クエスト全体概要ファイルマージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def do_logic_that_merge_farm_report_ind_sum_files(
        append_generated_file: bool
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'周回報告個人概要ファイルマージを開始します。')
        
        # 周回報告個人概要ファイルパスの取得
        file_paths: list[str] = __get_file_paths_from_file_path_with_wildcard(
            const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_FILE_PATH)
        
        # 周回報告個人概要ファイルの件数が0件の場合
        if len(file_paths) == 0:
            pyl.log_war(lg, f'周回報告個人概要ファイルの件数が0件です。(file_paths:{file_paths})')
        else:
            excel_writer: Optional[pd.ExcelWriter] = None
            try:
                # Excelライターの生成
                excel_writer = __generate_excel_writer(
                        append_generated_file,
                        const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_MERGE_RESULT_FILE_PATH
                    )
                
                # 周回報告個人概要マージ結果ファイルへの出力
                for file_path in reversed(file_paths):
                    # 周回報告個人概要データフレームの取得
                    pyl.log_inf(lg, f'周回報告個人概要ファイルパス：{file_path}')
                    farm_report_df: pd.DataFrame = pandas_util.read_farm_report_ind_sum_file(
                        file_path, reset_index_from_one=True, move_index_to_column=True)
                    
                    # Excel書式設定の適用
                    farm_report_sf: StyleFrame = __apply_formatting(
                            farm_report_df,
                            {
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[0]: 10,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[1]: 17,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[2]: 17,
                                const_util.FARM_REPORT_INDIVIDUAL_SUMMARY_HEADER[3]: 17,
                            }
                        )
                    
                    # 周回報告個人概要スタイルフレームの保存
                    pandas_util.save_farm_report_sf(
                            farm_report_sf,
                            excel_writer,
                            file_path,
                            columns_and_rows_to_freeze='C2',
                        )
            except Exception as e:
                pyl.log_err(lg, f'周回報告個人概要ファイルの書き込みに失敗しました。')
                raise(e)
            finally:
                if excel_writer is not None:
                    excel_writer.close()
        
        pyl.log_inf(lg, f'周回報告個人概要ファイルマージを終了します。')
    except Exception as e:
        raise(e)
    
    return None


def __get_file_paths_from_file_path_with_wildcard(path: str) -> list[str]:
    
    '''ファイルパス(複数)生成'''
    
    file_path_dir: str = os.path.dirname(path)
    file_path_ext: str = os.path.splitext(path)[1]
    file_path_with_wildcard: str = file_path_dir + '/*' + file_path_ext
    file_paths: list[str] = glob.glob(file_path_with_wildcard)
    
    return file_paths


def __generate_excel_writer(
        append_generated_file: bool,
        file_path: str
    ) -> Optional[pd.ExcelWriter]:
    
    '''Excelライター生成'''
    
    excel_writer: Optional[pd.ExcelWriter] = None
    
    if append_generated_file == True and os.path.isfile(file_path) == True:
        excel_writer = StyleFrame.ExcelWriter(
                file_path,
                mode='a',
                if_sheet_exists='replace',
            )
    else:
        excel_writer = StyleFrame.ExcelWriter(
                file_path,
                mode='w',
            )
    
    return excel_writer


def __apply_formatting(
        farm_report_df: pd.DataFrame,
        col_width_dict: dict[str, Union[int, float]]
    ) -> StyleFrame:
    
    '''書式設定適用'''
    
    # デフォルトのスタイルの適用
    default_style: Styler = Styler(
            bg_color=None,
            bold=False,
            font=const_util.FONT_NAME,
            font_size=const_util.FONT_SIZE,
            horizontal_alignment=utils.horizontal_alignments.general,
            wrap_text=False,
            shrink_to_fit=False,
            date_time_format='YYYY-MM-DD HH:MM:SS',
        )
    farm_report_sf: StyleFrame = StyleFrame(farm_report_df, default_style)
    
    # ヘッダのスタイルの適用
    header_style: Styler = Styler(
            bg_color=utils.colors.grey,
            bold=True,
            font=const_util.FONT_NAME,
            font_size=const_util.FONT_SIZE,
            horizontal_alignment=utils.horizontal_alignments.center,
            wrap_text=True,
            shrink_to_fit=False,
            date_time_format='YYYY-MM-DD HH:MM:SS',
        )
    farm_report_sf.apply_headers_style(styler_obj=header_style)
    
    # 列幅の適用
    farm_report_sf.set_column_width_dict(col_width_dict)
    
    # 行高さの適用
    farm_report_sf.set_row_height_dict({
            farm_report_sf.row_indexes[0] : 30,
            farm_report_sf.row_indexes[1:]: 15,
        })
    
    return farm_report_sf
