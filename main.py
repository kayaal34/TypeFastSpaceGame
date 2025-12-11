import random
import math
import pygame
import sys
import asyncio
from enum import Enum

# Pygame başlatma
pygame.init()

# Ekran ayarları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Renkler (Neon teması)
COLOR_BG = (5, 10, 40)
COLOR_PLAYER = (0, 255, 255)
COLOR_ENEMY = (255, 0, 127)
COLOR_BULLET = (0, 255, 0)
COLOR_STAR = (200, 200, 255)
COLOR_TEXT = (0, 255, 255)
COLOR_HEALTH = (0, 255, 0)
COLOR_HEALTH_BG = (50, 50, 50)
COLOR_BUTTON = (0, 150, 200)
COLOR_BUTTON_HOVER = (0, 200, 255)

# Rusça kelime havuzu (dalga seviyelerine göre)
RUSSIAN_WORDS = {
    1: ["Да", "Нет", "Дом", "Кот", "Сын", "Мир", "Год", "День"],
    2: ["Мама", "Папа", "Вода", "Небо", "Море", "Земля", "Рука", "Нога"],
    3: ["Собака", "Кошка", "Птица", "Рыба", "Солнце", "Луна", "Звезда"],
    4: ["Россия", "Москва", "Человек", "Дерево", "Цветок", "Облако"],
    5: ["Космонавт", "Галактика", "Планета", "Метеорит", "Астероид"],
    6: ["Вселенная", "Телескоп", "Спутник", "Ракета", "Зонд"],
    7: ["Космический", "Астронавт", "Орбита", "Гравитация", "Чёрная дыра"],
    8: ["Космология", "Релятивизм", "Квантовая", "Физика", "Астрономия"]
}

# Dalga başına kelime sayısı (İlk dalga 10, her dalga +5)
def get_wave_word_count(wave):
    return 10 + (wave - 1) * 5

class GameState(Enum):
    """Oyun durumları"""
    MENU = 1
    SETTINGS = 2
    PLAYING = 3
    GAME_OVER = 4

class ShipType(Enum):
    """Gemi tipleri"""
    NEON_HUNTER = 1  # Mavi üçgen
    HEAVY_CRUISER = 2   # Ağır kruvazör - kırmızı karemsi
    FAST_INTERCEPTOR = 3  # Hızlı önleyici - yeşil ok
    STAR_FIGHTER = 4     # Yıldız savaşçısı - sarı yıldız

class PlanetType(Enum):
    """Gezegen tipleri"""
    EARTH = 1    # Mavi/Yeşil
    MARS = 2     # Kızıl
    ICE_GIANT = 3  # Beyaz/Turkuaz

# Gemi özellikleri
SHIP_DATA = {
    ShipType.NEON_HUNTER: {
        'name': 'Neon Avcı',
        'color': (0, 200, 255),
        'bullet_color': (0, 255, 255),
        'shape': 'triangle'
    },
    ShipType.HEAVY_CRUISER: {
        'name': 'Ağır Kruvazör',
        'color': (255, 50, 50),
        'bullet_color': (255, 150, 0),
        'shape': 'square'
    },
    ShipType.FAST_INTERCEPTOR: {
        'name': 'Hızlı Önleyici',
        'color': (0, 255, 150),
        'bullet_color': (150, 255, 0),
        'shape': 'arrow'
    },
    ShipType.STAR_FIGHTER: {
        'name': 'Yıldız Savaşçısı',
        'color': (255, 255, 0),
        'bullet_color': (255, 255, 150),
        'shape': 'star'
    }
}
# Gezegen özellikleri
PLANET_DATA = {
    PlanetType.EARTH: {
        'name': 'Dünya',
        'color': (50, 150, 255),
        'secondary_color': (0, 200, 100),
        'atmosphere': (100, 150, 255, 50)
    },
    PlanetType.MARS: {
        'name': 'Kızıl Mars',
        'color': (200, 80, 50),
        'secondary_color': (150, 50, 30),
        'atmosphere': (255, 100, 50, 40)
    },
    PlanetType.ICE_GIANT: {
        'name': 'Buz Devi',
        'color': (200, 230, 255),
        'secondary_color': (0, 200, 200),
        'atmosphere': (150, 220, 255, 60)
    }
}

