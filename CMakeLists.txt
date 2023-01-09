cmake_minimum_required(VERSION 3.0.0)
project(DSE_GROUP_Q2_2022)

add_subdirectory(Solar_Angle_Calculator)
include(CTest)
enable_testing()

add_executable(cmake_test
        main.cpp)

# add_custom_target(SecondaryAllBuild)
# add_dependencies(SecondaryAllBuild Solar_Angle_Calculator)
