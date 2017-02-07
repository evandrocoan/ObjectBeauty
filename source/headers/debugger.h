/*********************** Licensing *******************************************************
*
*   Copyright 2016 @ Evandro Coan
*
*   Program Main Page: https://github.com/evandrocoan/ObjectBeautifier
*
*  This program is free software; you can redistribute it and/or modify it
*  under the terms of the GNU General Public License as published by the
*  Free Software Foundation; either version 3 of the License, or ( at
*  your option ) any later version.
*
*  This program is distributed in the hope that it will be useful, but
*  WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
*  General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*****************************************************************************************
*/

#include "utilities.h"



/**
 * Preprocessor directive designed to cause the current source file to be included only once in a
 * single compilation. Thus, serves the same purpose as #include guards, but with several
 * advantages, including: less code, avoidance of name clashes, and sometimes improvement in
 * compilation speed. In main file this is enabled by default.
 */
#pragma once



/**
 * This is to view internal program data while execution. Default value: 0
 * 
 *  0   Disables this feature.
 *  1   Basic debugging.
 */
#define DEBUG_LEVEL 0


#define DEBUG_LEVEL_DISABLED_DEBUG 0
#define DEBUG_LEVEL_BASIC_DEBUG    1


/**
 * MemoryManager debugging.
 */
#if DEBUG_LEVEL > DEBUG_LEVEL_DISABLED_DEBUG

/**
 * A value like a127 (111111) for 'g_debugLevel' enables all 'a' mask debugging levels. To enable all
 * debugging levels at once, use "a127 b127 c127" etc, supposing the level 64 is the highest to each
 * mask 'a', 'b', 'c', etc.
 * 
 * Level A debugging:
 * a0   - Disabled all debug.
 * a1   - Basic debug messages.
 * 
 * Level B debugging:
 * b0   - Disabled all debug.
 * b1   - Basic debug messages.
 */
const char* const g_debugLevel = "a1 b1";

#endif



#if DEBUG_LEVEL > DEBUG_LEVEL_DISABLED_DEBUG
#define DEBUG

#include <execinfo.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <cstring>
#include <iostream>
#include <string>
#include <cstdarg>

/**
 * Print like function for logging putting a new line at the end of string. See the variables
 * 'g_debugLevel', 'g_debugMask', for the avalibles levels.
 * 
 * @param level     the debugging desired level to be printed.
 * @param ...       variable number os formating arguments parameters.
 */
