import re
from os import makedirs
from os.path import join, dirname
from shutil import copy2

from hypothesis import given
from hypothesis import strategies as st
from pytest import mark

from comments_remover import Language, remove_comments_from_string, remove_comments_from_file, \
    DEFAULT_OUTPUT_FILE_PREFIX, _read_file, _extract_file_name_with_extension
from tests import get_input_and_output_source_file_paths, strip_spaces_and_linebreaks


@mark.parametrize('language', Language)
def test_remove_comments_from_string(language: Language):
    input_file_path, output_file_path = get_input_and_output_source_file_paths(language)

    actual_output = remove_comments_from_string(_read_file(input_file_path), language)

    actual_output = strip_spaces_and_linebreaks(actual_output)
    expected_output = strip_spaces_and_linebreaks(_read_file(output_file_path))

    assert actual_output == expected_output


@mark.parametrize('language', Language)
@mark.parametrize('provide_output_file_dir_path', [True, False])
def test_remove_comments_from_file(tmpdir_factory,
                                   language: Language,
                                   provide_output_file_dir_path: bool):
    input_file_path, output_file_path = get_input_and_output_source_file_paths(language)

    tmp_language_sources_dir_path = join(tmpdir_factory.getbasetemp(),
                                         'sources',
                                         language.name)
    makedirs(tmp_language_sources_dir_path, exist_ok=True)
    if provide_output_file_dir_path:
        output_file_dir_path = tmp_language_sources_dir_path
    else:
        output_file_dir_path = None
        # Prevent cluttering project dir with temporary test-only files.
        new_input_file_path = join(tmp_language_sources_dir_path,
                                   _extract_file_name_with_extension(input_file_path))
        copy2(input_file_path, new_input_file_path)
        input_file_path = new_input_file_path

    output_file_prefix = DEFAULT_OUTPUT_FILE_PREFIX

    remove_comments_from_file(input_file_path,
                              language,
                              output_file_dir_path=output_file_dir_path,
                              output_file_prefix=output_file_prefix)

    input_file_name = _extract_file_name_with_extension(input_file_path)
    if provide_output_file_dir_path:
        actual_output_file_path = join(output_file_dir_path,
                                       '{}{}'.format(output_file_prefix, input_file_name))
    else:
        actual_output_file_path = join(dirname(input_file_path),
                                       '{}{}'.format(output_file_prefix, input_file_name))
    actual_output_file_contents = strip_spaces_and_linebreaks(_read_file(actual_output_file_path))

    expected_output_file_contents = strip_spaces_and_linebreaks(_read_file(output_file_path))

    assert actual_output_file_contents == expected_output_file_contents


@mark.parametrize('language', Language)
@given(data=st.data())
def test_get_language_from_string(language: Language,
                                  data):
    assert Language.get_from_string(language.name, ignore_case=False) is language

    mixed_case_language_name_pattern = r'\A'
    for char in language.name:
        mixed_case_language_name_pattern += r'[{}]'.format(char)
    mixed_case_language_name_pattern += r'\Z'
    mixed_case_language_name_regex = re.compile(mixed_case_language_name_pattern, re.IGNORECASE)
    mixed_case_language_name = data.draw(st.from_regex(mixed_case_language_name_regex))
    assert Language.get_from_string(mixed_case_language_name, ignore_case=True) is language
