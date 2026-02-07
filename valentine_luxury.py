import customtkinter as ctk
import random
import math
from tkinter import font as tkfont

# Optional Music Support
try:
    import pygame
    MUSIC_AVAILABLE = True
except:
    MUSIC_AVAILABLE = False


# ---------------- THEME ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ---------------- LUXURY COLORS ----------------
class Colors:
    BG = "#FFF5F7"
    CARD = "#FFFFFF"
    PRIMARY = "#FF4D6D"
    PRIMARY_HOVER = "#FF1744"
    SOFT = "#FF8FA3"
    SOFT_HOVER = "#FF6B88"
    TEXT = "#2D1B20"
    TEXT_LIGHT = "#5A3E46"
    BORDER = "#FFD4DC"
    ACCENT = "#FFC2D1"
    HEART = "#FF6B9D"
    SHADOW = "#E8E8E8"


# ---------------- MAIN APP ----------------
class LuxuryValentineApp:

    def __init__(self, root):
        self.root = root
        self.root.title("💕 Valentine's Special")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size
        window_width = 1100
        window_height = 1000
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set geometry with position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=Colors.BG)
        
        # Prevent window resize
        self.root.resizable(False, False)

        # Animation state
        self.yes_grow_size = 220
        self.yes_growing = False
        self.no_shrink_factor = 1.0
        self.hover_count = 0
        
        # Music
        self.setup_music()
        
        # Background
        self.setup_background()
        
        # Main card
        self.setup_card()
        
        # Build UI
        self.build_ui()
        
        # Start animations
        self.animate_no()
        self.animate_yes_pulse()
        self.root.bind("<Motion>", self.mouse_detect)

    # ---------------- MUSIC ----------------
    def setup_music(self):
        if MUSIC_AVAILABLE:
            try:
                pygame.mixer.init()
                pygame.mixer.music.load("music.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            except:
                pass

    # ---------------- BACKGROUND ----------------
    def setup_background(self):
        self.canvas = ctk.CTkCanvas(
            self.root,
            bg=Colors.BG,
            highlightthickness=0,
            width=1100,
            height=1000
        )
        self.canvas.place(relwidth=1, relheight=1)
        
        # Gradient effect with overlapping circles
        self.create_gradient_bg()
        
        # Animated petals
        self.petals = []
        self.create_petals()
        self.animate_petals()
        
        # Floating hearts
        self.hearts = []
        self.create_hearts()
        self.animate_hearts()

    def create_gradient_bg(self):
        """Create soft gradient circles in background"""
        colors = ["#FFE5EC", "#FFF0F3", "#FFD4DC"]
        for i in range(6):
            x = random.randint(100, 1000)
            y = random.randint(100, 900)
            size = random.randint(180, 350)
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=random.choice(colors),
                outline="",
                tags="gradient"
            )
        self.canvas.tag_lower("gradient")

    # ---------------- CARD ----------------
    def setup_card(self):
        # Shadow effect
        self.shadow = ctk.CTkFrame(
            self.root,
            width=756,
            height=756,
            corner_radius=32,
            fg_color=Colors.SHADOW,
            border_width=0
        )
        self.shadow.place(relx=0.5, rely=0.5, anchor="center", y=3)
        
        # Main card
        self.card = ctk.CTkFrame(
            self.root,
            width=750,
            height=750,
            corner_radius=30,
            fg_color=Colors.CARD,
            border_width=3,
            border_color=Colors.BORDER
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

    # ---------------- UI ----------------
    def build_ui(self):
        # Decorative hearts at top
        heart_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        heart_frame.place(relx=0.5, rely=0.10, anchor="center")
        
        hearts_text = ctk.CTkLabel(
            heart_frame,
            text="♥  ♥  ♥",
            font=("Arial", 36),
            text_color=Colors.HEART
        )
        hearts_text.pack()
        
        # Main title
        self.title = ctk.CTkLabel(
            self.card,
            text="Tanishka \nWill you be my Valentine?",
            font=("Georgia", 52, "bold"),
            text_color=Colors.PRIMARY,
            justify="center"
        )
        self.title.place(relx=0.5, rely=0.32, anchor="center")
        
        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self.card,
            text="Choose wisely... 💕",
            font=("Arial", 20, "italic"),
            text_color=Colors.TEXT_LIGHT
        )
        self.subtitle.place(relx=0.5, rely=0.50, anchor="center")
        
        # YES BUTTON
        self.yes_btn = ctk.CTkButton(
            self.card,
            text="💕 Yes! 💕",
            width=220,
            height=85,
            corner_radius=42,
            fg_color=Colors.SOFT,
            hover_color=Colors.PRIMARY_HOVER,
            font=("Arial", 28, "bold"),
            text_color="white",
            command=self.show_success,
            border_width=3,
            border_color=Colors.PRIMARY
        )
        self.yes_btn.place(relx=0.30, rely=0.68, anchor="center")
        
        # NO BUTTON (starts smaller)
        self.no_btn = ctk.CTkButton(
            self.card,
            text="No",
            width=220,
            height=85,
            corner_radius=42,
            fg_color=Colors.ACCENT,
            hover_color=Colors.SOFT_HOVER,
            font=("Arial", 24),
            text_color=Colors.TEXT_LIGHT,
            border_width=2,
            border_color=Colors.BORDER
        )
        
        self.no_x = 0.70
        self.no_y = 0.68
        self.no_btn.place(relx=self.no_x, rely=self.no_y, anchor="center")
        
        self.no_dx = random.choice([-1, 1]) * 0.003
        self.no_dy = random.choice([-1, 1]) * 0.003
        
        # Hint text
        self.hint = ctk.CTkLabel(
            self.card,
            text="Psst... the 'Yes' button is getting bigger! 😊",
            font=("Arial", 15, "italic"),
            text_color=Colors.TEXT_LIGHT
        )
        self.hint.place(relx=0.5, rely=0.85, anchor="center")

    # ---------------- YES BUTTON PULSE/GROW ----------------
    def animate_yes_pulse(self):
        """Make Yes button grow over time"""
        if self.yes_grow_size < 340:
            self.yes_grow_size += 0.3
            self.yes_btn.configure(
                width=int(self.yes_grow_size),
                height=int(self.yes_grow_size * 0.4)
            )
        
        self.root.after(100, self.animate_yes_pulse)

    # ---------------- NO BUTTON ANIMATIONS ----------------
    def animate_no(self):
        """Float the No button around"""
        self.no_x += self.no_dx
        self.no_y += self.no_dy
        
        # Bounce off boundaries
        if self.no_x < 0.20 or self.no_x > 0.80:
            self.no_dx *= -1
        if self.no_y < 0.58 or self.no_y > 0.80:
            self.no_dy *= -1
        
        self.no_btn.place(relx=self.no_x, rely=self.no_y, anchor="center")
        self.root.after(20, self.animate_no)

    def mouse_detect(self, event):
        """Detect mouse near No button and make it run away + shrink"""
        try:
            bx = self.no_btn.winfo_rootx() + self.no_btn.winfo_width() // 2
            by = self.no_btn.winfo_rooty() + self.no_btn.winfo_height() // 2
            
            dist = math.sqrt(
                (event.x_root - bx) ** 2 +
                (event.y_root - by) ** 2
            )
            
            if dist < 150:
                # Jump away
                self.no_x = random.uniform(0.25, 0.75)
                self.no_y = random.uniform(0.58, 0.78)
                self.no_btn.place(relx=self.no_x, rely=self.no_y, anchor="center")
                
                # Shrink the button
                self.hover_count += 1
                if self.hover_count % 2 == 0 and self.no_shrink_factor > 0.3:
                    self.no_shrink_factor -= 0.08
                    new_width = int(220 * self.no_shrink_factor)
                    new_height = int(85 * self.no_shrink_factor)
                    new_font_size = max(10, int(24 * self.no_shrink_factor))
                    
                    self.no_btn.configure(
                        width=new_width,
                        height=new_height,
                        font=("Arial", new_font_size)
                    )
                
                # Speed up movement
                self.no_dx = random.choice([-1, 1]) * random.uniform(0.004, 0.008)
                self.no_dy = random.choice([-1, 1]) * random.uniform(0.004, 0.008)
                
        except:
            pass

    # ---------------- PETALS ----------------
    def create_petals(self):
        """Create falling flower petals"""
        symbols = ["❀", "✿", "🌸", "🌺", "🌷"]
        
        for _ in range(30):
            x = random.randint(0, 1100)
            y = random.randint(-1200, -100)
            
            p = self.canvas.create_text(
                x, y,
                text=random.choice(symbols),
                fill=random.choice([Colors.BORDER, Colors.SOFT, Colors.ACCENT]),
                font=("Arial", random.randint(16, 30)),
                tags="petal"
            )
            
            speed = random.uniform(0.5, 1.5)
            drift = random.uniform(-0.3, 0.3)
            self.petals.append([p, speed, drift, x, y])

    def animate_petals(self):
        """Animate falling petals with drift"""
        for i, (p, speed, drift, x, y) in enumerate(self.petals):
            y += speed
            x += drift
            
            # Wrap horizontally
            if x < 0:
                x = 1100
            elif x > 1100:
                x = 0
            
            coords = self.canvas.coords(p)
            if coords:
                self.canvas.coords(p, x, y)
            
            # Reset when below screen
            if y > 1020:
                x = random.randint(0, 1100)
                y = random.randint(-1200, -100)
                self.canvas.coords(p, x, y)
            
            self.petals[i] = [p, speed, drift, x, y]
        
        self.root.after(50, self.animate_petals)

    # ---------------- HEARTS ----------------
    def create_hearts(self):
        """Create floating hearts"""
        for _ in range(20):
            x = random.randint(50, 1050)
            y = random.randint(1000, 1500)
            
            h = self.canvas.create_text(
                x, y,
                text="♥",
                fill=random.choice([Colors.HEART, Colors.PRIMARY, Colors.SOFT]),
                font=("Arial", random.randint(20, 36)),
                tags="heart"
            )
            
            speed = random.uniform(0.6, 1.8)
            self.hearts.append([h, speed, x, y])

    def animate_hearts(self):
        """Animate rising hearts"""
        for i, (h, speed, x, y) in enumerate(self.hearts):
            y -= speed
            
            coords = self.canvas.coords(h)
            if coords:
                self.canvas.coords(h, x, y)
            
            # Reset when above screen
            if y < -50:
                x = random.randint(50, 1050)
                y = random.randint(1000, 1500)
                self.canvas.coords(h, x, y)
            
            self.hearts[i] = [h, speed, x, y]
        
        self.root.after(50, self.animate_hearts)

    # ---------------- SUCCESS SCREEN ----------------
    def show_success(self):
        """Show beautiful success message"""
        if MUSIC_AVAILABLE:
            try:
                pygame.mixer.music.set_volume(0.7)
            except:
                pass
        
        # Clear card
        for widget in self.card.winfo_children():
            widget.destroy()
        
        # Create celebration effect
        self.create_celebration()
        
        # Success message title
        msg_title = ctk.CTkLabel(
            self.card,
            text="💕 Yes! 💕",
            font=("Georgia", 60, "bold"),
            text_color=Colors.PRIMARY
        )
        msg_title.place(relx=0.5, rely=0.15, anchor="center")
        
        # Main message with proper wrapping
        msg_body = """You didn't just change my world —

I love being with you, walking beside you,
listening to you, mimicking you,
and then watching you make that cute face
that melts me every time.

You make me want to keep improving myself,
not out of pressure but out of love.

The laughter we share, the love we feel —
you complete me in a way
I never knew was possible."""
        
        label = ctk.CTkLabel(
            self.card,
            text=msg_body,
            font=("Georgia", 19),
            text_color=Colors.TEXT,
            justify="center",
            wraplength=650
        )
        label.place(relx=0.5, rely=0.52, anchor="center")
        
        # Date/time frame
        date_frame = ctk.CTkFrame(
            self.card,
            fg_color=Colors.BG,
            corner_radius=20,
            border_width=2,
            border_color=Colors.PRIMARY
        )
        date_frame.place(relx=0.5, rely=0.82, anchor="center")
        
        date_label = ctk.CTkLabel(
            date_frame,
            text="Stop being so amazing, it's distracting.🫠\nI love you so much",
            font=("Freestyle Script", 26, "bold"),
            text_color=Colors.PRIMARY,
            padx=35,
            pady=18
        )
        date_label.pack()
        
        # Bottom hearts
        bottom_hearts = ctk.CTkLabel(
            self.card,
            text="♥ ♥ ♥ ♥ ♥",
            font=("Caveat", 25, "bold"),
            text_color=Colors.HEART
        )
        bottom_hearts.place(relx=0.5, rely=0.93, anchor="center")

    def create_celebration(self):
        """Create celebration hearts explosion"""
        for _ in range(40):
            x = 550
            y = 500
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            h = self.canvas.create_text(
                x, y,
                text="♥",
                fill=random.choice([Colors.PRIMARY, Colors.HEART, Colors.SOFT]),
                font=("Arial", random.randint(20, 40)),
                tags="celebration"
            )
            
            self.animate_celebration_heart(h, x, y, dx, dy, 0)

    def animate_celebration_heart(self, heart, x, y, dx, dy, count):
        """Animate single celebration heart"""
        if count > 50:
            self.canvas.delete(heart)
            return
        
        x += dx
        y += dy
        dy += 0.2  # Gravity
        
        self.canvas.coords(heart, x, y)
        self.root.after(30, lambda: self.animate_celebration_heart(heart, x, y, dx, dy, count + 1))


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    
    # Bring window to front
    root.attributes("-topmost", True)
    
    app = LuxuryValentineApp(root)
    
    root.after(1500, lambda: root.attributes("-topmost", False))
    
    root.mainloop()


from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome ❤️</h1>
    <p>This is my Valentine Web App</p>
    <button onclick="alert('Yes clicked ❤️')">Yes</button>
    <button onclick="alert('No clicked 💔')">No</button>
    """

if __name__ == "__main__":
    app.run(debug=True)

