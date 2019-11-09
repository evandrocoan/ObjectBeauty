### The formatting is performed abstracted of language.

The languages still existing, however the formatting will not be based on languages
but in visual formatting concepts. The formatting based in visual formatting concepts.
There will not be a setting to add spaces in paren for java, c++, etc. There will be a
setting to add spaces in paren for specific regex and/or inclusion and exclusion laws
formed on that particular setting file, together within its Unit Tests.

Basically a setting file it will be very big and complex and only will treat a specific
kind of visual formatting concept. Therefore to simply allow how to choose and setup a
visual style for your own taste or needs, not all settings will be loaded to be processed
and applied to parse the source code. Moreover not loading any settings file will imply
on a zero-configuration, i.e., nothing will be changed on the source code after the parsing.

Each formatting rule file contains always the same blocks of data. Therefore a default
loader can be used for all settings to get their settings data from the disk. Also, each
setting will be loaded by its own thread, and not the opposite, first I read the setting
then I create the thread. Doing so increase the parallelism reality. Each rule setting
file will be equipped within the following data:
```pawn
// This is the rule loaded class this configuration is designed for. When this parser class
// will load its configuration, will it open this file to get its settings data. The file name
// must to be on the form `insert_spaces_inside_paren`.
Rule Name:
Insert spaces inside paren

// This set on which languages this block should be included. Setting it to empty will allow
// it to be parsed for any languages.
Languages Inclusion:
Java, Octave, Matlab, C++, Pawn, C, Javascript

// This will set which regions are set to allow the insertion process to happens. Each settings
// file can have from 1 until several inclusion blocks it wants to. For example, I can include
// only the lines set with the `^\s*#define\s*.*` regex expression where the contents of the
// regex expression match it. Defines a expression which will map the beginning of a
// inclusion block. Setting this block to empty will include all the source code. Setting an
// `Inclusion Block` after a `Exclusion Block` will perform the inclusion within that block.
// Example, `/\*\*`
Inclusion Blocks:

// This will set which regions are set to not allow the insertion to happens. The final
// operating region is the sequentially declarations' sum of the Inclusion/Exclusion Blocks
// by their declarations order. Each settings file can have from 0 until several exclusion
// blocks it wants to. Defines a expression which will map the beginning of a exclusion
// block. Setting this block to empty will not exclude anything. Example, `/\*\*`
Exclusion Blocks:
c++_like_block_comment
Matlab_like_block_coment

// First Unit Test to be performed for this setting. This sets the languages which this Unit Test
// is valid to. It does not accept Languages names, but the Scopes. This is because each test
// has to be done per scope and not per language.
Unit Test Scope:

// He we put the sample input data to be parsed and generate the final formatted/beautified
// code.
Unit Test Input:
if(hi)

// This is the first Unit Test expected result for this settings file. You must to let this
// result exactly as you wish and properly set the settings to generate it.
Unit Test Expected Output:
if( hi )

// Here will be output the Unit Test result from the input data just above.
Unit Test Actual Output:
if( hi )
```

Each one of these data sets are store per file on the folder `Configurations/Formatting Rules`.



