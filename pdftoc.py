import utils
import sys
import pymupdf

toc: list[utils.Entry]


def elist_to_pymupdf(elist: list[utils.Entry]) -> list[tuple[int, str, int]]:
    pymupdf_toc: list[tuple[int, str, int]] = []

    def process_children(entry_children: list[utils.Entry], depth=2):
        for ec in entry_children:
            pymupdf_toc.append((depth, ec.name, ec.page))
            if ec.children:
                process_children(ec.children, depth+1)

    for e in elist:
        pymupdf_toc.append((1, e.name, e.page))
        if e.children:
            process_children(e.children)

    return pymupdf_toc


with open(sys.argv[1]) as f:
    toc = utils.toc_to_elist(f.read())

doc = pymupdf.open(sys.argv[2])
doc.set_toc(elist_to_pymupdf(toc))
doc.save(sys.argv[3])
