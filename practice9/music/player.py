import pygame
import os

class MusicPlayer:
    def __init__(self, musics_folder):
        pygame.mixer.init()
        self.folder = musics_folder
        self.playlist = [f for f in os.listdir(musics_folder) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_playing = False

    def load_track(self):
        if self.playlist:
            track_path = os.path.join(self.folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)

    def play(self):
        if not self.is_playing:
            if not pygame.mixer.music.get_busy():
                self.load_track()
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop()
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop()
        self.play()

    def get_current_track_name(self):
        return self.playlist[self.current_index] if self.playlist else "No tracks found"