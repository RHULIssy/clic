'''
Parse plain text into initial XML format, divided into chapters and paragraphs.

We expect the following format:
(Book title)
(Book author)

  . . .

[PART I. (title of the part)]

(CHAPTER|BOOK|MORAL) (I|1). (title of the chapter)

 . . .

(CHAPTER|BOOK|MORAL) (II|2). (title of the chapter)

 . . .

Chapter numbering in CLiC is based on order of chapters in the text file, any
chapter number in the text is only visible in the chapter.

A book divided into parts has the part title appended to each chapter title.
Parts will be ignored when it comes to chapter numbering in CLiC.
'''
import cgi
import io
import os.path
import sys
import re
from lxml import etree

PART_BREAK = re.compile(
    '^' +
    '(PART|BOOK)' +
    ' ([0-9IVXLC]+)\.'
)
CHAPTER_BREAK = re.compile(
    '^' +
    '(APPENDIX|INTRODUCTION|PREFACE|CHAPTER|CONCLUSION|PROLOGUE|PRELUDE|MORAL)' +
    '\s?' +
    '([0-9IVXLC]*)\.'
)

def end_chapter(state, xml_out):
    paragraph_break("", state, xml_out)
    if state['in_chapter']:
        xml_out.write(u'</div>\n')
        state['in_chapter'] = False

def chapter_break(line, state, xml_out, force=False):
    """If line is a chapter break, start new chapter, return True"""
    if not(force or CHAPTER_BREAK.match(line)):
        return False

    if state['current_chapter'] == 0 and (force == 'preface' or line.startswith('INTRODUCTION') or line.startswith('PREFACE')):
        if state['in_chapter']:
            # We're already in a chapter 0, ignore the extra chapter 0 marker
            return False
        end_chapter(state, xml_out)
    else:
        end_chapter(state, xml_out)
        state['current_chapter'] += 1
    state['in_chapter'] = True
    state['current_paragraph'] = 1

    xml_out.write(u'<div id="%s.%d" subcorpus="%s" booktitle="%s" bookauthor="%s" book="%s" type="chapter" num="%d">\n' % (
        cgi.escape(state['book_abbreviation'], quote=True), state['current_chapter'],
        cgi.escape(state['subcorpus'], quote=True), cgi.escape(state['book_title'], quote=True),
        cgi.escape(state['book_author'], quote=True),
        cgi.escape(state['book_abbreviation'], quote=True), state['current_chapter'],
    ))
    xml_out.write(u'<title>%s%s%s</title>\n' % (
        cgi.escape(state['part_prefix']),
        ' ' if state['part_prefix'] and line.strip() else '',
        cgi.escape(line.strip()),
    ))
    return True


def paragraph_break(line, state, xml_out):
    """If line is empty, state has paragraph content, write a paragraph break, return True"""
    if line.strip() != '':
        # Not a paragraph-separator
        return False

    if state['paragraph_text'] == '':
        # Not in a paragraph, so don't do anything
        return False

    xml_out.write(u'<p pid="%d" id="%s.c%d.p%d">\n%s</p>\n\n' % (
        state['current_paragraph'],
        cgi.escape(state['book_abbreviation'], quote=True),
        state['current_chapter'] or 0,
        state['current_paragraph'],
        cgi.escape(state['paragraph_text'][1:]), # NB: Remove initial space
    ))
    state['current_paragraph'] += 1
    state['paragraph_text'] = ""
    return True


def paragraphs(lines, filename, subcorpus):
    xml_out = io.StringIO()

    # Define all useful state in a dict so we can pass-by-reference
    state = dict(
        part_prefix="",
        current_chapter=0,
        in_chapter=False,
        current_paragraph=1,
        paragraph_text="",
        book_title="",
        book_abbreviation=os.path.basename(filename).replace('.txt', ''),
        subcorpus=subcorpus,
    )

    xml_out.write(u"<div0 id=\"%s\" type=\"book\" subcorpus=\"%s\" filename=\"%s\">\n\n\n" % (state['book_abbreviation'], state['subcorpus'], os.path.basename(filename)))

    for index, line in enumerate(lines):
        # Title
        if index == 0 and line.strip() != '':
            state['book_title'] = line.strip()
            xml_out.write(u'<title>%s</title>\n' % cgi.escape(line.strip()))
            continue

        # Author
        if index == 1 and line.strip() != '':
            state['book_author'] = line.strip()
            xml_out.write(u'<author>%s</author>\n' % cgi.escape(line.strip()))
            continue

        m = PART_BREAK.match(line)
        if m:
            end_chapter(state, xml_out)
            state['part_prefix'] = line.strip()
            continue

        if chapter_break(line, state, xml_out):
            continue

        if paragraph_break(line, state, xml_out):
            # TODO: What about chapter 0 content? We're not wrapping that.
            continue

        if line.strip() != '':
            if not state['in_chapter']:
                # Didn't find a chapter marker. Add an implicit PREFACE or CHAPTER,
                # depending on if we've already seen a part marker
                chapter_break("", state, xml_out, force="chapter" if state['part_prefix'] else "preface")
            state['paragraph_text'] += ' ' + line.strip()

    end_chapter(state, xml_out)
    xml_out.write(u"\n\n</div0>\n")

    # Return a parsed tree of the output
    xml_out.seek(0)
    return etree.parse(xml_out)


if __name__ == "__main__":
    filename = sys.argv[1]
    tree = paragraphs(open(filename).readlines(), filename, subcorpus=sys.argv[2])
    tree.write(sys.argv[3])
