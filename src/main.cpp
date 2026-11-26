#include <Geode/Geode.hpp>
#include <Geode/utils/web.hpp>
#include <Geode/utils/async.hpp>

using namespace geode::prelude;

$on_mod(Loaded) {
    log::info("GDCapture {} loaded.", Mod::get()->getVersion().toString());

    auto request = web::WebRequest();
    request.header("Content-Type", "application/json");
    request.bodyString(R"({"type":"geode-loaded","message":"Hello from Geometry Dash"})");
    request.timeout(std::chrono::seconds(4));

    async::spawn(
        request.post("http://127.0.0.1:8766/geode-loaded"),
        [](web::WebResponse response) {
            if (response.ok()) {
                log::info("GDCapture local server handshake succeeded (HTTP {}).", response.code());
            } else {
                log::warn("GDCapture local server handshake failed (HTTP {}). Is the Mac server running?", response.code());
            }
        }
    );
}
