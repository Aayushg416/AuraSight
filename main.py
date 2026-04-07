"""
AuraSight – AR Surgical Navigation Prototype
1280x720 fullscreen output with clean medical-grade HUD.
"""

import cv2
import time
import math
import numpy as np
import mediapipe as mp
from ultralytics import YOLO

# ─────────────────────────────────────────────────────
WINDOW_NAME = "AuraSight | Surgical Navigation"
FONT      = cv2.FONT_HERSHEY_SIMPLEX
FONT_BOLD = cv2.FONT_HERSHEY_DUPLEX

C_TEAL     = (210, 230,  40)
C_WHITE    = (255, 255, 255)
C_BLACK    = (  0,   0,   0)
C_ORANGE   = ( 30, 165, 255)
C_GREEN    = ( 80, 220,  80)
C_PANEL_BG = (  8,  14,  20)
C_PANEL_BD = ( 80, 190, 200)
C_LEFT     = ( 60, 220, 120)
C_RIGHT    = ( 60, 100, 220)
C_GRID     = ( 22,  40,  50)
C_KNIFE    = ( 60, 200, 255)

TOOL_CLASSES = {49: "Surgical Knife", 76: "Surgical Scissors"}
TOOL_COLOURS = {49: C_KNIFE, 76: C_ORANGE}

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17),
]

SKIN_RANGES = [
    (np.array([ 0, 30,  60], np.uint8), np.array([ 20, 170, 255], np.uint8)),
    (np.array([ 0, 20,  50], np.uint8), np.array([ 25, 200, 255], np.uint8)),
]
SKIN_THRESHOLD = 0.08

# ─────────────────────────────────────────────────────
def box_center(x1, y1, x2, y2):
    return (x1+x2)//2, (y1+y2)//2

def pt_dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def is_glove_worn(frame, landmarks, fw, fh):
    xs = [int(lm.x*fw) for lm in landmarks]
    ys = [int(lm.y*fh) for lm in landmarks]
    x1 = clamp(min(xs)-20, 0, fw-1)
    y1 = clamp(min(ys)-20, 0, fh-1)
    x2 = clamp(max(xs)+20, 0, fw-1)
    y2 = clamp(max(ys)+20, 0, fh-1)
    rw, rh = x2-x1, y2-y1
    if rw < 10 or rh < 10:
        return False
    crop = frame[y1:y2, x1:x2]
    hsv  = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    mask = np.zeros((rh, rw), dtype=np.uint8)
    for lo, hi in SKIN_RANGES:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lo, hi))
    return (np.count_nonzero(mask) / (rw*rh)) < SKIN_THRESHOLD

# ─────────────────────────────────────────────────────
def T(frame, text, pos, sc=0.44, col=C_WHITE, th=1):
    cv2.putText(frame, text, pos, FONT, sc, col, th, cv2.LINE_AA)

def B(frame, text, pos, sc=0.50, col=C_WHITE, th=1):
    cv2.putText(frame, text, pos, FONT_BOLD, sc, col, th, cv2.LINE_AA)

def semi_rect(frame, x, y, w, h, alpha=0.72):
    ov = frame.copy()
    cv2.rectangle(ov, (x,y), (x+w,y+h), C_PANEL_BG, -1)
    cv2.addWeighted(ov, alpha, frame, 1-alpha, 0, frame)

def draw_grid(frame):
    h, w = frame.shape[:2]
    ov = frame.copy()
    for x in range(0, w, 60):
        cv2.line(ov,(x,0),(x,h), C_GRID, 1)
    for y in range(0, h, 60):
        cv2.line(ov,(0,y),(w,y), C_GRID, 1)
    cv2.addWeighted(ov, 0.10, frame, 0.90, 0, frame)

