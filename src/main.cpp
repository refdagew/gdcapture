#include <Geode/Geode.hpp>

using namespace geode::prelude;

$on_mod(Loaded) {
    log::info("GDCapture {} loaded (Geode 5.11.2 / GD 2.2081 target).",
        Mod::get()->getVersion().toString()
    );
}
