[app]

# (str) Title of your application
title = Space Shooter

# (str) Package name
package.name = spaceshooter

# (str) Package domain (needed for android/ios packaging)
package.domain = org.oyun

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the source project)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Pygame projeleri icin "pygame" mutlaka eklenmelidir.
requirements = python3,pygame

# (str) Supported orientations (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip try to update the sdk
android.skip_update = False

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
