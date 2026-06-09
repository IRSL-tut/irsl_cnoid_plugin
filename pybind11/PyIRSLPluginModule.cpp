/**
   @author YoheiKakiuchi
*/

#include <cnoid/PyUtil>
#include <cnoid/PySignal>
#include "../src/IRSLPlugin.h"

using namespace cnoid;
namespace py = pybind11;

PYBIND11_MODULE(IRSLPlugin, m)
{
    m.doc() = "python-binding for IRSLPlugin";

    py::module::import("cnoid.Body");
    py::module::import("cnoid.Util");
    py::module::import("cnoid.Base");
#if 0
    py::class_< IRSLPlugin, ref_ptr<IRSLPlugin> > plugin_cls(m, "IRSLPlugin");
#endif
    m.def("sigPickedName", []() {
        IRSLPlugin *ptr = IRSLPlugin::instance();
        return ptr->sigPickedName();
    });
}
