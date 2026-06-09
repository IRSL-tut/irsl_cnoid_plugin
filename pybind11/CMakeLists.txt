###
set(TARGET PyIRSLPlugin)

add_cnoid_python_module(${TARGET}
  PyIRSLPluginModule.cpp
)

Message("pybind11: ${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR}")
if(${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR}/pybind11)
  Message ("Build(pybind11) : IRSLPlugin (independent)")
  # Build as an independent project
  target_link_libraries(${TARGET}
    CnoidIRSLPlugin Choreonoid::CnoidBody Choreonoid::CnoidUtil Choreonoid::CnoidBase
  )
  target_compile_definitions(${TARGET} PUBLIC ${CHOREONOID_COMPILE_DEFINITIONS})
  ##target_include_directories(${TARGET} /tmp)
  ## Not tested
  message("CHOREONOID_BIN_DIR: ${CHOREONOID_BIN_DIR}")
  if ("${CHOREONOID_BIN_DIR}" MATCHES ".*install.*")
    ## install
    message("in INSTALLSPACE")
    install(TARGETS ${TARGET} LIBRARY DESTINATION ${choreonoid_PYTHON_DIR})
  else()
    ## devel
    message("in DEVELSPACE")
    set_target_properties(${TARGET}
      PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${choreonoid_PYTHON_DIR})# copy the library for calling 'import cnoid.hoge'
  endif()
else()
  Message ("Build(pybind11) : IRSLPlugin (under choreonoid/ext)")
  # Build as a bundled project / under ext
  target_link_libraries(${TARGET}
    ${catkin_LIBRARIES}
    CnoidBody CnoidUtil CnoidBase
    )
endif()
