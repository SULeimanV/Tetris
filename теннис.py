from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

Window.clearcolor = (0, 0, 0, 1)

import json
import os
import math

RECORDS_FILE = 'records.json'

DIFFICULTY_SETTINGS = {
    'easy': {'name': 'Лёгкий', 'base_speed': 7, 'speed_increase': 0.1},
    'medium': {'name': 'Средний', 'base_speed': 10, 'speed_increase': 0.13},
    'hard': {'name': 'Сложный', 'base_speed': 12, 'speed_increase': 0.2}
}

class GameRecords:
    def __init__(self):
        self.records = self.load_records()
    
    def load_records(self):
        if os.path.exists(RECORDS_FILE):
            try:
                with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_records(self):
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False)
    
    def add_record(self, name, score, difficulty):
        self.records.append({'name': name, 'score': score, 'difficulty': difficulty})
        self.records.sort(key=lambda x: x['score'], reverse=True)
        self.records = self.records[:10]
        self.save_records()
    
    def get_top_records(self):
        return self.records

records_manager = GameRecords()

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        title = Label(
            text='РЕТРО ТЕННИС',
            font_size='36sp',
            bold=True,
            color=(0.7, 1, 0.7, 1),
            size_hint=(0.8, 0.12),
            pos_hint={'center_x': 0.5, 'top': 0.97}
        )
        layout.add_widget(title)
        
        self.name_label = Label(
            text='Введите ник:',
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint=(0.8, 0.04),
            pos_hint={'center_x': 0.5, 'top': 0.82}
        )
        layout.add_widget(self.name_label)
        
        self.name_input = TextInput(
            text='Игрок',
            multiline=False,
            font_size='18sp',
            size_hint=(0.8, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.77},
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.name_input)
        
        self.difficulty_label = Label(
            text='Сложность:',
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint=(0.8, 0.04),
            pos_hint={'center_x': 0.5, 'top': 0.7}
        )
        layout.add_widget(self.difficulty_label)
        
        self.difficulty = 'easy'
        
        btn_easy = Button(
            text='ЛЁГКИЙ',
            font_size='16sp',
            background_color=(0.3, 1, 0.3, 1),
            color=(0, 0, 0, 1),
            size_hint=(0.25, 0.05),
            pos_hint={'x': 0.05, 'top': 0.64}
        )
        btn_easy.bind(on_press=lambda x: self.set_difficulty('easy'))
        layout.add_widget(btn_easy)
        
        btn_medium = Button(
            text='СРЕДНИЙ',
            font_size='16sp',
            background_color=(1, 1, 0, 1),
            color=(0, 0, 0, 1),
            size_hint=(0.25, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.64}
        )
        btn_medium.bind(on_press=lambda x: self.set_difficulty('medium'))
        layout.add_widget(btn_medium)
        
        btn_hard = Button(
            text='СЛОЖНЫЙ',
            font_size='16sp',
            background_color=(1, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.25, 0.05),
            pos_hint={'right': 0.95, 'top': 0.64}
        )
        btn_hard.bind(on_press=lambda x: self.set_difficulty('hard'))
        layout.add_widget(btn_hard)
        
        self.selected_difficulty_label = Label(
            text='Выбрано: Лёгкий',
            font_size='14sp',
            color=(0.3, 1, 0.3, 1),
            size_hint=(0.8, 0.03),
            pos_hint={'center_x': 0.5, 'top': 0.58}
        )
        layout.add_widget(self.selected_difficulty_label)
        
        btn_play = Button(
            text='ИГРАТЬ',
            font_size='22sp',
            background_color=(0.2, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.47}
        )
        btn_play.bind(on_press=self.start_game)
        layout.add_widget(btn_play)
        
        btn_records = Button(
            text='ТАБЛИЦА РЕКОРДОВ',
            font_size='18sp',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.8, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.37}
        )
        btn_records.bind(on_press=self.show_records)
        layout.add_widget(btn_records)
        
        self.add_widget(layout)
    
    def set_difficulty(self, diff):
        self.difficulty = diff
        colors = {
            'easy': (0.3, 1, 0.3, 1),
            'medium': (1, 1, 0, 1),
            'hard': (1, 0.3, 0.3, 1)
        }
        self.selected_difficulty_label.text = f'Выбрано: {DIFFICULTY_SETTINGS[diff]["name"]}'
        self.selected_difficulty_label.color = colors[diff]
    
    def start_game(self, instance):
        player_name = self.name_input.text.strip()
        if not player_name:
            player_name = 'Игрок'
        
        game_screen = self.manager.get_screen('game')
        game_screen.setup_game(player_name, self.difficulty)
        self.manager.current = 'game'
    
    def show_records(self, instance):
        records_screen = self.manager.get_screen('records')
        records_screen.update_records()
        self.manager.current = 'records'

class RecordsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        title = Label(
            text='ТАБЛИЦА РЕКОРДОВ',
            font_size='28sp',
            bold=True,
            color=(0.7, 1, 0.7, 1),
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        layout.add_widget(title)
        
        scroll = ScrollView(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'top': 0.8}
        )
        
        self.records_container = BoxLayout(
            orientation='vertical', 
            spacing=5,
            size_hint_y=None
        )
        self.records_container.bind(minimum_height=self.records_container.setter('height'))
        scroll.add_widget(self.records_container)
        layout.add_widget(scroll)
        
        btn_back = Button(
            text='НАЗАД',
            font_size='20sp',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.15}
        )
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def update_records(self):
        self.records_container.clear_widgets()
        records = records_manager.get_top_records()
        
        if not records:
            no_records = Label(
                text='Пока нет рекордов',
                color=(1, 1, 1, 1),
                font_size='16sp',
                size_hint_y=None,
                height=40
            )
            self.records_container.add_widget(no_records)
        else:
            for i, record in enumerate(records, 1):
                diff = record.get('difficulty', 'easy')
                diff_name = DIFFICULTY_SETTINGS.get(diff, {}).get('name', 'Лёгкий')
                record_text = f"{i}. {record['name']}: {record['score']} ({diff_name})"
                record_label = Label(
                    text=record_text,
                    color=(1, 1, 1, 1),
                    font_size='16sp',
                    size_hint_y=None,
                    height=30
                )
                self.records_container.add_widget(record_label)
    
    def go_back(self, instance):
        self.manager.current = 'menu'

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = None
    
    def setup_game(self, player_name, difficulty):
        if self.game_widget:
            self.remove_widget(self.game_widget)
        self.game_widget = SinglePlayerGame(player_name=player_name, difficulty=difficulty)
        self.add_widget(self.game_widget)

