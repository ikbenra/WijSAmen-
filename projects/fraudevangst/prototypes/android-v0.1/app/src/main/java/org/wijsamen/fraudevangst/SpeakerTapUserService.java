package org.wijsamen.fraudevangst;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Process;

import java.io.File;
import java.io.FileOutputStream;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicBoolean;

public class SpeakerTapUserService extends ISpeakerTapService.Stub {
    private static final int SAMPLE_RATE = 48000;
    private static final int CHANNEL_MASK = AudioFormat.CHANNEL_IN_STEREO;
    private static final int CHANNELS = 2;
    private static final int PCM_ENCODING = AudioFormat.ENCODING_PCM_16BIT;
    private static final int REMOTE_SUBMIX_SOURCE = 8;

    private final AtomicBoolean running = new AtomicBoolean(false);
    private Thread worker;
    private AudioRecord record;
    private File output;
    private volatile String status = "SpeakerTap UserService gereed";

    public SpeakerTapUserService() {
        status = "UserService actief · uid=" + Process.myUid();
    }

    @Override public synchronized String startTap() {
        if (running.get()) return "SpeakerTap is al actief";
        try {
            int min = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_MASK, PCM_ENCODING);
            if (min <= 0) min = SAMPLE_RATE * CHANNELS * 2 / 5;
            final int bufferSize = Math.max(min * 2, 32768);

            AudioFormat fmt = new AudioFormat.Builder()
                    .setEncoding(PCM_ENCODING)
                    .setSampleRate(SAMPLE_RATE)
                    .setChannelMask(CHANNEL_MASK)
                    .build();

            record = new AudioRecord.Builder()
                    .setAudioSource(REMOTE_SUBMIX_SOURCE)
                    .setAudioFormat(fmt)
                    .setBufferSizeInBytes(bufferSize)
                    .build();

            if (record.getState() != AudioRecord.STATE_INITIALIZED) {
                safeRelease();
                status = "Remote Submix kon niet initialiseren";
                return status;
            }

            File dir = new File("/sdcard/Download/WijSAmenFraude");
            if (!dir.exists() && !dir.mkdirs()) {
                safeRelease();
                status = "Kan Downloads/WijSAmenFraude niet maken";
                return status;
            }

            String id = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
            output = new File(dir, "speakertap_" + id + ".wav");
            running.set(true);

            final int bs = bufferSize;
            worker = new Thread(() -> captureLoop(bs), "FraudeVangst-SpeakerTap");
            worker.start();

            status = "DIGITALE TAP ACTIEF · uid=" + Process.myUid() + " · " + output.getName();
            return status;
        } catch (SecurityException e) {
            safeRelease();
            status = "Geen toegang tot digitale audio: " + e.getClass().getSimpleName();
            return status;
        } catch (Throwable e) {
            safeRelease();
            status = "SpeakerTap startfout: " + e.getClass().getSimpleName() + ": " + e.getMessage();
            return status;
        }
    }

    private void captureLoop(int bufferSize) {
        byte[] buf = new byte[bufferSize];
        long pcmBytes = 0;
        try (FileOutputStream out = new FileOutputStream(output)) {
            out.write(new byte[44]);
            record.startRecording();

            while (running.get()) {
                int n = record.read(buf, 0, buf.length, AudioRecord.READ_BLOCKING);
                if (n > 0) {
                    out.write(buf, 0, n);
                    pcmBytes += n;
                } else if (n < 0) {
                    status = "AudioRecord read-fout " + n;
                    break;
                }
            }
            out.flush();
        } catch (Throwable e) {
            status = "Capturefout: " + e.getClass().getSimpleName() + ": " + e.getMessage();
        } finally {
            running.set(false);
            try { if (record != null) record.stop(); } catch (Throwable ignored) {}
            safeRelease();
            try {
                patchWavHeader(output, pcmBytes, SAMPLE_RATE, CHANNELS, 16);
                if (output != null && output.exists()) {
                    status = "OPGESLAGEN · " + output.getAbsolutePath() + " · " + output.length() + " bytes";
                }
            } catch (Throwable e) {
                status = "WAV-afwerking fout: " + e.getMessage();
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
            if (worker != null) worker.join(2500);
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
        System.exit(0);
    }

    private synchronized void safeRelease() {
        if (record != null) {
            try { record.release(); } catch (Throwable ignored) {}
            record = null;
        }
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
