package com.bbasa21.smartchargr.diag;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

import java.util.Collections;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Diagnostic-only probe. It does not change views, resources, battery state,
 * charging behavior, or any SystemUI method result.
 */
public final class SystemUiProbe implements IXposedHookLoadPackage {
    private static final String TAG = "SMARTCHARGR-PROBE";
    private static final Set<String> SEEN = Collections.newSetFromMap(
            new ConcurrentHashMap<String, Boolean>());
    private static final String[] TOKENS = new String[] {
            "Battery", "StatusBar", "Keyguard", "Clock", "Percent",
            "CollapsedStatusBar", "CentralSurfaces", "PhoneStatusBar",
            "NotificationPanel", "KeyguardIndication", "QSClock"
    };

    @Override
    public void handleLoadPackage(final XC_LoadPackage.LoadPackageParam lpparam) {
        if (!"com.android.systemui".equals(lpparam.packageName)) return;

        XposedBridge.log(TAG + ": attached to package=" + lpparam.packageName
                + " process=" + lpparam.processName
                + " sdk=" + android.os.Build.VERSION.SDK_INT
                + " manufacturer=" + android.os.Build.MANUFACTURER
                + " model=" + android.os.Build.MODEL);

        try {
            XposedHelpers.findAndHookMethod(ClassLoader.class, "loadClass",
                    String.class, new XC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) {
                    Object arg = param.args[0];
                    if (!(arg instanceof String)) return;
                    String name = (String) arg;
                    if (!isInteresting(name) || !SEEN.add(name)) return;
                    XposedBridge.log(TAG + ": CLASS " + name);
                }
            });
            XposedBridge.log(TAG + ": class-load observer installed");
        } catch (Throwable t) {
            XposedBridge.log(TAG + ": observer install failed: " + t);
        }
    }

    private static boolean isInteresting(String name) {
        for (String token : TOKENS) {
            if (name.contains(token)) return true;
        }
        return false;
    }
}
