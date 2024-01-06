# 用处是统计PDF文件中的文字数量
# 使用方法: python wc.py <file_path>
import pdfplumber as plb
import sys

# 检查是否提供了文件路径参数
if len(sys.argv) != 2:
    print("Usage: python wc.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]
del_f = [' ', '\n', '\s', '!', '.', '(', ')', ';', '-', '/', ':', ',', '. ', ', ', '；', '《', '》', '“', '"', ': ', ' (', ') ']

pdf_words = 0
with plb.open(file_path) as pdf:
    for page in pdf.pages:
        print(' ')
        print('[Page ' + str(page.page_number) + ']: ', end="")
        pg = page.extract_text()
        for j in del_f:
            pg = pg.translate({ord(i): '' for i in j})
        print(len(pg), end="")
        pdf_words += len(pg)

print(' ')
print('Word Count in Total:', pdf_words)
