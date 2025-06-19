import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hands and Drawing.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure Hands: Using one hand, with high detection/tracking confidence.
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# Get screen dimensions.
screen_width, screen_height = pyautogui.size()

# Open webcam.
cap = cv2.VideoCapture(0)

# Smoothing parameters.
prev_x, prev_y = 0, 0
smoothening = 3  # Lower value gives faster response (less smoothing).

# Click flags to avoid multiple clicks per gesture.
click_flag = False
double_click_flag = False
right_click_flag = False
scroll_flag = False

def count_fingers(hand_landmarks, frame_width, frame_height):
    """
    Determines which fingers are open.
    Returns a list with 5 elements (for thumb, index, middle, ring, pinky) where 1 indicates open.
    
    For the thumb: In a flipped image (mirror view) using the right hand,
    the thumb is considered open if its tip (id 4) is to the right of its IP joint (id 3)
    by a threshold (here, 10 pixels).
    
    For the other fingers, we check if the tip is higher (y-value is smaller) than the PIP joint.
    """
    def to_pixel(i):
        return int(hand_landmarks.landmark[i].x * frame_width), int(hand_landmarks.landmark[i].y * frame_height)
    
    fingers = []
    
    # Thumb: Adjusted for a flipped image (right hand).
    thumb_tip_x, _ = to_pixel(4)
    thumb_ip_x, _ = to_pixel(3)
    if thumb_tip_x > thumb_ip_x + 10:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Index finger: tip id 8, pip id 6.
    if to_pixel(8)[1] < to_pixel(6)[1] - 10:
        fingers.append(1)
    else:
        fingers.append(0)
        
    # Middle finger: tip id 12, pip id 10.
    if to_pixel(12)[1] < to_pixel(10)[1] - 10:
        fingers.append(1)
    else:
        fingers.append(0)
        
    # Ring finger: tip id 16, pip id 14.
    if to_pixel(16)[1] < to_pixel(14)[1] - 10:
        fingers.append(1)
    else:
        fingers.append(0)
        
    # Pinky: tip id 20, pip id 18.
    if to_pixel(20)[1] < to_pixel(18)[1] - 10:
        fingers.append(1)
    else:
        fingers.append(0)
        
    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror view.
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert BGR to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame.
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Determine which fingers are open.
            finger_status = count_fingers(hand_landmarks, frame_width, frame_height)
            total_fingers = sum(finger_status)
            
            # Display finger status for debugging.
            cv2.putText(frame, f'Fingers: {finger_status}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Use a reference landmark as the hand center. (Landmark 9 is a good choice.)
            cx = int(hand_landmarks.landmark[9].x * frame_width)
            cy = int(hand_landmarks.landmark[9].y * frame_height)
            
            # Map hand center to screen coordinates.
            # Since the frame is already flipped, we map directly.
            screen_x = np.interp(cx, [0, frame_width], [0, screen_width])
            screen_y = np.interp(cy, [0, frame_height], [0, screen_height])
            
            # Smooth the pointer movement.
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            
            # Gesture Actions:
            if total_fingers == 0:
                # Fist: move the mouse pointer.
                pyautogui.moveTo(curr_x, curr_y)
                click_flag = double_click_flag = right_click_flag = scroll_flag = False
            
            elif total_fingers == 1 and finger_status[1] == 1:
                # Only index finger open: single left click.
                if not click_flag:
                    pyautogui.click()
                    click_flag = True
            else:
                click_flag = False
            
            if total_fingers == 2 and finger_status[1] == 1 and finger_status[2] == 1:
                # Index and middle fingers open: double left click.
                if not double_click_flag:
                    pyautogui.doubleClick()
                    double_click_flag = True
            else:
                double_click_flag = False
            
            if total_fingers == 4:
                # Four fingers open: right click.
                if not right_click_flag:
                    pyautogui.rightClick()
                    right_click_flag = True
            else:
                right_click_flag = False
            
            if total_fingers == 5:
                # All fingers open: scroll up/down based on vertical hand position.
                if not scroll_flag:
                    scroll_flag = True
                if cy < frame_height // 2:
                    pyautogui.scroll(40)  # Scroll up.
                else:
                    pyautogui.scroll(-40)  # Scroll down.
            else:
                scroll_flag = False
            
            # Update previous coordinates.
            prev_x, prev_y = curr_x, curr_y
    
    # Display the webcam feed.
    cv2.imshow("Virtual Mouse", frame)
    
    # Exit if 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources.
cap.release()
cv2.destroyAllWindows()