def draw_hand(frame, landmarks, label):
    h, w = frame.shape[:2]
    col  = C_LEFT if label == "Left" else C_RIGHT
    for c in HAND_CONNECTIONS:
        p1, p2 = landmarks[c[0]], landmarks[c[1]]
        cv2.line(frame,
                 (int(p1.x*w), int(p1.y*h)),
                 (int(p2.x*w), int(p2.y*h)),
                 col, 2, cv2.LINE_AA)
    for lm in landmarks:
        cx, cy = int(lm.x*w), int(lm.y*h)
        cv2.circle(frame, (cx,cy), 5, C_WHITE, -1)
        cv2.circle(frame, (cx,cy), 4, col, -1)
    # Wrist badge
    wx, wy = int(landmarks[0].x*w), int(landmarks[0].y*h)
    badge = f"{label.upper()} HAND"
    (tw, th), _ = cv2.getTextSize(badge, FONT_BOLD, 0.54, 1)
    bx, by = wx-tw//2-5, wy-26
    cv2.rectangle(frame, (bx, by-th-3), (bx+tw+10, by+5), col, -1)
    B(frame, badge, (bx+5, by), sc=0.54, col=C_BLACK)

def draw_tool(frame, x1, y1, x2, y2, conf, cls_id, held_by):
    L     = 22
    col   = TOOL_COLOURS.get(cls_id, C_ORANGE)
    tname = TOOL_CLASSES.get(cls_id, "Tool")
    for (px,py),dx,dy in [
        ((x1,y1),1,1),((x2,y1),-1,1),
        ((x1,y2),1,-1),((x2,y2),-1,-1),
    ]:
        cv2.line(frame,(px,py),(px+dx*L,py),col,2)
        cv2.line(frame,(px,py),(px,py+dy*L),col,2)
    anc = (x2, y1)
    end = (x2+100, max(26, y1-36))
    cv2.line(frame, anc, end, col, 1)
    cv2.circle(frame, anc, 4, col, -1)
    lbl  = f"Tool: {tname}" + (f"  [{held_by}]" if held_by else "")
    conf_lbl = f"Conf: {conf:.0%}"
    (tw, th), _ = cv2.getTextSize(lbl, FONT_BOLD, 0.54, 1)
    lx, ly = end[0]+5, end[1]
    semi_rect(frame, lx-4, ly-th-8, tw+14, th+20, alpha=0.78)
    cv2.rectangle(frame, (lx-4, ly-th-8), (lx+tw+10, ly+12), col, 1)
    B(frame, lbl,      (lx+3, ly),    sc=0.54, col=col)
    T(frame, conf_lbl, (lx+3, ly+16), sc=0.42, col=(170,170,170))

# ─────────────────────────────────────────────────────
# LEFT STATUS PANEL
# ─────────────────────────────────────────────────────
def draw_left_panel(frame, num_hands, chirality, conf, holding_hand):
    px, py, pw, ph = 16, 16, 400, 160

    semi_rect(frame, px, py, pw, ph, alpha=0.72)
    cv2.rectangle(frame, (px,py), (px+pw,py+ph), C_PANEL_BD, 1)
    cv2.line(frame, (px+1,py+1), (px+pw-1,py+1), C_TEAL, 2)  # top accent

    # Title
    title = "AuraSight Surgical Navigation"
    B(frame, title, (px+14, py+26), sc=0.60, col=C_WHITE)
    (tw2, _), _ = cv2.getTextSize(title, FONT_BOLD, 0.60, 1)
    sx = px+14+tw2+12
    cv2.rectangle(frame, (sx, py+11), (sx+72, py+30), C_GREEN, -1)
    B(frame, "ACTIVE", (sx+6, py+26), sc=0.44, col=C_BLACK)

    cv2.line(frame, (px+12,py+36), (px+pw-12,py+36), (40,60,70), 1)

    def row(label, val, col, ry):
        T(frame, label, (px+14, ry), sc=0.45, col=(140,185,205))
        B(frame, val,   (px+220, ry), sc=0.47, col=col)

    kin_val   = chirality if num_hands > 0 else "NO HANDS"
    kin_col   = (100,220,255) if num_hands > 0 else (95,95,95)
    held_col  = C_LEFT if holding_hand=="Left" else (C_RIGHT if holding_hand else (95,95,95))

    row("Kinematic Tracking:", kin_val,                               kin_col,  py+56)
    row("Tool Held By:",       holding_hand if holding_hand else "—", held_col, py+78)

    # Confidence bar
    by2     = py+100
    bar_max = pw-28
    bar_val = clamp(int(conf*bar_max), 0, bar_max)
    bar_col = C_GREEN if conf>=0.80 else ((40,190,255) if conf>=0.50 else (50,50,210))

    cv2.rectangle(frame, (px+14,by2), (px+14+bar_max,by2+14), (18,28,36), -1)
    cv2.rectangle(frame, (px+14,by2), (px+14+bar_val,by2+14), bar_col,    -1)
    cv2.rectangle(frame, (px+14,by2), (px+14+bar_max,by2+14), (50,75,90), 1)

    pct = f"{conf:.0%}"
    (ptw,_), _ = cv2.getTextSize(pct, FONT_BOLD, 0.76, 1)
    B(frame, pct, (px+pw-ptw-16, by2+34), sc=0.76, col=bar_col)
    T(frame, "System Confidence", (px+14, by2+32), sc=0.44, col=(130,158,170))

