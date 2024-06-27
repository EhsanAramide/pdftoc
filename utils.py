# https://github.com/yutayamamoto/pdfoutline/blob/master/pdfoutline.py

import re

class Entry():

    def __init__(self, name, page, children):
        self.name = name
        self.page = page
        self.children = children  # Entry list

    def pritty_print(self, depth):
        print(depth * '  ' + self.name + ':' + str(self.page))
        for c in self.children:
            c.pritty_print(depth+1)


# Parse the start of the line for whitespace characters and return "tab";
# should only be called once on first occurrence of an indent while tab == ""
def parse_tab(line):
    tab = ""

    # add whitespace characters to tab
    for ch in line:
        if (ch.isspace()):
            tab += ch
        else:
            break

    return tab


def toc_to_elist(toc) -> list[Entry]:

    tab = ""  # indentation character(s) evaluated and assigned to this later
    lines = toc.split('\n')
    cur_entry = [[]]  # current entries by depth
    offset = 0

    for line in lines:

        # if indentation style hasn't been evaluated yet and the line starts
        # with a whitespace character, assume its an indent and assign all the
        # leading whitespace to tab
        if ((tab == "") and (line != "") and (line[0].isspace())):
            tab = parse_tab(line)

        depth = 0

        # determine depth level of indent
        if (tab != ""):
            # find length of leading whitespace in string
            ws_len = 0
            for ch in line:
                if (ch.isspace()):
                    ws_len += 1
                else:
                    break

            # count indent level up to first non-whitespace character;
            # allows for "indents" to appear inside section titles e.g. if an
            # indent level of a single space was chosen
            depth = line.count(tab, 0, ws_len)

        line = line.split('#')[0].strip()  # strip comments and white spaces

        if not line:
            continue

        if line[0] == '+':
            offset += int(line[1:])
            continue

        if line[0] == '-':
            offset -= int(line[1:])
            continue

        try:
            (name, page) = re.findall(r'(.*) (\d+)$', line)[0]
            page = int(page) + offset
            cur_entry = cur_entry[:depth+1] + [[]]
            cur_entry[depth].append(Entry(name, page, cur_entry[depth+1]))

        except:
            print('syntax error in toc-file. line:\n' + line)
            exit(1)

    return cur_entry[0]
