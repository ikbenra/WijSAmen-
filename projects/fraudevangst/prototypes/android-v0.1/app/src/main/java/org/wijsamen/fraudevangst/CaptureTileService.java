package org.wijsamen.fraudevangst;

import android.Manifest;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.service.quicksettings.Tile;
import android.service.quicksettings.TileService;

public class CaptureTileService extends TileService {
    @Override
    public void onStartListening() {
        super.onStartListening();
        boolean running = getSharedPreferences("state", MODE_PRIVATE).getBoolean("running", false);
        if (getQsTile() != null) {
            getQsTile().setState(running ? Tile.STATE_ACTIVE : Tile.STATE_INACTIVE);
            getQsTile().updateTile();
        }
    }

    @Override
    public void onClick() {
        super.onClick();

        boolean running = getSharedPreferences("state", MODE_PRIVATE).getBoolean("running", false);

        if (running) {
            startService(new Intent(this, CaptureService.class).setAction(CaptureService.ACTION_STOP));
            if (getQsTile() != null) {
                getQsTile().setState(Tile.STATE_INACTIVE);
                getQsTile().updateTile();
            }
            return;
        }

        /*
         * Android 14 treats RECORD_AUDIO as a while-in-use permission.
         * A TileService itself is a background component, so directly starting a
         * microphone foreground service from here can be rejected. Route the user
         * click through a tiny visible activity; that activity starts CaptureService
         * while the app is in a user-visible state, then closes immediately.
         */
        Intent open;
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            open = new Intent(this, CaptureLaunchActivity.class);
        } else {
            open = new Intent(this, MainActivity.class);
        }
        open.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_NO_ANIMATION);

        if (Build.VERSION.SDK_INT >= 34) {
            PendingIntent pi = PendingIntent.getActivity(
                    this,
                    902,
                    open,
                    PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT
            );
            startActivityAndCollapse(pi);
        } else {
            startActivityAndCollapse(open);
        }
    }
}