class SinglePlayerGame(Widget):
    def __init__(self, player_name='Игрок', difficulty='easy', **kwargs):
        super().__init__(**kwargs)
        
        self.player_name = player_name
        self.difficulty = difficulty
        self.game_width = Window.width
        self.game_height = Window.height
        
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.base_speed = settings['base_speed']
        self.speed_increase = settings['speed_increase']
        
        # Платформа
        self.paddle_width = self.game_width * 0.3
        self.paddle_height = 20
        self.paddle_x = self.game_width / 2 - self.paddle_width / 2
        self.paddle_y = 40
        
        # Мяч (увеличен в 2 раза: было 14, стало 28)
        self.ball_size = 28
        self.ball_x = self.game_width / 2 - self.ball_size / 2
        self.ball_y = self.paddle_y + self.paddle_height + 20
        self.current_speed = self.base_speed
        angle = math.radians(60)
        self.ball_vx = self.base_speed * math.cos(angle)
        self.ball_vy = self.base_speed * math.sin(angle)
        
        # Кирпичики
        self.bricks = []
        self.brick_points = 10
        self.create_bricks()
        
        self.score = 0
        self.touch_x = None
        self.game_over_flag = False
        self.return_timer = 0
        self.return_started = False
        
        diff_names = {'easy': 'Лёгкий', 'medium': 'Средний', 'hard': 'Сложный'}
        diff_colors = {'easy': (0.3, 1, 0.3, 1), 'medium': (1, 1, 0, 1), 'hard': (1, 0.3, 0.3, 1)}
        
        self.diff_label = Label(
            text=diff_names[difficulty],
            font_size='12sp',
            color=diff_colors[difficulty],
            bold=True,
            size_hint=(None, None),
            size=(100, 20),
            pos=(10, self.game_height - 30)
        )
        self.add_widget(self.diff_label)
        
        self.draw_game()
        self.update_event = Clock.schedule_interval(self.update, 1/60)
    
    def update_score_display(self):
        if hasattr(self, 'score_label') and self.score_label:
            self.remove_widget(self.score_label)
        self.score_label = Label(
            text=f'Очки: {self.score}',
            font_size='18sp',
            color=(1, 1, 1, 1),
            bold=True,
            size_hint=(None, None),
            size=(150, 30),
            pos=(self.game_width - 160, self.game_height - 40)
        )
        self.add_widget(self.score_label)
    
    def draw_game(self):
        self.canvas.clear()
        
        with self.canvas:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0, 0), size=(self.game_width, self.game_height))
            
            Color(0.2, 0.5, 1, 1)
            self.paddle = Rectangle(pos=(self.paddle_x, self.paddle_y), 
                                   size=(self.paddle_width, self.paddle_height))
            
            Color(1, 1, 1, 1)
            self.ball = Rectangle(pos=(self.ball_x, self.ball_y), 
                                 size=(self.ball_size, self.ball_size))
            
            self.brick_rects = []
            for brick in self.bricks:
                if not brick[2]:
                    Color(0, 0, 0, 0)
                elif brick[5] > 1:
                    Color(1, 1, 0, 1)
                elif brick[5] == 1 and brick[2]:
                    Color(1, 0.5, 0, 1)
                else:
                    Color(0.3, 1, 0.3, 1)
                
                rect = Rectangle(pos=(brick[0], brick[1]), 
                               size=(brick[3], brick[4]))
                self.brick_rects.append(rect)
        
        self.update_score_display()
    
    def create_bricks(self):
        """Создание сетки кирпичиков"""
        cols = 16
        rows = 15
        padding = 1
        top_margin = 60
        
        self.brick_width = (self.game_width - padding * (cols + 1)) / cols
        self.brick_height = 18
        
        start_y = self.game_height - top_margin - self.brick_height
        
        for row in range(rows):
            for col in range(cols):
                x = padding + col * (self.brick_width + padding)
                y = start_y - row * (self.brick_height + padding)
                
                if row < 5:
                    hits_needed = 2
                else:
                    hits_needed = 1
                
                self.bricks.append([x, y, True, self.brick_width, self.brick_height, hits_needed])
    
    def increase_speed(self):
        """Увеличение скорости мяча"""
        self.current_speed += self.speed_increase
        speed_ratio = self.current_speed / (self.current_speed - self.speed_increase)
        self.ball_vx *= speed_ratio
        self.ball_vy *= speed_ratio
    
    def normalize_speed(self):
        """Нормализация скорости до current_speed"""
        current_magnitude = math.sqrt(self.ball_vx**2 + self.ball_vy**2)
        if current_magnitude > 0:
            ratio = self.current_speed / current_magnitude
            self.ball_vx *= ratio
            self.ball_vy *= ratio
    
    def on_touch_down(self, touch):
        if self.game_over_flag:
            return
        self.touch_x = touch.x
        self.move_paddle(touch.x)
    
    def on_touch_move(self, touch):
        if self.game_over_flag:
            return
        self.touch_x = touch.x
        self.move_paddle(touch.x)
    
    def on_touch_up(self, touch):
        self.touch_x = None
    
    def move_paddle(self, x):
        self.paddle_x = x - self.paddle_width / 2
        if self.paddle_x < 0:
            self.paddle_x = 0
        elif self.paddle_x > self.game_width - self.paddle_width:
            self.paddle_x = self.game_width - self.paddle_width
    
    def update(self, dt):
        if self.game_over_flag:
            if self.return_started:
                self.return_timer += dt
                if self.return_timer >= 3:
                    self.return_to_menu()
            return
        
        new_x = self.ball_x + self.ball_vx
        new_y = self.ball_y + self.ball_vy
        
        hit_anything = False
        
        # Отскок от боковых стен
        if new_x <= 0:
            new_x = 0
            self.ball_vx = abs(self.ball_vx)
            hit_anything = True
        elif new_x >= self.game_width - self.ball_size:
            new_x = self.game_width - self.ball_size
            self.ball_vx = -abs(self.ball_vx)
            hit_anything = True
        
        # Отскок от верха
        if new_y >= self.game_height - self.ball_size:
            new_y = self.game_height - self.ball_size
            self.ball_vy = -abs(self.ball_vy)
            hit_anything = True
        
        # Отскок от платформы
        if (new_y <= self.paddle_y + self.paddle_height and 
            new_y + self.ball_size >= self.paddle_y and
            new_x + self.ball_size >= self.paddle_x and 
            new_x <= self.paddle_x + self.paddle_width and
            self.ball_vy < 0):
            
            hit_pos = (new_x + self.ball_size/2 - self.paddle_x) / self.paddle_width
            angle = (hit_pos - 0.5) * math.radians(120)
            
            self.ball_vx = self.current_speed * math.sin(angle)
            self.ball_vy = self.current_speed * math.cos(angle)
            
            new_y = self.paddle_y + self.paddle_height + 1
            hit_anything = True
        
        # Проверка столкновения с кирпичами
        ball_left = new_x
        ball_right = new_x + self.ball_size
        ball_bottom = new_y
        ball_top = new_y + self.ball_size
        
        for i, brick in enumerate(self.bricks):
            if not brick[2]:
                continue
            
            brick_left = brick[0]
            brick_right = brick[0] + brick[3]
            brick_bottom = brick[1]
            brick_top = brick[1] + brick[4]
            
            if (ball_right > brick_left and
                ball_left < brick_right and
                ball_top > brick_bottom and
                ball_bottom < brick_top):
                
                overlap_left = ball_right - brick_left
                overlap_right = brick_right - ball_left
                overlap_bottom = ball_top - brick_bottom
                overlap_top = brick_top - ball_bottom
                
                min_overlap = min(overlap_left, overlap_right, overlap_bottom, overlap_top)
                
                if min_overlap == overlap_bottom:
                    self.ball_vy = -abs(self.ball_vy)
                elif min_overlap == overlap_top:
                    self.ball_vy = abs(self.ball_vy)
                elif min_overlap == overlap_left:
                    self.ball_vx = -abs(self.ball_vx)
                elif min_overlap == overlap_right:
                    self.ball_vx = abs(self.ball_vx)
                
                brick[5] -= 1
                
                if brick[5] <= 0:
                    brick[2] = False
                    self.score += self.brick_points
                else:
                    self.score += 5
                
                hit_anything = True
                
                self.update_score_display()
                self.draw_game()
                
                if all(not b[2] for b in self.bricks):
                    self.game_over(True)
                    return
                
                break
        
        if hit_anything:
            self.increase_speed()
            self.normalize_speed()
        
        self.ball_x = new_x
        self.ball_y = new_y
        
        self.paddle.pos = (self.paddle_x, self.paddle_y)
        self.ball.pos = (self.ball_x, self.ball_y)
        
        if self.ball_y < -self.ball_size:
            self.game_over(False)
    
    def game_over(self, victory):
        self.game_over_flag = True
        self.return_started = True
        self.return_timer = 0
        
        records_manager.add_record(self.player_name, self.score, self.difficulty)
        
        if victory:
            result_text = 'ПОБЕДА!'
            result_color = (0.3, 1, 0.3, 1)
        else:
            result_text = 'ПРОИГРЫШ!'
            result_color = (1, 0.3, 0.3, 1)
        
        self.result_widget = FloatLayout()
        
        with self.result_widget.canvas:
            Color(0.1, 0.1, 0.1, 0.95)
            RoundedRectangle(
                pos=(self.game_width/2 - 150, self.game_height/2 - 100),
                size=(300, 200),
                radius=[20]
            )
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=(self.game_width/2 - 148, self.game_height/2 - 98),
                size=(296, 196),
                radius=[18]
            )
            Color(0.05, 0.05, 0.05, 1)
            RoundedRectangle(
                pos=(self.game_width/2 - 145, self.game_height/2 - 95),
                size=(290, 190),
                radius=[17]
            )
        
        title_label = Label(
            text=result_text,
            font_size='32sp',
            bold=True,
            color=result_color,
            size_hint=(None, None),
            size=(200, 50),
            pos=(self.game_width/2 - 100, self.game_height/2 + 50)
        )
        self.result_widget.add_widget(title_label)
        
        score_label = Label(
            text=f'Очки: {self.score}',
            font_size='24sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos=(self.game_width/2 - 100, self.game_height/2 + 10)
        )
        self.result_widget.add_widget(score_label)
        
        return_label = Label(
            text='Возврат в меню...',
            font_size='16sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(None, None),
            size=(200, 30),
            pos=(self.game_width/2 - 100, self.game_height/2 - 40)
        )
        self.result_widget.add_widget(return_label)
        
        self.add_widget(self.result_widget)
    
    def return_to_menu(self):
        if self.update_event:
            self.update_event.cancel()
        app = App.get_running_app()
        app.root.current = 'menu'

class PongApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RecordsScreen(name='records'))
        return sm

if __name__ == '__main__':
    PongApp().run()