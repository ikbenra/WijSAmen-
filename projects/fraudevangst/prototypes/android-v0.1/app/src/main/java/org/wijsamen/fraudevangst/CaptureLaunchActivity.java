package org.wijsamen.fraudevangst;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.Window;

public class CaptureLaunchActivity extends Activity {
    private boolean launched;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window w = getWindow();
        w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        w.setDimAmount(0f);
    }

    @Override
    protected void onPostResume() {
        super.onPostResume();
        if (launched) return;
        launched = true;

        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            startActivity(new Intent(this, MainActivity.class)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_NO_ANIMATION));
            finish();
            return;
        }

        /*
         * Post to the visible activity's UI queue so Android has completed the
         * foreground transition before the microphone foreground service is created.
         */
        getWindow().getDecorView().postDelayed(() -> {
            Intent service = new Intent(this, CaptureService.class)
                    .setAction(CaptureService.ACTION_START);
            try {
                if (Build.VERSION.SDK_INT >= 26) startForegroundService(service);
                else startService(service);
            } finally {
                finish();
                overridePendingTransition(0, 0);
            }
        }, 120);
    }
}
