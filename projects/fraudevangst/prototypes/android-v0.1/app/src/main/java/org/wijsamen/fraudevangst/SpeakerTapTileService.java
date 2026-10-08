package org.wijsamen.fraudevangst;

import android.app.PendingIntent;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.IBinder;
import android.os.RemoteException;
import android.service.quicksettings.Tile;
import android.service.quicksettings.TileService;

import rikka.shizuku.Shizuku;

public class SpeakerTapTileService extends TileService {
    private ISpeakerTapService tap;
    private boolean binding;

    private Shizuku.UserServiceArgs args() {
        return new Shizuku.UserServiceArgs(
                new ComponentName(this, SpeakerTapUserService.class))
                .daemon(true)
                .processNameSuffix("speaker_tap")
                .debuggable(true)
                .version(2);
    }

    private final ServiceConnection connection = new ServiceConnection() {
        @Override public void onServiceConnected(ComponentName name, IBinder service) {
            tap = ISpeakerTapService.Stub.asInterface(service);
            binding = false;
            toggleBoundService();
        }

        @Override public void onServiceDisconnected(ComponentName name) {
            tap = null;
            binding = false;
            setTile(false, "FraudeVangst");
        }
    };

    @Override public void onStartListening() {
        super.onStartListening();
        refreshFromService();
    }

    @Override public void onClick() {
        super.onClick();

        if (!shizukuReady()) {
            openMainActivity();
            return;
        }

        if (tap != null) {
            toggleBoundService();
            return;
        }

        if (!binding) {
            binding = true;
            setTile(false, "Verbinden…");
            Shizuku.bindUserService(args(), connection);
        }
    }

    private boolean shizukuReady() {
        try {
            return Shizuku.pingBinder()
                    && Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED;
        } catch (Throwable ignored) {
            return false;
        }
    }

    private void refreshFromService() {
        if (!shizukuReady()) {
            setTile(false, "Shizuku nodig");
            return;
        }
        if (tap == null && !binding) {
            binding = true;
            Shizuku.bindUserService(args(), connection);
            return;
        }
        if (tap != null) {
            try {
                String s = tap.getStatus();
                setTile(s != null && s.contains("ACTIEF"), s != null && s.contains("ACTIEF") ? "Tap actief" : "FraudeVangst");
            } catch (RemoteException ignored) {
                setTile(false, "FraudeVangst");
            }
        }
    }

    private void toggleBoundService() {
        if (tap == null) return;
        try {
            String s = tap.getStatus();
            boolean active = s != null && s.contains("ACTIEF");
            String result = active ? tap.stopTap() : tap.startTap();
            boolean nowActive = result != null && result.contains("ACTIEF");
            setTile(nowActive, nowActive ? "Tap actief" : "FraudeVangst");
        } catch (RemoteException e) {
            setTile(false, "Tap fout");
        }
    }

    private void openMainActivity() {
        Intent open = new Intent(this, MainActivity.class)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_NO_ANIMATION);

        if (Build.VERSION.SDK_INT >= 34) {
            PendingIntent pi = PendingIntent.getActivity(
                    this, 921, open,
                    PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
            startActivityAndCollapse(pi);
        } else {
            startActivityAndCollapse(open);
        }
    }

    private void setTile(boolean active, String label) {
        Tile t = getQsTile();
        if (t == null) return;
        t.setState(active ? Tile.STATE_ACTIVE : Tile.STATE_INACTIVE);
        if (Build.VERSION.SDK_INT >= 29) t.setSubtitle(label);
        t.updateTile();
    }
}
