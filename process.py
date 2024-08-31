import cv2
import pytesseract
import db_manager

def OpenCV(media):
    video = cv2.VideoCapture(media)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 100, 200)
        
        # Kontúrok keresése
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000: # Azon kontúrok kiválasztása, melyek területe elég nagy
                x, y, w, h = cv2.boundingRect(contour)
                roi = frame[y:y+h, x:x+w]
                
                
                # Rendszám szövegének kinyerése Tesseract segítségével
                text = pytesseract.image_to_string(roi, config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
                if len(text) >= 6:
                    validation =  db_manager.check(text)
                    print("Felismert rendszám: ", text, " - ",validation)
                    cv2.putText(frame, validation, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow(validation, roi)
                
                
                #if text.strip() == "KHE-440":
                    # Kép készítése a rendszámról
                    #cv2.imwrite("rendszam_khe440.jpg", roi)
                    # Érvényes üzenet kiírás
                    #cv2.putText(frame, "Ervenyes matrica", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    #cv2.imshow('Ervenyes matrica', roi)
                
                cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Kép megjelenítése
        cv2.imshow('Rendszam felismerese', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    '''
    for plate_info in detected_plates:
        print(plate_info)'''