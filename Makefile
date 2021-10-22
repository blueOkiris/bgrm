# Author: Dylan Turner
# Description: Build instructions for application

# Build variables

## Cpp compiler
CPPC :=		g++
CPPFLAGS :=	-O2 -Wall -Werror -std=c++17
INC :=		-Iinclude -I/usr/include/opencv4/
LD :=		g++
LDFLAGS :=	-lopencv_core \
			-lopencv_videoio \
			-lopencv_highgui \
			-lopencv_imgproc

## Project settings
OBJNAME :=	rmbg
SRC :=		$(wildcard src/*.cpp)
HFILES :=	$(wildcard include/*.hpp)

## Used for changing to a path with no spaces
ALT_BUILD_DIR := $(shell pwd)

# Targets

.PHONY : all
all : v4l2loopback.ko

## Create the v4l2loopback.ko
$(ALT_BUILD_DIR)/v4l2loopback/v4l2loopback.ko :
	$(shell \
		mkdir -p $(ALT_BUILD_DIR); \
		if [ ! -d "$(ALT_BUILD_DIR)/v4l2loopback" ]; then \
			git clone https://github.com/umlaeute/v4l2loopback \
				$(ALT_BUILD_DIR)/v4l2loopback; \
		else \
    		echo "Git directory already exists. Skipping clone."; \
		fi \
	)
	$(MAKE) -C $(ALT_BUILD_DIR)/v4l2loopback

## Get the v4l2loopback.ko from the build dir
v4l2loopback.ko : $(ALT_BUILD_DIR)/v4l2loopback/v4l2loopback.ko
	cp $< $@
