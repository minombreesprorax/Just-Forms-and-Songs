from typing import Callable, Union
import pygame

# Define a custom enumeration for keys
class KEnum:
    # Dictionary to map non-character keys to readable strings
    non_chr_keys = {
        pygame.K_BACKSPACE: 'BACKSPACE',
        pygame.K_TAB: 'TAB',
        pygame.K_RETURN: 'RETURN',
        pygame.K_ESCAPE: 'ESCAPE',
        pygame.K_SPACE: 'SPACE',
        pygame.K_DELETE: 'DELETE',
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_LSHIFT: 'LSHIFT',
        pygame.K_RSHIFT: 'RSHIFT',
        pygame.K_LCTRL: 'LCTRL',
        pygame.K_RCTRL: 'RCTRL',
        pygame.K_LALT: 'LALT',
        pygame.K_RALT: 'RALT',
        pygame.K_CAPSLOCK: 'CAPSLOCK',
        pygame.K_F1: 'F1',
        pygame.K_F2: 'F2',
        pygame.K_F3: 'F3',
        pygame.K_F4: 'F4',
        pygame.K_F5: 'F5',
        pygame.K_F6: 'F6',
        pygame.K_F7: 'F7',
        pygame.K_F8: 'F8',
        pygame.K_F9: 'F9',
        pygame.K_F10: 'F10',
        pygame.K_F11: 'F11',
        pygame.K_F12: 'F12',
        1073742051: 'LWIN',
        1073742055: 'RWIN',
        pygame.K_INSERT: 'INSERT',
        pygame.K_NUMLOCK: 'NUMLOCK',
        pygame.K_PAGEUP: 'PAGEUP',
        pygame.K_PAGEDOWN: 'PAGEDOWN',
        pygame.K_PRINTSCREEN: 'PRINTSCREEN',
        pygame.K_SCROLLLOCK: 'SCROLLLOCK',
        pygame.K_PAUSE: 'PAUSE',
        pygame.K_HOME: 'HOME',
        pygame.K_END: 'END',
        pygame.K_MENU: 'MENU',
        1073741925: 'MENU',
        pygame.K_KP_ENTER: 'KPENTER',
        pygame.K_KP0: 'KP0',
        pygame.K_KP1: 'KP1',
        pygame.K_KP2: 'KP2',
        pygame.K_KP3: 'KP3',
        pygame.K_KP4: 'KP4',
        pygame.K_KP5: 'KP5',
        pygame.K_KP6: 'KP6',
        pygame.K_KP7: 'KP7',
        pygame.K_KP8: 'KP8',
        pygame.K_KP9: 'KP9',
        pygame.K_KP_PERIOD: 'KP0',
        pygame.K_KP_PLUS: '+',
        pygame.K_KP_MINUS: '-',
        pygame.K_KP_DIVIDE: '/',
        pygame.K_KP_MULTIPLY: '*',
        # Add other non-character keys as needed
    }

    @staticmethod
    def get_key(key: int) -> str:
        if key in KEnum.non_chr_keys:
            return KEnum.non_chr_keys[key]
        try:
            k = str(chr(key))
            return k
        except ValueError:
            return key

# Define the Keyhole class
class Kh:
    def __init__(self):
        self.KTable = []
        self.Dbindings = {}
        self.Pbindings = {}
        self.Ubindings = {}

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            key = KEnum.get_key(event.key)
            if key not in self.KTable:  # Ensure the key is not already in the list
                self.KTable.append(key)
                # Call the bound functions
                if key in self.Dbindings:
                    for binding in self.Dbindings[key]:
                        binding()
        if event.type == pygame.KEYUP:
            key = KEnum.get_key(event.key)
            if key in self.KTable:
                self.KTable.remove(key)
                # Call the bound functions
                if key in self.Ubindings:
                    for binding in self.Ubindings[key]:
                        binding()
    
    def update(self):
        for key in self.KTable:
            # Call the bound functions
            if key in self.Pbindings:
                for binding in self.Pbindings[key]:
                    binding()
    
    def getKeys(self):
        return self.KTable

    def bind_key_down(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str not in self.Dbindings:
            self.Dbindings[key_str] = []
        self.Dbindings[key_str].append(binding)

    def bind_key_tick(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str not in self.Pbindings:
            self.Pbindings[key_str] = []
        self.Pbindings[key_str].append(binding)

    def bind_key_up(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str not in self.Ubindings:
            self.Ubindings[key_str] = []
        self.Ubindings[key_str].append(binding)

    def unbind_key_down(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str in self.Dbindings:
            self.Dbindings[key_str].remove(binding)
            if self.Dbindings[key_str] == []:
                del self.Dbindings[key_str]

    def unbind_key_tick(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str in self.Pbindings:
            self.Pbindings[key_str].remove(binding)
            if self.Pbindings[key_str] == []:
                del self.Pbindings[key_str]

    def unbind_key_up(self, key: Union[int, str], binding: Callable):
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        if key_str in self.Ubindings:
            self.Ubindings[key_str].remove(binding)
            if self.Ubindings[key_str] == []:
                del self.Ubindings[key_str]
    
    def is_pressed(self, key: Union[int, str]) -> bool:
        key_str = KEnum.get_key(key) if isinstance(key, int) else key
        return key_str in self.KTable