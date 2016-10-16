
# Object Beautifier

Is an Advanced Object Oriented Programming Text and Source Code Beautifier which come in place to easy
and improve the Source Code Beautifiers, using a well understood architecture, development
and configuration process.

1. https://en.wikipedia.org/wiki/Object-oriented_programming



___
## Initial Motivation Standards

>I think the best way to fix this is create a new `Beautifier` from 0. Why? Because I have seen the way Uncrustify is coded, and it is basically a structured programming for most things, and not fully documented. Therefore, it has a very high learning curve for new programmer get engaged/involved efficiently. Also is hard for new user to create a unified configuration file for all languages they use. For example, I to program on several languages, I need to create a big configuration file for each of them. In addition, when there is a change to my style, I need to go across several configuration files changing the same thing, if applicable on that target language.

>Then while building this new `Beautifier` take in account everybody in the world. Create a serious Object Oriented Program, fully documented and aiming it be to easily extended program and configurable by the users. Most things I want to point out is:

>1. Unify all the languages configuration and explicit very well what each settings is doing and what will be the results, using very clear and several examples. On this point, a GUI application written on Java or C++ QT, would be welcome to easy the settings creation. Also, this application could integrate the Unit Tests run as it integrates all settings together, or even better, the setting application would just show the Unit Texts Before and After the run for that settings specifically. This would enforce to each setting to have an Unit Tests setup.
>1. Code maintainability over performance. At this point, we should take care to not use exponential algorithms instead of quadratic and linear ones. Here I tough about several modules run against a give source code. On the first step, would be setup the whole source code as an object from the class SourceCode. Which would be manipulated by all the other modules. The SourceCode object would firstly be parsed to identify all the source code scopes, and after everything on the code being identified as class_declaration, conditional_keyword, creation_operator, etc, ... Several manipulation modules would receive one SourceCode object, and to perform its task, as the WhiteSpace module, which would control how all white spaces on the source code should be. The same to the New line Module, receiving a SourceCode object and control how all the new lines should be handled and perform them on the SourceCode object. The SpecialDelimiters module, would insert/remove brackets, paren, etc. 
>1. Zero-configuration, which can leave the file untouched. A module may be though as the AutoConfigurationModule (an IA heuristic), which would parse the file and detect how most the code is formatted and generate a settings file and apply it on the next modules. This would be very useful for anyone, which has its code well formatted, and do not want to set up a setting file, then the program would just get to know how it is coded and keep everything with the same pattern. For example, if someone usually use a bracket on a new line, but some lines not, then set the setting to always put them a new lines and fix the inconsistencies found when the later modules are run against it. Nevertheless, this decoupling from the settings to the parsing and formatting, does not look good as they are the very same thing, so couple everything together and who writes the new settings, is going to on the same place, write the tests, and the detection. This way, we may think about an interface called Settings where each module inherits its interface, and all settings would be an object of the class Settings, which inherits the ModuleSettingsInterface. However, firstly this would need a serious UML diagram and proper responsibilities attribution for each one of the classes before further discussion.

>For now I have not time to start this, but in some months I am going get engaged on it, if I still/keep interested on it.
https://github.com/uncrustify/uncrustify/issues/132#issuecomment-249205619



___
## Licence

All files in this repository are released under GNU General Public License v3.0, unless stated otherwise.
See:

1. The [LICENSE](LICENSE.TXT) file.
1. And the website [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).

For more information.

