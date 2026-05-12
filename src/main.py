# /// script
# dependencies = [
#     'pygame-ce'
# ]
# ///


from settings import *
from support import *
from timer import Timer # type: ignore
from monster import *
from random import choice
from ui import *
from attack import AttackAnimationSprite
import sys
import asyncio
from pygame.locals import *


async def main():
    class Game:
        def __init__(self):
            pygame.init()
            
            # True hardware screen, let the browser define the size
            self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
            # Virtual resolution surface (Everything draws to this first!)
            self.display_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('Monster Battle')
            self.clock = pygame.time.Clock()
            self.running = True
            self.import_assets()
            pygame.display.set_icon(self.simple_surfs['Sparchu'])
            self.bg_surfs['bg'] = pygame.transform.scale(self.bg_surfs['bg'], (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.audio['music'].play(-1)
            self.player_active = True
            self.state = 'battle'
            self.opponent_kills = 0
            self.win_condition = 3

            # groups 
            self.all_sprites = pygame.sprite.Group()

            # data 
            player_monster_list = ['Sparchu', 'Jacana', 'Plumette', 'Atrox']
            self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
            self.monster = self.player_monsters[0]
            self.all_sprites.add(self.monster)
            opponent_name = choice(list(MONSTER_DATA.keys()))
            self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

            # ui 
            self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input, self.display_surface, self.screen)
            self.opponent_ui = OpponentUI(self.opponent, self.display_surface)

            # timers
            self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}

            self.end_button_rects = {}
        
        def normalize_pos(self, pos):
            # Get actual screen dimensions and calculate scale
            screen_w, screen_h = self.screen.get_size()
            scale = min(screen_w / WINDOW_WIDTH, screen_h / WINDOW_HEIGHT)
            
            # Calculate letterbox offsets
            scaled_w = int(WINDOW_WIDTH * scale)
            scaled_h = int(WINDOW_HEIGHT * scale)
            offset_x = (screen_w - scaled_w) // 2
            offset_y = (screen_h - scaled_h) // 2
            
            # Convert true screen coordinates back to virtual coordinates
            return (
                (pos[0] - offset_x) / scale,
                (pos[1] - offset_y) / scale
            )

        def reset_game(self):
            self.player_active = True
            self.state = 'battle'
            self.opponent_kills = 0

            # groups 
            self.all_sprites.empty()

            # data 
            player_monster_list = ['Sparchu', 'Jacana', 'Plumette', 'Atrox']
            self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
            self.monster = self.player_monsters[0]
            self.all_sprites.add(self.monster)
            opponent_name = choice(list(MONSTER_DATA.keys()))
            self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

            # ui 
            self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input, self.display_surface, self.screen)
            self.opponent_ui = OpponentUI(self.opponent, self.display_surface)

            # timers
            self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}

        def get_input(self, state, data = None):
            if state == 'attack':
                self.apply_attack(self.opponent, data)
            elif state == 'heal':
                self.monster.health += 50
                AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
                self.audio['green'].play()
            elif state == 'switch':
                self.monster.kill()
                self.monster = data
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster

            elif state == 'escape':
                self.running = False
            self.player_active = False
            self.timers['player end'].activate()

        def apply_attack(self, target, attack):
            attack_data = ABILITIES_DATA[attack]
            attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
            target.health -= attack_data['damage'] * attack_multiplier
            AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
            self.audio[attack_data['animation']].play()

        def opponent_turn(self):
            if self.opponent.health <= 0:
                self.opponent_kills += 1
                if self.opponent_kills >= self.win_condition:
                    self.state = 'victory'
                else:
                    self.player_active = True
                    self.opponent.kill()
                    monster_name = choice(list(MONSTER_DATA.keys()))
                    self.opponent = Opponent(monster_name, self.front_surfs[monster_name], self.all_sprites)
                    self.opponent_ui.monster = self.opponent
            else:
                attack = choice(self.opponent.abilities)
                self.apply_attack(self.monster, attack)
                self.timers['opponent end'].activate()

        def player_turn(self):
            self.player_active = True
            if self.monster.health <= 0:
                available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
                if available_monsters:
                    self.monster.kill()
                    self.monster = available_monsters[0]
                    self.all_sprites.add(self.monster)
                    self.ui.monster = self.monster
                else:
                    self.state = 'game_over'

        def update_timers(self):
            for timer in self.timers.values():
                timer.update()

        def import_assets(self):
            self.back_surfs = folder_importer('images', 'back')
            self.front_surfs = folder_importer('images', 'front')
            self.bg_surfs = folder_importer('images', 'other')
            self.simple_surfs = folder_importer('images', 'simple')
            self.attack_frames = tile_importer(4,'images', 'attacks')
            self.audio = audio_importer('audio')

        def draw_monster_floor(self):
            for sprite in self.all_sprites:
                if isinstance(sprite, Creature):
                    floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                    self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

        async def run(self):
            while self.running:
                dt = self.clock.tick(60) / 1000
                pygame.event.pump()
                for event in pygame.event.get(pygame.QUIT, pump=False):
                    self.running = False
            
                if self.state == 'battle':
                    # update
                    self.update_timers()
                    self.all_sprites.update(dt)
                    if self.player_active:
                        self.ui.update()

                self.display_surface.blit(self.bg_surfs['bg'], (0,0))
                self.draw_monster_floor()
                self.all_sprites.draw(self.display_surface)
                self.ui.draw()
                self.opponent_ui.draw()

                if self.state != 'battle':
                    screen_copy = self.display_surface.copy()
                    tiny_surf = pygame.transform.smoothscale(screen_copy, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
                    blur_surf = pygame.transform.smoothscale(tiny_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    
                    tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                    tint_surf.fill(COLORS['black'])
                    tint_surf.set_alpha(150)
                    blur_surf.blit(tint_surf, (0, 0))
                    self.display_surface.blit(blur_surf, (0, 0))

                    font = pygame.font.Font(None, 100)
                    text = 'VICTORY' if self.state == 'victory' else 'GAME OVER'
                    color = COLORS['green'] if self.state == 'victory' else COLORS['red']
                    text_surf = font.render(text, True, color)
                    text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
                    self.display_surface.blit(text_surf, text_rect)

                    button_font = pygame.font.Font(None, 50)

                    restart_rect = pygame.FRect(
                        WINDOW_WIDTH / 2 - 220,
                        WINDOW_HEIGHT / 2 + 20,
                        180,
                        70
                    )

                    quit_rect = pygame.FRect(
                        WINDOW_WIDTH / 2 + 40,
                        WINDOW_HEIGHT / 2 + 20,
                        180,
                        70
                    )

                    self.end_button_rects = {
                        'restart': restart_rect,
                        'quit': quit_rect
                    }

                    pygame.draw.rect(
                        self.display_surface,
                        COLORS['white'],
                        restart_rect,
                        0,
                        8
                    )

                    pygame.draw.rect(
                        self.display_surface,
                        COLORS['gray'],
                        restart_rect,
                        3,
                        8
                    )

                    pygame.draw.rect(
                        self.display_surface,
                        COLORS['white'],
                        quit_rect,
                        0,
                        8
                    )

                    pygame.draw.rect(
                        self.display_surface,
                        COLORS['gray'],
                        quit_rect,
                        3,
                        8
                    )

                    restart_surf = button_font.render(
                        "Restart",
                        True,
                        COLORS['black']
                    )

                    quit_surf = button_font.render(
                        "Quit",
                        True,
                        COLORS['black']
                    )

                    self.display_surface.blit(
                        restart_surf,
                        restart_surf.get_frect(center=restart_rect.center)
                    )

                    self.display_surface.blit(
                        quit_surf,
                        quit_surf.get_frect(center=quit_rect.center)
                    )

                    for event in pygame.event.get(pygame.KEYDOWN, pump=False):

                        if event.key == pygame.K_SPACE:
                            self.reset_game()

                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

                    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False):

                        if event.button == 1:

                            mouse_pos = self.normalize_pos(event.pos)

                            if self.end_button_rects['restart'].collidepoint(mouse_pos):
                                self.reset_game()

                            elif self.end_button_rects['quit'].collidepoint(mouse_pos):
                                self.running = False

                    for event in pygame.event.get(pygame.FINGERDOWN, pump=False):

                        x = event.x * self.screen.get_width()
                        y = event.y * self.screen.get_height()

                        if self.end_button_rects['restart'].collidepoint(self.normalize_pos((x, y))):
                            self.reset_game()

                        elif self.end_button_rects['quit'].collidepoint(self.normalize_pos((x, y))):
                            self.running = False

                # Render Virtual Surface to True Screen
                screen_w, screen_h = self.screen.get_size()
                scale = min(screen_w / WINDOW_WIDTH, screen_h / WINDOW_HEIGHT)
                scaled_w, scaled_h = int(WINDOW_WIDTH * scale), int(WINDOW_HEIGHT * scale)
                
                self.screen.fill(COLORS['black']) # Fill borders with black
                scaled_surf = pygame.transform.scale(self.display_surface, (scaled_w, scaled_h))
                scaled_rect = scaled_surf.get_rect(center=(screen_w // 2, screen_h // 2))
                self.screen.blit(scaled_surf, scaled_rect)

                pygame.display.update()

                await asyncio.sleep(0) # allow other tasks to run
            
            pygame.quit()
        
            # if sys.platform in ("emscripten", "wasi", "android"):
            #     import platform
            #     platform.window.close()
                
            sys.exit()
    

    game = Game()
    await game.run()


asyncio.run(main())
