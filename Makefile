# blockchain101 (c) by Taibiao Guo.
#
# 该Makefile 用于编译 Beamer 制作的课件
# 运行环境需求：Linux、Texlive、evince reader
#

Compiler = xelatex -shell-escape -interaction=nonstopmode -outdir=out 
Reader = evince

Target = ./src/chTemplate.pdf
Source = ./src/chTemplate.tex
TmpFile = *.out *.log *.aux *.nav *.snm *.toc *.vrb *.pyg *.nav

$(Target): $(Source)
	$(Compiler) $(Source)
	$(Compiler) $(Source)
	
# make all
# 生成所有的课件
.PHONY: clean
all: $(Target) clean read

# make read <number>
# 打开指定的课件并阅读
# 如果未编译首先执行编译
# 如果未指定课件名字，则默认为0.pdf
.PHONY read
read:
	$(Reader) $(Taget)

# make clean
# 清除编译产生的所有中间文件和日志文件
.PHONY clean
clean:
	find . -name "*.out"  | xargs rm -f
	find . -name "*.log"  | xargs rm -f
	find . -name "*.aux"  | xargs rm -f
	find . -name "*.nav"  | xargs rm -f
	find . -name "*.snm"  | xargs rm -f
	find . -name "*.toc"  | xargs rm -f
	find . -name "*.vrb"  | xargs rm -f
	find . -name "*.pyg"  | xargs rm -f
	find . -name "*.nav"  | xargs rm -f
	find . -name "*.atfi"  | xargs rm -f
	find . -name "*.toc"  | xargs rm -f
	find  -name "*.*~"  | xargs rm -f
	find  -name "*~"  | xargs rm -f

# make cleanall
# 清除编译产生的中间文件、日志文件和课件
.PHONY cleanall
cleanall:
	-rm -r $(TmpFile) $(Target)

