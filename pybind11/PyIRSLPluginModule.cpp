/**
   @author YoheiKakiuchi
*/

#include <cnoid/PyUtil>
#include <cnoid/PySignal>
#include "../src/IRSLPlugin.h"
#include <memory>

using namespace cnoid;
namespace py = pybind11;

typedef std::shared_ptr<IRSLPlugin> IRSLPluginPtr;

PYBIND11_MODULE(IRSLPlugin, m)
{
    m.doc() = "python-binding for IRSLPlugin";

    py::module::import("cnoid.Body");
    py::module::import("cnoid.Util");
    py::module::import("cnoid.Base");

    PySignal<void(const std::string&, int, int)>(m, "VoidStringIntIntSignal");

    py::class_< IRSLPlugin, IRSLPluginPtr > plugin_cls(m, "IRSLPlugin");
    plugin_cls
        .def_static("instance", &IRSLPlugin::instance, py::return_value_policy::reference)
        .def("sigPickedName", &IRSLPlugin::sigPickedName)
        .def("sigPickedNamePoint", &IRSLPlugin::sigPickedNamePoint)
    ;
}
