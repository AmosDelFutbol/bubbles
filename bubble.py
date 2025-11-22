import pygame
import sys
import random
import math
import os
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (bright and child-friendly)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
ORANGE = (255, 150, 50)
PINK = (255, 150, 200)
CYAN = (50, 255, 255)
LIGHT_BLUE = (150, 200, 255)
LIGHT_GREEN = (150, 255, 150)
LIGHT_YELLOW = (255, 255, 150)
LIGHT_PURPLE = (230, 150, 255)
LIGHT_PINK = (255, 200, 230)
DARK_BLUE = (50, 50, 150)
BROWN = (150, 100, 50)

# Game states
class GameState(Enum):
    MENU = 1
    COUNTING = 2
    ALPHABET = 3
    DRAWING = 4
    SHAPES = 5
    REWARD = 6

# Create a simple sound generator function (since we can't load external files)
def generate_sound(frequency, duration):
    sample_rate = 22050
    samples = int(sample_rate * duration)
    waves = [int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate)) for i in range(samples)]
    sound = pygame.sndarray.make_sound(waves)
    return sound

# Create some simple sounds
try:
    import numpy as np
    correct_sound = generate_sound(523, 0.2)  # C5 note
    wrong_sound = generate_sound(200, 0.3)    # Low frequency
    click_sound = generate_sound(800, 0.1)    # High frequency
except ImportError:
    # If numpy is not available, create dummy sounds
    correct_sound = None
    wrong_sound = None
    click_sound = None

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont('Arial', font_size, bold=True)
        self.hovered = False
        self.clicked = False
        
    def draw(self, screen):
        # Draw button with shadow
        shadow_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=15)
        
        # Draw button
        color = self.color
        if self.hovered:
            color = tuple(min(255, c + 30) for c in self.color)
        if self.clicked:
            color = tuple(max(0, c - 30) for c in self.color)
            
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=15)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                if click_sound:
                    click_sound.play()
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        return False

