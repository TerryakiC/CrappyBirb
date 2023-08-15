import pygame
import random
from sklearn.linear_model import LogisticRegression
def main():
    green = pygame.Color(0, 255, 0)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    light_blue = pygame.Color(0, 255, 255)
    yellow = pygame.Color(255, 255, 0)
    beakSize = [30, 20]
    eye_size = [5, 15]
    window_x = 720
    window_y = 480
    birb_speed = 30
    birb_size = [60, 40]
    birb_position = [30, window_y // 2]
    wing_size = [30, 20]
    birb_fall_rate = 5
    score = 0

    cpu = False

    alive = True
    pipe_size = [100, 500]
    pipe_position = [450, random.randrange (150, 450, 25)]
    pipe2_size = [100, window_y - (window_y - pipe_position[1]) - 150]
    pipe2_position = [450, 0]
    pipe3_size = [100, 500]
    pipe3_position = [800, random.randrange(150, 450, 25)]
    pipe4_size = [100, window_y - (window_y - pipe3_position[1]) - 150]
    pipe4_position = [800, 0]
    pygame.init()

    pygame.display.set_caption('Crappy birb')
    game_window = pygame.display.set_mode((window_x, window_y))
    fall = 0
    birb_velocity = 20
    flapped = False
    fps = pygame.time.Clock()
    flap = 70


    def gameOver():
        font = pygame.font.SysFont('boldarial', 60)
        text = font.render('Game Over', True, red)
        game_window.blit(text, (window_x // 3, 100))
    def showScore():
        font = pygame.font.SysFont('boldarial', 100)

        text = font.render(str(score), True, white)

        game_window.blit(text, (window_x / 2 - 50, 40))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if alive:
                    if event.key == pygame.K_SPACE:
                        if not cpu:
                            flapped = True
                            flap = 0
                            birb_fall_rate = 5
                            fall = 0
                if event.key == pygame.K_RIGHT:
                    pygame.quit()
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_t:
                    if not cpu:
                        cpu = True
                    else:
                        cpu = False
        if alive:
            if cpu:

                training_data = [[100, 200], [400, 300], [50, 300], [450, 200], [50, 100],[200, 100], [250, 300], [400, 0]]
                target_values = [1, 0, 1, 0, 1, 0, 1, 0]
                model = LogisticRegression()
                model.fit(training_data, target_values)

                pipes2_center = pipe4_size[1] + abs(pipe3_position[1] - pipe4_size[1]) / 2
                pipes1_center = pipe2_size[1] + abs(pipe_position[1] - pipe2_size[1]) / 2
                birb_center = birb_position[1] + birb_size[1] / 2

                if pipe_position[0] <= pipe3_position[0] and pipe_position[0] + pipe_size[0] > birb_position[0]:
                    prediction = model.predict([[birb_center, pipes1_center]])

                else:
                    prediction = model.predict([[birb_center, pipes2_center]])

                #print('input: [{}, {}], prediction: {}'.format(birb_center, pipes1_center, prediction))
                if prediction == 0:
                    flapped = True
                    flap = 0
                    birb_fall_rate = 5
                    fall = 0
            if flapped:
                birb_position[1] -= birb_velocity
                flap += abs(birb_velocity)

            if flap >= 60:
                fall += 1
                if fall >= 7:
                    birb_fall_rate += 0.1
                    birb_position[1] += birb_fall_rate
                flapped = False
            pipe_position[0] -= 5
            pipe2_position[0] -= 5
            pipe3_position[0] -= 5
            pipe4_position[0] -= 5

        if birb_position[0] == pipe_position[0] + pipe_size[0]:
                score += 10
        if birb_position[0] == pipe3_position[0] + pipe_size[0]:
                score += 10



        if pipe2_position[0] + pipe2_size[0] < 0 and pipe_position[0] + pipe_size[0] < 0:
            if pipe3_position[0] < 300:
                pipe_position[0] = 600
                pipe_position[1] = random.randrange(150, 450, 25)
                pipe2_position[0] = 600
                pipe2_size[1] = window_y - (window_y - pipe_position[1]) - 150


        if pipe4_position[0] + pipe4_size[0] < 0 and pipe3_position[0] + pipe3_size[0] < 0:
            if pipe_position[0] < 250:
                pipe3_position[0] = 600

                pipe3_position[1] = random.randrange(150, 450, 25)
                pipe4_position[0] = 600
                if pipe_position[1] == pipe3_position[1]:
                    pipe3_position[1] = random.randrange(150, 450, 25)
                pipe4_size[1] = window_y - (window_y - pipe3_position[1]) - 150


        game_window.fill(light_blue)

        if birb_position[1] < 5:
            alive = False

        if birb_position[1] + birb_size[1] > 480:
            alive = False

        if birb_position[0] + birb_size[0] == pipe_position[0]:
            if birb_position[1] >= pipe_position[1] and birb_position[1] + birb_size[1] <= pipe_position[1] + pipe_size[1]:
                alive = False

        if birb_position[1] + birb_size[1] >= pipe_position[1]:
            if birb_position[0] + birb_size[0] <= pipe_position[0] + pipe_size[0] + 50 and birb_position[0] >= pipe_position[0] - 60:
                alive = False

        if birb_position[1] <= pipe2_position[1] + pipe2_size[1]:
            if birb_position[0] + birb_size[0] <= pipe2_position[0] + pipe2_size[0] + 50 and birb_position[0] >= pipe2_position[0] - 60:
                alive = False

        if birb_position[0] + birb_size[0] == pipe2_position[0]:
            if birb_position[1] >= pipe2_position[1] and birb_position[1] + birb_size[1] <= pipe2_position[1] + pipe2_size[1]:
                alive = False

        if birb_position[0] + birb_size[0] == pipe3_position[0]:
            if birb_position[1] >= pipe3_position[1] and birb_position[1] + birb_size[1] <= pipe3_position[1] + \
                    pipe3_size[1]:
                alive = False

        if birb_position[1] + birb_size[1] >= pipe3_position[1]:
            if birb_position[0] + birb_size[0] <= pipe3_position[0] + pipe3_size[0] + 50 and birb_position[0] >= \
                    pipe3_position[0] - 60:
                alive = False

        if birb_position[1] <= pipe4_position[1] + pipe4_size[1]:
            if birb_position[0] + birb_size[0] <= pipe4_position[0] + pipe4_size[0] + 50 and birb_position[0] >= \
                    pipe4_position[0] - 60:
                alive = False

        if birb_position[0] + birb_size[0] == pipe4_position[0]:
            if birb_position[1] >= pipe4_position[1] and birb_position[1] + birb_size[1] <= pipe4_position[1] + \
                    pipe4_size[1]:
                alive = False


        beak_position = [birb_position[0] + birb_size[0] - 25, birb_position[1] + birb_size[1] // 2]
        eye_position = [birb_position[0] + birb_size[0] - 10, birb_position[1] + birb_size[1] // 5 - 5]
        wing_position = [birb_position[0] - 10, birb_position[1] + birb_size[1] // 5]

        pygame.draw.rect(game_window, yellow, pygame.Rect(birb_position[0], birb_position[1], birb_size[0], birb_size[1]))
        pygame.draw.rect(game_window, red, pygame.Rect(beak_position[0], beak_position[1], beakSize[0], beakSize[1]))
        pygame.draw.rect(game_window, white, pygame.Rect(wing_position[0], wing_position[1], wing_size[0], wing_size[1]))
        pygame.draw.rect(game_window, black, pygame.Rect(eye_position[0], eye_position[1], eye_size[0], eye_size[1]))
        pygame.draw.rect(game_window, green, pygame.Rect(pipe_position[0], pipe_position[1], pipe_size[0], pipe_size[1]))
        pygame.draw.rect(game_window, green, pygame.Rect(pipe2_position[0], pipe2_position[1], pipe2_size[0], pipe2_size[1]))
        pygame.draw.rect(game_window, green, pygame.Rect(pipe3_position[0], pipe3_position[1], pipe3_size[0], pipe3_size[1]))
        pygame.draw.rect(game_window, green, pygame.Rect(pipe4_position[0], pipe2_position[1], pipe4_size[0], pipe4_size[1]))

        showScore()
        if not alive:
            gameOver()
        pygame.display.update()

        fps.tick(40)

main()





