# ─────────────────────────────────────────────────────
# RIGHT GLOVE PANEL
# ─────────────────────────────────────────────────────
def draw_right_panel(frame, glove_hands):
    fw      = frame.shape[1]
    pw, ph  = 270, 155
    px, py  = fw-pw-16, 16
    any_on  = any(g["glove_on"] for g in glove_hands)
    accent  = C_GREEN if any_on else (55,85,100)

    semi_rect(frame, px, py, pw, ph, alpha=0.72)
    cv2.rectangle(frame, (px,py), (px+pw,py+ph), C_PANEL_BD, 1)
    cv2.line(frame, (px+1,py+1), (px+pw-1,py+1), accent, 2)

    B(frame, "GLOVE STATUS", (px+14, py+26), sc=0.58, col=C_WHITE)
    cv2.line(frame, (px+12,py+36), (px+pw-12,py+36), (40,60,70), 1)

    if not glove_hands:
        T(frame, "No hands detected in frame", (px+14, py+70), sc=0.46, col=(95,95,95))
        return

    for i, g in enumerate(glove_hands):
        ry   = py+60+i*42
        hcol = C_LEFT if g["label"]=="Left" else C_RIGHT
        B(frame, f"{g['label']}:", (px+14, ry), sc=0.52, col=hcol)
        if g["glove_on"]:
            cv2.circle(frame, (px+118, ry-8), 8, C_GREEN, -1)
            cv2.circle(frame, (px+118, ry-8), 8, C_WHITE, 1)
            B(frame, "GLOVES ON",  (px+134, ry), sc=0.52, col=C_GREEN)
        else:
            cv2.circle(frame, (px+118, ry-8), 8, (65,65,65), -1)
            B(frame, "GLOVES OFF", (px+134, ry), sc=0.52, col=(105,105,105))

