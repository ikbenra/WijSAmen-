package org.wijsamen.fraudevangst;

interface ISpeakerTapService {
    String startTap();
    String stopTap();
    String getStatus();
    void destroy();
}
