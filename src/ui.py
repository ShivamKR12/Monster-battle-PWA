from settings import * 

class UI:
    def __init__(self, monster, player_monsters, simple_surfs, get_input, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100 
        self.top = WINDOW_HEIGHT / 2 + 50
        self.monster = monster
        self.simple_surfs = simple_surfs
        self.get_input = get_input

        # control 
        self.general_options = ['attack', 'heal', 'switch', 'escape']
        self.general_index = {'col': 0, 'row': 0}
        self.attack_index = {'col': 0, 'row': 0}
        self.state = 'general'
        self.rows, self.cols = 2,2
        self.visible_monsters = 4
        self.player_monsters = player_monsters
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]
        self.switch_index = 0

        # touch / mouse button rects
        self.button_rects = []
        self.switch_rects = []

    def input(self):
        pygame.event.pump()

        for event in pygame.event.get(pygame.KEYDOWN, pump=False):

            if self.state == 'general':

                if event.key == pygame.K_DOWN:
                    self.general_index['row'] = (
                        self.general_index['row'] + 1
                    ) % self.rows

                elif event.key == pygame.K_UP:
                    self.general_index['row'] = (
                        self.general_index['row'] - 1
                    ) % self.rows

                elif event.key == pygame.K_RIGHT:
                    self.general_index['col'] = (
                        self.general_index['col'] + 1
                    ) % self.cols

                elif event.key == pygame.K_LEFT:
                    self.general_index['col'] = (
                        self.general_index['col'] - 1
                    ) % self.cols

                elif event.key == pygame.K_SPACE:
                    self.state = self.general_options[
                        self.general_index['col'] +
                        self.general_index['row'] * 2
                    ]

            elif self.state == 'attack':

                if event.key == pygame.K_DOWN:
                    self.attack_index['row'] = (
                        self.attack_index['row'] + 1
                    ) % self.rows

                elif event.key == pygame.K_UP:
                    self.attack_index['row'] = (
                        self.attack_index['row'] - 1
                    ) % self.rows

                elif event.key == pygame.K_RIGHT:
                    self.attack_index['col'] = (
                        self.attack_index['col'] + 1
                    ) % self.cols

                elif event.key == pygame.K_LEFT:
                    self.attack_index['col'] = (
                        self.attack_index['col'] - 1
                    ) % self.cols

                elif event.key == pygame.K_SPACE:

                    attack = self.monster.abilities[
                        self.attack_index['col'] +
                        self.attack_index['row'] * 2
                    ]

                    self.get_input(self.state, attack)
                    self.state = 'general'

            elif self.state == 'switch':

                if self.available_monsters:

                    if event.key == pygame.K_DOWN:
                        self.switch_index = (
                            self.switch_index + 1
                        ) % len(self.available_monsters)

                    elif event.key == pygame.K_UP:
                        self.switch_index = (
                            self.switch_index - 1
                        ) % len(self.available_monsters)

                    elif event.key == pygame.K_SPACE:
                        self.get_input(
                            self.state,
                            self.available_monsters[self.switch_index]
                        )

                        self.state = 'general'

            elif self.state == 'heal':

                self.get_input('heal')
                self.state = 'general'

            elif self.state == 'escape':

                self.get_input('escape')

            if event.key == pygame.K_ESCAPE:

                if self.state == 'general':
                    self.get_input('escape')

                else:
                    self.state = 'general'

                    self.general_index = {
                        'col': 0,
                        'row': 0
                    }

                    self.attack_index = {
                        'col': 0,
                        'row': 0
                    }

                    self.switch_index = 0

        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False):

            if event.button == 1:
                self.handle_touch(event.pos)

        for event in pygame.event.get(pygame.FINGERDOWN, pump=False):

            x = event.x * WINDOW_WIDTH
            y = event.y * WINDOW_HEIGHT

            self.handle_touch((x, y))

    def handle_touch(self, pos):

        if self.state == 'general':

            for i, rect in enumerate(self.button_rects):

                if rect.collidepoint(pos):

                    self.general_index['col'] = i % 2
                    self.general_index['row'] = i // 2

                    selected = self.general_options[i]

                    if selected == 'heal':
                        self.get_input('heal')

                    elif selected == 'escape':
                        self.get_input('escape')

                    else:
                        self.state = selected

                    break

        elif self.state == 'attack':

            for i, rect in enumerate(self.button_rects):

                if rect.collidepoint(pos):

                    self.attack_index['col'] = i % 2
                    self.attack_index['row'] = i // 2

                    attack = self.monster.abilities[i]

                    self.get_input('attack', attack)
                    self.state = 'general'
                    break

        elif self.state == 'switch':

            for i, rect in enumerate(self.switch_rects):

                if rect.collidepoint(pos):

                    self.switch_index = i

                    self.get_input(
                        'switch',
                        self.available_monsters[i]
                    )

                    self.state = 'general'
                    break

    def quad_select(self, index, options):
        # bg
        rect = pygame.FRect(self.left + 40, self.top + 60 ,400, 200)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)

        # menu
        self.button_rects = []

        for col in range(self.cols):
            for row in range(self.rows):

                x = rect.left + rect.width / (self.cols * 2) + \
                    (rect.width / self.cols) * col

                y = rect.top + rect.height / (self.rows * 2) + \
                    (rect.height / self.rows) * row

                i = col + 2 * row

                button_rect = pygame.FRect(
                    0, 0,
                    rect.width / 2,
                    rect.height / 2
                )

                button_rect.center = (x, y)

                self.button_rects.append(button_rect)

                selected = (
                    col == index['col'] and
                    row == index['row']
                )

                color = COLORS['white'] if selected else COLORS['black']

                pygame.draw.rect(
                    self.display_surface,
                    COLORS['gray'] if selected else COLORS['white'],
                    button_rect,
                    0,
                    4
                )

                pygame.draw.rect(
                    self.display_surface,
                    COLORS['black'] if selected else COLORS['gray'],
                    button_rect,
                    2,
                    4
                )

                text_surf = self.font.render(
                    options[i],
                    True,
                    color
                )

                text_rect = text_surf.get_frect(
                    center=(x, y)
                )

                self.display_surface.blit(
                    text_surf,
                    text_rect
                )

    def switch(self):
        # bg
        rect = pygame.FRect(self.left + 40, self.top - 140 ,400, 400)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)

        # menu 
        self.switch_rects = []
        v_offset = 0 if self.switch_index < self.visible_monsters else -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters
        for i in range(len(self.available_monsters)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset
            color = COLORS['white'] if i == self.switch_index else COLORS['black']
            name = self.available_monsters[i].name

            simple_surf = self.simple_surfs[name]
            simple_rect = simple_surf.get_frect(center = (x - 100, y))
            
            entry_rect = pygame.FRect(
                rect.left + 20,
                y - 30,
                rect.width - 40,
                60
            )

            self.switch_rects.append(entry_rect)

            pygame.draw.rect(
                self.display_surface,
                COLORS['gray'] if i == self.switch_index else COLORS['white'],
                entry_rect,
                0,
                4
            )

            pygame.draw.rect(
                self.display_surface,
                COLORS['gray'],
                entry_rect,
                2,
                4
            )

            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_frect(midleft = (x,y))
            if rect.collidepoint(text_rect.center):
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(simple_surf, simple_rect)

    def stats(self):
        # bg 
        rect = pygame.FRect(self.left, self.top, 250, 80)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)

        # data 
        name_surf = self.font.render(self.monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
        self.display_surface.blit(name_surf, name_rect)

        # health bar 
        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)
        self.draw_bar(health_rect, self.monster.health, self.monster.max_health)
    
    def draw_bar(self, rect, value, max_value):
        ratio = rect.width / max_value
        progress_rect = pygame.FRect(rect.topleft, (value * ratio,rect.height))
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)

    def update(self):
        self.input()
        self.available_monsters = [monster for monster in self.player_monsters if monster!= self.monster and monster.health > 0]

    def draw(self):
        match self.state:
            case 'general': self.quad_select(self.general_index, self.general_options)
            case 'attack': self.quad_select(self.attack_index, self.monster.abilities)
            case 'switch': self.switch()
        
        if self.state != 'switch':
            self.stats()

class OpponentUI:
    def __init__(self, monster, display_surface):
        self.display_surface = display_surface
        self.monster = monster
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        # bg 
        rect = pygame.FRect((0,0), (250,80)).move_to(midleft = (500, self.monster.rect.centery))
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)

        # name
        name_surf = self.font.render(self.monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
        self.display_surface.blit(name_surf, name_rect)

        # health
        health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        ratio = health_rect.width / self.monster.max_health
        progress_rect = pygame.FRect(health_rect.topleft, (self.monster.health * ratio, health_rect.height))
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)
