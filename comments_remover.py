import re
from argparse import ArgumentParser
from enum import Enum, unique, auto
from itertools import chain
from os.path import join, dirname
from os.path import realpath
from typing import Optional, Dict, Sequence, Tuple

from python_humble_utils.commands import read_file, create_or_update_file, extract_file_name_with_extension


@unique
class Language(Enum):
    @classmethod
    def from_string(cls, name: str) -> 'Language':
        ignore_case = True
        if ignore_case:
            name = name.lower()
        return Language(next(v for n, v in vars(Language).items() if n.lower() == name))

    PHP = auto()
    Python = auto()
    CSS = auto()
    HTML = auto()
    JavaScript = auto()
    ActionScript = auto()
    Ruby = auto()
    Assembly = auto()
    AppleScript = auto()
    Bash = auto()
    CSharp = auto()
    VB = auto()
    XML = auto()
    SQL = auto()
    C = auto()


SINGLE_QUOTATION: str = r"'"
DOUBLE_QUOTATION: str = r'"'

DOUBLE_SLASH_SINGLELINE_COMMENT: str = r'//'
HASH_SINGLELINE_COMMENT: str = r'#'
DOUBLE_MINUS_SINGLELINE_COMMENT: str = r'--'
SEMICOLON_SINGLELINE_COMMENT: str = r';'
APOSTROPHE_SINGLELINE_COMMENT: str = SINGLE_QUOTATION

SLASH_STAR_MULTILINE_COMMENT: Tuple[str, str] = (r'/\*', r'\*/')
ANGLEBRACKET_EXCLAMATIONMARK_MULTILINE_COMMENT: Tuple[str, str] = (r'<!--', r'-->')
EQUALS_BEGIN_END_MULTILINE_COMMENT: Tuple[str, str] = (r'\=begin', r'\=end')

LANGUAGE_COMMENTS_MAP: Dict[Language, Tuple[Sequence[str], Sequence[Tuple[str, str]]]] = {
    Language.PHP: (
        [
            DOUBLE_SLASH_SINGLELINE_COMMENT,
            HASH_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.Python: (
        [
            HASH_SINGLELINE_COMMENT,
        ], []
    ),
    Language.CSS: (
        [], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.HTML: (
        [], [
            ANGLEBRACKET_EXCLAMATIONMARK_MULTILINE_COMMENT,
        ]
    ),
    Language.JavaScript: (
        [
            DOUBLE_SLASH_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.ActionScript: (
        [
            DOUBLE_SLASH_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.Ruby: (
        [
            HASH_SINGLELINE_COMMENT,
        ], [
            EQUALS_BEGIN_END_MULTILINE_COMMENT,
        ]
    ),
    Language.Assembly: (
        [
            HASH_SINGLELINE_COMMENT,
            SEMICOLON_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.AppleScript: (
        [
            DOUBLE_MINUS_SINGLELINE_COMMENT,
            HASH_SINGLELINE_COMMENT,
        ], []
    ),
    Language.Bash: (
        [
            HASH_SINGLELINE_COMMENT,
        ], []
    ),
    Language.CSharp: (
        [
            DOUBLE_SLASH_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
    Language.VB: (
        [
            APOSTROPHE_SINGLELINE_COMMENT,
        ], []
    ),
    Language.XML: (
        [], [
            ANGLEBRACKET_EXCLAMATIONMARK_MULTILINE_COMMENT,
        ]
    ),
    Language.SQL: (
        [
            DOUBLE_MINUS_SINGLELINE_COMMENT,
        ], []
    ),
    Language.C: (
        [
            DOUBLE_SLASH_SINGLELINE_COMMENT,
        ], [
            SLASH_STAR_MULTILINE_COMMENT,
        ]
    ),
}


def remove_comments_from_string(source: str,
                                language: Language,
                                orphan_multiline_comments: bool = True) -> str:
    """

    :param source:
    :param language:
    :param orphan_multiline_comments: a workaround accounting for nested multiline comments.
    :return:
    """
    pattern = r''

    quotations = {SINGLE_QUOTATION, DOUBLE_QUOTATION}
    singleline_comments, multiline_comments = LANGUAGE_COMMENTS_MAP[language]
    # Should any of the quotation marks happen to indicate comments,
    # that can serve as the former no more.
    allowed_quotations = quotations.difference(chain(singleline_comments, multiline_comments))
    allowed_quotation_patterns = {r'\{0}.*?\{0}'.format(q) for q in allowed_quotations}
    quotation_pattern = r'({})'.format(r'|'.join(allowed_quotation_patterns))
    pattern += quotation_pattern

    comment_patterns = []
    for singleline_comment in singleline_comments:
        comment_patterns.append(r'{}[^\n\r]*$'.format(singleline_comment))
    for multiline_comment in multiline_comments:
        beginning = multiline_comment[0]
        ending = multiline_comment[1]
        comment_patterns.append(r'{}.*?{}'.format(beginning, ending))
        if orphan_multiline_comments:
            comment_patterns.append(beginning)
            comment_patterns.append(ending)
    comment_pattern = r'({})'.format(r'|'.join(comment_patterns))
    pattern += r'|{}'.format(comment_pattern)

    output = re \
        .compile(pattern, re.DOTALL | re.MULTILINE) \
        .sub(lambda match: "" if match.group(2) is not None else match.group(1), source)

    return output


DEFAULT_OUTPUT_FILE_PREFIX = "rc."


def remove_comments_from_file(input_file_path: str,
                              language: Language,
                              output_file_dir_path: Optional[str] = None,
                              output_file_prefix: str = DEFAULT_OUTPUT_FILE_PREFIX) -> None:
    input_file_contents = read_file(input_file_path)

    output_file_contents = remove_comments_from_string(input_file_contents, language)

    input_file_name = extract_file_name_with_extension(input_file_path)

    if output_file_dir_path is None:
        output_file_dir_path = dirname(input_file_path)
    output_file_path = join(output_file_dir_path,
                            '{}{}'.format(output_file_prefix, input_file_name))
    create_or_update_file(output_file_path, output_file_contents)


def main():
    argument_parser = ArgumentParser(description="""Comments remover.""")
    argument_parser.add_argument('input_file_path',
                                 type=str,
                                 help="""""")
    argument_parser.add_argument('language',
                                 type=str,
                                 choices=[l.name for l in Language],
                                 help="""""")
    argument_parser.add_argument('output_file_dir_path',
                                 type=str,
                                 default=None,
                                 nargs='?',
                                 help="""""")
    argument_parser.add_argument('output_file_prefix',
                                 type=str,
                                 default=DEFAULT_OUTPUT_FILE_PREFIX,
                                 nargs='?',
                                 help="""""")
    arguments = argument_parser.parse_args()

    remove_comments_from_file(realpath(arguments.input_file_path),
                              Language.from_string(arguments.language),
                              output_file_dir_path=arguments.output_file_dir_path,
                              output_file_prefix=arguments.output_file_prefix)


if __name__ == '__main__':
    main()
