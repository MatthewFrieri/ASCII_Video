import pygame as pg
import pygame.camera as pgcam
import sys

pg.init()
pgcam.init()

WIDTH, HEIGHT = 1345, 998

# Setup
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASCII Converter")
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pg.font.SysFont("Courier", 12)
width, height = 192, 100

# Start camera
cameras = pg.camera.list_cameras()
webcam = pg.camera.Camera(cameras[0])
webcam.start()


def draw(chars):
    WIN.fill(BLACK)
   
    for i, row in enumerate(chars):
        letters = font.render(row, True, WHITE)
        WIN.blit(letters, (0, i*10))

    pg.display.update()


def get_brightness(px):
    return (px[0] + px[2] + px[3]) / 3

def all_brightnesses(pxArray):
    
    brightnesses = []
    for row in pxArray:
        bRow = []
        for px in row:
            px = frame.unmap_rgb(px)       
            bRow.append(get_brightness(px))

        brightnesses.append(bRow)

    return brightnesses


def get_chars(brightnesses):
    density = "     `.-+c$m@MÑ" #[::-1]

    rnge = 256/len(density)

    chars = []
    for row in brightnesses:
        cRow = ""
        for px in row:
            cRow += density[int(px/rnge)]
        chars.append(cRow)

    return chars


def main():
    global frame
    clock = pg.time.Clock()

    # Main loop
    while True:
        clock.tick(FPS)

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        frame = webcam.get_image()
        frame = pg.transform.scale(frame, (width, height))
        frame = pg.transform.flip(frame, True, False)

        pxArray = pg.PixelArray(frame)
        pxArray = pg.PixelArray.transpose(pxArray)
        brightnesses = all_brightnesses(pxArray) 
        chars = get_chars(brightnesses)

        draw(chars)
        

main()