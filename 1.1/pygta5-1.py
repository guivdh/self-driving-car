import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui


def draw_lines(img, lines):
    try:
        line_left = [0, 0, 0, 0]
        line_right = [0, 0, 0, 0]
        nbre_line_left = 0
        nbre_line_right = 0

        for line in lines:
            coords = line[0]
            if coords[0] < coords[1]:
                for i in range(4):
                    line_left[i] += coords[i]
                nbre_line_left += 1

            if coords[0] > coords[1]:
                for i in range(4):
                    line_right[i] += coords[i]
                nbre_line_right += 1

        for i in range(4):
            line_left[i] = line_left[i] / nbre_line_left
            line_right[i] = line_right[i] / nbre_line_right

        for i in range(4):
            line_left[i] = int(line_left[i])
            line_right[i] = int(line_right[i])

        print(line_left)
        print(line_right)
        cv2.line(img, (line_left[0], line_left[1]), (line_left[2], line_left[3]), [255, 255, 255], 3)
        cv2.line(img, (line_right[0], line_right[1]), (line_right[2], line_right[3]), [255, 255, 255], 3)
    except:
        pass



def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

#def get_car_position():


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    #processed_img = cv2.fastNlMeansDenoising(processed_img, None, 10, 10, 7)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    vertices = np.array([[0, 500], [0, 400], [380, 200], [580, 200], [960, 400], [960, 500], [580,500], [580,400], [380,400], [380,500]])
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 20, 50)
    draw_lines(original_image, lines)

    return processed_img



def main():
    last_time = time.time()
    while(True):
        screen = np.array(ImageGrab.grab(bbox=(0, 275, 960, 805)))
        new_screen = process_img(screen)

        cv2.circle(screen, (480,300), 5, (255,255,255), -1)

        print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


for i in range(4):
    time.sleep(1)
    print(i)
main()