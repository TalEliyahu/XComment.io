import os
import re
import sys
import codecs
import shutil
import tempfile
import logging
from pyunpack import Archive
from argparse import ArgumentParser
from enum import Enum, unique, auto
from itertools import chain
from os.path import join, dirname, realpath, basename
from typing import Callable, Dict, Sequence, Tuple, Optional


@unique
class Language(Enum):
    @classmethod
    def get_from_string(cls, name: str,
                        ignore_case: bool = True) -> 'Language':
        for n, v in vars(Language).items():
            if n == name or (ignore_case and n.lower() == name.lower()):
                return Language(v)

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
ANGLEBRACKET_EXCLAMATIONMARK_MULTILINE_COMMENT: Tuple[str, str] = (
    r'<!--', r'-->')
EQUALS_BEGIN_END_MULTILINE_COMMENT: Tuple[str, str] = (
    r'\=begin', r'\=end')

LANGUAGE_COMMENTS_MAP: Dict[
        Language, Tuple[Sequence[str], Sequence[Tuple[str, str]]]] = {
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


def getListOfLangs():
    return [lang.name for lang_name, lang in Language.__members__.items()]


def clean_results(path):
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            logging.debug("Processing file: " + currentFile)
            if currentFile.lower().startswith("rc."):
                os.remove(os.path.join(root, currentFile))


def check_compressed(filepath):
    """
    Checks if a file is compressed using the file extension.

    Parameters
    ----------
    filepath : string
        Path to input file.

    Returns
    -------
    boolean
        True if compressed, False if not.
    """

    comp_ext = ['.zip', '.bz2', '.tar', '.7z', '.ace', '.rar', '.adf', '.alz',
                '.cab', '.Z', '.cpio', '.deb', '.dms', '.gz', '.iso', '.lrz',
                '.lha', '.lzh', '.lz', '.lzma', '.lzo', '.rpm', '.rz', '.shn',
                '.xz', '.zoo']

    if os.path.splitext(filepath)[1].lower() in comp_ext:
        return True
    else:
        return False


def unpack_file(path):
    # using tmp dir with random name
    dirpath = tempfile.mkdtemp(dir=os.path.dirname(path))
    logging.debug(
        "Unpacked files placed to temp {} directory".format(dirpath))
    # check what archive exist
    if os.path.isfile(path):
        # check valid archive
        if check_compressed(path):
            logging.debug("Check compressed: Ok. Processing extract files")
            Archive(path).extractall(dirpath)
        else:
            logging.error('%s file not valid archive' % path)
            raise IOError('%s file not valid archive' % path)
    else:
        logging.error('%s file does not exist' % path)
        raise IOError('%s file does not exist' % path)

    resultpath = dirpath + "/"
    listd = os.listdir(resultpath)

    logging.debug("Files in archive :")

    if len(listd) >= 1:
        for i in listd:
            logging.debug(i)
    else:
        logging.error('Archive is empty')
        raise IOError('Archive is empty')

    return dirpath


def pack_back(upath, ipath):
    ipath = re.sub(r'(.zip|.rar)$', '', ipath)
    shutil.make_archive(ipath, 'zip', upath)


def construct_pattern(language: Language,
                      orphan_multiline_comments: bool = True) -> str:
    pattern = r''
    logging.debug('String processing')
    logging.debug('Current language - {}'.format(language))

    quotations = {SINGLE_QUOTATION, DOUBLE_QUOTATION}
    singleline_comments, multiline_comments = LANGUAGE_COMMENTS_MAP[language]
    # Should any of the quotation marks happen to indicate comments,
    # that can serve as the former no more.
    allowed_quotations = quotations.difference(
        chain(singleline_comments, multiline_comments))
    allowed_quotation_patterns = {
        r'\{0}.*?\{0}'.format(q) for q in allowed_quotations}
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
    return pattern


def remove_comments_from_string(source: str,
                                language: Language,
                                orphan_multiline_comments: bool = True) -> str:

    pattern = construct_pattern(language, orphan_multiline_comments)
    output = re \
        .compile(pattern, re.DOTALL | re.MULTILINE) \
        .sub(lambda m: "" if m.group(2) is not None else m.group(1), source)
    return output


def find_comments_from_string(source: str,
                              language: Language,
                              orphan_multiline_comments: bool = True) -> str:
    pattern = construct_pattern(language, orphan_multiline_comments)
    output = re \
        .compile(pattern, re.DOTALL | re.MULTILINE) \
        .finditer(source)

    output = [m.group(2) for m in output if m.group(2) is not None]
    return output


DEFAULT_OUTPUT_FILE_PREFIX: str = "rc."


def _write_to_output_file(output_file_contents: str,
                          input_file_path: str,
                          output_file_dir_path: str,
                          output_file_prefix: str) -> None:
    input_file_name = _extract_file_name_with_extension(input_file_path)
    if output_file_dir_path is None:
        output_file_dir_path = dirname(input_file_path)
    output_file_path = join(
        output_file_dir_path,
        '{}{}'.format(output_file_prefix, input_file_name))
    logging.debug('Write output file to {}'.format(output_file_path))

    _create_or_update_file(output_file_path, output_file_contents)


def remove_comments_from_file(input_file_path: str,
                              language: Language,
                              output_file_dir_path: Optional[str] = None,
                              output_file_prefix: str = DEFAULT_OUTPUT_FILE_PREFIX,  # noqa
                              archived: bool = None) -> None:

    logging.debug("Result directory set to {}".format(output_file_dir_path))

    # for input_file_path in input_file_paths:
    input_file_contents = _read_file(os.path.abspath(input_file_path))
    output_file_contents = remove_comments_from_string(
        input_file_contents, language)
    _write_to_output_file(
        output_file_contents, input_file_path, output_file_dir_path,
        output_file_prefix)


def find_comments_in_file(input_file_path: str,
                          language: Language,
                          output_file_dir_path: Optional[str] = None,
                          output_file_prefix: str = DEFAULT_OUTPUT_FILE_PREFIX,  # noqa
                          archived: bool = None) -> None:

    logging.debug("Result directory set to {}".format(output_file_dir_path))

    # for input_file_path in input_file_paths:
    input_file_contents = _read_file(os.path.abspath(input_file_path))
    comments = find_comments_from_string(input_file_contents, language)
    output_file_contents = "\n".join(comments)
    _write_to_output_file(
        output_file_contents, input_file_path, output_file_dir_path,
        output_file_prefix)


def _process_batch(processor: Callable[
                       [str, Language, str, str, bool], None],
                   dirpath: str,
                   language: Language,
                   output_file_dir_path: str,
                   output_file_prefix: str,
                   archived) -> None:
    if output_file_dir_path is None:
        output_file_dir_path = dirpath

    logging.debug("Result directory set to {}".format(output_file_dir_path))

    for paths, dirs, files in os.walk(dirpath):
        for input_file_path in files:
            input_file_abs = (
                os.path.join(os.path.abspath(paths), input_file_path))
            logging.debug("Processing file : {} ".format(input_file_abs))
            print(output_file_dir_path)

            processor(
                input_file_abs,
                language,
                output_file_dir_path=os.path.dirname(input_file_abs),
                output_file_prefix=output_file_prefix,
                archived=archived)


def remove_comments_batch(dirpath: str,
                          language: Language,
                          output_file_dir_path: Optional[str] = None,
                          output_file_prefix: str = DEFAULT_OUTPUT_FILE_PREFIX,  # noqa
                          archived: bool = None) -> None:

    _process_batch(remove_comments_from_file,
                   dirpath,
                   language,
                   output_file_dir_path,
                   output_file_prefix,
                   archived)


def find_comments_batch(dirpath: str,
                        language: Language,
                        output_file_dir_path: Optional[str] = None,
                        output_file_prefix: str = DEFAULT_OUTPUT_FILE_PREFIX,  # noqa
                        archived: bool = None) -> None:

    _process_batch(find_comments_in_file,
                   dirpath,
                   language,
                   output_file_dir_path,
                   output_file_prefix,
                   archived)


def _read_file(file_path: str,
               as_single_line: bool = False) -> str:
    """Source:
    https://github.com/webyneter/python-humble-utils
    """
    with codecs.open(
            file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = []
        for line in file.readlines():
            if as_single_line:
                line = line.replace(os.linesep, '')
            lines.append(line)
        return ''.join(lines)


def _create_or_update_file(file_path: str,
                           file_content: str = '',
                           file_content_encoding: str = 'utf-8') -> None:
    """Source:
    https://github.com/webyneter/python-humble-utils
    """
    with open(file_path, 'wb+') as file:
        file.write(file_content.encode(file_content_encoding))


def _extract_file_name_with_extension(file_path: str) -> str:
    """Source:
    https://github.com/webyneter/python-humble-utils
    """
    return basename(file_path)


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
    argument_parser.add_argument('-i',
                                 '--language-list',
                                 action='store_true')

    argument_parser.add_argument('-a',
                                 '--archived',
                                 action='store_true',
                                 help="""""")
    argument_parser.add_argument('-l',
                                 '--log',
                                 action='store_true',
                                 help="Enable logging")

    argument_parser.add_argument('-f',
                                 '--log_file',
                                 type=str,
                                 default=None,
                                 help="Specify path to log file")
    argument_parser.add_argument('-p',
                                 '--parse-comments',
                                 action='store_true',
                                 help="Print out comments")

    arguments = argument_parser.parse_args()

    if arguments.log:
        if arguments.log_file:
            logging.basicConfig(
                filename=arguments.log_file, level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("LOG File not specified, set to stdout")

    logging.debug('Start processing with arguments : ')
    logging.debug('Path to file :{}'.format(
        realpath(arguments.input_file_path)))
    logging.debug('Language : {} '.format(arguments.language))
    logging.debug('Output files dir  : {}'.format(
        arguments.output_file_dir_path))
    logging.debug('Output files prefix : {}'.format(
        arguments.output_file_prefix))
    logging.debug('File is archive : {}'.format(arguments.archived))
    logging.debug('Path to logfile : {}'.format(arguments.log_file))

    if arguments.language_list:
        print(getListOfLangs())
        sys.exit()
    if os.path.isdir(realpath(arguments.input_file_path)):
        logging.debug("Directory processing")
        remove_comments_batch(
            realpath(arguments.input_file_path),
            Language.get_from_string(arguments.language),
            output_file_dir_path=arguments.output_file_dir_path,
            output_file_prefix=arguments.output_file_prefix,
            archived=arguments.archived)
    else:
        if arguments.archived:
            logging.debug("Archive processing")
            unpackeddir = unpack_file(realpath(arguments.input_file_path))
            remove_comments_batch(
                unpackeddir,
                Language.get_from_string(arguments.language),
                output_file_dir_path=None,
                output_file_prefix=arguments.output_file_prefix,
                archived=arguments.archived)
            logging.debug("Archive will be packed again with changed sources")
            pack_back(unpackeddir, realpath(arguments.input_file_path))
            logging.debug("Remove temporary files: {}".format(unpackeddir))
            shutil.rmtree(unpackeddir)
        else:
            logging.debug("Single file processing")
            language = Language.get_from_string(arguments.language)
            input_file_path = realpath(arguments.input_file_path)
            if arguments.parse_comments:
                logging.debug("Printing comments only")
                find_comments_in_file(
                    input_file_path,
                    language,
                    output_file_dir_path=arguments.output_file_dir_path,
                    output_file_prefix=arguments.output_file_prefix,
                    archived=arguments.archived)
                sys.exit()
            remove_comments_from_file(
                input_file_path,
                language,
                output_file_dir_path=arguments.output_file_dir_path,
                output_file_prefix=arguments.output_file_prefix,
                archived=arguments.archived)


if __name__ == '__main__':
    main()