class Mascot:
    def __init__(self):
        self.x = SCREEN_WIDTH - 150
        self.y = SCREEN_HEIGHT - 150
        self.size = 100
        self.eye_offset = 0
        self.eye_direction = 1
        self.message = ""
        self.message_timer = 0
        
    def update(self):
        # Animate eyes
        self.eye_offset += 0.5 * self.eye_direction
        if abs(self.eye_offset) > 5:
            self.eye_direction *= -1
            
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self, screen):
        # Draw body (cute bear-like creature)
        pygame.draw.circle(screen, BROWN, (self.x, self.y), self.size)
        pygame.draw.circle(screen, BROWN, (self.x - self.size//2, self.y), self.size//2)
        pygame.draw.circle(screen, BROWN, (self.x + self.size//2, self.y), self.size//2)
        
        # Draw ears
        pygame.draw.circle(screen, BROWN, (self.x - self.size//2, self.y - self.size//2), self.size//3)
        pygame.draw.circle(screen, BROWN, (self.x + self.size//2, self.y - self.size//2), self.size//3)
        pygame.draw.circle(screen, PINK, (self.x - self.size//2, self.y - self.size//2), self.size//5)
        pygame.draw.circle(screen, PINK, (self.x + self.size//2, self.y - self.size//2), self.size//5)
        
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (self.x - 30, self.y - 10), 20)
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y - 10), 20)
        pygame.draw.circle(screen, BLACK, (self.x - 30 + self.eye_offset, self.y - 10), 10)
        pygame.draw.circle(screen, BLACK, (self.x + 30 + self.eye_offset, self.y - 10), 10)
        
        # Draw nose
        pygame.draw.circle(screen, BLACK, (self.x, self.y + 10), 10)
        
        # Draw mouth
        pygame.draw.arc(screen, BLACK, (self.x - 20, self.y + 5, 40, 30), 0, math.pi, 3)
        
        # Draw message if active
        if self.message_timer > 0:
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.message, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.x, self.y - self.size - 30))
            
            # Draw speech bubble
            bubble_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=10)
            
            # Draw triangle pointing to mascot
            points = [
                (self.x, self.y - self.size - 10),
                (self.x - 10, self.y - self.size - 25),
                (self.x + 10, self.y - self.size - 25)
            ]
            pygame.draw.polygon(screen, WHITE, points)
            pygame.draw.polygon(screen, BLACK, points, 2)
            
            screen.blit(text_surface, text_rect)
    
    def set_message(self, message, duration=120):
        self.message = message
        self.message_timer = duration

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(15, 30)
        self.color = random.choice([YELLOW, ORANGE, WHITE])
        self.angle = 0
        self.speed = random.uniform(1, 3)
        self.direction = random.uniform(0, 2 * math.pi)
        
    def update(self):
        self.angle += 0.05
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        
        # Bounce off edges
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.direction = -self.direction
    
    def draw(self, screen):
        # Draw a star
        points = []
        for i in range(10):
            angle = self.angle + i * math.pi / 5
            if i % 2 == 0:
                radius = self.size
            else:
                radius = self.size // 2
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)

class CountingGame:
    def __init__(self):
        self.objects = []
        self.count = 0
        self.question = ""
        self.options = []
        self.correct_option = None
        self.score = 0
        self.stars = []
        self.feedback_timer = 0
        self.feedback_message = ""
        self.font = pygame.font.SysFont('Arial', 36)
        self.big_font = pygame.font.SysFont('Arial', 48)
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, CYAN]
        self.shapes = ['circle', 'square', 'triangle', 'star']
        self.generate_question()
        
    def generate_question(self):
        # Generate random objects to count
        self.objects = []
        self.count = random.randint(3, 10)
        
        for _ in range(self.count):
            x = random.randint(100, SCREEN_WIDTH - 200)
            y = random.randint(150, SCREEN_HEIGHT - 200)
            color = random.choice(self.colors)
            shape = random.choice(self.shapes)
            size = random.randint(30, 60)
            self.objects.append((x, y, color, shape, size))
        
        # Create question
        self.question = f"How many {random.choice(['stars', 'circles', 'squares', 'triangles'])} do you see?"
        
        # Create answer options
        self.correct_option = self.count
        wrong_options = [self.count - 1, self.count + 1, self.count + 2]
        wrong_options = [opt for opt in wrong_options if opt > 0 and opt != self.count]
        
        if len(wrong_options) < 3:
            wrong_options.extend([self.count - 2, self.count + 3, self.count - 3])
            wrong_options = [opt for opt in wrong_options if opt > 0 and opt != self.count]
        
        self.options = [self.correct_option] + random.sample(wrong_options, min(3, len(wrong_options)))
        random.shuffle(self.options)
        
    def draw(self, screen):
        # Draw title
        title_surface = self.big_font.render("Counting Game", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Draw question
        question_surface = self.font.render(self.question, True, BLACK)
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(question_surface, question_rect)
        
        # Draw objects
        for x, y, color, shape, size in self.objects:
            if shape == 'circle':
                pygame.draw.circle(screen, color, (x, y), size)
            elif shape == 'square':
                pygame.draw.rect(screen, color, (x - size, y - size, size * 2, size * 2))
            elif shape == 'triangle':
                points = [
                    (x, y - size),
                    (x - size, y + size),
                    (x + size, y + size)
                ]
                pygame.draw.polygon(screen, color, points)
            elif shape == 'star':
                points = []
                for i in range(10):
                    angle = i * math.pi / 5
                    if i % 2 == 0:
                        radius = size
                    else:
                        radius = size // 2
                    px = x + radius * math.cos(angle - math.pi/2)
                    py = y + radius * math.sin(angle - math.pi/2)
                    points.append((px, py))
                pygame.draw.polygon(screen, color, points)
        
        # Draw options as buttons
        button_width = 100
        button_height = 60
        button_spacing = 20
        total_width = len(self.options) * button_width + (len(self.options) - 1) * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        button_y = SCREEN_HEIGHT - 150
        
        for i, option in enumerate(self.options):
            x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(x, button_y, button_width, button_height)
            pygame.draw.rect(screen, LIGHT_BLUE, button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
            
            option_text = self.font.render(str(option), True, BLACK)
            option_rect = option_text.get_rect(center=button_rect.center)
            screen.blit(option_text, option_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Draw feedback if active
        if self.feedback_timer > 0:
            feedback_surface = self.big_font.render(self.feedback_message, True, GREEN if "Correct" in self.feedback_message else RED)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Draw background for feedback
            bg_rect = feedback_rect.inflate(40, 20)
            pygame.draw.rect(screen, WHITE, bg_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bg_rect, 2, border_radius=10)
            
            screen.blit(feedback_surface, feedback_rect)
            self.feedback_timer -= 1
        
        # Draw stars
        for star in self.stars:
            star.update()
            star.draw(screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if an option was clicked
            button_width = 100
            button_height = 60
            button_spacing = 20
            total_width = len(self.options) * button_width + (len(self.options) - 1) * button_spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 150
            
            for i, option in enumerate(self.options):
                x = start_x + i * (button_width + button_spacing)
                button_rect = pygame.Rect(x, button_y, button_width, button_height)
                
                if button_rect.collidepoint(event.pos):
                    if option == self.correct_option:
                        self.score += 1
                        self.feedback_message = "Correct! Great job!"
                        self.feedback_timer = 60
                        
                        # Add celebration stars
                        for _ in range(10):
                            self.stars.append(Star(event.pos[0], event.pos[1]))
                        
                        if correct_sound:
                            correct_sound.play()
                        
                        # Generate new question after a delay
                        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                    else:
                        self.feedback_message = "Try again!"
                        self.feedback_timer = 60
                        if wrong_sound:
                            wrong_sound.play()
                    return True
        
        elif event.type == pygame.USEREVENT + 1:
            # Generate new question
            self.generate_question()
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel the timer
            
        return False

class AlphabetGame:
    def __init__(self):
        self.current_letter = 'A'
        self.letter_display = 'A'
        self.score = 0
        self.feedback_timer = 0
        self.feedback_message = ""
        self.font = pygame.font.SysFont('Arial', 72)
        self.big_font = pygame.font.SysFont('Arial', 96)
        self.small_font = pygame.font.SysFont('Arial', 36)
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, CYAN]
        self.letter_color = random.choice(self.colors)
        self.stars = []
        self.show_word = False
        self.word_examples = {
            'A': 'Apple', 'B': 'Ball', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant',
            'F': 'Fish', 'G': 'Goat', 'H': 'Hat', 'I': 'Ice cream', 'J': 'Jump',
            'K': 'Kite', 'L': 'Lion', 'M': 'Moon', 'N': 'Nest', 'O': 'Orange',
            'P': 'Penguin', 'Q': 'Queen', 'R': 'Rainbow', 'S': 'Sun', 'T': 'Tree',
            'U': 'Umbrella', 'V': 'Violin', 'W': 'Water', 'X': 'Xylophone', 'Y': 'Yacht', 'Z': 'Zebra'
        }
        
    def next_letter(self):
        if self.current_letter == 'Z':
            self.current_letter = 'A'
        else:
            self.current_letter = chr(ord(self.current_letter) + 1)
        self.letter_display = self.current_letter
        self.letter_color = random.choice(self.colors)
        self.show_word = False
        
    def prev_letter(self):
        if self.current_letter == 'A':
            self.current_letter = 'Z'
        else:
            self.current_letter = chr(ord(self.current_letter) - 1)
        self.letter_display = self.current_letter
        self.letter_color = random.choice(self.colors)
        self.show_word = False
        
    def draw(self, screen):
        # Draw title
        title_surface = self.big_font.render("Alphabet Learning", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Draw letter in center
        letter_surface = self.font.render(self.letter_display, True, self.letter_color)
        letter_rect = letter_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(letter_surface, letter_rect)
        
        # Draw word example if visible
        if self.show_word:
            word = self.word_examples.get(self.current_letter, '')
            word_surface = self.small_font.render(word, True, BLACK)
            word_rect = word_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(word_surface, word_rect)
        
        # Draw navigation buttons
        prev_button = Button(100, SCREEN_HEIGHT - 150, 150, 60, "Previous", LIGHT_GREEN)
        next_button = Button(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150, 150, 60, "Next", LIGHT_GREEN)
        word_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 150, 150, 60, "Word", LIGHT_YELLOW)
        
        prev_button.draw(screen)
        next_button.draw(screen)
        word_button.draw(screen)
        
        # Draw score
        score_text = self.small_font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Draw feedback if active
        if self.feedback_timer > 0:
            feedback_surface = self.small_font.render(self.feedback_message, True, GREEN)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            
            # Draw background for feedback
            bg_rect = feedback_rect.inflate(40, 20)
            pygame.draw.rect(screen, WHITE, bg_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bg_rect, 2, border_radius=10)
            
            screen.blit(feedback_surface, feedback_rect)
            self.feedback_timer -= 1
        
        # Draw stars
        for star in self.stars:
            star.update()
            star.draw(screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if previous button was clicked
            prev_button_rect = pygame.Rect(100, SCREEN_HEIGHT - 150, 150, 60)
            if prev_button_rect.collidepoint(event.pos):
                self.prev_letter()
                if click_sound:
                    click_sound.play()
                return True
                
            # Check if next button was clicked
            next_button_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150, 150, 60)
            if next_button_rect.collidepoint(event.pos):
                self.next_letter()
                if click_sound:
                    click_sound.play()
                return True
                
            # Check if word button was clicked
            word_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 150, 150, 60)
            if word_button_rect.collidepoint(event.pos):
                self.show_word = not self.show_word
                if self.show_word:
                    self.score += 1
                    self.feedback_message = "Great job learning!"
                    self.feedback_timer = 60
                    
                    # Add celebration stars
                    for _ in range(5):
                        self.stars.append(Star(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    
                    if correct_sound:
                        correct_sound.play()
                if click_sound:
                    click_sound.play()
                return True
                
        elif event.type == pygame.KEYDOWN:
            # Check if a letter key was pressed
            if pygame.K_a <= event.key <= pygame.K_z:
                pressed_letter = chr(event.key).upper()
                if pressed_letter == self.current_letter:
                    self.score += 1
                    self.feedback_message = f"Correct! That's the letter {self.current_letter}!"
                    self.feedback_timer = 60
                    
                    # Add celebration stars
                    for _ in range(5):
                        self.stars.append(Star(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    
                    if correct_sound:
                        correct_sound.play()
                    
                    # Move to next letter after a delay
                    pygame.time.set_timer(pygame.USEREVENT + 2, 1500)
                else:
                    self.feedback_message = f"That's the letter {pressed_letter}, not {self.current_letter}."
                    self.feedback_timer = 60
                    if wrong_sound:
                        wrong_sound.play()
                return True
                
        elif event.type == pygame.USEREVENT + 2:
            # Move to next letter
            self.next_letter()
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Cancel the timer
            
        return False

class DrawingGame:
    def __init__(self):
        self.canvas = pygame.Surface((SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200))
        self.canvas.fill(WHITE)
        self.drawing = False
        self.last_pos = None
        self.current_color = BLACK
        self.brush_size = 5
        self.colors = [
            BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, 
            ORANGE, PINK, CYAN, BROWN, WHITE
        ]
        self.brush_sizes = [2, 5, 10, 15, 20]
        self.font = pygame.font.SysFont('Arial', 36)
        
    def draw(self, screen):
        # Draw title
        title_surface = self.font.render("Drawing Canvas", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(title_surface, title_rect)
        
        # Draw canvas
        canvas_rect = pygame.Rect(100, 80, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        screen.blit(self.canvas, canvas_rect)
        pygame.draw.rect(screen, BLACK, canvas_rect, 3)
        
        # Draw color palette
        palette_y = SCREEN_HEIGHT - 100
        palette_width = 40
        palette_height = 40
        palette_spacing = 10
        palette_start_x = (SCREEN_WIDTH - (len(self.colors) * (palette_width + palette_spacing))) // 2
        
        for i, color in enumerate(self.colors):
            x = palette_start_x + i * (palette_width + palette_spacing)
            color_rect = pygame.Rect(x, palette_y, palette_width, palette_height)
            pygame.draw.rect(screen, color, color_rect)
            pygame.draw.rect(screen, BLACK, color_rect, 2)
            
            # Highlight current color
            if color == self.current_color:
                pygame.draw.rect(screen, BLACK, color_rect.inflate(6, 6), 3)
        
        # Draw brush size options
        brush_y = palette_y - 60
        brush_start_x = (SCREEN_WIDTH - (len(self.brush_sizes) * (palette_width + palette_spacing))) // 2
        
        for i, size in enumerate(self.brush_sizes):
            x = brush_start_x + i * (palette_width + palette_spacing)
            brush_rect = pygame.Rect(x, brush_y, palette_width, palette_height)
            pygame.draw.rect(screen, LIGHT_GRAY, brush_rect)
            pygame.draw.rect(screen, BLACK, brush_rect, 2)
            
            # Draw circle representing brush size
            pygame.draw.circle(screen, BLACK, (x + palette_width // 2, brush_y + palette_height // 2), size)
            
            # Highlight current brush size
            if size == self.brush_size:
                pygame.draw.rect(screen, BLACK, brush_rect.inflate(6, 6), 3)
        
        # Draw clear button
        clear_button = Button(SCREEN_WIDTH - 150, 30, 100, 40, "Clear", LIGHT_RED)
        clear_button.draw(screen)
        
        # Draw instructions
        instructions = [
            "Click and drag to draw",
            "Select colors and brush sizes below",
            "Click Clear to start over"
        ]
        for i, instruction in enumerate(instructions):
            text_surface = pygame.font.SysFont('Arial', 24).render(instruction, True, BLACK)
            screen.blit(text_surface, (20, 100 + i * 30))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clear button was clicked
            clear_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 30, 100, 40)
            if clear_button_rect.collidepoint(event.pos):
                self.canvas.fill(WHITE)
                if click_sound:
                    click_sound.play()
                return True
                
            # Check if a color was selected
            palette_y = SCREEN_HEIGHT - 100
            palette_width = 40
            palette_height = 40
            palette_spacing = 10
            palette_start_x = (SCREEN_WIDTH - (len(self.colors) * (palette_width + palette_spacing))) // 2
            
            for i, color in enumerate(self.colors):
                x = palette_start_x + i * (palette_width + palette_spacing)
                color_rect = pygame.Rect(x, palette_y, palette_width, palette_height)
                if color_rect.collidepoint(event.pos):
                    self.current_color = color
                    if click_sound:
                        click_sound.play()
                    return True
                    
            # Check if a brush size was selected
            brush_y = palette_y - 60
            brush_start_x = (SCREEN_WIDTH - (len(self.brush_sizes) * (palette_width + palette_spacing))) // 2
            
            for i, size in enumerate(self.brush_sizes):
                x = brush_start_x + i * (palette_width + palette_spacing)
                brush_rect = pygame.Rect(x, brush_y, palette_width, palette_height)
                if brush_rect.collidepoint(event.pos):
                    self.brush_size = size
                    if click_sound:
                        click_sound.play()
                    return True
                    
            # Check if drawing on canvas
            canvas_rect = pygame.Rect(100, 80, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
            if canvas_rect.collidepoint(event.pos):
                self.drawing = True
                self.last_pos = (event.pos[0] - 100, event.pos[1] - 80)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False
            self.last_pos = None
            
        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                current_pos = (event.pos[0] - 100, event.pos[1] - 80)
                if self.last_pos:
                    pygame.draw.line(self.canvas, self.current_color, self.last_pos, current_pos, self.brush_size)
                    pygame.draw.circle(self.canvas, self.current_color, current_pos, self.brush_size // 2)
                self.last_pos = current_pos
                return True
                
        return False

class ShapesGame:
    def __init__(self):
        self.shapes = []
        self.target_shape = None
        self.target_shape_name = ""
        self.score = 0
        self.feedback_timer = 0
        self.feedback_message = ""
        self.font = pygame.font.SysFont('Arial', 36)
        self.big_font = pygame.font.SysFont('Arial', 48)
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, CYAN]
        self.shape_types = ['circle', 'square', 'triangle', 'star', 'rectangle', 'diamond']
        self.generate_question()
        self.stars = []
        
    def generate_question(self):
        # Generate random shapes
        self.shapes = []
        num_shapes = random.randint(6, 10)
        
        # Choose target shape
        self.target_shape = random.choice(self.shape_types)
        self.target_shape_name = self.target_shape.capitalize()
        
        # Create shapes
        for _ in range(num_shapes):
            x = random.randint(150, SCREEN_WIDTH - 150)
            y = random.randint(200, SCREEN_HEIGHT - 250)
            color = random.choice(self.colors)
            shape_type = random.choice(self.shape_types)
            size = random.randint(40, 80)
            self.shapes.append((x, y, color, shape_type, size))
        
        # Ensure at least one target shape exists
        if not any(shape[3] == self.target_shape for shape in self.shapes):
            # Replace a random shape with the target shape
            idx = random.randint(0, len(self.shapes) - 1)
            x, y, color, _, size = self.shapes[idx]
            self.shapes[idx] = (x, y, color, self.target_shape, size)
    
    def draw(self, screen):
        # Draw title
        title_surface = self.big_font.render("Shape Recognition", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Draw question
        question_surface = self.font.render(f"Find all the {self.target_shape_name}s!", True, BLACK)
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(question_surface, question_rect)
        
        # Draw shapes
        for x, y, color, shape_type, size in self.shapes:
            if shape_type == 'circle':
                pygame.draw.circle(screen, color, (x, y), size)
            elif shape_type == 'square':
                pygame.draw.rect(screen, color, (x - size, y - size, size * 2, size * 2))
            elif shape_type == 'rectangle':
                pygame.draw.rect(screen, color, (x - size, y - size//2, size * 2, size))
            elif shape_type == 'triangle':
                points = [
                    (x, y - size),
                    (x - size, y + size),
                    (x + size, y + size)
                ]
                pygame.draw.polygon(screen, color, points)
            elif shape_type == 'star':
                points = []
                for i in range(10):
                    angle = i * math.pi / 5
                    if i % 2 == 0:
                        radius = size
                    else:
                        radius = size // 2
                    px = x + radius * math.cos(angle - math.pi/2)
                    py = y + radius * math.sin(angle - math.pi/2)
                    points.append((px, py))
                pygame.draw.polygon(screen, color, points)
            elif shape_type == 'diamond':
                points = [
                    (x, y - size),
                    (x + size, y),
                    (x, y + size),
                    (x - size, y)
                ]
                pygame.draw.polygon(screen, color, points)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Draw feedback if active
        if self.feedback_timer > 0:
            feedback_surface = self.font.render(self.feedback_message, True, GREEN if "Correct" in self.feedback_message else RED)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            
            # Draw background for feedback
            bg_rect = feedback_rect.inflate(40, 20)
            pygame.draw.rect(screen, WHITE, bg_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bg_rect, 2, border_radius=10)
            
            screen.blit(feedback_surface, feedback_rect)
            self.feedback_timer -= 1
        
        # Draw stars
        for star in self.stars:
            star.update()
            star.draw(screen)
        
        # Draw new game button
        new_game_button = Button(SCREEN_WIDTH - 200, 20, 150, 50, "New Game", LIGHT_GREEN)
        new_game_button.draw(screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if new game button was clicked
            new_game_button_rect = pygame.Rect(SCREEN_WIDTH - 200, 20, 150, 50)
            if new_game_button_rect.collidepoint(event.pos):
                self.generate_question()
                if click_sound:
                    click_sound.play()
                return True
                
            # Check if a shape was clicked
            for i, (x, y, color, shape_type, size) in enumerate(self.shapes):
                # Check if click is within shape bounds
                if shape_type == 'circle':
                    distance = math.sqrt((event.pos[0] - x)**2 + (event.pos[1] - y)**2)
                    if distance <= size:
                        if shape_type == self.target_shape:
                            self.score += 1
                            self.feedback_message = "Correct! That's a " + self.target_shape_name + "!"
                            self.feedback_timer = 60
                            
                            # Add celebration stars
                            for _ in range(5):
                                self.stars.append(Star(x, y))
                            
                            if correct_sound:
                                correct_sound.play()
                            
                            # Remove the shape
                            self.shapes.pop(i)
                            
                            # Check if all target shapes have been found
                            if not any(shape[3] == self.target_shape for shape in self.shapes):
                                self.feedback_message = "Great job! You found all the " + self.target_shape_name + "s!"
                                self.feedback_timer = 120
                                # Generate new question after a delay
                                pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                        else:
                            self.feedback_message = "That's not a " + self.target_shape_name + ". Try again!"
                            self.feedback_timer = 60
                            if wrong_sound:
                                wrong_sound.play()
                        return True
                        
                elif shape_type in ['square', 'rectangle']:
                    if shape_type == 'square':
                        rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
                    else:  # rectangle
                        rect = pygame.Rect(x - size, y - size//2, size * 2, size)
                    
                    if rect.collidepoint(event.pos):
                        if shape_type == self.target_shape:
                            self.score += 1
                            self.feedback_message = "Correct! That's a " + self.target_shape_name + "!"
                            self.feedback_timer = 60
                            
                            # Add celebration stars
                            for _ in range(5):
                                self.stars.append(Star(x, y))
                            
                            if correct_sound:
                                correct_sound.play()
                            
                            # Remove the shape
                            self.shapes.pop(i)
                            
                            # Check if all target shapes have been found
                            if not any(shape[3] == self.target_shape for shape in self.shapes):
                                self.feedback_message = "Great job! You found all the " + self.target_shape_name + "s!"
                                self.feedback_timer = 120
                                # Generate new question after a delay
                                pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                        else:
                            self.feedback_message = "That's not a " + self.target_shape_name + ". Try again!"
                            self.feedback_timer = 60
                            if wrong_sound:
                                wrong_sound.play()
                        return True
                        
                elif shape_type in ['triangle', 'star', 'diamond']:
                    # Create a polygon for the shape and check if point is inside
                    if shape_type == 'triangle':
                        points = [
                            (x, y - size),
                            (x - size, y + size),
                            (x + size, y + size)
                        ]
                    elif shape_type == 'star':
                        points = []
                        for j in range(10):
                            angle = j * math.pi / 5
                            if j % 2 == 0:
                                radius = size
                            else:
                                radius = size // 2
                            px = x + radius * math.cos(angle - math.pi/2)
                            py = y + radius * math.sin(angle - math.pi/2)
                            points.append((px, py))
                    else:  # diamond
                        points = [
                            (x, y - size),
                            (x + size, y),
                            (x, y + size),
                            (x - size, y)
                        ]
                    
                    # Simple bounding box check for these shapes
                    min_x = min(p[0] for p in points)
                    max_x = max(p[0] for p in points)
                    min_y = min(p[1] for p in points)
                    max_y = max(p[1] for p in points)
                    
                    if min_x <= event.pos[0] <= max_x and min_y <= event.pos[1] <= max_y:
                        if shape_type == self.target_shape:
                            self.score += 1
                            self.feedback_message = "Correct! That's a " + self.target_shape_name + "!"
                            self.feedback_timer = 60
                            
                            # Add celebration stars
                            for _ in range(5):
                                self.stars.append(Star(x, y))
                            
                            if correct_sound:
                                correct_sound.play()
                            
                            # Remove the shape
                            self.shapes.pop(i)
                            
                            # Check if all target shapes have been found
                            if not any(shape[3] == self.target_shape for shape in self.shapes):
                                self.feedback_message = "Great job! You found all the " + self.target_shape_name + "s!"
                                self.feedback_timer = 120
                                # Generate new question after a delay
                                pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                        else:
                            self.feedback_message = "That's not a " + self.target_shape_name + ". Try again!"
                            self.feedback_timer = 60
                            if wrong_sound:
                                wrong_sound.play()
                        return True
        
        elif event.type == pygame.USEREVENT + 3:
            # Generate new question
            self.generate_question()
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)  # Cancel the timer
            
        return False

class RewardScreen:
    def __init__(self, total_score):
        self.total_score = total_score
        self.font = pygame.font.SysFont('Arial', 48)
        self.big_font = pygame.font.SysFont('Arial', 72)
        self.stars = []
        
        # Create celebration stars
        for _ in range(30):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.stars.append(Star(x, y))
    
    def draw(self, screen):
        # Draw background
        screen.fill(LIGHT_BLUE)
        
        # Draw stars
        for star in self.stars:
            star.update()
            star.draw(screen)
        
        # Draw title
        title_surface = self.big_font.render("Congratulations!", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Draw message
        message_surface = self.font.render(f"You've completed all activities!", True, BLACK)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(message_surface, message_rect)
        
        # Draw score
        score_surface = self.font.render(f"Total Score: {self.total_score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(score_surface, score_rect)
        
        # Draw certificate
        cert_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 400, 500, 300)
        pygame.draw.rect(screen, WHITE, cert_rect, border_radius=10)
        pygame.draw.rect(screen, GOLD := (255, 215, 0), cert_rect, 5, border_radius=10)
        
        # Draw certificate text
        cert_title = self.font.render("Certificate of Achievement", True, DARK_BLUE)
        cert_title_rect = cert_title.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(cert_title, cert_title_rect)
        
        cert_text = pygame.font.SysFont('Arial', 36).render("For excellent performance in learning!", True, BLACK)
        cert_text_rect = cert_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(cert_text, cert_text_rect)
        
        # Draw back button
        back_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50, "Back to Menu", LIGHT_GREEN)
        back_button.draw(screen)
        
        return back_button
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if back button was clicked
            back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50)
            if back_button_rect.collidepoint(event.pos):
                if click_sound:
                    click_sound.play()
                return True
        return False

class MainGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kids Learning Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.mascot = Mascot()
        
        # Initialize games
        self.counting_game = CountingGame()
        self.alphabet_game = AlphabetGame()
        self.drawing_game = DrawingGame()
        self.shapes_game = ShapesGame()
        self.reward_screen = None
        
        # Create menu buttons
        self.menu_buttons = [
            Button(SCREEN_WIDTH // 2 - 150, 250, 300, 80, "Counting Game", LIGHT_BLUE),
            Button(SCREEN_WIDTH // 2 - 150, 350, 300, 80, "Alphabet Learning", LIGHT_GREEN),
            Button(SCREEN_WIDTH // 2 - 150, 450, 300, 80, "Drawing Canvas", LIGHT_YELLOW),
            Button(SCREEN_WIDTH // 2 - 150, 550, 300, 80, "Shape Recognition", LIGHT_PURPLE)
        ]
        
        # Set initial mascot message
        self.mascot.set_message("Welcome! Choose an activity to start learning!")
        
        # Total score for reward screen
        self.total_score = 0
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if self.state == GameState.MENU:
                    self.handle_menu_event(event)
                elif self.state == GameState.COUNTING:
                    self.counting_game.handle_event(event)
                elif self.state == GameState.ALPHABET:
                    self.alphabet_game.handle_event(event)
                elif self.state == GameState.DRAWING:
                    self.drawing_game.handle_event(event)
                elif self.state == GameState.SHAPES:
                    self.shapes_game.handle_event(event)
                elif self.state == GameState.REWARD:
                    if self.reward_screen.handle_event(event):
                        self.state = GameState.MENU
                        self.mascot.set_message("Welcome back! Choose another activity!")
            
            # Update
            self.mascot.update()
            
            # Draw
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.COUNTING:
                self.counting_game.draw(self.screen)
            elif self.state == GameState.ALPHABET:
                self.alphabet_game.draw(self.screen)
            elif self.state == GameState.DRAWING:
                self.drawing_game.draw(self.screen)
            elif self.state == GameState.SHAPES:
                self.shapes_game.draw(self.screen)
            elif self.state == GameState.REWARD:
                self.reward_screen.draw(self.screen)
            
            # Always draw mascot
            self.mascot.draw(self.screen)
            
            # Draw back button if not in menu or reward screen
            if self.state not in [GameState.MENU, GameState.REWARD]:
                back_button = Button(20, 20, 100, 40, "Back", LIGHT_RED)
                back_button.draw(self.screen)
                
                # Check if back button was clicked
                if pygame.mouse.get_pressed()[0]:
                    if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.state = GameState.MENU
                        self.mascot.set_message("Welcome back! Choose another activity!")
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_menu_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.menu_buttons):
                if button.handle_event(event):
                    if i == 0:  # Counting Game
                        self.state = GameState.COUNTING
                        self.mascot.set_message("Let's count together!")
                    elif i == 1:  # Alphabet Learning
                        self.state = GameState.ALPHABET
                        self.mascot.set_message("Time to learn the alphabet!")
                    elif i == 2:  # Drawing Canvas
                        self.state = GameState.DRAWING
                        self.mascot.set_message("Express your creativity!")
                    elif i == 3:  # Shape Recognition
                        self.state = GameState.SHAPES
                        self.mascot.set_message("Can you find the shapes?")
                    return True
    
    def draw_menu(self):
        # Draw background with gradient
        for i in range(SCREEN_HEIGHT):
            color_value = int(150 + (105 * i / SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (color_value, color_value, 255), (0, i), (SCREEN_WIDTH, i))
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 72, bold=True)
        title_surface = title_font.render("Kids Learning Adventure", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        # Draw title shadow
        shadow_surface = title_font.render("Kids Learning Adventure", True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 3, 103))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Draw menu buttons
        for button in self.menu_buttons:
            button.draw(self.screen)
        
        # Draw decorative elements
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(2, 6)
            color = random.choice([WHITE, YELLOW, LIGHT_BLUE, LIGHT_GREEN, LIGHT_PINK])
            pygame.draw.circle(self.screen, color, (x, y), size)

if __name__ == "__main__":
    game = MainGame()
    game.run()
