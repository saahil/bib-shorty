from optparse import OptionParser

mand_article_fields = ['author', 'title', 'journal', 'year']
mand_book_fields = ['author', 'editor', 'title', 'publisher', 'year']
mand_inproceedings_fields = ['author', 'title', 'booktitle', 'year']
mand_techreport_fields = ['author', 'title', 'institution', 'year']
mand_phdthesis_fields = ['author', 'title', 'school', 'year']
mand_misc_fields = ['title', 'howpublished']
mand_incollection_fields = ['author', 'title', 'booktitle', 'year']

def trim_authors(line):
    line = line.strip(',')
    author_block = line.split('=')[1].strip('{}')
    authors = author_block.split('and')
    new_authors = []
    for a in authors:
        if ',' not in a:
            new_authors.append(a)
        else:
            last, first = a.split(',')
            if not first[1]=='.':
                first = first.strip()[0] + '.'
            new_authors.append('%s, %s' %(last, first))
    new_authors = ' and '.join(new_authors)
    author_block = 'author={%s},'%(new_authors)
    line = author_block

    return line

def proc_block(in_block):
    out_block = []
    mand_fields = []

    line = in_block[0]

    if line.startswith('@article'):
        mand_fields = mand_article_fields
    elif line.startswith('@book'):
        mand_fields = mand_book_fields
    elif line.startswith('@inproceedings'):
        mand_fields = mand_inproceedings_fields
    elif line.startswith('@techreport'):
        mand_fields = mand_techreport_fields
    elif line.startswith('@phdthesis'):
        mand_fields=mand_phdthesis_fields
    elif line.startswith('@misc'):
        mand_fields=mand_misc_fields
    elif line.startswith('@incollection'):
        mand_fields=mand_incollection_fields

    for line in in_block:
        line = line.strip()
        if line.startswith('@') or line.startswith('}'):
            out_block.append(line+'\n')
            continue
        field = line.split('=')[0].strip()
        if field not in mand_fields:
            continue
        elif line.startswith('author'):
            line = trim_authors(line)
        out_block.append(line+'\n')

    return out_block

if __name__=='__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', dest='filename', help='bib file to be parsed')

    (options, args) = parser.parse_args()

    filename = options.filename
    
    f = open(filename, 'r')
    new_f = open(filename+'.short', 'w+')

    lines = f.readlines()
    i = 0
    while i<len(lines):
        line = lines[i]
        if not line.startswith('@'):
            i += 1
            continue
        
        cur_block = []
        braces_n = 1
        cur_block.append(line.strip())
        
        while braces_n>0:
            i += 1
            line = lines[i]
            braces_n += line.count('{')
            braces_n -= line.count('}')
            cur_block.append(line)

        out_block = proc_block(cur_block)
        print out_block
        for l in out_block:
            new_f.write(l)
        i += 1

    new_f.close()
    f.close()

