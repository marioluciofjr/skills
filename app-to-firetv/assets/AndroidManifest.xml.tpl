<?xml version="1.0" encoding="utf-8" standalone="no"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="__PKG__">
    __INTERNET_PERMISSION__
    <uses-feature android:name="android.hardware.touchscreen" android:required="false"/>
    <uses-feature android:name="android.software.leanback" android:required="false"/>
    <application android:allowBackup="true" android:banner="@drawable/banner" android:hardwareAccelerated="true"
        android:icon="@mipmap/ic_launcher" android:label="@string/app_name"
        android:theme="@android:style/Theme.Black.NoTitleBar.Fullscreen">
        <activity android:name="__PKG__.MainActivity" android:exported="true" android:launchMode="singleTask"
            android:screenOrientation="landscape" android:label="@string/app_name"
            android:configChanges="keyboard|keyboardHidden|navigation|orientation|screenLayout|screenSize|uiMode">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
                <category android:name="android.intent.category.LEANBACK_LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
