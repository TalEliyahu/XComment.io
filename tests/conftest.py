from os import listdir
from os.path import realpath, dirname, join
from typing import Tuple

from ..comments_remover import Language

TESTS_DIR_PATH: str = realpath(dirname(realpath(__file__)))
SOURCES_DIR_PATH: str = join(TESTS_DIR_PATH, 'sources')
INPUT_SOURCE_FILE_PREFIX = 'input'
OUTPUT_SOURCE_FILE_PREFIX = 'output'


def get_source_file_paths(language: Language) -> Tuple[str, str]:
    language_sources_dir_path = join(SOURCES_DIR_PATH, language.name)

    for input_file_name in listdir(language_sources_dir_path):
        if input_file_name.startswith(INPUT_SOURCE_FILE_PREFIX):
            input_file_path = join(language_sources_dir_path, input_file_name)

    for output_file_name in listdir(language_sources_dir_path):
        if output_file_name.startswith(OUTPUT_SOURCE_FILE_PREFIX):
            output_file_path = join(language_sources_dir_path, output_file_name)

    return input_file_path, output_file_path