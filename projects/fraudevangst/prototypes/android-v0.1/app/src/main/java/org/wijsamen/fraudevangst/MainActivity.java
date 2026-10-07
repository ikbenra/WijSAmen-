package org.wijsamen.fraudevangst;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    private static final int REQ = 7301;
    private TextView status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        buildUi();
        if (hasPermissions()) {
            startCapture();
        } else {
            requestNeededPermissions();
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if (hasPermissions()) startCapture();
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(32, 64, 32, 32);

        TextView title = new TextView(this);
        title.setText("WijSAmen FraudeVangst");
        title.setTextSize(28);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setGravity(Gravity.CENTER);
        root.addView(title, new LinearLayout.LayoutParams(-1, -2));

        TextView info = new TextView(this);
        info.setText("Eén tik start lokale capture. De app probeert luidspreker + microfoon, maakt een lokale opname en laat Termux metadata en transcriptie verwerken.");
        info.setTextSize(17);
        info.setPadding(0, 28, 0, 28);
        root.addView(info, new LinearLayout.LayoutParams(-1, -2));

        status = new TextView(this);
        status.setTextSize(18);
        status.setGravity(Gravity.CENTER);
        status.setPadding(0, 18, 0, 24);
        root.addView(status, new LinearLayout.LayoutParams(-1, -2));

        Button start = new Button(this);
        start.setText("START VANGST");
        start.setTextSize(22);
        start.setMinHeight(140);
        start.setOnClickListener(v -> {
            if (hasPermissions()) startCapture(); else requestNeededPermissions();
        });
        root.addView(start, new LinearLayout.LayoutParams(-1, -2));

        Button stop = new Button(this);
        stop.setText("STOP + VERWERK");
        stop.setTextSize(22);
        stop.setMinHeight(140);
        stop.setOnClickListener(v -> stopCapture());
        LinearLayout.LayoutParams stopLp = new LinearLayout.LayoutParams(-1, -2);
        stopLp.topMargin = 18;
        root.addView(stop, stopLp);

        TextView tile = new TextView(this);
        tile.setText("Tip: voeg de Quick Settings-tegel ‘FraudeVangst’ toe. Dan kun je tijdens een gesprek starten zonder eerst deze app te zoeken.");
        tile.setTextSize(15);
        tile.setPadding(0, 28, 0, 0);
        root.addView(tile, new LinearLayout.LayoutParams(-1, -2));

        setContentView(root);
        refreshStatus();
    }

    private boolean hasPermissions() {
        return checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED;
    }

    private void requestNeededPermissions() {
        List<String> perms = new ArrayList<>();
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            perms.add(Manifest.permission.RECORD_AUDIO);
        }
        if (Build.VERSION.SDK_INT >= 33 && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            perms.add(Manifest.permission.POST_NOTIFICATIONS);
        }
        if (checkSelfPermission("com.termux.permission.RUN_COMMAND") != PackageManager.PERMISSION_GRANTED) {
            perms.add("com.termux.permission.RUN_COMMAND");
        }
        if (!perms.isEmpty()) requestPermissions(perms.toArray(new String[0]), REQ);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ && hasPermissions()) startCapture();
        else refreshStatus();
    }

    private void startCapture() {
        Intent i = new Intent(this, CaptureService.class).setAction(CaptureService.ACTION_START);
        if (Build.VERSION.SDK_INT >= 26) startForegroundService(i); else startService(i);
        status.setText("Capture gestart — laat de app lopen of keer terug naar het gesprek.");
    }

    private void stopCapture() {
        startService(new Intent(this, CaptureService.class).setAction(CaptureService.ACTION_STOP));
        status.setText("Capture gestopt. Termux verwerkt de opname lokaal.");
    }

    private void refreshStatus() {
        boolean running = getSharedPreferences("state", MODE_PRIVATE).getBoolean("running", false);
        status.setText(running ? "CAPTURE ACTIEF" : "Gereed");
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (status != null) refreshStatus();
    }
}
