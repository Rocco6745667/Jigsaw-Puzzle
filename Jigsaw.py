import pygame
import random
import sys
import pygame.locals

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PIECE_SIZE = 100
GRID_SIZE = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PuzzlePiece:
    def __init__(self, image, pos, correct_pos):
        self.image = image
        self.pos = pos
        self.correct_pos = correct_pos
        self.rect = pygame.Rect(pos[0] * PIECE_SIZE, pos[1] * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE)
        self.dragging = False

class JigsawPuzzle:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Jigsaw Puzzle')
        
        # Load and scale the image
        self.original_image = pygame.image.load('puzzle_image.jpg')
        self.original_image = pygame.transform.scale(self.original_image, 
                                                   (PIECE_SIZE * GRID_SIZE, PIECE_SIZE * GRID_SIZE))
        
        self.pieces = []
        self.selected_piece = None
        self.create_pieces()
        
    def create_pieces(self):
        positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        random.shuffle(positions)
        
        for i, pos in enumerate(positions):
            correct_x = i % GRID_SIZE
            correct_y = i // GRID_SIZE
            
            # Create subsurface for each piece
            piece_surface = self.original_image.subsurface(
                (correct_x * PIECE_SIZE, correct_y * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))
            
            self.pieces.append(PuzzlePiece(piece_surface, pos, (correct_x, correct_y)))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for piece in self.pieces:
                    if piece.rect.collidepoint(mouse_pos):
                        self.selected_piece = piece
                        piece.dragging = True
                        
            elif event.type == MOUSEBUTTONUP:
                if self.selected_piece:
                    self.selected_piece.dragging = False
                    # Snap to grid
                    grid_x = round(self.selected_piece.rect.x / PIECE_SIZE)
                    grid_y = round(self.selected_piece.rect.y / PIECE_SIZE)
                    self.selected_piece.pos = (grid_x, grid_y)
                    self.selected_piece.rect.x = grid_x * PIECE_SIZE
                    self.selected_piece.rect.y = grid_y * PIECE_SIZE
                    self.selected_piece = None
                    
            elif event.type == MOUSEMOTION:
                if self.selected_piece and self.selected_piece.dragging:
                    mouse_x, mouse_y = event.pos
                    self.selected_piece.rect.x = mouse_x - PIECE_SIZE // 2
                    self.selected_piece.rect.y = mouse_y - PIECE_SIZE // 2

    def check_win(self):
        for piece in self.pieces:
            if piece.pos != piece.correct_pos:
                return False
        return True

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, BLACK, 
                           (i * PIECE_SIZE, 0), 
                           (i * PIECE_SIZE, GRID_SIZE * PIECE_SIZE))
            pygame.draw.line(self.screen, BLACK, 
                           (0, i * PIECE_SIZE), 
                           (GRID_SIZE * PIECE_SIZE, i * PIECE_SIZE))
        
        # Draw pieces
        for piece in self.pieces:
            self.screen.blit(piece.image, piece.rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            
            if self.check_win():
                font = pygame.font.Font(None, 74)
                text = font.render('Puzzle Completed!', True, BLACK)
                self.screen.blit(text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))
                pygame.display.flip()

if __name__ == '__main__':
    game = JigsawPuzzle()
    game.run()
