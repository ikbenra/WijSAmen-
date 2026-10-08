package org.wijsamen.fraudevangst;

import android.app.Activity;
import android.content.ComponentName;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import rikka.shizuku.Shizuku;
import rikka.shizuku.ShizukuProvider;

public class MainActivity extends Activity {
    private static final int SHIZUKU_REQ = 8200;

    private TextView shizukuState;
    private TextView tapState;
    private ISpeakerTapService tap;
    private boolean binding;

    private final Shizuku.OnRequestPermissionResultListener permissionListener =
            (requestCode, grantResult) -> {
                if (requestCode == SHIZUKU_REQ) {
                    refreshShizuku();
                    if (grantResult == PackageManager.PERMISSION_GRANTED) bindTapService();
                }
            };

    private final ServiceConnection connection = new ServiceConnection() {
        @Override public void onServiceConnected(ComponentName name, IBinder service) {
            tap = ISpeakerTapService.Stub.asInterface(service);
            binding = false;
            tapState.setText("SpeakerTap verbonden als Shizuku UserService");
            tapState.setTextColor(Color.rgb(215, 170, 255));
        }

        @Override public void onServiceDisconnected(ComponentName name) {
            tap = null;
            binding = false;
            tapState.setText("SpeakerTap niet verbonden");
        }
    };

    private Shizuku.UserServiceArgs userServiceArgs() {
        return new Shizuku.UserServiceArgs(
                new ComponentName(this, SpeakerTapUserService.class))
                .daemon(true)
                .processNameSuffix("speaker_tap")
                .debuggable(true)
                .version(2);
    }

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
        Shizuku.addRequestPermissionResultListener(permissionListener);
        refreshShizuku();
        if (hasShizukuPermission()) bindTapService();
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 52, 36, 36);
        root.setBackgroundColor(Color.rgb(13, 9, 18));

        TextView title = new TextView(this);
        title.setText("FraudeVangst · SpeakerTap");
        title.setTextSize(28);
        title.setTextColor(Color.WHITE);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setGravity(Gravity.CENTER);
        root.addView(title, new LinearLayout.LayoutParams(-1, -2));

        TextView subtitle = new TextView(this);
        subtitle.setText("v0.2 alpha · digitale playback-probe via Shizuku\nMicrofoon wordt niet overgenomen.");
        subtitle.setTextSize(16);
        subtitle.setTextColor(Color.rgb(206, 188, 218));
        subtitle.setGravity(Gravity.CENTER);
        subtitle.setPadding(0, 12, 0, 28);
        root.addView(subtitle, new LinearLayout.LayoutParams(-1, -2));

        shizukuState = card(root, "Shizuku controleren…");
        tapState = card(root, "SpeakerTap nog niet verbonden");

        Button authorize = button("SHIZUKU TOESTAAN");
        authorize.setOnClickListener(v -> requestShizuku());
        root.addView(authorize, lp(16));

        Button start = button("START DIGITALE TAP");
        start.setOnClickListener(v -> startTap());
        root.addView(start, lp(16));

        Button stop = button("STOP + OPSLAAN");
        stop.setOnClickListener(v -> stopTap());
        root.addView(stop, lp(12));

        TextView note = new TextView(this);
        note.setText("Test eerst met muziek of video. De tap schrijft een WAV in Downloads/WijSAmenFraude. "
                + "Pas als gewone playback werkt, testen we voice-communication. "
                + "Wit/paars transcriptkanaal en OpaalView blijven in de verwerkingslaag.");
        note.setTextColor(Color.rgb(190, 174, 201));
        note.setTextSize(14);
        note.setPadding(2, 28, 2, 0);
        root.addView(note, new LinearLayout.LayoutParams(-1, -2));

        setContentView(root);
    }

    private TextView card(LinearLayout root, String text) {
        TextView v = new TextView(this);
        v.setText(text);
        v.setTextSize(17);
        v.setTextColor(Color.WHITE);
        v.setPadding(24, 22, 24, 22);
        v.setBackgroundColor(Color.rgb(35, 24, 45));
        root.addView(v, lp(10));
        return v;
    }

    private Button button(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(18);
        b.setMinHeight(118);
        return b;
    }

    private LinearLayout.LayoutParams lp(int top) {
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(-1, -2);
        p.topMargin = top;
        return p;
    }

    private boolean hasShizukuPermission() {
        try {
            return Shizuku.pingBinder()
                    && Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED;
        } catch (Throwable ignored) {
            return false;
        }
    }

    private void refreshShizuku() {
        try {
            if (!Shizuku.pingBinder()) {
                shizukuState.setText("Shizuku: niet actief");
                shizukuState.setTextColor(Color.rgb(255, 180, 180));
            } else if (Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED) {
                shizukuState.setText("Shizuku: toegestaan ✓");
                shizukuState.setTextColor(Color.rgb(220, 190, 255));
            } else {
                shizukuState.setText("Shizuku: actief · toestemming nodig");
                shizukuState.setTextColor(Color.rgb(255, 220, 170));
            }
        } catch (Throwable t) {
            shizukuState.setText("Shizuku: " + t.getClass().getSimpleName());
        }
    }

    private void requestShizuku() {
        if (!Shizuku.pingBinder()) {
            shizukuState.setText("Start Shizuku eerst.");
            return;
        }
        if (hasShizukuPermission()) {
            bindTapService();
            return;
        }
        Shizuku.requestPermission(SHIZUKU_REQ);
    }

    private void bindTapService() {
        if (!hasShizukuPermission() || tap != null || binding) return;
        binding = true;
        tapState.setText("SpeakerTap UserService starten…");
        Shizuku.bindUserService(userServiceArgs(), connection);
    }

    private void startTap() {
        if (!hasShizukuPermission()) {
            requestShizuku();
            return;
        }
        if (tap == null) {
            bindTapService();
            tapState.setText("Verbinden… tik START nogmaals zodra verbonden.");
            return;
        }
        try {
            String result = tap.startTap();
            tapState.setText(result);
            tapState.setTextColor(Color.rgb(215, 170, 255));
        } catch (RemoteException e) {
            tapState.setText("Startfout: " + e.getMessage());
        }
    }

    private void stopTap() {
        if (tap == null) {
            tapState.setText("Geen actieve SpeakerTap-service.");
            return;
        }
        try {
            tapState.setText(tap.stopTap());
        } catch (RemoteException e) {
            tapState.setText("Stopfout: " + e.getMessage());
        }
    }

    @Override protected void onDestroy() {
        Shizuku.removeRequestPermissionResultListener(permissionListener);
        super.onDestroy();
    }
}
