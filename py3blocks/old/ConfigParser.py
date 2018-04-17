import collections
import configparser

from itertools import chain


class ConfigParser(configparser.ConfigParser):

    class Interpolation(configparser.Interpolation):
        def before_get(self, parser, section, option, value, defaults):
            value = super().before_get(parser, section, option, value, defaults)

            value = value.replace('$BLOCK_NAME', section)
            value = value.replace('${BLOCK_NAME}', section)

            return value

    def __init__(self,
                 defaults=None,
                 dict_type=collections.OrderedDict,
                 allow_no_value=False,
                 *,
                 delimiters=('=', ':'),
                 comment_prefixes=('#', ';'),
                 inline_comment_prefixes=None,
                 strict=False,
                 empty_lines_in_values=True,
                 default_section='DEFAULT'):
        super().__init__(defaults=defaults,
                         dict_type=dict_type,
                         allow_no_value=allow_no_value,
                         delimiters=delimiters,
                         comment_prefixes=comment_prefixes,
                         inline_comment_prefixes=inline_comment_prefixes,
                         strict=strict,
                         empty_lines_in_values=empty_lines_in_values,
                         default_section=default_section,
                         interpolation=self.Interpolation())

    def _read(self, fp, fpname):
        fp = chain(['[{}]\n'.format(self.default_section)], fp)

        return super()._read(fp, fpname)
