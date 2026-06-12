////
#include <cnoid/SceneWidgetEventHandler>
#include <cnoid/SceneView>
#include <cnoid/SceneWidget>
#include <cnoid/SceneDrawables>
#include <fmt/format.h>

#include "IRSLPlugin.h"

//#define IRSL_DEBUG
#include "irsl_debug.h"

using namespace cnoid;

namespace {
IRSLPlugin* instance_ = nullptr;
}

namespace cnoid {

class IRSLPlugin::Impl : public SceneWidgetEventHandler
{
public:
    Impl() = delete;
    Impl(IRSLPlugin *_self) {
        self = _self;
    }

    void initialize() {
        uniq_id = SceneWidget::issueUniqueCustomModeId();
        SceneView::instance()->sceneWidget()->activateCustomMode(this, uniq_id);
        DEBUG_STREAM(" initialize : " << uniq_id );
    }

    IRSLPlugin *self;
    int uniq_id;

    SignalProxy<void(const std::string&)> sigPickedName() {
        return buttonPressedFunc;
    };
    Signal<void(const std::string&)> buttonPressedFunc;

#if 0
    //// overrides : SceneWidgetEventHandler
    virtual void onSceneModeChanged(SceneWidgetEvent* event) override;
    //
    virtual bool onPointerMoveEvent(SceneWidgetEvent* event) override;
    virtual void onPointerLeaveEvent(SceneWidgetEvent* event) override;
    //
    virtual bool onButtonPressEvent(SceneWidgetEvent* event) override;
    virtual bool onDoubleClickEvent(SceneWidgetEvent* event) override;
    virtual bool onButtonReleaseEvent(SceneWidgetEvent* event) override;
    //
    virtual bool onKeyPressEvent(SceneWidgetEvent* event) override;
    virtual bool onKeyReleaseEvent(SceneWidgetEvent* event) override;
    virtual bool onScrollEvent(SceneWidgetEvent* event) override;
    virtual void onFocusChanged(SceneWidgetEvent* event, bool on) override;
    virtual bool onContextMenuRequest(SceneWidgetEvent* event) override;
#endif
    virtual bool onButtonPressEvent(SceneWidgetEvent* event) override {
        //DEBUG_STREAM(" IRSL: press");

        SgNodePath enp = event->nodePath();

        int shape_id = SgNode::findClassId<SgShape>();
#if 0
        DEBUG_STREAM(" shape_id = " << shape_id);
        DEBUG_STREAM(" path = " << enp.size());
#endif
        for (int i = 0 ; i < enp.size(); i++) {
            SgNode *ptr = enp[i];
#if 0
            DEBUG_STREAM(" ---");
            DEBUG_STREAM(" " << static_cast<void *> (ptr));
            DEBUG_STREAM(" name: "  << ptr->name());
            DEBUG_STREAM(" class: " << ptr->className() << ", id: " << ptr->classId());
            DEBUG_STREAM(" attr: "  << ptr->attributes());
            if (ptr->hasUri()) {
                DEBUG_STREAM( " uri: " << ptr->uri());
            }
            if (ptr->hasAbsoluteUri()) {
                DEBUG_STREAM( " abs_uri: " << ptr->absoluteUri());
            }
            if (ptr->hasParents()) {
                int j = 0;
                for(auto it = ptr->parentBegin(); it != ptr->parentEnd(); it++, j++) {
                    DEBUG_STREAM("   p" << j << " : " << static_cast<void *>(*it));
                }
            }
#endif
            if ( ptr->classId() == shape_id ) {
                const std::string name(ptr->name());
                buttonPressedFunc(name);
            }
        }

        return false; // process event after here
        //return true; // do not process event after here
    };
};

} //// namespace cnoid

IRSLPlugin* IRSLPlugin::instance()
{
    return instance_;
}

IRSLPlugin::IRSLPlugin()
    : Plugin("IRSL")
{
    DEBUG_PRINT();
    setActivationPriority(99);
    instance_ = this;

    impl = new Impl(this);
}
IRSLPlugin::~IRSLPlugin()
{
    delete impl;
}
bool IRSLPlugin::initialize()
{
    impl->initialize();
    DEBUG_STREAM(" FINISH IRSLPlugin initialize");
    return true;
}
bool IRSLPlugin::finalize()
{
    DEBUG_PRINT();
    instance_ = nullptr;
    return true;
}
const char* IRSLPlugin::description() const
{
    static std::string text =
        fmt::format("IRSL Plugin Version {}\n", CNOID_FULL_VERSION_STRING) +
        "\n" +
        "Copyrigh (c) 2026 IRSL-tut Development Team.\n"
        "\n" +
        MITLicenseText() +
        "\n"  ;

    return text.c_str();
}

SignalProxy<void(const std::string&)> IRSLPlugin::sigPickedName()
{
    return impl->sigPickedName();
}

CNOID_IMPLEMENT_PLUGIN_ENTRY(IRSLPlugin);
