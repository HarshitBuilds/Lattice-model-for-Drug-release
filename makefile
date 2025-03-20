PROG = ANT

SRC = main.cpp system.cpp
OBJS = ${SRC:.cpp=.o}

# Compiler configuration
CXX = g++
CXXFLAGS = -O3 -g -Wall 
INCLUDES = -I/home/root1/Desktop/boost/include -I/home/root1/Desktop/gsl/include
LDFLAGS = -L/home/root1/Desktop/boost/lib -L/home/root1/Desktop/gsl/lib
LDLIBS = -lboost_program_options -lgsl -lgslcblas
RPATH = -Wl,-rpath=/home/root1/Desktop/gsl/lib:/home/root1/Desktop/boost/lib

all: $(PROG)

$(PROG): $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ $(LDLIBS) $(RPATH) -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf *.o

distclean: clean
	rm -f $(PROG) *.debug
