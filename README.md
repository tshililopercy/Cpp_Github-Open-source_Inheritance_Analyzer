# Cpp_Github-Open-source_Inheritance_Analyzer

Software tool that analyzes inheritance of GitHub Open source c++ projects, written using clang with python3.11. It uses these metrics to analyse (Method Novelty, Abstract classes, Overriden Methods, Public interfaces, Hierachy Depth, Width and Types of classes used as Types(to evaluate if inheritance is being used polymorphically(Role modelling or as Re-use)

It Runs on windows and Linux (Ubuntu 22.04)

### Installation:

Ubuntu:

1. `sudo pip install libclang-dev`

Windows:

1. install clang using MSYS2 (link)...set the installation directory (msys64\mingw64\bin) on the path.
2. verify the installation

For Both Linux and Windows:

3. `pip install Gitpython`
4. `pip install ccsyspath`
5. `git clone https://github.com/tshililopercy/Cpp_Github-Open-source_Inheritance_Analyzer.git`
