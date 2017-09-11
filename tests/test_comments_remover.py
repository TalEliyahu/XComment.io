from os.path import join, dirname

from pytest import mark
from python_humble_utils.commands import read_file, extract_file_name_with_extension

from . import get_input_and_output_source_file_paths
from comments_remover import Language, remove_comments_from_string, remove_comments_from_file, \
    DEFAULT_OUTPUT_FILE_PREFIX


def strip_spaces_and_linebreaks(s: str) -> str:
    return ''.join(s.split())


@mark.parametrize('language', Language)
def test_when_removing_comments_from_string_given_valid_arguments_should_succeed(language: Language):
    input_file_path, output_file_path = get_input_and_output_source_file_paths(language)

    actual_output = remove_comments_from_string(read_file(input_file_path), language)

    actual_output = strip_spaces_and_linebreaks(actual_output)
    expected_output = strip_spaces_and_linebreaks(read_file(output_file_path))

    assert actual_output == expected_output


@mark.parametrize('language', Language)
@mark.parametrize('provide_output_file_dir_path', [True, False])
def test_when_removing_comments_from_file_given_output_file_dir_path_should_succeed(tmpdir_factory,
                                                                                    language: Language,
                                                                                    provide_output_file_dir_path: bool):
    input_file_path, output_file_path = get_input_and_output_source_file_paths(language)

    if provide_output_file_dir_path:
        output_file_dir_path = str(tmpdir_factory.mktemp(language.name))
    else:
        output_file_dir_path = None

    output_file_prefix = DEFAULT_OUTPUT_FILE_PREFIX

    remove_comments_from_file(input_file_path,
                              language,
                              output_file_dir_path=output_file_dir_path,
                              output_file_prefix=output_file_prefix)

    input_file_name = extract_file_name_with_extension(input_file_path)
    if provide_output_file_dir_path:
        actual_output_file_path = join(output_file_dir_path,
                                       '{}{}'.format(output_file_prefix, input_file_name))
    else:
        actual_output_file_path = join(dirname(input_file_path),
                                       '{}{}'.format(output_file_prefix, input_file_name))
    actual_output_file_contents = strip_spaces_and_linebreaks(read_file(actual_output_file_path))

    expected_output_file_contents = strip_spaces_and_linebreaks(read_file(output_file_path))

    assert actual_output_file_contents == expected_output_file_contents
