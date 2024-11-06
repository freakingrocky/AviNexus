CXX = g++
CXXFLAGS = -std=c++17 -D_GLIBCXX_USE_CXX11_ABI=0 -D_FILE_OFFSET_BITS=64 -lstdc++fs -Wall -Wextra -O2
LIBS = -lzip -lstdc++fs

TARGET = unzip_and_organize
SRCS = unzip_and_organize.cpp
OBJS = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS) $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean