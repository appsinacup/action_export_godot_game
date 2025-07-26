# Export Godot Game Action

|[Website](https://appsinacup.com)|[Discord](https://discord.gg/56dMud8HYn)|
|-|-|

![export godot game](./docs/example.png)

Reusable Action that build a Godot game. These actions build and sign the games with the [Godot Engine](https://godotengine.org) of the version specified.

Sample usage:
```yml
- name: Build Game Linux
  uses: appsinacup/action_export_godot_game@master
  with:
    game-name: MyGame
    platform-name: Linux x86_64
```

Complete usage on [appsinacup/project_godot_autobuild](https://github.com/appsinacup/project_godot_autobuild):

The `platform-name` has to match one of the following:

```yml
env:
  GAME_NAME: GameName
  ANDROID_PACKAGE: com.godot.game
  IOS_PACKAGE: com.godot.game
jobs:
  build:
    runs-on: ${{ matrix.platform.os }}
    strategy:
      fail-fast: false
      matrix:
        platform: [
          { name: "Windows Desktop x86_64", os: "ubuntu-latest" },
          { name: "Windows Desktop x86_32", os: "ubuntu-latest" },
          { name: "Windows Desktop arm64", os: "ubuntu-latest" },
          { name: "Linux x86_64", os: "ubuntu-latest" },
          { name: "Linux x86_32", os: "ubuntu-latest" },
          { name: "Linux arm64", os: "ubuntu-latest" },
          { name: "Linux arm32", os: "ubuntu-latest" },
          { name: "macOS", os: "macos-latest" },
          { name: "iOS", os: "macos-latest" },
          { name: "Android", os: "ubuntu-latest" },
          { name: "Web", os: "ubuntu-latest" },
        ]

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Build Game
        uses: appsinacup/action_export_godot_game@master
        with:
          godot-version: 4.4.1-stable
          game-name: ${{ env.GAME_NAME }}
          android-package: ${{ env.ANDROID_PACKAGE }}
          ios-package: ${{ env.IOS_PACKAGE }}
          platform-name: ${{ matrix.platform }}
          secret-macos-build-certificate-base64: ${{ secrets.BUILD_CERTIFICATE_BASE64 }}
          secret-p12-password: ${{ secrets.P12_PASSWORD }}
          secret-keychain-password: ${{ secrets.KEYCHAIN_PASSWORD }}
          secret-ios-distribution-certificate-base64: ${{ secrets.DISTRIBUTION_CERTIFICATE_BASE64 }}
          secret-ios-deploy-provision-profile-ios-base64: ${{ secrets.DEPLOY_PROVISION_PROFILE_IOS_BASE64 }}
          secret-apple-id: ${{ secrets.APPLE_ID }}
          secret-apple-team-id: ${{ secrets.APPLE_TEAM_ID }}
          secret-apple-password: ${{ secrets.APP_SPECIFIC_PASSWORD }}
          secret-android-keystore-base64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}
          secret-android-keystore-password: ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          secret-android-keystore-user: ${{ secrets.ANDROID_KEYSTORE_USER }}
```

If you want to build for steam, you need to send `steam-app-id` and `store-name` set to `steam`:

```yml
- name: Build Game Steam
  uses: appsinacup/action_export_godot_game@master
  with:
    game-name: MyGame
    platform-name: Linux x86_64
    steam-app-id: 1234
    store-name: steam
```


## Inputs


| Name                                      | Description                                                      | Required | Secret |
|-------------------------------------------|------------------------------------------------------------------|----------|--------|
| godot-repo                                | Repository to download Godot from  (default godotengine/godot)   |  No.     | No     |
| godot-release-tag                         | Tag to take release from  (default ''). If empty uses version    |  No.     | No     |
| godot-version                           | Godot Engine version to use (e.g. `4.4.1-stable`)           | No       | No     |
| game-name                                 | Name of the game to export                                       | Yes      | No     |
| android-package                           | Android package name (e.g. com.godot.game_android)             | No      | No     |
| ios-package                               | iOS package name (e.g. com.godot.game_ios)                     | No      | No     |
| platform-name                             | Platform export preset name (must match export preset)            | Yes      | No     |
| secret-macos-build-certificate-base64      | macOS build certificate (base64)                                 | No       | Yes    |
| secret-p12-password                       | Password for P12 certificate                                     | No       | Yes    |
| secret-keychain-password                  | Keychain password for macOS/iOS builds                           | No       | Yes    |
| secret-ios-distribution-certificate-base64 | iOS distribution certificate (base64)                            | No       | Yes    |
| secret-ios-deploy-provision-profile-ios-base64 | iOS deploy provision profile (base64)                        | No       | Yes    |
| secret-apple-id                           | Apple ID (for macOS/iOS deployment)                              | No       | Yes    |
| secret-apple-team-id                      | Apple Team ID                                                    | No       | Yes    |
| secret-apple-password                     | Apple app-specific password                                      | No       | Yes    |
| secret-android-keystore-base64            | Android keystore (base64)                                        | No       | Yes    |
| secret-android-keystore-password          | Android keystore password                                        | No       | Yes    |
| secret-android-keystore-user              | Android keystore alias                                           | No       | Yes    |
| steam-app-id                              | Steam App ID (for Steam builds)                                  | No       | No     |
| store-name                                | Store name (e.g. `steam`, `itch`)                                | No       | No     |
| base-game-version                         | Base version of the game (for versioning/export presets)         | No       | No     |
| use-cache                                 | Use cache (default: true)                                        | No       | No     |

## Outputs

| Name         | Description                |
|--------------|---------------------------|
| game_version | The version of the game.  |

This action will also generate exported game builds for the specified platform(s) in the configured output directory.

For all of the job inputs that need to be secrets, add them to the github actions secrets.

# Apple Secrets configuration

The deploy secrets are needed for deploying to App Store or Mac App Store.

## Apple Mac Flow for Export

### 1. How to get Certificate P12 to Mac

Prerequisites:

- P12 Password (You create this manually, keep it safe)

First go to `Certificates, Identifiers & Profiles` -> `Certificates`:

- `https://developer.apple.com/account/resources/certificates/list`

Then, download the certificate which was previously generated using a file called `CertificateSigningRequest.certSigningReque` (PRIVATE KEY). The private key is created by following this link `https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request`. The public key is unusable without the private key for our use cases.

After this, import the public key and also import the privat key. Now, go to XCode -> Settings -> Accounts -(Click the team to which the certificate belongs to)> Manage Certificates... -> (Right Click the Certificate) it has to match by name, DO NOT import multiple certificates with same name -> Export Certificate - put password> Obtain a P12 file

Certificate Types:
- Developer ID Application - For Mac Binary Exports
- Mac App Distribution - For Mac Binary to be sent to Mac App Store (inside the installer)
- Mac Installer Distribution - For Mac Installer (contains the Mac Binary) to be sent to the Mac App Store

#### Generate base64 from Certificate P12

To use them in CI/CD you need to make them in base64 so they can be put in env vars:
```sh
# eg.
base64 -i DeveloperID.p12 > certificate_development_id_base64.txt
```

### 2. Obtain the certificates

Prerquisites:
- Developer ID Certificate
- P12 Password
- Keychain Password (you set this)

#### How to list certificates installed

You installed the certificate by a file, but now you need a name to use it. In order to get that name, you can do:

```sh
security find-identity -v -p codesigning
```

### 3. Build the mac app without signing and without notarization

There are 3 types of mac apps:
- .app: Folder with files
- .dmg: Virtual Volume, basically a single file
- .pkg: Installer

You want to use the .app and create a .pkg with it. Using .dmg is also possible but more difficult.

### 4. Sign the app

Prerequisite:

- APPLE_ID: Your apple id (usually email)
- APP_SPECIFIC_PASSWORD: https://support.apple.com/en-us/102654
- APPLE_TEAM_ID: Your apple team id (usually a number, eg. 12345678)
- entitlements file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
  </dict>
</plist>
```

You need to sign the app using the `Developer ID Application` for your team if you want to export it (outside of Mac App Store).

## Apple Mac Flow for Publish

### 1. Provisioning Profile

In order to deploy to Mac App Store you need a `Mac App Store Connect` Distribution Profile from `https://developer.apple.com/account/resources/profiles/add`. The distribution profile is a text file that contains also some entitlements, these will be added to the entitlements file later on.

How to get it:
- Go to Certificates, Identifiers & Profiles: `https://developer.apple.com/account/resources/profiles/add`. Add a provisioning profile of type `Mac App Store Connect` at the `Distribution` section. Select App Id that matches your game. This is how it will know to link the provisioning profile with the certificate. Then click Next, Next..

### 2. Obtain the certificates

Prerquisites:
- Mac App Distribution
- Mac Installer Distribution
- P12 Password
- Keychain Password (you set this)
- Provisioning Profile of type `Mac App Store Connect`

### 3. Code Sign

Prerequisites:
- `DEPLOY_SIGNING_IDENTITY` you obtained from Step 2.

### 4. Make an installer

Prerequisites:
- `INSTALL_SIGNING_IDENTITY` you obtained from Step 2.

### 5. Deploy to Test Flight

Prerequisites:
- `APPLE_ID`: Your apple id (usually email)
- `APP_SPECIFIC_PASSWORD`: https://support.apple.com/en-us/102654


## Apple iOS Flow for Publish

This flow works pretty well from Godot. All you need to do is set in Godot same stuff in export window as for actions:

### 1. Obtain certificates and provisioning profile

Prerequisites:
- `DISTRIBUTION_CERTIFICATE_BASE64`: Apple Distribution Certificate
- `P12_PASSWORD`: Password used to encrypt P12 Certificates
- `DEPLOY_PROVISION_PROFILE_IOS_BASE64`: iOS Deploy Certificate for App
- `KEYCHAIN_PASSWORD`: Keychain Password (you enter this manually to what you want)

# Android Secrets configuration

For android you need the :
- secret-android-keystore-base64: Base64 encoded keystore for Android.
- secret-android-keystore-password: Android keystore password.
- secret-android-keystore-user: Android keystore alias.

How to generate android keystore:

```sh
keytool -genkey -v -keystore release.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```

To list aliases run:

```sh
keytool -v -list -keystore godot.keystore
```
