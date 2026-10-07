package org.wijsamen.fraudevangst;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.media.AudioDeviceInfo;
import android.media.AudioManager;
import android.media.MediaRecorder;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.os.IBinder;
import android.os.ParcelFileDescriptor;
import android.provider.MediaStore;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class CaptureService extends Service {
    public static final String ACTION_START = "org.wijsamen.fraudevangst.START";
    public static final String ACTION_STOP = "org.wijsamen.fraudevangst.STOP";
    private static final String CHANNEL = "fraude_capture";
    private static final int NOTIF_ID = 7302;

    private MediaRecorder recorder;
    private ParcelFileDescriptor pfd;
    private Uri audioUri;
    private String fileName;
    private String sharedPath;
    private String caseId;
    private AudioManager audioManager;
    private boolean oldSpeaker;

    @Override
    public void onCreate() {
        super.onCreate();
        createChannel();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String action = intent == null ? ACTION_START : intent.getAction();
        if (ACTION_STOP.equals(action)) {
            stopCapture();
            return START_NOT_STICKY;
        }
        startForeground(NOTIF_ID, buildNotification("Capture wordt gestart…"));
        startCapture();
        return START_STICKY;
    }

    private synchronized void startCapture() {
        if (recorder != null) return;
        getSharedPreferences("state", MODE_PRIVATE).edit().putBoolean("running", true).apply();
        caseId = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
        fileName = "fraude_" + caseId + ".m4a";
        sharedPath = "/storage/emulated/0/Music/WijSAmenFraude/" + fileName;

        trySpeakerOn();
        try {
            ContentValues v = new ContentValues();
            v.put(MediaStore.Audio.Media.DISPLAY_NAME, fileName);
            v.put(MediaStore.Audio.Media.MIME_TYPE, "audio/mp4");
            if (Build.VERSION.SDK_INT >= 29) {
                v.put(MediaStore.Audio.Media.RELATIVE_PATH, Environment.DIRECTORY_MUSIC + "/WijSAmenFraude");
                v.put(MediaStore.Audio.Media.IS_PENDING, 1);
            }
            ContentResolver cr = getContentResolver();
            audioUri = cr.insert(MediaStore.Audio.Media.EXTERNAL_CONTENT_URI, v);
            if (audioUri == null) throw new IllegalStateException("MediaStore insert gaf null");
            pfd = cr.openFileDescriptor(audioUri, "w");
            if (pfd == null) throw new IllegalStateException("Geen file descriptor");

            recorder = Build.VERSION.SDK_INT >= 31 ? new MediaRecorder(this) : new MediaRecorder();
            recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
            recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
            recorder.setAudioChannels(1);
            recorder.setAudioEncodingBitRate(96000);
            recorder.setAudioSamplingRate(44100);
            recorder.setOutputFile(pfd.getFileDescriptor());
            recorder.prepare();
            recorder.start();
            notifyNow("CAPTURE ACTIEF — tik STOP wanneer klaar");
            sendTermuxEvent("start");
            snapshotBridgeAndNetwork();
        } catch (Exception e) {
            sendTermuxEvent("record_error:" + e.getClass().getSimpleName());
            stopCapture();
        }
    }

    private synchronized void stopCapture() {
        boolean hadRecorder = recorder != null;
        if (recorder != null) {
            try { recorder.stop(); } catch (Exception ignored) {}
            try { recorder.reset(); } catch (Exception ignored) {}
            try { recorder.release(); } catch (Exception ignored) {}
            recorder = null;
        }
        if (pfd != null) {
            try { pfd.close(); } catch (Exception ignored) {}
            pfd = null;
        }
        if (audioUri != null && Build.VERSION.SDK_INT >= 29) {
            try {
                ContentValues done = new ContentValues();
                done.put(MediaStore.Audio.Media.IS_PENDING, 0);
                getContentResolver().update(audioUri, done, null, null);
            } catch (Exception ignored) {}
        }
        trySpeakerRestore();
        getSharedPreferences("state", MODE_PRIVATE).edit().putBoolean("running", false).apply();
        if (hadRecorder) sendTermuxEvent("stop");
        stopForeground(STOP_FOREGROUND_REMOVE);
        stopSelf();
    }

    private void trySpeakerOn() {
        try {
            audioManager = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
            oldSpeaker = audioManager.isSpeakerphoneOn();
            if (Build.VERSION.SDK_INT >= 31) {
                for (AudioDeviceInfo d : audioManager.getAvailableCommunicationDevices()) {
                    if (d.getType() == AudioDeviceInfo.TYPE_BUILTIN_SPEAKER) {
                        audioManager.setCommunicationDevice(d);
                        return;
                    }
                }
            }
            audioManager.setSpeakerphoneOn(true);
        } catch (Exception ignored) {}
    }

    private void trySpeakerRestore() {
        try {
            if (audioManager == null) return;
            if (Build.VERSION.SDK_INT >= 31) audioManager.clearCommunicationDevice();
            audioManager.setSpeakerphoneOn(oldSpeaker);
        } catch (Exception ignored) {}
    }

    private void createChannel() {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel ch = new NotificationChannel(CHANNEL, "FraudeVangst capture", NotificationManager.IMPORTANCE_LOW);
            getSystemService(NotificationManager.class).createNotificationChannel(ch);
        }
    }

    private Notification buildNotification(String text) {
        Intent stop = new Intent(this, CaptureService.class).setAction(ACTION_STOP);
        PendingIntent piStop = PendingIntent.getService(this, 77, stop, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Intent open = new Intent(this, MainActivity.class);
        PendingIntent piOpen = PendingIntent.getActivity(this, 78, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, CHANNEL) : new Notification.Builder(this);
        return b.setContentTitle("WijSAmen FraudeVangst")
                .setContentText(text)
                .setSmallIcon(android.R.drawable.ic_btn_speak_now)
                .setOngoing(true)
                .setContentIntent(piOpen)
                .addAction(new Notification.Action.Builder(android.R.drawable.ic_media_pause, "STOP + VERWERK", piStop).build())
                .build();
    }

    private void notifyNow(String text) {
        getSystemService(NotificationManager.class).notify(NOTIF_ID, buildNotification(text));
    }

    private void sendTermuxEvent(String event) {
        try {
            Intent i = new Intent("com.termux.RUN_COMMAND");
            i.setClassName("com.termux", "com.termux.app.RunCommandService");
            i.putExtra("com.termux.RUN_COMMAND_PATH", "/data/data/com.termux/files/usr/bin/bash");
            String cmd = "wijfraude-event " + shell(event) + " " + shell(sharedPath == null ? "" : sharedPath) + " " + shell(fileName == null ? "" : fileName) + " " + shell(caseId == null ? "" : caseId);
            i.putExtra("com.termux.RUN_COMMAND_ARGUMENTS", new String[]{"-lc", cmd});
            i.putExtra("com.termux.RUN_COMMAND_WORKDIR", "/data/data/com.termux/files/home");
            i.putExtra("com.termux.RUN_COMMAND_BACKGROUND", true);
            startService(i);
        } catch (Exception ignored) {}
    }

    private String shell(String s) {
        return "'" + s.replace("'", "'\\''") + "'";
    }

    private void snapshotBridgeAndNetwork() {
        new Thread(() -> {
            String bridge = "unreachable";
            try {
                HttpURLConnection c = (HttpURLConnection) new URL("http://127.0.0.1:8765/v1/scene").openConnection();
                c.setConnectTimeout(700);
                c.setReadTimeout(700);
                c.setRequestMethod("GET");
                int code = c.getResponseCode();
                BufferedReader r = new BufferedReader(new InputStreamReader(code < 400 ? c.getInputStream() : c.getErrorStream()));
                String line = r.readLine();
                bridge = "http=" + code + ";" + (line == null ? "" : line.substring(0, Math.min(200, line.length())));
                r.close();
                c.disconnect();
            } catch (Exception ignored) {}

            String net = "unknown";
            try {
                ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
                Network n = cm.getActiveNetwork();
                NetworkCapabilities nc = cm.getNetworkCapabilities(n);
                if (nc != null) {
                    if (nc.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)) net = "cellular";
                    else if (nc.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) net = "wifi";
                    else net = "other";
                }
            } catch (Exception ignored) {}
            sendTermuxEvent("snapshot:" + net + ":" + bridge);
        }, "fraude-snapshot").start();
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }

    @Override
    public void onDestroy() {
        if (recorder != null) stopCapture();
        super.onDestroy();
    }
}
