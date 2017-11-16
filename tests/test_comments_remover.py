import re
import os
import logging
from os import makedirs
from os.path import join, dirname
from shutil import copy2, rmtree
from hypothesis import given
from hypothesis import strategies as st
from pytest import mark

from comments_remover import (
    Language, remove_comments_from_string, remove_comments_from_file,
    DEFAULT_OUTPUT_FILE_PREFIX, _read_file, _extract_file_name_with_extension,
    clean_results, remove_comments_batch, pack_back,
    check_compressed, unpack_file)
from tests import (
    get_input_and_output_source_file_paths,
    strip_spaces_and_linebreaks)


MULTI_FILE = "tests,sources,multi".split(",")


@mark.parametrize('language', Language)
def test_remove_comments_from_string(language: Language):
    input_file_path, output_file_path = \
        get_input_and_output_source_file_paths(language)

    actual_output = remove_comments_from_string(
        _read_file(input_file_path), language)

    actual_output = strip_spaces_and_linebreaks(actual_output)
    expected_output = strip_spaces_and_linebreaks(_read_file(
        output_file_path))

    assert actual_output == expected_output


@mark.parametrize('language', Language)
@mark.parametrize('provide_output_file_dir_path', [True, False])
@mark.parametrize('archived', [True, False])
@mark.parametrize('loggerc', [True, False])
def test_remove_comments_from_file(tmpdir_factory,
                                   language: Language,
                                   provide_output_file_dir_path: bool,
                                   loggerc: bool,
                                   capsys,
                                   archived: bool):
    input_file_path, output_file_path = \
        get_input_and_output_source_file_paths(language)

    tmp_language_sources_dir_path = join(tmpdir_factory.getbasetemp(),
                                         'sources',
                                         language.name)
    makedirs(tmp_language_sources_dir_path, exist_ok=True)

    if provide_output_file_dir_path:
        output_file_dir_path = tmp_language_sources_dir_path
    else:
        output_file_dir_path = None
        # Prevent cluttering project dir with temporary test-only files.
        new_input_file_path = join(
            tmp_language_sources_dir_path,
            _extract_file_name_with_extension(input_file_path))
        copy2(input_file_path, new_input_file_path)
        input_file_path = new_input_file_path

    output_file_prefix = DEFAULT_OUTPUT_FILE_PREFIX

    if loggerc:
        logging.basicConfig(level=logging.DEBUG)

    remove_comments_from_file(input_file_path,
                              language,
                              output_file_dir_path=output_file_dir_path,
                              output_file_prefix=output_file_prefix,
                              archived=archived)

    if loggerc:
        out, err = capsys.readouterr()
        assert out.find("DEBUG")
        assert out.find("output file")

    input_file_name = _extract_file_name_with_extension(input_file_path)

    if provide_output_file_dir_path:
        actual_output_file_path = join(
            output_file_dir_path,
            '{}{}'.format(output_file_prefix, input_file_name))
    else:
        actual_output_file_path = join(
            dirname(input_file_path),
            '{}{}'.format(output_file_prefix, input_file_name))
    actual_output_file_contents = strip_spaces_and_linebreaks(
        _read_file(actual_output_file_path))

    expected_output_file_contents = strip_spaces_and_linebreaks(
        _read_file(output_file_path))

    assert actual_output_file_contents == expected_output_file_contents


@mark.parametrize('provide_output_file_dir_path', [True])
@mark.parametrize('archived', [False])
def test_remove_files_batch(provide_output_file_dir_path: bool,
                            archived: False,
                            capsys):
    logging.basicConfig(level=logging.DEBUG)
    input_directory = os.path.join(*MULTI_FILE)
    output_file_dir_path = input_directory

    actual_counts_files = sum(
        [len(files) for r, d, files in os.walk(input_directory)])

    remove_comments_batch(input_directory,
                          Language.get_from_string("Python"),
                          output_file_dir_path=output_file_dir_path,
                          output_file_prefix=DEFAULT_OUTPUT_FILE_PREFIX,
                          archived=archived)

    result_counts_files = sum(
        [len(files) for r, d, files in os.walk(input_directory)])

    clean_results(input_directory)

    assert result_counts_files / 2 == actual_counts_files


@mark.parametrize('input_path', [MULTI_FILE])
def test_packed_files(tmpdir_factory, input_path: list):
    input_directory = os.path.join(*MULTI_FILE)
    init__counts_files = sum(
        [len(files) for r, d, files in os.walk(input_directory)])

    tmp_pack_dir_path = join(
        tmpdir_factory.getbasetemp(), 'unpacked')
    makedirs(tmp_pack_dir_path, exist_ok=True)

    zipped = os.path.join(tmp_pack_dir_path, 'packed.zip')

    pack_back(input_directory, os.path.join(tmp_pack_dir_path, zipped))

    assert check_compressed(zipped)

    unpacked_sec = unpack_file(zipped)

    assert os.path.isdir(unpacked_sec)

    remove_comments_batch(
        unpacked_sec, Language.get_from_string("Python"),
        output_file_dir_path=None, output_file_prefix=None, archived=True)
    unpack_counts_files = sum(
        [len(files) for r, d, files in os.walk(unpacked_sec)])

    assert init__counts_files == unpack_counts_files / 2

    rmtree(tmp_pack_dir_path)


@mark.parametrize('language', Language)
@given(data=st.data())
def test_get_language_from_string(language: Language,
                                  data):
    assert Language.get_from_string(
        language.name, ignore_case=False) is language

    mixed_case_language_name_pattern = r'\A'
    for char in language.name:
        mixed_case_language_name_pattern += r'[{}]'.format(char)
    mixed_case_language_name_pattern += r'\Z'
    mixed_case_language_name_regex = re.compile(
        mixed_case_language_name_pattern, re.IGNORECASE)
    mixed_case_language_name = data.draw(
        st.from_regex(mixed_case_language_name_regex))
    assert Language.get_from_string(
        mixed_case_language_name, ignore_case=True) is language
