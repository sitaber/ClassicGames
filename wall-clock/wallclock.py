import math
import time

import pygame

'''NOTES
HOUR - 360 degrees in an hour
360 degrees / 12 hours = 30 -> hour hand moves 30 degress per hour
30 degrees / 60 minutes = 0.5 -> 0.5 degress per min
0.5 degrees / 60 seconds = 0.0083333 -> degress per sec

MIN
360/60 = 6 degress per min
6/60 = 0.1 degress per sec

SEC
360/60 = 6 degress per sec
'''

# --- VARS ---
WIDTH = 300
HEIGHT = 300
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

# in pygame, angle increases clock-wise, 
# subtract 90 to make 12 o'clock be pointing up when angle is 0 
ANGLE_OFFSET = 90 

def rotate_hands(SURFACE, surf_rect):
    c_time = time.localtime()
    hour = c_time.tm_hour - 12
    minute = c_time.tm_min
    sec = c_time.tm_sec
    
    
    # HOUR | Convert to seconds to get degrees per second
    hour_degree = (3600*hour + 60*minute + sec) * (0.5 / 60)
    rad = math.radians(hour_degree - ANGLE_OFFSET)
    x = surf_rect.centerx + 90 * math.cos(rad)
    y = surf_rect.centery + 90 * math.sin(rad)
    pygame.draw.line(SURFACE, BLACK, surf_rect.center, (x, y), 3) 
    
    # MIN | Convert to seconds to get degrees per second
    minute_degree = 6*minute + 0.1*sec
    rad = math.radians(minute_degree - ANGLE_OFFSET)
    x = surf_rect.centerx + 120 * math.cos(rad)
    y = surf_rect.centery + 120 * math.sin(rad)
    pygame.draw.line(SURFACE, BLACK, surf_rect.center, (x, y), 3) 
    
    # SEC
    rad = math.radians(6*sec - ANGLE_OFFSET)
    x = surf_rect.centerx + 120 * math.cos(rad)
    y = surf_rect.centery + 120 * math.sin(rad)
    pygame.draw.aaline(SURFACE, RED, surf_rect.center, (x, y), 3)

    return None

def draw_clock(font, surf_rect):
    radius = 150
    rects = []
  
    # Clock text
    angle = 0
    for number in [12,1,2,3,4,5,6,7,8,9,10,11]:
        text = font.render(str(number), 1, BLACK)
        text_rect = text.get_rect(center=surf_rect.center) 
        
        rad = math.radians(angle-90) 
        text_rect.centerx += (radius-40) * math.cos(rad)
        text_rect.centery += (radius-40) * math.sin(rad)
        
        rects.append([text, text_rect])
        angle += 30
    
    # Draw clock surface/outline
    tick_locs = []
    for angle in range(0,360,6):      
        rad = math.radians(angle-ANGLE_OFFSET)
        x = surf_rect.centerx + ((radius-5) * math.cos(rad))
        y = surf_rect.centery + ((radius-5) * math.sin(rad))
        tick_locs.append([x, y])
    
    # Blit to seperate surface, then  blit that surface to display
    clock_surf = pygame.Surface((WIDTH, HEIGHT))
    clock_surf.fill('cornflowerblue')
    
    pygame.draw.circle(clock_surf, WHITE, surf_rect.center, radius)  
    
    # draw tick marks
    for loc in tick_locs:
        pygame.draw.aaline(clock_surf, (0,0,0), surf_rect.center, loc) # Line indicator

    # ticks extend from center, draw circle over 
    pygame.draw.circle(clock_surf, WHITE, surf_rect.center, radius-20)  
    pygame.draw.circle(clock_surf, BLACK, surf_rect.center, radius, 8) 
    pygame.draw.circle(clock_surf, BLACK, surf_rect.center, radius-20, 2) 
    
    clock_surf.blits(rects)
    
    return clock_surf
    

def main():
    # -- INIT -- #
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 25, True) # 'Arial' looks nice, but use system default

    SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clock")
    
    surf_rect = SURFACE.get_rect()
    clock_surf = draw_clock(font, surf_rect)

    # -- MAIN LOOP -- #           
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SURFACE.blit(clock_surf, (0,0))
        rotate_hands(SURFACE, surf_rect)
        
        pygame.draw.circle(SURFACE, BLACK, surf_rect.center, 5)
        pygame.display.update()

        clock.tick(120)

     
 
if __name__ == "__main__":
    main()
    pygame.quit() 


# eof
