from os import listdir
from os.path import dirname, realpath, join
from typing import Tuple

from comments_remover import Language

TESTS_DIR_PATH: str = dirname(realpath(__file__))
SOURCES_DIR_PATH: str = join(TESTS_DIR_PATH, 'sources')
INPUT_SOURCE_FILE_PREFIX: str = 'input'
OUTPUT_SOURCE_FILE_PREFIX: str = 'output'


def get_input_and_output_source_file_paths(language: Language) -> Tuple[str, str]:
    language_sources_dir_path = join(SOURCES_DIR_PATH, language.name)
    input_file_path = output_file_path = None
    for file_name in listdir(language_sources_dir_path):
        if file_name.startswith(INPUT_SOURCE_FILE_PREFIX):
            input_file_path = join(language_sources_dir_path, file_name)
        if file_name.startswith(OUTPUT_SOURCE_FILE_PREFIX):
            output_file_path = join(language_sources_dir_path, file_name)
        if input_file_path and output_file_path:
            return input_file_path, output_file_path
