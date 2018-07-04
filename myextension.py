# existing markdown inlinePatterns
# https://github.com/Python-Markdown/markdown/blob/2.6/markdown/inlinepatterns.py

from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern, Pattern
from markdown.inlinepatterns import SubstituteTagPattern
from markdown.util import etree
from markdown import util

DEL_RE = r'(~)(.*?)~' # Strikeout in slack
INS_RE = r'(__)(.*?)__' # not slack ;-)
STRONG_RE = r'(\*)(.*?)\*' # Bold in slack
EMPH_RE = r'(_)(.*?)_' # Italics in slack
CODE_RE = r'(`)(.*?)`' # code in slack
PREFORMATTED_RE = r'(```\n)(.*?)\n```' # preformatted in slack
NEWLINE_RE = r'\n' # newline in slack
USERNAME_RE = r'(<@)(.*?)>' # username tag
CHANNEL_RE = r'(<#.+?\|)(.*?)>' # username tag

class MyExtension(Extension):
  def extendMarkdown(self, md, md_globals):
    # del md.inlinePatterns['backtick'] # `backtick style`

    del_tag = SimpleTagPattern(DEL_RE, 'del')
    md.inlinePatterns.add('del', del_tag, '>not_strong')

    ins_tag = SimpleTagPattern(INS_RE, 'ins')
    md.inlinePatterns.add('ins', ins_tag, '>del')

    strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
    md.inlinePatterns['strong'] = strong_tag

    emph_tag = SimpleTagPattern(EMPH_RE, 'em')
    md.inlinePatterns.add('em', emph_tag, '>del')

    preformatted_tag = SimpleTagPattern(PREFORMATTED_RE, 'pre')
    md.inlinePatterns.add('preformatted', preformatted_tag, '<backtick')

    newline_tag = SubstituteTagPattern(NEWLINE_RE, 'br')
    md.inlinePatterns.add('linebreak2', newline_tag, '>linebreak') 

    username_tag = SimpleTagPatternWithClassOptions(USERNAME_RE, 'span', 'username')
    md.inlinePatterns.add('username', username_tag, '<link')

    channel_tag = SimpleTagPatternWithClassOptions(CHANNEL_RE, 'span', 'channel')
    md.inlinePatterns.add('channel', channel_tag, '<username')

class SimpleTagPatternWithClassOptions(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern.
    """
    def __init__(self, pattern, tag, class_name_in_html):
        Pattern.__init__(self, pattern)
        self.tag = tag
        self.class_name_in_html = class_name_in_html

    def handleMatch(self, m):
        el = util.etree.Element(self.tag)
        el.text = m.group(3)
        el.set('class', self.class_name_in_html)
        return el
