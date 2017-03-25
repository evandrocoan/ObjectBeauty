





PROGRAM_MAIN_DEBUGGER       = headers/debugger
PROGRAM_MAIN_FILE_NAME      = main

PROGRAM_INCLUDES_GCC  = -I.
PROGRAM_INCLUDES_MSVC = /I.

DOCTEST_TESTS_FILE   = unit_tests/doctest_tests
DOCTEST_DRIVER_CLASS = unit_tests/doctest_main


main: $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_MAIN_DEBUGGER).h
	g++ --std=c++11 $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_INCLUDES_GCC) -o $(PROGRAM_MAIN_FILE_NAME)
	./main



visual_studio: $(PROGRAM_MAIN_FILE_NAME).cpp $(PROGRAM_MAIN_DEBUGGER).h
	./cl_env.bat $(PROGRAM_INCLUDES_MSVC) /EHsc /Fe$(PROGRAM_MAIN_FILE_NAME).exe $(PROGRAM_MAIN_FILE_NAME).cpp
	./main

# Rule not used for now.
$(DOCTEST_DRIVER_CLASS).obj: $(DOCTEST_DRIVER_CLASS).cpp $(PROGRAM_MAIN_DEBUGGER).h
	./cl_env.bat $(PROGRAM_INCLUDES_MSVC) /EHsc /Fo$(DOCTEST_DRIVER_CLASS).obj $(DOCTEST_DRIVER_CLASS).cpp



doctest_tests: $(DOCTEST_DRIVER_CLASS).o $(PROGRAM_MAIN_DEBUGGER).h
	g++ --std=c++11 $(DOCTEST_DRIVER_CLASS).o $(DOCTEST_TESTS_FILE).cpp $(PROGRAM_INCLUDES_GCC) -o main
	./main --force-colors=true

$(DOCTEST_DRIVER_CLASS).o: $(DOCTEST_DRIVER_CLASS).cpp
	g++ $(DOCTEST_DRIVER_CLASS).cpp $(PROGRAM_INCLUDES_GCC) -c -o $(DOCTEST_DRIVER_CLASS).o




clean:
	$(RM) $(PROGRAM_MAIN_FILE_NAME)
	$(RM) $(PROGRAM_MAIN_FILE_NAME).exe
	$(RM) $(PROGRAM_MAIN_FILE_NAME).obj



veryclean: clean
	$(RM) $(DOCTEST_DRIVER_CLASS).o


