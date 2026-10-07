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
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            Intent open = new Intent(this, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            if (Build.VERSION.SDK_INT >= 34) {
                PendingIntent pi = PendingIntent.getActivity(this, 902, open, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
                startActivityAndCollapse(pi);
            } else {
                startActivityAndCollapse(open);
            }
            return;
        }
        boolean running = getSharedPreferences("state", MODE_PRIVATE).getBoolean("running", false);
        Intent i = new Intent(this, CaptureService.class).setAction(running ? CaptureService.ACTION_STOP : CaptureService.ACTION_START);
        if (!running && Build.VERSION.SDK_INT >= 26) startForegroundService(i); else startService(i);
        if (getQsTile() != null) {
            getQsTile().setState(running ? Tile.STATE_INACTIVE : Tile.STATE_ACTIVE);
            getQsTile().updateTile();
        }
    }
}
