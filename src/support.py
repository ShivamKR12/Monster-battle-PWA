from settings import * 
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(resource_path(join(*path))):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(resource_path(join(*path))):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict

def tile_importer(cols, *path):
    attack_frames = {}
    for folder_path, _, file_names in walk(resource_path(join(*path))):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            attack_frames[file_name.split('.')[0]] = []
            cutout_width = surf.get_width() / cols
            for col in range(cols):
                cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)
                cutout_rect = pygame.FRect(cutout_width * col,0,cutout_width,surf.get_height())
                cutout_surf.blit(surf, (0,0),cutout_rect)
                attack_frames[file_name.split('.')[0]].append(cutout_surf)
    return attack_frames
