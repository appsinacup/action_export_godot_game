import subprocess
import re
import os

# Get the total number of commits in the repository
commit_count = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode("utf-8").strip()

# Define the base version (e.g., 1.0)
base_version = os.environ.get("BASE_GAME_VERSION", "1.0")

# Create the version string
version = f"{base_version}.{commit_count}"

# Update the version in project.godot
with open("project.godot", "r") as file:
    content = file.read()

# Replace the version string in project.godot
content = re.sub(
    r'config/version="([^"]+)"',
    f'config/version="{version}"',
    content
)

store_name = os.environ.get("STORE_NAME", "")

# Update the store name if present
content = re.sub(
    r'game/store_name=""',
    f'game/store_name="{store_name}"',
    content
)

# Replace game/lobby_server_local=true with false if it appears
content = re.sub(
    r"game/lobby_server_local=true",
    "game/lobby_server_local=false",
    content
)

# Write the updated content back to project.godot
with open("project.godot", "w") as file:
    file.write(content)

print(f"Updated version to: {version}")

# Update android version version/code from export_presets.cfg

with open("export_presets.cfg", "r") as file:
    content = file.read()

content = re.sub(
    r'version/code=\d+',
    f'version/code={commit_count}',
    content
)

with open("export_presets.cfg", "w") as file:
    file.write(content)

print(f"Updated android version to: {commit_count}")
print(f"Updated store_name to: {store_name}")
# Put it in env var GAME_VERSION
with open("version.txt", "w") as file:
    file.write(version)

for file_name in ["deploy/ios/exportOptions.plist"]:
    # Update ios and mac provisioning profiles
    with open(file_name, "r") as file:
        content = file.read()

    # Replace com.godot.game with IOS_PACKAGE env
    ios_package = os.environ.get("IOS_PACKAGE", "com.godot.game")
    content = re.sub(
        r'<key>com\.godot\.game</key>',
        f'<key>{ios_package}</key>',
        content
    )
    with open(file_name, "w") as file:
        file.write(content)

# Update export_presets.cfg 
with open("export_presets.cfg", "r") as file:
    content = file.read()

# Replace com.godot.game_android with ANDROID_PACKAGE env
android_package = os.environ.get("ANDROID_PACKAGE", "com.godot.game_android")
content = re.sub(
    r'com\.godot\.game_android',
    f'{android_package}',
    content
)

# Replace com.godot.game_ios with IOS_PACKAGE env
ios_package = os.environ.get("IOS_PACKAGE", "com.godot.game_ios")
content = re.sub(
    r'com\.godot\.game_ios',
    f'{ios_package}',
    content
)

# Replace APPLE_TEAM_ID with the environment variable
apple_team_id = os.environ.get("APPLE_TEAM_ID", "")
content = re.sub(
    r'APPLE_TEAM_ID',
    f'{apple_team_id}',
    content
)


with open("export_presets.cfg", "w") as file:
    file.write(content)
