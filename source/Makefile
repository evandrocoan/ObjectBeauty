





PROGRAM_MAIN_FILE_NAME      = main
PROGRAM_MAIN_FOLDER_INCLUDE = .

main: $(PROGRAM_MAIN_FILE_NAME).cpp
	g++ --std=c++11 $(PROGRAM_MAIN_FILE_NAME).cpp -I $(PROGRAM_MAIN_FOLDER_INCLUDE) -o $(PROGRAM_MAIN_FILE_NAME)
	./main

visual_studio: $(PROGRAM_MAIN_FILE_NAME).cpp
	./cl_env.bat /I$(PROGRAM_MAIN_FOLDER_INCLUDE) /EHsc /Fe$(PROGRAM_MAIN_FILE_NAME).exe $(PROGRAM_MAIN_FILE_NAME).cpp
	./main



CATCH_TESTS_FILE   = unit_tests/catch_tests
CATCH_DRIVER_CLASS = unit_tests/catch_main

catch_tests: $(CATCH_DRIVER_CLASS).o
	g++ --std=c++11 $(CATCH_DRIVER_CLASS).o $(CATCH_TESTS_FILE).cpp -I $(PROGRAM_MAIN_FOLDER_INCLUDE) -o main
	./main

$(CATCH_DRIVER_CLASS).o: $(CATCH_DRIVER_CLASS).cpp
	g++ $(CATCH_DRIVER_CLASS).cpp -I $(PROGRAM_MAIN_FOLDER_INCLUDE) -c -o $(CATCH_DRIVER_CLASS).o



DOCTEST_TESTS_FILE   = unit_tests/doctest_tests
DOCTEST_DRIVER_CLASS = unit_tests/doctest_main

doctest_tests: $(DOCTEST_DRIVER_CLASS).o
	g++ --std=c++11 $(DOCTEST_DRIVER_CLASS).o $(DOCTEST_TESTS_FILE).cpp -I $(PROGRAM_MAIN_FOLDER_INCLUDE) -o main
	./main --force-colors=true

$(DOCTEST_DRIVER_CLASS).o: $(DOCTEST_DRIVER_CLASS).cpp
	g++ $(DOCTEST_DRIVER_CLASS).cpp -I $(PROGRAM_MAIN_FOLDER_INCLUDE) -c -o $(DOCTEST_DRIVER_CLASS).o



clean:
	$(RM) $(PROGRAM_MAIN_FILE_NAME)
	$(RM) $(PROGRAM_MAIN_FILE_NAME).exe
	$(RM) $(PROGRAM_MAIN_FILE_NAME).obj



veryclean: clean
	$(RM) $(CATCH_DRIVER_CLASS).o
	$(RM) $(DOCTEST_DRIVER_CLASS).o


