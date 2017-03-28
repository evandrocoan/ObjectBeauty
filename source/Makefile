





PROGRAM_MAIN_DEBUGGER       = headers/debugger
PROGRAM_MAIN_FILE_NAME      = main

YAML_INCLUDE_FOLDER   = ./libraries/yaml-cpp/include
PROGRAM_INCLUDES_GCC  = -I. -I$(YAML_INCLUDE_FOLDER) -Llibraries/yaml-cpp/bin_g++ -lyaml-cpp
PROGRAM_INCLUDES_MSVC = /I. /I$(YAML_INCLUDE_FOLDER) libraries/yaml-cpp/bin_msvs/Release/libyaml-cppmd.lib

DOCTEST_TESTS_FILE   = unit_tests/doctest_tests
DOCTEST_DRIVER_CLASS = unit_tests/doctest_main


# g++ --std=c++11 main.cpp -I. -I./libraries/yaml-cpp/include -L./libraries/yaml-cpp -lyaml-cpp -o main
main: $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_MAIN_DEBUGGER).h
	g++ --std=c++11 $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_INCLUDES_GCC) -o $(PROGRAM_MAIN_FILE_NAME)



visual_studio: $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_MAIN_DEBUGGER).h
	./cl_env.bat $(PROGRAM_INCLUDES_MSVC) /EHsc /MD /Fe$(PROGRAM_MAIN_FILE_NAME).exe $(PROGRAM_MAIN_FILE_NAME).cpp

# Rule not used for now.
$(DOCTEST_DRIVER_CLASS).obj: $(DOCTEST_DRIVER_CLASS).cpp $(PROGRAM_MAIN_DEBUGGER).h
	./cl_env.bat $(PROGRAM_INCLUDES_MSVC) /EHsc /Fo$(DOCTEST_DRIVER_CLASS).obj $(DOCTEST_DRIVER_CLASS).cpp



doctest_tests: $(DOCTEST_DRIVER_CLASS).o $(PROGRAM_MAIN_DEBUGGER).h
	g++ --std=c++11 $(DOCTEST_DRIVER_CLASS).o $(DOCTEST_TESTS_FILE).cpp $(PROGRAM_INCLUDES_GCC) -o main

$(DOCTEST_DRIVER_CLASS).o: $(DOCTEST_DRIVER_CLASS).cpp
	g++ $(DOCTEST_DRIVER_CLASS).cpp $(PROGRAM_INCLUDES_GCC) -c -o $(DOCTEST_DRIVER_CLASS).o




clean:
	$(RM) $(PROGRAM_MAIN_FILE_NAME)
	$(RM) $(PROGRAM_MAIN_FILE_NAME).exe
	$(RM) $(PROGRAM_MAIN_FILE_NAME).obj



veryclean: clean
	$(RM) $(DOCTEST_DRIVER_CLASS).o


