import pygame

from ui import Button, draw_text, draw_title, get_text_input, BIG_FONT, FONT
from ui import BLACK, BLUE, GREEN, RED
from persistence import load_settings, save_settings, load_leaderboard
from racer import RacerGame, WIDTH, HEIGHT


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")
clock = pygame.time.Clock()


def main_menu(settings):
    buttons = {
        "play": Button("Play", (200, 220, 200, 55), GREEN),
        "leaderboard": Button("Leaderboard", (200, 295, 200, 55), BLUE),
        "settings": Button("Settings", (200, 370, 200, 55), BLUE),
        "quit": Button("Quit", (200, 445, 200, 55), RED),
    }

    while True:
        screen.fill((230, 230, 230))

        draw_title(screen, "TSIS3 Racer", WIDTH)
        draw_text(screen, "Advanced Driving, Leaderboard & Power-Ups", WIDTH // 2, 155, BLACK, FONT, center=True)

        for button in buttons.values():
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            for name, button in buttons.items():
                if button.is_clicked(event):
                    return name

        pygame.display.flip()
        clock.tick(60)


def settings_screen(settings):
    sound_button = Button("", (180, 190, 240, 50), BLUE)
    color_button = Button("", (180, 270, 240, 50), BLUE)
    diff_button = Button("", (180, 350, 240, 50), BLUE)
    back_button = Button("Back", (200, 500, 200, 55), RED)

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill((235, 235, 235))

        draw_title(screen, "Settings", WIDTH)

        sound_button.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_button.text = f"Car color: {settings['car_color']}"
        diff_button.text = f"Difficulty: {settings['difficulty']}"

        sound_button.draw(screen)
        color_button.draw(screen)
        diff_button.draw(screen)
        back_button.draw(screen)

        draw_text(screen, "Settings are saved to settings.json", WIDTH // 2, 445, BLACK, FONT, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_button.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            elif color_button.is_clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            elif diff_button.is_clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            elif back_button.is_clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back_button = Button("Back", (200, 690, 200, 50), RED)

    while True:
        screen.fill((240, 240, 240))

        draw_title(screen, "Leaderboard Top 10", WIDTH)

        scores = load_leaderboard()

        y = 160
        draw_text(screen, "Rank", 55, 125)
        draw_text(screen, "Name", 130, 125)
        draw_text(screen, "Score", 285, 125)
        draw_text(screen, "Distance", 410, 125)

        if not scores:
            draw_text(screen, "No scores yet", WIDTH // 2, 250, BLACK, FONT, center=True)

        for i, item in enumerate(scores, start=1):
            draw_text(screen, i, 65, y)
            draw_text(screen, item["name"], 130, y)
            draw_text(screen, item["score"], 285, y)
            draw_text(screen, f"{item['distance']}m", 410, y)
            y += 45

        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_button.is_clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(status, score, distance, coins):
    retry_button = Button("Retry", (200, 420, 200, 55), GREEN)
    menu_button = Button("Main Menu", (200, 500, 200, 55), BLUE)

    while True:
        screen.fill((235, 235, 235))

        title = "Finished!" if status == "finished" else "Game Over"

        draw_text(screen, title, WIDTH // 2, 150, BLACK, BIG_FONT, center=True)
        draw_text(screen, f"Score: {score}", WIDTH // 2, 240, BLACK, FONT, center=True)
        draw_text(screen, f"Distance: {distance}m", WIDTH // 2, 285, BLACK, FONT, center=True)
        draw_text(screen, f"Coins: {coins}", WIDTH // 2, 330, BLACK, FONT, center=True)

        retry_button.draw(screen)
        menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_button.is_clicked(event):
                return "retry"

            if menu_button.is_clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def run_game(settings):
    name = get_text_input(screen, clock, WIDTH, HEIGHT)

    if name is None:
        return "menu"

    while True:
        game = RacerGame(screen, clock, settings, name)
        status, score, distance, coins = game.run()

        if status == "quit":
            return "quit"

        action = game_over_screen(status, score, distance, coins)

        if action == "retry":
            continue

        return action


def main():
    settings = load_settings()

    while True:
        action = main_menu(settings)

        if action == "quit":
            break

        elif action == "play":
            result = run_game(settings)
            if result == "quit":
                break

        elif action == "leaderboard":
            result = leaderboard_screen()
            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(settings)
            if result == "quit":
                break

    pygame.quit()


if __name__ == "__main__":
    main()