#define LOG( level, ... ) \
do \
{ \
    if( __computeDeggingLevel( #level ) ) \
    { \
        std::cout << format( __VA_ARGS__ ) << std::endl; \
    } \
} \
while( 0 )

/**
 * The same as LOGLN(...) just below, but do not put automatically a new line.
 */
#define LOGLN( level, ... ) \
do \
{ \
    if( __computeDeggingLevel( #level ) ) \
    { \
            std::cout << format( __VA_ARGS__ ); \
    } \
} \
while( 0 )

/**
 * The same as LOGLN(...), but it is for standard program output.
 */
#define PRINT( level, ... ) \
do \
{ \
    if( __computeDeggingLevel( #level ) ) \
    { \
        std::cout << format( __VA_ARGS__ ) << std::endl; \
    } \
} \
while( 0 )

/**
 * The same as LOG(...), but it is for standard program output.
 */
#define PRINTLN( level, ... ) \
do \
{ \
    if( __computeDeggingLevel( #level ) ) \
    { \
        std::cout << format( __VA_ARGS__ ); \
    } \
} \
while( 0 )


/**
 * Print to the standard out stream the stack trace until this call.
 */
inline void __printBacktrace()
{
#define BACKTRACE_SIZE 100
    
    int traceIndex;
    int traceLevels;
    
    void *buffer[ BACKTRACE_SIZE ];
    char **strings;
    
    traceLevels = backtrace( buffer, BACKTRACE_SIZE );
    std::cout << "backtrace() returned " << traceLevels << " addresses" << std::endl;
    
    strings = backtrace_symbols( buffer, traceLevels );
    
    if( strings == NULL )
    {
        std::cout << "ERROR! We failure at failing!" << std::endl;
        std::cout << "There are none backtrace_symbols!" << std::endl;
        exit( EXIT_FAILURE );
    }
    else
    {
        for( traceIndex = 0; traceIndex < traceLevels; traceIndex++ )
        {
            std::cout << strings[traceIndex] << std::endl;
        }
    }
    
    free( strings );
}

/**
 * Determines whether the given debug level is enabled.
 * 
 * @param debugLevel       the given char* string level to the debugger.
 * @return true when the current debug output is enabled, false otherwise.
 */
inline bool __computeDeggingLevel( const char* debugLevel )
{
#define COMPUTE_DEBUGGING_LEVEL_DEBUG      0
#define COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE 32
    
    int inputLevel;
    int builtInLevel;
    
    int inputLevelSize;
    int builtInLevelSize;
    
    int inputLevelTokenSize;
    int builtInLevelTokenSize;
    
    char* inputLevelToken;
    char* builtInLevelToken;
    
    char builtInLevelChar[ COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE ];
    char inputLevelChar  [ COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE ];
    char inputLevelChars [ COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE ][ COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE ];
    
    int        inputLevels  = 0;
    const char separator[2] = " ";
    
    inputLevelSize   = strlen( debugLevel );
    builtInLevelSize = strlen( g_debugLevel );
    
    if( 2 > inputLevelSize > COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE
        || 2 > builtInLevelSize > COMPUTE_DEBUGGING_DEBUG_INPUT_SIZE )
    {
        std::cout << "ERROR while processing the DEBUG LEVEL: " << debugLevel << std::endl;
        std::cout << "! The masks sizes are " << inputLevelSize << " and " << builtInLevelSize;
        std::cout << ", but they must to be between 1 and 32." << std::endl;
        
        __printBacktrace();
        exit( EXIT_FAILURE );
    }
    
    strcpy( inputLevelChar, debugLevel );
    strcpy( builtInLevelChar, g_debugLevel );
    
    // So, how do we debug the debugger?
#if COMPUTE_DEBUGGING_LEVEL_DEBUG > 0
    int currentExternLoop = 0;
    int currentInternLoop = 0;

    std::cout << "\ng_debugLevel: " << g_debugLevel << ", builtInLevelSize: " << builtInLevelSize ;
    std::cout << ", debugLevel: " << debugLevel << ", inputLevelSize: " << inputLevelSize  << std::endl;
#endif
    
    inputLevelToken = strtok( inputLevelChar, separator );
    
    do
    {
        strcpy( inputLevelChars[ inputLevels++ ], inputLevelToken );
    } while( ( inputLevelToken = strtok( NULL, separator ) ) != NULL );
    
    while( inputLevels-- > 0 )
    {
    #if COMPUTE_DEBUGGING_LEVEL_DEBUG > 0
        currentInternLoop = 0;
        std::cout << "CURRENT_ExternLoop: " << currentExternLoop++ << std::endl;
    #endif
        
        builtInLevelToken   = strtok( builtInLevelChar, separator );
        inputLevelTokenSize = strlen( inputLevelChars[ inputLevels ] );
        
        do
        {
            builtInLevelTokenSize = strlen( builtInLevelToken );
            
        #if COMPUTE_DEBUGGING_LEVEL_DEBUG > 0
            std::cout << "space" << std::endl;
            std::cout << "CURRENT_InternLoop: " << currentInternLoop++ << std::endl;
            
            std::cout << "builtInLevelToken: " << builtInLevelToken << std::endl;
            std::cout << "builtInLevelTokenSize: " << builtInLevelTokenSize << std::endl;
            std::cout << "inputLevelChars[" << inputLevels << "]: " << inputLevelChars[ inputLevels ] << std::endl;
            std::cout << "inputLevelTokenSize: " << inputLevelTokenSize << std::endl;
        #endif
            
            if( inputLevelTokenSize > 0
                && builtInLevelTokenSize > 0 )
            {
                if( isdigit( inputLevelChars[ inputLevels ][ 1 ] )
                    && isdigit( builtInLevelToken[ 1 ] ) )
                {
                    if( builtInLevelToken[ 0 ] == inputLevelChars[ inputLevels ][ 0 ] )
                    {
                        sscanf( &inputLevelChars[ inputLevels ][ 1 ], "%d", &inputLevel );
                        sscanf( &builtInLevelToken[ 1 ], "%d", &builtInLevel );
                        
                    #if COMPUTE_DEBUGGING_LEVEL_DEBUG > 0
                        std::cout << "builtInLevel: " << builtInLevel << std::endl;
                        std::cout << "inputLevel: " << inputLevel << std::endl;
                        std::cout << "Is activeated? " << ( ( inputLevel & builtInLevel ) > 0 ) << std::endl;
                    #endif
                        
                        if( ( inputLevel & builtInLevel ) > 0 )
                        {
                            return true;
                        }
                    }
                }
            }
            
        } while( ( builtInLevelToken = strtok( NULL, separator ) ) != NULL );
        
    #if COMPUTE_DEBUGGING_LEVEL_DEBUG > 0
        std::cout << "space" << std::endl;
    #endif
    }
    
    return false;
}

#else
    #define LOG( level, ... )
    #define LOGLN( level, ... )


/**
 * The same as LOGLN(...), but it is for standard program output when the debugging is disabled.
 */
#define PRINT( level, ... ) \
do \
{ \
    std::cout << format( __VA_ARGS__ ) << std::endl; \
} \
while( 0 )

/**
 * The same as LOG(...), but it is for standard program output when the debugging is disabled.
 */
#define PRINTLN( level, ... ) \
do \
{ \
    std::cout << format( __VA_ARGS__ ); \
} \
while( 0 )

#endif // #if DEBUG_LEVEL > 0





