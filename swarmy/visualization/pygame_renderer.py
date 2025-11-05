"""
Pygame Visualization Renderer
----------------------------
Real-time interactive visualization of Swarmy using Pygame.
"""
import pygame
from swarmy.visualization.renderer_base import RendererBase

class PygameRenderer(RendererBase):
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Swarmy Visualization (Pygame)')
        self.clock = pygame.time.Clock()

    def render(self, state):
        self.screen.fill((240, 240, 240))
        for agent in state['agents']:
            color = (100, 100, 100) if not agent['is_scout'] else (150, 150, 150)
            pos = (int(agent['position'][0]), int(agent['position'][1]))
            pygame.draw.circle(self.screen, color, pos, 3)
        for queen in state['queens']:
            pos = (int(queen['position'][0]), int(queen['position'][1]))
            pygame.draw.circle(self.screen, (255, 215, 0), pos, 15)
        for resource in state['resources']:
            color = (255, 0, 0) if resource['resource_type'] == 'red' else (0, 255, 0) if resource['resource_type'] == 'green' else (0, 0, 255)
            pos = (int(resource['position'][0]), int(resource['position'][1]))
            pygame.draw.circle(self.screen, color, pos, 10)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self.clock.tick(60)
