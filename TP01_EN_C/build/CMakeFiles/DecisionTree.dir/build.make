# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build

# Include any dependencies generated for this target.
include CMakeFiles/DecisionTree.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/DecisionTree.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/DecisionTree.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/DecisionTree.dir/flags.make

CMakeFiles/DecisionTree.dir/src/main.cpp.o: CMakeFiles/DecisionTree.dir/flags.make
CMakeFiles/DecisionTree.dir/src/main.cpp.o: /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/main.cpp
CMakeFiles/DecisionTree.dir/src/main.cpp.o: CMakeFiles/DecisionTree.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/DecisionTree.dir/src/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/DecisionTree.dir/src/main.cpp.o -MF CMakeFiles/DecisionTree.dir/src/main.cpp.o.d -o CMakeFiles/DecisionTree.dir/src/main.cpp.o -c /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/main.cpp

CMakeFiles/DecisionTree.dir/src/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/DecisionTree.dir/src/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/main.cpp > CMakeFiles/DecisionTree.dir/src/main.cpp.i

CMakeFiles/DecisionTree.dir/src/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/DecisionTree.dir/src/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/main.cpp -o CMakeFiles/DecisionTree.dir/src/main.cpp.s

CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o: CMakeFiles/DecisionTree.dir/flags.make
CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o: /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/DataLoader.cpp
CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o: CMakeFiles/DecisionTree.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o -MF CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o.d -o CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o -c /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/DataLoader.cpp

CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/DataLoader.cpp > CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.i

CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/DataLoader.cpp -o CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.s

CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o: CMakeFiles/DecisionTree.dir/flags.make
CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o: /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/Noeud.cpp
CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o: CMakeFiles/DecisionTree.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o -MF CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o.d -o CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o -c /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/Noeud.cpp

CMakeFiles/DecisionTree.dir/src/Noeud.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/DecisionTree.dir/src/Noeud.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/Noeud.cpp > CMakeFiles/DecisionTree.dir/src/Noeud.cpp.i

CMakeFiles/DecisionTree.dir/src/Noeud.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/DecisionTree.dir/src/Noeud.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/Noeud.cpp -o CMakeFiles/DecisionTree.dir/src/Noeud.cpp.s

# Object files for target DecisionTree
DecisionTree_OBJECTS = \
"CMakeFiles/DecisionTree.dir/src/main.cpp.o" \
"CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o" \
"CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o"

# External object files for target DecisionTree
DecisionTree_EXTERNAL_OBJECTS =

DecisionTree: CMakeFiles/DecisionTree.dir/src/main.cpp.o
DecisionTree: CMakeFiles/DecisionTree.dir/src/DataLoader.cpp.o
DecisionTree: CMakeFiles/DecisionTree.dir/src/Noeud.cpp.o
DecisionTree: CMakeFiles/DecisionTree.dir/build.make
DecisionTree: CMakeFiles/DecisionTree.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable DecisionTree"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/DecisionTree.dir/link.txt --verbose=$(VERBOSE)
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --blue --bold "Exécution du programme et du script Python après la compilation"
	/usr/bin/cmake -E echo Exécution\ du\ programme\ C++...
	/usr/bin/cmake -E env ./DecisionTree
	/usr/bin/cmake -E echo Exécution\ du\ script\ Python...
	/usr/bin/cmake -E env python3 /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/src/display.py

# Rule to build all files generated by this target.
CMakeFiles/DecisionTree.dir/build: DecisionTree
.PHONY : CMakeFiles/DecisionTree.dir/build

CMakeFiles/DecisionTree.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/DecisionTree.dir/cmake_clean.cmake
.PHONY : CMakeFiles/DecisionTree.dir/clean

CMakeFiles/DecisionTree.dir/depend:
	cd /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build /home/youcef/Documents/C++/Learning_C++/ML_C++/decision_tree/build/CMakeFiles/DecisionTree.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/DecisionTree.dir/depend
