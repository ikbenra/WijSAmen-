package org.wijsamen.fraudevangst;

import android.content.Context;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.os.Process;

import java.io.File;
import java.io.FileOutputStream;
import java.io.RandomAccessFile;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicBoolean;

public class SpeakerTapUserService extends ISpeakerTapService.Stub {
    private static final int SAMPLE_RATE = 48000;
    private static final int CHANNELS = 2;
    private static final int BITS = 16;

    private final AtomicBoolean running = new AtomicBoolean(false);
    private Thread worker;
    private AudioRecord record;
    private File output;
    private File diagFile;
    private volatile String status = "SpeakerTap UserService gereed";

    private Object audioPolicy;
    private Object audioMix;
    private AudioManager audioManager;

    public SpeakerTapUserService() {
        status = "UserService actief · uid=" + Process.myUid();
    }

    @Override public synchronized String startTap() {
        if (running.get()) return "SpeakerTap is al actief";
        try {
            File dir = new File("/sdcard/Download/WijSAmenFraude");
            if (!dir.exists() && !dir.mkdirs()) {
                status = "Kan Downloads/WijSAmenFraude niet maken";
                return status;
            }

            String id = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
            output = new File(dir, "speakertap_" + id + ".wav");
            diagFile = new File(dir, "speakertap_" + id + ".txt");

            AudioFormat mixFormat = new AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(SAMPLE_RATE)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_STEREO)
                    .build();

            setupAudioPolicy(mixFormat);

            if (record == null || record.getState() != AudioRecord.STATE_INITIALIZED) {
                cleanupPolicy();
                status = "AudioPolicy actief maar AudioRecord-sink kon niet initialiseren";
                writeDiag(status);
                return status;
            }

            running.set(true);
            worker = new Thread(this::captureLoop, "FraudeVangst-SpeakerTap");
            worker.start();

            status = "DIGITALE TAP ACTIEF · uid=" + Process.myUid()
                    + " · AudioPolicy LOOPBACK+RENDER · " + output.getName();
            writeDiag(status);
            return status;
        } catch (Throwable e) {
            safeRelease();
            cleanupPolicy();
            status = "SpeakerTap startfout: " + root(e);
            writeDiag(status);
            return status;
        }
    }

    private void setupAudioPolicy(AudioFormat mixFormat) throws Exception {
        Context ctx = getSystemContext();
        if (ctx == null) throw new IllegalStateException("geen system Context");

        audioManager = (AudioManager) ctx.getSystemService(Context.AUDIO_SERVICE);
        if (audioManager == null) throw new IllegalStateException("geen AudioManager");

        Class<?> ruleBuilderCl = Class.forName("android.media.audiopolicy.AudioMixingRule$Builder");
        Object ruleBuilder = ruleBuilderCl.getConstructor().newInstance();

        Method addRule = ruleBuilderCl.getMethod("addRule", AudioAttributes.class, int.class);
        int RULE_MATCH_ATTRIBUTE_USAGE = 1;

        int[] usages = new int[] {
                AudioAttributes.USAGE_MEDIA,
                AudioAttributes.USAGE_GAME,
                AudioAttributes.USAGE_UNKNOWN,
                AudioAttributes.USAGE_VOICE_COMMUNICATION
        };
        for (int usage : usages) {
            AudioAttributes attr = new AudioAttributes.Builder().setUsage(usage).build();
            addRule.invoke(ruleBuilder, attr, RULE_MATCH_ATTRIBUTE_USAGE);
        }

        // Capture also apps that normally opt out, when shell CAPTURE_AUDIO_OUTPUT/MEDIA_OUTPUT permits it.
        try {
            Method allowPriv = ruleBuilderCl.getMethod("allowPrivilegedPlaybackCapture", boolean.class);
            allowPriv.invoke(ruleBuilder, true);
        } catch (NoSuchMethodException ignored) {}

        Object rule = ruleBuilderCl.getMethod("build").invoke(ruleBuilder);

        Class<?> ruleCl = Class.forName("android.media.audiopolicy.AudioMixingRule");
        Class<?> mixBuilderCl = Class.forName("android.media.audiopolicy.AudioMix$Builder");
        Constructor<?> mixCtor = mixBuilderCl.getConstructor(ruleCl);
        Object mixBuilder = mixCtor.newInstance(rule);

        mixBuilderCl.getMethod("setFormat", AudioFormat.class).invoke(mixBuilder, mixFormat);
        mixBuilderCl.getMethod("setRouteFlags", int.class).invoke(mixBuilder, 0x1 | 0x2);
        audioMix = mixBuilderCl.getMethod("build").invoke(mixBuilder);

        Class<?> policyBuilderCl = Class.forName("android.media.audiopolicy.AudioPolicy$Builder");
        Object policyBuilder = policyBuilderCl.getConstructor(Context.class).newInstance(ctx);

        Class<?> mixCl = Class.forName("android.media.audiopolicy.AudioMix");
        policyBuilderCl.getMethod("addMix", mixCl).invoke(policyBuilder, audioMix);
        audioPolicy = policyBuilderCl.getMethod("build").invoke(policyBuilder);

        Class<?> policyCl = Class.forName("android.media.audiopolicy.AudioPolicy");
        Method register = AudioManager.class.getMethod("registerAudioPolicy", policyCl);
        int result = (Integer) register.invoke(audioManager, audioPolicy);
        if (result != 0) throw new IllegalStateException("registerAudioPolicy result=" + result);

        Method sink = policyCl.getMethod("createAudioRecordSink", mixCl);
        record = (AudioRecord) sink.invoke(audioPolicy, audioMix);
        if (record == null) throw new IllegalStateException("createAudioRecordSink gaf null");

        writeDiag("AudioPolicy geregistreerd; recordState=" + record.getState()
                + "; uid=" + Process.myUid());
    }

    private Context getSystemContext() throws Exception {
        Class<?> at = Class.forName("android.app.ActivityThread");

        try {
            Method current = at.getDeclaredMethod("currentActivityThread");
            current.setAccessible(true);
            Object thread = current.invoke(null);
            if (thread != null) {
                Method getSystemContext = at.getDeclaredMethod("getSystemContext");
                getSystemContext.setAccessible(true);
                Object c = getSystemContext.invoke(thread);
                if (c instanceof Context) return (Context) c;
            }
        } catch (Throwable ignored) {}

        Method systemMain = at.getDeclaredMethod("systemMain");
        systemMain.setAccessible(true);
        Object thread = systemMain.invoke(null);
        Method getSystemContext = at.getDeclaredMethod("getSystemContext");
        getSystemContext.setAccessible(true);
        Object c = getSystemContext.invoke(thread);
        return c instanceof Context ? (Context) c : null;
    }

    private void captureLoop() {
        byte[] buf = new byte[32768];
        long pcmBytes = 0;
        long reads = 0;
        long zeroReads = 0;
        int lastRead = 0;

        try (FileOutputStream out = new FileOutputStream(output)) {
            out.write(new byte[44]);
            record.startRecording();

            while (running.get()) {
                int n = record.read(buf, 0, buf.length, AudioRecord.READ_BLOCKING);
                lastRead = n;
                reads++;
                if (n > 0) {
                    out.write(buf, 0, n);
                    pcmBytes += n;
                } else if (n == 0) {
                    zeroReads++;
                } else {
                    status = "AudioRecord read-fout " + n;
                    break;
                }
            }
            out.flush();
        } catch (Throwable e) {
            status = "Capturefout: " + root(e);
        } finally {
            running.set(false);
            try { if (record != null) record.stop(); } catch (Throwable ignored) {}
            safeRelease();
            cleanupPolicy();
            try {
                patchWavHeader(output, pcmBytes, SAMPLE_RATE, CHANNELS, BITS);
                writeDiag("reads=" + reads + "; zeroReads=" + zeroReads
                        + "; lastRead=" + lastRead + "; pcmBytes=" + pcmBytes
                        + "; wavBytes=" + (output == null ? -1 : output.length()));
                if (output != null && output.exists()) {
                    status = "OPGESLAGEN · " + output.getAbsolutePath()
                            + " · " + output.length() + " bytes";
                }
            } catch (Throwable e) {
                status = "WAV-afwerking fout: " + root(e);
            }
        }
    }

    @Override public synchronized String stopTap() {
        if (!running.get()) return status;
        running.set(false);
        try {
            if (record != null) record.stop();
        } catch (Throwable ignored) {}
        try {
            if (worker != null) worker.join(3000);
        } catch (InterruptedException ignored) {
            Thread.currentThread().interrupt();
        }
        return status;
    }

    @Override public String getStatus() {
        return status;
    }

    @Override public void destroy() {
        stopTap();
        cleanupPolicy();
        System.exit(0);
    }

    private synchronized void safeRelease() {
        if (record != null) {
            try { record.release(); } catch (Throwable ignored) {}
            record = null;
        }
    }

    private synchronized void cleanupPolicy() {
        if (audioManager != null && audioPolicy != null) {
            try {
                Class<?> policyCl = Class.forName("android.media.audiopolicy.AudioPolicy");
                Method unregister = AudioManager.class.getMethod("unregisterAudioPolicy", policyCl);
                unregister.invoke(audioManager, audioPolicy);
            } catch (Throwable ignored) {}
        }
        audioPolicy = null;
        audioMix = null;
        audioManager = null;
    }

    private void writeDiag(String line) {
        if (diagFile == null) return;
        try (FileOutputStream out = new FileOutputStream(diagFile, true)) {
            String s = new SimpleDateFormat("HH:mm:ss.SSS", Locale.US).format(new Date())
                    + " " + line + "\n";
            out.write(s.getBytes());
        } catch (Throwable ignored) {}
    }

    private static String root(Throwable t) {
        Throwable x = t;
        while (x.getCause() != null && x.getCause() != x) x = x.getCause();
        String m = x.getMessage();
        return x.getClass().getSimpleName() + (m == null ? "" : ": " + m);
    }

    private static void patchWavHeader(File file, long dataSize, int sampleRate, int channels, int bits) throws Exception {
        if (file == null || !file.exists()) return;
        long byteRate = (long) sampleRate * channels * bits / 8;
        int blockAlign = channels * bits / 8;
        try (RandomAccessFile raf = new RandomAccessFile(file, "rw")) {
            raf.seek(0);
            raf.writeBytes("RIFF");
            writeLE32(raf, 36 + dataSize);
            raf.writeBytes("WAVE");
            raf.writeBytes("fmt ");
            writeLE32(raf, 16);
            writeLE16(raf, 1);
            writeLE16(raf, channels);
            writeLE32(raf, sampleRate);
            writeLE32(raf, byteRate);
            writeLE16(raf, blockAlign);
            writeLE16(raf, bits);
            raf.writeBytes("data");
            writeLE32(raf, dataSize);
        }
    }

    private static void writeLE16(RandomAccessFile r, long v) throws Exception {
        r.write((int)(v & 0xff));
        r.write((int)((v >> 8) & 0xff));
    }

    private static void writeLE32(RandomAccessFile r, long v) throws Exception {
        r.write((int)(v & 0xff));
        r.write((int)((v >> 8) & 0xff));
        r.write((int)((v >> 16) & 0xff));
        r.write((int)((v >> 24) & 0xff));
    }
}
