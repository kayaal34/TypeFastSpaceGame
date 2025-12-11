[app]
title = Neon Russian Typing Defender
package.name = neonrussian
package.domain = org.example
source.dir = .
source.include_exts = py,txt,kv,png,jpg,jpeg,svg,ttf,otf

version = 0.1.0
requirements = python3, pygame
orientation = landscape
fullscreen = 1
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET

# Optional: keep screen on during play
android.presplash_color = #050A28

[buildozer]
log_level = 2
warn_on_root = 0

[python]
# If you need fonts, ensure they're packaged
# android.add_src = fonts/
