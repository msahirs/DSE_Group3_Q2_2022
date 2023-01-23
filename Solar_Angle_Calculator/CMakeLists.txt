cmake_minimum_required(VERSION 3.0.0)
project(Solar_Angle_Calculator)


add_executable(SPA
spa.c
spa.h spatest.c)

add_executable(SPA_old
spa.c
spa.h spatest_old.c)