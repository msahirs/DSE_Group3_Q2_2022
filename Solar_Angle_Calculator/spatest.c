

/////////////////////////////////////////////
//          SPA TESTER for SPA.C           //
//                                         //
//      Solar Position Algorithm (SPA)     //
//                   for                   //
//        Solar Radiation Application      //
//                                         //
//             August 12, 2004             //
//                                         //
//   Filename: SPA_TESTER.C                //
//                                         //
//   Afshin Michael Andreas                //
//   afshin_andreas@nrel.gov (303)384-6383 //
//                                         //
//   Measurement & Instrumentation Team    //
//   Solar Radiation Research Laboratory   //
//   National Renewable Energy Laboratory  //
//   1617 Cole Blvd, Golden, CO 80401      //
/////////////////////////////////////////////

/////////////////////////////////////////////
// This sample program shows how to use    //
//    the SPA.C code.                      //
/////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include "spa.h"  //include the SPA header file

int main (int argc, char *argv[])
{
    spa_data spa;  //declare the SPA structure
    int result;
    float min, sec;

    int REQ_ARGS = 18;

    //enter required input values into SPA structure
    // &argv[1] -> spa.year;

    if (argc < REQ_ARGS)
    {
        printf("Incorrect number of input arguments! Expected %2d,\
                got%2d\n\nProgram Terminated", REQ_ARGS, argc - 1);
        
        return -1;
    };
    
    spa.year          = atoi(argv[1]);
    spa.month         = atoi(argv[2]);
    spa.day           = atoi(argv[3]);
    spa.hour          = atoi(argv[4]);
    spa.minute        = atoi(argv[5]);
    spa.second        = atof(argv[6]);
    spa.timezone      = atof(argv[7]);
    spa.delta_ut1     = atof(argv[8]);
    spa.delta_t       = atof(argv[9]);
    spa.longitude     = atof(argv[10]);
    spa.latitude      = atof(argv[11]);
    spa.elevation     = atof(argv[12]);
    spa.pressure      = atof(argv[13]);
    spa.temperature   = atof(argv[14]);
    spa.slope         = atof(argv[15]);
    spa.azm_rotation  = atof(argv[16]);
    spa.atmos_refract = atof(argv[17]);
    spa.function      = atof(argv[18]);

    // spa.year          = 2022;
    // spa.month         = 7;
    // spa.day           = 1;
    // spa.hour          = 12;
    // spa.minute        = 30;
    // spa.second        = 30;
    // spa.timezone      = 2.0;
    // spa.delta_ut1     = 0;
    // spa.delta_t       = 67;
    // spa.longitude     = 4.3;
    // spa.latitude      = 51.98;
    // spa.elevation     = 1000;
    // spa.pressure      = 1015.3;
    // spa.temperature   = 25;
    // spa.slope         = 0;
    // spa.azm_rotation  = 0;
    // spa.atmos_refract = 0.5667;
    // spa.function      = SPA_ZA_INC;

    //call the SPA calculate function and pass the SPA structure

    result = spa_calculate(&spa);

    if (result == 0)  //check for SPA errors
    {
        //display the results inside the SPA structure

        printf("%.6f ",spa.jd); //Julian Day
        printf("%.6e ",spa.l); //L
        printf("%.6e ",spa.b); //B
        printf("%.6f ",spa.r); //R
        printf("%.6f ",spa.h); //H
        printf("%.6e ",spa.del_psi); //Delta PSI
        printf("%.6e ",spa.del_epsilon); //Delta Epsilon
        printf("%.6f ",spa.epsilon); //Epsilon
        printf("%.6f ",spa.zenith); //Zenith
        printf("%.6f ",spa.azimuth_astro); //Azimuth (westward from south facing)
        printf("%.6f ",spa.incidence); //Incidence
        printf("%.6f ",spa.del_e); //zenith refraction correction

        /*
        min = 60.0*(spa.sunrise - (int)(spa.sunrise));
        sec = 60.0*(min - (int)min);
        printf("%02d:%02d:%02d ", (int)(spa.sunrise), (int)min, (int)sec); //Sunrise

        min = 60.0*(spa.sunset - (int)(spa.sunset));
        sec = 60.0*(min - (int)min);
        printf("%02d:%02d:%02d ", (int)(spa.sunset), (int)min, (int)sec); //Sunset
        */

        // printf("\n");

    } else printf("SPA Error Code: %d\n", result);

    return 0;
}

/////////////////////////////////////////////
// The output of this program should be:
//
//Julian Day:    2452930.312847
//L:             2.401826e+01 degrees
//B:             -1.011219e-04 degrees
//R:             0.996542 AU
//H:             11.105902 degrees
//Delta Psi:     -3.998404e-03 degrees
//Delta Epsilon: 1.666568e-03 degrees
//Epsilon:       23.440465 degrees
//Zenith:        50.111622 degrees
//Azimuth:       194.340241 degrees
//Incidence:     25.187000 degrees
//Sunrise:       06:12:43 Local Time
//Sunset:        17:20:19 Local Time
//
/////////////////////////////////////////////
