#ifndef CNOID_IRSL_PLUGIN_H
#define CNOID_IRSL_PLUGIN_H

#include <cnoid/Plugin>
#include "exportdecl.plugin.h"

namespace cnoid {

class CNOID_EXPORT IRSLPlugin : public Plugin
{
public:
    static IRSLPlugin* instance();
    IRSLPlugin();
    ~IRSLPlugin();
    virtual bool initialize() override;
    virtual bool finalize() override;
    virtual const char* description() const override;

    SignalProxy<void(const std::string&)> sigPickedName();
    SignalProxy<void(const std::string&, int, int)> sigPickedNamePoint();
private:
    class Impl;
    Impl *impl;
};

}

#endif
