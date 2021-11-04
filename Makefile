# https://www.tutorialspoint.com/makefile/makefile_example.htm
# https://opensource.com/article/18/8/what-how-makefile

# Define required macros here
SHELL = /bin/sh

composer-up:
	@echo "Create folders"
	mkdir -p chop output load rubberband split
