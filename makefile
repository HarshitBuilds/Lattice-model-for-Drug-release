PROG = ANT

SRC = main.cpp system.cpp
OBJS = ${SRC:.cpp=.o}

# Compiler configuration
CXX = g++
CXXFLAGS = -O3 -g -Wall 
INCLUDES = -I/usr/include/boost -I/usr/include/gsl
LDFLAGS = -L/usr/lib/x86_64-linux-gnu
LDLIBS = -lboost_program_options -lboost_system -lgsl -lgslcblas
RPATH = -Wl,-rpath=/usr/lib/x86_64-linux-gnu

all: $(PROG)

$(PROG): $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ $(LDLIBS) $(RPATH) -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf *.o

distclean: clean
	rm -f $(PROG) *.debug