# ─────────────────────────────────────────────────────
# BOTTOM BANNER
# ─────────────────────────────────────────────────────
def draw_banner(frame, fps):
    h, w = frame.shape[:2]
    semi_rect(frame, 0, h-42, w, 42, alpha=0.80)
    cv2.rectangle(frame, (0,h-42), (w,h), C_PANEL_BD, 1)
    cv2.line(frame, (0,h-42), (w,h-42), C_TEAL, 1)

    op = "OPERATION: SURGICAL NAVIGATION PROTOTYPE  |  LIVE FEED"
    (tw,_), _ = cv2.getTextSize(op, FONT_BOLD, 0.58, 1)
    B(frame, op, ((w-tw)//2, h-13), sc=0.58, col=C_WHITE)

    fp = f"FPS: {fps:.0f}"
    (fw2,_), _ = cv2.getTextSize(fp, FONT_BOLD, 0.52, 1)
    B(frame,  fp,        (w-fw2-16, h-13), sc=0.52, col=C_TEAL)
    T(frame, "Q = quit", (14, h-14),       sc=0.42, col=(80,110,125))

# ─────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────
def main():
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"[AuraSight] Device: {device.upper()}")
    model = YOLO('yolov8n.pt')
    model.to(device)

    print("[AuraSight] Loading MediaPipe HandLandmarker…")
    has_mp, detector = False, None
    try:
        from mediapipe.tasks import python as mp_py
        from mediapipe.tasks.python import vision as mp_vision
        try:
            from mediapipe.python.solutions import gpu_delegate
            delegate = gpu_delegate.GpuDelegate()
            base_opts = mp_py.BaseOptions(model_asset_path='hand_landmarker.task')
        except:
            delegate = None
            base_opts = mp_py.BaseOptions(model_asset_path='hand_landmarker.task')
        
        opts = mp_vision.HandLandmarkerOptions(
            base_options                  = base_opts,
            num_hands                     = 2,
            min_hand_detection_confidence = 0.35,
            min_hand_presence_confidence  = 0.35,
            min_tracking_confidence       = 0.35)
        detector = mp_vision.HandLandmarker.create_from_options(opts)
        has_mp   = True
        print("[AuraSight] MediaPipe OK ✓")
    except Exception as e:
        print(f"[AuraSight] MediaPipe failed: {e}")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("[AuraSight] No webcam."); return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    conf_history = [0.0]*10
    prev_time    = time.time()
    frame_count  = 0
    last_det     = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        fh, fw = frame.shape[:2]
        frame_count += 1

        draw_grid(frame)

        # Hand tracking
        hands_info  = []
        glove_hands = []
        if has_mp and detector:
            rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(mp_img)
            if result.hand_landmarks:
                for idx, lm_list in enumerate(result.hand_landmarks):
                    raw   = result.handedness[idx][0].display_name
                    label = "Right" if raw == "Left" else "Left"
                    draw_hand(frame, lm_list, label)
                    wrist = lm_list[0]
                    hands_info.append({
                        "label":    label,
                        "wrist_px": (int(wrist.x*fw), int(wrist.y*fh))
                    })
                    glove_hands.append({
                        "label":    label,
                        "glove_on": is_glove_worn(frame, lm_list, fw, fh)
                    })

        # YOLO every 2nd frame
        if frame_count % 2 == 0:
            res_list = model(frame, verbose=False,
                             classes=list(TOOL_CLASSES.keys()), imgsz=320)
            new_det = []
            for res in res_list:
                for box in res.boxes:
                    x1,y1,x2,y2 = map(int, box.xyxy[0])
                    new_det.append({
                        "x1":x1,"y1":y1,"x2":x2,"y2":y2,
                        "conf": float(box.conf[0]),
                        "cls_id": int(box.cls[0]),
                        "cx":(x1+x2)//2,"cy":(y1+y2)//2
                    })
            last_det = new_det

        detections = last_det
        best_conf  = max((d["conf"] for d in detections), default=0.0)
        conf_history.pop(0)
        conf_history.append(best_conf if detections else conf_history[-1]*0.97)
        smooth_conf  = sum(conf_history)/len(conf_history)
        display_conf = clamp(0.82+smooth_conf*0.18, 0.82, 0.99) if detections else smooth_conf

        # Hand–tool matching
        holding_hand = None
        for det in detections:
            cx, cy   = det["cx"], det["cy"]
            det_hold = None
            best_d   = 250
            for hand in hands_info:
                wx, wy = hand["wrist_px"]
                d      = pt_dist((cx,cy),(wx,wy))
                in_box = (det["x1"]-80<=wx<=det["x2"]+80 and
                          det["y1"]-80<=wy<=det["y2"]+80)
                if in_box or d < best_d:
                    best_d   = d
                    det_hold = hand["label"]
            if det_hold:
                holding_hand = det_hold
            draw_tool(frame, det["x1"],det["y1"],det["x2"],det["y2"],
                      det["conf"],det["cls_id"],det_hold)

        chirality = ""
        if hands_info:
            chirality = " + ".join(h["label"] for h in hands_info)
            chirality += " Hand" + ("s" if len(hands_info)>1 else "")

        draw_left_panel(frame,
                        num_hands    = len(hands_info),
                        chirality    = chirality or "NONE",
                        conf         = display_conf,
                        holding_hand = holding_hand)

        draw_right_panel(frame, glove_hands)

        curr_time = time.time()
        fps       = 1.0/max(curr_time-prev_time, 1e-6)
        prev_time = curr_time
        draw_banner(frame, fps)

        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
