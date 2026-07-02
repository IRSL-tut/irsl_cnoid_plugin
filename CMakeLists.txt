set(sources
  src/IRSLPlugin.cpp
  )
set(headers
  src/IRSLPlugin.h
  src/exportdecl.plugin.h
  )
#set(libsources
#  )
#set(libheaders
#  )

if (NOT WIN32)
  add_definitions(-Wno-deprecated-declarations)
endif()
option(DEBUG_MESSAGE "print debug message" ON)

if(DEBUG_MESSAGE)
  add_definitions(-DIRSL_DEBUG)
endif()

Message ("org: ${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR}")

if(${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR})
  Message ("Build : IRSLPlugin (independent)")
  # Build as an independent project
  cmake_minimum_required(VERSION 3.10)
  project(irsl_cnoid_plugin)
  find_package(Choreonoid REQUIRED)
  #if ( ${CHOREONOID_VERSION_STRING} VERSION_GREATER_EQUAL "2.2.0" )
  #  CHOREONOID_QT_ADD_RESOURCES(RC_SRCS src/RA.qrc)
  #else()
  #  QT5_ADD_RESOURCES(RC_SRCS src/RA.qrc)
  #endif()
  if ( ${CHOREONOID_VERSION_STRING} VERSION_LESS "2.1.0" )
    add_definitions(-DUSE_OLD_OPTION)
  endif()
  set(CMAKE_CXX_STANDARD ${CHOREONOID_CXX_STANDARD})

  ### libraries
  #set(targetlib IRSLPluginLib)
  #choreonoid_add_library(${targetlib} SHARED ${libsources} ${RC_SRCS} HEADERS ${libheaders})
  #target_link_libraries(${targetlib} Choreonoid::CnoidBody Choreonoid::CnoidUtil ${CHOREONOID_QT_LIBRARIES})

  set(targetplugin CnoidIRSLPlugin)
  choreonoid_add_plugin(${targetplugin} ${sources} HEADERS ${headers})
  #target_link_libraries(${targetplugin} ${targetlib})
  target_link_libraries(${targetplugin} PUBLIC Choreonoid::CnoidBody Choreonoid::CnoidUtil Choreonoid::CnoidBase)
  include_directories(${PROJECT_SOURCE_DIR}/src)
  add_subdirectory(pybind11)
  ## install
else()
  Message ("Build : IRSLPlugin (under choreonoid/ext)")
  #if ( ${CHOREONOID_VERSION_STRING} VERSION_GREATER_EQUAL "2.2.0" )
  #  CHOREONOID_QT_ADD_RESOURCES(RC_SRCS src/RA.qrc)
  #else()
  #  QT5_ADD_RESOURCES(RC_SRCS src/RA.qrc)
  #endif()
  if ( ${CHOREONOID_VERSION_STRING} VERSION_LESS "2.1.0" )
    add_definitions(-DUSE_OLD_OPTION)
  endif()
  ### [todo] build libXXX.so and link it
  #set(targetlib IRSLPluginLib)
  #choreonoid_add_library(${targetlib} SHARED ${libsources} ${RC_SRCS} HEADERS ${libheaders})
  #target_link_libraries(${targetlib} PUBLIC CnoidBody CnoidUtil ${CHOREONOID_QT_LIBRARIES})
  #
  set(targetplugin CnoidIRSLPlugin)
  choreonoid_add_plugin(${targetplugin} ${sources} HEADERS ${headers})
  #target_link_libraries(${targetplugin} PUBLIC ${targetlib})
  target_link_libraries(${targetplugin} PUBLIC CnoidBody CnoidUtil CnoidBase)
  add_subdirectory(pybind11)
  #file(RELATIVE_PATH rel_src_dir ${PROJECT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
  install(DIRECTORY samples DESTINATION ${CHOREONOID_SHARE_SUBDIR}/irsl_cnoid_plugin)
endif()
