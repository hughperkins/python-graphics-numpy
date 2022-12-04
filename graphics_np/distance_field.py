import argparse
import time

import pygame
import numpy as np
from numpy.typing import NDArray


def distance_shading(tile_size: int) -> NDArray[np.float32]:
    """
    coord[150, 70] = [150, 70]
    """
    # [W][H][2]
    coord = np.mgrid[0:tile_size, 0:tile_size].transpose(1, 2, 0)
    # [2]
    center = np.array([tile_size // 2, tile_size // 2])
    # [W][H][2]
    delta = coord - center
    # print('delta.shape', delta.shape)
    # v = (x, y)
    # length(v) = sqrt(x^2 + y^2)
    # _delta = (x, y)
    # _delta * _delta = (x * x, y * y)
    # [W][H]
    distance_to_center = np.sqrt((delta * delta).sum(axis=-1))

    # [W][H][C]
    image = np.zeros((tile_size, tile_size, 3), dtype=np.float32)   # 0...1

    image[:, :, 0] = distance_to_center / np.sqrt(tile_size * tile_size * 2)
    # image[distance_to_center]

    return image


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

    tile_size = 256 * args.res // 480

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

        distance_field_np = distance_shading(tile_size=tile_size)
        distance_field_surf = pygame.pixelcopy.make_surface(
            (distance_field_np * 255).astype(np.uint8))
        screen.blit(distance_field_surf, (0, 0))

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
