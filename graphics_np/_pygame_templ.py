import argparse
import time

import pygame


def run(args: argparse.Namespace) -> None:
    pygame.init()
    screen_height = args.res
    screen_width = screen_height * 16 // 9
    if screen_width == 853:
        screen_width = 854
    print("screen", screen_width, "x", screen_height)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(__file__.split("/")[-1].split(".")[0])
    content_font = pygame.font.SysFont("Arial", 18 * args.res // 480)
    clock = pygame.time.Clock()

    running = True
    last_print = time.time()
    render_time_since_last = 0.0
    render_time_ms_avg = 0.0
    all_frames = 0
    last_frames = 0
    fps = 0.0
    while running:
        render_start = time.time()
        screen.fill((0, 0, 0, 255))

        render_time_since_last += time.time() - render_start
        screen.blit(
            content_font.render(
                f"{fps:.1f} fps render {render_time_ms_avg:.1f}ms",
                True,
                pygame.Color("white"),
            ),
            (20 * args.res // 480, screen_height - 40 * args.res // 480),
        )
        pygame.display.flip()
        clock.tick(args.fps)
        if time.time() - last_print >= 1.0:
            frames_since_last = all_frames - last_frames
            time_since_last = time.time() - last_print
            fps = frames_since_last / time_since_last
            render_time_ms_avg = render_time_since_last / frames_since_last * 1000
            render_time_since_last = 0.0
            last_print = time.time()
            last_frames = all_frames
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode == "q" or event.key == pygame.K_ESCAPE:
                    running = False
        all_frames += 1
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--res", type=int, choices=[480, 720, 1080], default=480)
    parser.add_argument("--fps", type=int, default=60)
    args = parser.parse_args()
    run(args)
