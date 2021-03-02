cmake_minimum_required(VERSION 3.4)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

option(WITH_GALILEO "Enable galileo support" ON)
option(WITH_BEIDOU "Enable beidou support" ON)
option(WITH_QZSS "Enable qzss support" ON)
option(WITH_IRNSS "Enable irnss support" ON)

set(rtklib_DIR ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder)

set(SRCS_FILES
    ${rtklib_DIR}/src/convgpx.c
    ${rtklib_DIR}/src/convkml.c
    ${rtklib_DIR}/src/convrnx.c
    ${rtklib_DIR}/src/datum.c
    ${rtklib_DIR}/src/download.c
    ${rtklib_DIR}/src/ephemeris.c
    ${rtklib_DIR}/src/geoid.c
    ${rtklib_DIR}/src/gis.c
    ${rtklib_DIR}/src/ionex.c
    ${rtklib_DIR}/src/lambda.c
    ${rtklib_DIR}/src/options.c
    ${rtklib_DIR}/src/pntpos.c
    ${rtklib_DIR}/src/postpos.c
    ${rtklib_DIR}/src/ppp.c
    ${rtklib_DIR}/src/ppp_ar.c
    ${rtklib_DIR}/src/preceph.c
    ${rtklib_DIR}/src/rcvraw.c
    ${rtklib_DIR}/src/rinex.c
    ${rtklib_DIR}/src/rtcm.c
    ${rtklib_DIR}/src/rtcm2.c
    ${rtklib_DIR}/src/rtcm3.c
    ${rtklib_DIR}/src/rtcm3e.c
    ${rtklib_DIR}/src/rtkcmn.c
    ${rtklib_DIR}/src/rtkpos.c
    ${rtklib_DIR}/src/rtksvr.c
    ${rtklib_DIR}/src/sbas.c
    ${rtklib_DIR}/src/solution.c
    ${rtklib_DIR}/src/stream.c
    ${rtklib_DIR}/src/streamsvr.c
    ${rtklib_DIR}/src/tides.c
    ${rtklib_DIR}/src/tle.c
    ${rtklib_DIR}/src/rcv/binex.c
    ${rtklib_DIR}/src/rcv/crescent.c
    ${rtklib_DIR}/src/rcv/javad.c
    ${rtklib_DIR}/src/rcv/novatel.c
    ${rtklib_DIR}/src/rcv/nvs.c
    ${rtklib_DIR}/src/rcv/rt17.c
    ${rtklib_DIR}/src/rcv/septentrio.c
    ${rtklib_DIR}/src/rcv/skytraq.c
    ${rtklib_DIR}/src/rcv/ss2.c
    ${rtklib_DIR}/src/rcv/ublox.c
)

set(HDRS_FILES
    ${rtklib_DIR}/src/rtklib.h
)

add_library(rtklib ${SRCS_FILES} ${HDRS_FILES})
target_include_directories(rtklib PUBLIC ${rtklib_DIR}/src/)
target_compile_definitions(rtklib 
    PRIVATE
        _CRT_SECURE_NO_WARNINGS
        _WINSOCK_DEPRECATED_NO_WARNINGS
    PUBLIC
        ENAGLO
)

if (WITH_GALILEO)
    target_compile_definitions(rtklib PUBLIC ENAGAL)
endif()

if (WITH_BEIDOU)
    target_compile_definitions(rtklib PUBLIC ENACMP)
endif()

if (WITH_QZSS)
    target_compile_definitions(rtklib PUBLIC ENAQZS)
endif()

if (WITH_IRNSS)
    target_compile_definitions(rtklib PUBLIC ENAIRN)
endif()

if (WIN32)
    target_link_libraries(rtklib PRIVATE Winmm Ws2_32)
endif()

if (BUILD_SHARED_LIBS AND WIN32)
    target_compile_definitions(rtklib PRIVATE WIN_DLL)
endif()

install(TARGETS rtklib
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(FILES ${HDRS_FILES} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})