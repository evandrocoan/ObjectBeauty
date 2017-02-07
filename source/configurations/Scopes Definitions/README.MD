### The General Scoping Rules

Instead of always to writing the rule for opening and defining a commentary scope rule on every
settings files, create it at only one file per language characteristic scoping rules as aliases
which can be used across all settings files. We will not create one scoping setting file per
language because it would be pointless as the several languages uses the exactly construct tool.
For example, the C++ block comments constructs `/* */` are the same on C, Java and Pawn. So it
would be created one file per scoping concept as `block comments`. On this file all the scoping
rules for all languages will be defined and used across the configurations files.
```pawn
// This is the name used to reference this scope around the settings files.
Scope Name:
c++_like_block_comment

// This set on which languages this block should be included. Setting it to empty will allow
// it to be parsed for any languages.
Language Inclusion:
Java, C++, Pawn

// Defines a expression which will map the beginning of a exclusion block. Example, `/\*\*`
Scope Start:

// Defines a expression which will map the ending of a exclusion block. Example, `\*/`
Scope End:

// First Unit Test to be performed for this Scope. He we put the sample input data to be
// parsed and it must to generate a match for the specified Scope Expression.
Unit Test:
/** */
```
Each one of these data sets are store per file on the folder `Configurations/Scopes Definitions`.

Also, to avoid extra write up everywhere when specifically want to exclude something as from
all types of comments, you specify classes of Scopes on the main language configuration file
`language_settings.object-beauty`.
```pawn
Scope Class:
block_comment

Scope Blocks:
c++_like_block_comment
Matlab_like_block_coment
```