class Button:
    """Menü butonu sınıfı"""
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
    
    def draw(self, screen):
        """Butonu çiz"""
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        """Hover durumunu güncelle"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        """Butona tıklandı mı?"""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

class Particle:
    """Parçacık sınıfı"""
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = 4
    
    def update(self):
        """Parçacığı güncelle"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # Yerçekimi
        self.lifetime -= 1
    
    def draw(self, screen):
        """Parçacığı çiz"""
        if self.lifetime > 0:
            alpha_factor = self.lifetime / self.max_lifetime
            current_size = int(self.size * alpha_factor)
            if current_size > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), current_size)
    
    def is_alive(self):
        return self.lifetime > 0

class ParticleSystem:
    """Parçacık sistemi"""
    def __init__(self):
        self.particles = []
    
    def create_explosion(self, x, y, count=30, colors=None):
        """Patlama efekti oluştur"""
        if colors is None:
            colors = [(0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0)]
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(colors)
            lifetime = random.randint(25, 50)
            
            self.particles.append(Particle(x, y, vx, vy, color, lifetime))
    
    def update(self):
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

class Bullet:
    """Homing mermi sınıfı"""
    def __init__(self, x, y, target_x, target_y, color):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.color = color
        self.speed = 8
        self.size = 4
        self.hit = False
    
    def update(self):
        """Hedefe doğru yönelerek hareket et"""
        if not self.hit:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            
            # Hedefe ulaştı mı kontrol et
            if distance < 10:
                self.hit = True
    
    def draw(self, screen):
        """Mermiyi çiz"""
        if not self.hit:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            # Glow efekti
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size + 2, 1)
    
    def is_hit(self):
        return self.hit

class Word:
    """Rusça kelime düşmanı"""
    def __init__(self, text, x, y, wave):
        self.text = text
        self.original_x = x
        self.x = x
        self.y = y
        self.wave = wave
        # Hız artışı: biraz daha fazla
        difficulty_multiplier = 1.2 ** (wave - 1)
        self.base_speed = 0.3 * difficulty_multiplier
        self.float_amplitude = 30 * difficulty_multiplier
        self.float_frequency = 0.015 + wave * 0.003
        self.time = 0
        self.typed_chars = 0
        self.font = pygame.font.Font(None, 36)
        self.width = 0
        self.height = 30
        self.calculate_width()
    
    def calculate_width(self):
        """Kelimenin genişliğini hesapla"""
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.width = text_surface.get_width() + 20
    
    def update(self):
        """Kelimeyi güncelle - yumuşak süzülme hareketi"""
        self.time += 1
        self.y += self.base_speed
        # Sinüs dalgası ile sağa-sola süzülme
        self.x = self.original_x + math.sin(self.time * self.float_frequency) * self.float_amplitude
    
    def draw(self, screen):
        """Kelimeyi çiz"""
        # Arka plan kutusu
        box_rect = pygame.Rect(int(self.x - 10), int(self.y - 5), self.width, self.height)
        pygame.draw.rect(screen, (30, 30, 60), box_rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_ENEMY, box_rect, 2, border_radius=5)
        
        # Yazılan harfler yeşil, yazılmayanlar beyaz
        typed_part = self.text[:self.typed_chars]
        untyped_part = self.text[self.typed_chars:]
        
        x_offset = int(self.x)
        
        if typed_part:
            typed_surface = self.font.render(typed_part, True, (0, 255, 0))
            screen.blit(typed_surface, (x_offset, int(self.y)))
            x_offset += typed_surface.get_width()
        
        if untyped_part:
            untyped_surface = self.font.render(untyped_part, True, (255, 255, 255))
            screen.blit(untyped_surface, (x_offset, int(self.y)))
    
    def type_char(self, char):
        """Harf yazıldı mı kontrol et"""
        if self.typed_chars < len(self.text):
            if self.text[self.typed_chars].upper() == char.upper():
                self.typed_chars += 1
                return True
        return False
    
    def is_complete(self):
        """Kelime tamamlandı mı?"""
        return self.typed_chars >= len(self.text)
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT - 150  # Gezegen bölgesine çarpma
    
    def get_center(self):
        """Kelimenin merkez noktası"""
        return (int(self.x + self.width / 2), int(self.y + self.height / 2))

