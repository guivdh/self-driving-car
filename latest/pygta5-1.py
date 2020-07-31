import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui


def draw_lines(img, lines):
    line_left = [0, 0, 0, 0]
    line_right = [0, 0, 0, 0]
    nbre_line_left = 0
    nbre_line_right = 0
    try:
        # Dessine toutes les lignes détectées dans l'image
        for line in lines:
            coords = line[0]
            pente = (coords[3] - coords[1]) / (coords[2] - coords[0])
            #print(pente)

            # Si la pente de la ligne n'est pas comprise dans les normes, elle n'est pas prise en compte
            if (0.6 < pente < 0.7) or (-0.8 < pente < -0.5):
                cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)

        # Dessine la ligne à partir de la moyennes des lignes détectées
        for line in lines:
            coords = line[0]
            penteMoyenne = (coords[3] - coords[1]) / (coords[2] - coords[0])
            #print(penteMoyenne)

            # Si la pente de la ligne n'est pas comprise dans les normes, elle n'est pas prise en compte
            if (0.6 < penteMoyenne < 0.7) or (-0.8 < penteMoyenne < -0.6):

                # Ligne gauche
                if coords[0] < coords[1]:
                    for i in range(4):
                        line_left[i] += coords[i]
                        # print("Pente gauche : " + str(penteMoyenne))
                    nbre_line_left += 1

                # Ligne droite
                if coords[0] > coords[1]:
                    for i in range(4):
                        line_right[i] += coords[i]
                        # print("Pente droite : " + str(penteMoyenne))
                    nbre_line_right += 1
            else:
                continue

        # Calcul de la moyenne de chaque coordonnées
        for i in range(4):
            line_left[i] = line_left[i] / nbre_line_left
            line_right[i] = line_right[i] / nbre_line_right

        # Calcul de la moyenne de chaque coordonnées
        for i in range(4):
            line_left[i] = int(line_left[i])
            line_right[i] = int(line_right[i])

        # print(line_left)
        # print(line_right)
        # Dessine la ligne moyenne de gauche et de droite
        cv2.line(img, (line_left[0], line_left[1]), (line_left[2], line_left[3]), [255, 255, 255], 3)
        cv2.line(img, (line_right[0], line_right[1]), (line_right[2], line_right[3]), [255, 255, 255], 3)

        # Calcule de l'équation de la ligne afin de trouver les coodonnées d'un point sur la droite (y=ax+b)

        # Trouver a
        a_left = (line_left[3] - line_left[1]) / (line_left[2] - line_left[0])

        # Trouver b
        b_left = line_left[1] - (a_left * line_left[0])

        # Trouver x
        x_left = (300 - b_left) / a_left
        x_left = int(x_left)

        # Dessiner le point sur la ligne gauche qui a la même coordonnée en Y que le centre de la voiture
        cv2.circle(img, (x_left, 300), 5, (0, 0, 255), -1)

        a_right = (line_right[3] - line_right[1]) / (line_right[2] - line_right[0])
        b_right = line_right[1] - (a_right * line_right[0])

        x_right = (300 - b_right) / a_right
        x_right = int(x_right)
        cv2.circle(img, (x_right, 300), 5, (0, 0, 255), -1)

        # Calcul de distance entre la ligne gauche, le centre de la voiture et la ligne droite
        distance_line_left = 480 - x_left
        distance_line_right = abs(480 - x_right)
        print(str(distance_line_left) + " | " + str(distance_line_right))

        # if distance_line_left < 100:
        #    right()
        # if distance_line_left > 150:
        #    left()

    except:
        # stop()
        pass


# Function qui permet de découper une image sur base d'un polynôme
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    # processed_img = cv2.fastNlMeansDenoising(processed_img, None, 10, 10, 7)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    vertices = np.array(
        [[0, 500], [0, 400], [380, 200], [580, 200], [960, 400], [960, 500], [580, 500], [580, 400], [380, 400],
         [380, 500]])
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, np.array([]), 20, 50)
    draw_lines(original_image, lines)

    return processed_img


def straight():
    pyautogui.keyDown('z')
    pyautogui.keyUp('q')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')


def left():
    pyautogui.keyDown('q')
    # pyautogui.keyUp('z')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')
    pyautogui.keyUp('q')


def right():
    pyautogui.keyDown('d')
    # pyautogui.keyUp('z')
    pyautogui.keyUp('s')
    pyautogui.keyUp('q')
    pyautogui.keyUp('d')


def stop():
    pyautogui.keyDown('s')
    pyautogui.keyUp('z')
    pyautogui.keyUp('q')
    pyautogui.keyUp('d')
    pyautogui.keyUp('s')


def main():
    last_time = time.time()
    # straight()
    while (True):
        screen = np.array(ImageGrab.grab(bbox=(0, 275, 960, 805)))
        new_screen = process_img(screen)

        cv2.circle(screen, (480, 300), 5, (255, 255, 255), -1)
        cv2.line(screen, (480, 400), (480, 200), (255, 255, 255), 2)
        # print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


for i in range(1):
    time.sleep(1)
    print(i)
main()