class Player:
    """Oyuncu gemisi"""
    def __init__(self, x, y, ship_type):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 35
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.ship_type = ship_type
        self.ship_data = SHIP_DATA[ship_type]
        self.shoot_cooldown = 0
    
    def update(self, keys, mouse_pos):
        """Oyuncuyu güncelle - sabit konumda"""
        # Hareket kaldırıldı, sabit konum
        # Ekran sınırları (gereksiz ama tut)
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def draw(self, screen):
        """Gemiyi çiz"""
        color = self.ship_data['color']
        shape = self.ship_data['shape']
        
        if shape == 'triangle':
            # Üçgen gemi
            points = [
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        
        elif shape == 'square':
            # Karemsi gemi
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
            # Kanatlar
            pygame.draw.polygon(screen, color, [
                (self.x, self.y + 10),
                (self.x - 8, self.y + 20),
                (self.x, self.y + 25)
            ])
            pygame.draw.polygon(screen, color, [
                (self.x + self.width, self.y + 10),
                (self.x + self.width + 8, self.y + 20),
                (self.x + self.width, self.y + 25)
            ])
        
        elif shape == 'arrow':
            # Ok şeklinde gemi
            points = [
                (self.x + self.width // 2, self.y),
                (self.x + self.width, self.y + self.height // 2),
                (self.x + self.width * 0.7, self.y + self.height // 2),
                (self.x + self.width * 0.7, self.y + self.height),
                (self.x + self.width * 0.3, self.y + self.height),
                (self.x + self.width * 0.3, self.y + self.height // 2),
                (self.x, self.y + self.height // 2)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        
        elif shape == 'star':
            # Yıldız şeklinde gemi (havalı)
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            outer_radius = self.width // 2
            inner_radius = outer_radius * 0.4
            
            points = []
            for i in range(10):
                angle = math.radians(i * 36)
                if i % 2 == 0:
                    radius = outer_radius
                else:
                    radius = inner_radius
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def shoot(self, target_x, target_y):
        """Homing mermi oluştur"""
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 8
            bullet_color = self.ship_data['bullet_color']
            return Bullet(self.x + self.width // 2, self.y, target_x, target_y, bullet_color)
        return None
    
    def take_damage(self, amount):
        self.health -= amount
        self.health = max(0, self.health)
    
    def is_alive(self):
        return self.health > 0

class Planet:
    """Arka planda dönen gezegen"""
    def __init__(self, x, y, planet_type):
        self.x = x
        self.y = y
        self.radius = 120  # Büyük gezegen
        self.planet_type = planet_type
        self.planet_data = PLANET_DATA[planet_type]
        self.rotation = 0
    
    def update(self):
        """Gezegeni döndür"""
        self.rotation += 0.5
    
    def draw(self, screen):
        """Gezegeni çiz"""
        color = self.planet_data['color']
        secondary = self.planet_data['secondary_color']
        
        # Ana gezegen gövdesi
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
        # Detay çizgileri (kıtalar/atmosfer)
        for i in range(4):
            offset = int(math.sin(math.radians(self.rotation + i * 45)) * 30)
            pygame.draw.circle(screen, secondary, 
                             (int(self.x + offset), int(self.y - 30 + i * 15)), 
                             self.radius - 20 - i * 8, 2)
        
        # Atmosfer halkası
        atm_color = self.planet_data['atmosphere']
        surf = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, atm_color, 
                          (0, self.radius, self.radius * 3, self.radius // 2))
        screen.blit(surf, (int(self.x - self.radius * 1.5), int(self.y - self.radius * 0.5)))

class Star:
    """Arka plan yıldızı"""
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.randint(1, 3)
        self.brightness = random.randint(150, 255)
    
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, 255)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class WaveMessage:
    """Dalga geçiş mesajı sınıfı"""
    def __init__(self, text, font):
        self.text = text
        self.font = font
        self.alpha = 0
        self.max_alpha = 255
        self.fade_speed = 3
        self.active = True
        self.timer = 0
        self.pause_game = True  # Oyun duracak
    
    def update(self):
        if self.active:
            self.timer += 1
            if self.timer < 60:  # Fade in
                self.alpha = min(self.max_alpha, self.alpha + self.fade_speed)
            elif self.timer > 120:  # Fade out
                self.alpha = max(0, self.alpha - self.fade_speed)
                if self.alpha == 0:
                    self.active = False
                    self.pause_game = False  # Oyun devam et
    
    def draw(self, screen):
        if self.active:
            # Ekranı karart
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_surface.set_alpha(self.alpha)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)

class OnScreenKeyboard:
    """Basit ekranda Rusça klavye (dokunmatik için)"""
    def __init__(self, font):
        self.font = font
        self.visible = False
        self.rows = [
            list("ЙЦУКЕНГШЩЗХЪ"),
            list("ФЫВАПРОЛДЖЭ"),
            list("ЯЧСМИТЬБЮ"),
        ]
        self.key_rects = []  # (rect, char)
        self.padding = 6
        self.key_w = 34
        self.key_h = 38
        self.area = pygame.Rect(0, 0, 0, 0)
        self._layout()

    def _layout(self):
        bottom_margin = 8
        total_h = len(self.rows) * (self.key_h + self.padding) + self.padding
        y_start = SCREEN_HEIGHT - total_h - bottom_margin
        self.key_rects.clear()
        max_cols = max(len(r) for r in self.rows)
        total_w = max_cols * (self.key_w + self.padding) + self.padding
        x_start = (SCREEN_WIDTH - total_w) // 2
        self.area = pygame.Rect(x_start, y_start, total_w, total_h)
        y = y_start + self.padding
        for row in self.rows:
            # Row-centered
            row_w = len(row) * (self.key_w + self.padding)
            rx = x_start + (total_w - row_w) // 2 + self.padding // 2
            x = rx
            for ch in row:
                rect = pygame.Rect(x, y, self.key_w, self.key_h)
                self.key_rects.append((rect, ch))
                x += self.key_w + self.padding
            y += self.key_h + self.padding

    def draw(self, screen):
        if not self.visible:
            return
        # Panel
        pygame.draw.rect(screen, (20, 25, 50), self.area, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT, self.area, 2, border_radius=10)
        # Keys
        for rect, ch in self.key_rects:
            pygame.draw.rect(screen, (40, 50, 90), rect, border_radius=6)
            pygame.draw.rect(screen, (0, 180, 220), rect, 2, border_radius=6)
            ts = self.font.render(ch, True, (255, 255, 255))
            tr = ts.get_rect(center=rect.center)
            screen.blit(ts, tr)

    def handle_touch(self, pos):
        """Dokunulduğunda basılan karakteri döndürür"""
        if not self.visible:
            return None
        for rect, ch in self.key_rects:
            if rect.collidepoint(pos):
                return ch
        return None

class GameManager:
    """Ana oyun yöneticisi"""
    def __init__(self):
        # Web ortamı kontrolü
        self.is_web = sys.platform == "emscripten"
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Russian Typing Defender")
        self.clock = pygame.time.Clock()

        # Fontlar
        try:
            self.font_large = pygame.font.SysFont('arial', 72)
            self.font_medium = pygame.font.SysFont('arial', 48)
            self.font_small = pygame.font.SysFont('arial', 28)
        except:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 28)

        self.state = GameState.PLAYING
        self.score = 0
        self.wave = 1

        # Oyuncu ve savaş bileşenleri
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 140, ShipType.NEON_HUNTER)
        self.bullets = []
        self.particles = ParticleSystem()

        # Kelimeler
        self.words = []
        self.spawn_interval = FPS * 2  # Yaklaşık 2 saniyede bir yeni kelime
        self.spawn_timer = 0
        self.current_input = ""
        self.wave_word_pool = []  # Bu dalgada tekrar etmemek için havuz

        # Yıldızlar
        self.stars = [Star(random.randint(0, SCREEN_WIDTH), 
                          random.randint(0, SCREEN_HEIGHT), 
                          random.uniform(0.3, 1.2)) for _ in range(80)]

    def spawn_word(self):
        """Yeni bir kelime oluştur"""
        pool = RUSSIAN_WORDS.get(self.wave, RUSSIAN_WORDS[max(RUSSIAN_WORDS.keys())])
        if not self.wave_word_pool:
            self.wave_word_pool = pool.copy()
            random.shuffle(self.wave_word_pool)
        text = self.wave_word_pool.pop()
        x = random.randint(50, SCREEN_WIDTH - 150)
        y = -40
        self.words.append(Word(text, x, y, self.wave))

    async def run(self):
        """Ana oyun döngüsü (asyncio ile)"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)  # Web uyumluluğu için asyncio kullanımı
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        """Olayları işle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE and self.words:
                    # En yakın kelimeye ateş et
                    target = self.words[0]
                    bullet = self.player.shoot(*target.get_center())
                    if bullet:
                        self.bullets.append(bullet)
                    continue
                char = event.unicode
                if char:
                    for word in list(self.words):
                        if word.type_char(char):
                            if word.is_complete():
                                self.score += len(word.text)
                                cx, cy = word.get_center()
                                self.particles.create_explosion(cx, cy, count=35)
                                self.words.remove(word)
                            break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.words:
                target = self.words[0]
                bullet = self.player.shoot(*target.get_center())
                if bullet:
                    self.bullets.append(bullet)
        return True

    def update(self):
        """Oyun mantığını güncelle"""
        for star in self.stars:
            star.update()
        if self.state != GameState.PLAYING:
            return

        # Oyuncu cooldown/güncelleme
        self.player.update(None, None)

        if self.spawn_timer <= 0 and len(self.words) < get_wave_word_count(self.wave):
            self.spawn_word()
            self.spawn_timer = self.spawn_interval
        else:
            self.spawn_timer = max(0, self.spawn_timer - 1)

        for word in list(self.words):
            word.update()
            if word.is_off_screen():
                self.words.remove(word)

        # Mermiler ve çarpışmalar
        for bullet in list(self.bullets):
            bullet.update()
            hit_word = None
            for word in self.words:
                wx, wy = word.get_center()
                if math.hypot(wx - bullet.x, wy - bullet.y) < 18:
                    hit_word = word
                    break
            if hit_word:
                self.score += len(hit_word.text)
                cx, cy = hit_word.get_center()
                self.particles.create_explosion(cx, cy, count=35)
                self.words.remove(hit_word)
                bullet.hit = True
            if bullet.is_hit():
                self.bullets.remove(bullet)

        # Parçacıklar
        self.particles.update()

    def draw(self):
        """Ekranı çiz"""
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        for word in self.words:
            word.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.particles.draw(self.screen)

        score_surface = self.font_small.render(f"Skor: {self.score}  Dalga: {self.wave}", True, COLOR_TEXT)
        self.screen.blit(score_surface, (10, 10))
        pygame.display.flip()

# Oyunu başlat
if __name__ == "__main__":
    game = GameManager()
    if sys.platform == "emscripten":
        import asyncio
        asyncio.run(game.run())
    else:
        asyncio.run(game.run())
