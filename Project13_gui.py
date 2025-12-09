#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random


import Project13_db as db
from Project13_game import BlackjackGame


# Try to import tkmacosx for better button styling on Mac
try:
    from tkmacosx import Button as MacButton
except ImportError:
    MacButton = None

class BlackjackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack Pro")
        self.geometry("800x600")
        self.configure(bg="#2E8B57") # Sea Green table color
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.db = db
        self.db.connect()
        
        self.game = BlackjackGame()
        self.player = None
        self.current_bet = 0.0

        # UI Containers
        self.container = tk.Frame(self, bg="#2E8B57")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Start with Login
        self.show_login()

    def create_colored_button(self, parent, text, command, bg, fg, font, **kwargs):
        """Helper to create cross-platform colored buttons with black border."""
        if MacButton:
            # Use highlight options for fake border on Mac
            return MacButton(parent, text=text, command=command, bg=bg, fg=fg, 
                           font=font, activebackground=bg, borderless=1, 
                           focuscolor="", highlightthickness=2, highlightbackground="black", **kwargs)
        else:
            # Standard tkinter button fallback
            # CRITICAL FIX: Standard buttons treat 'height' as text lines, not pixels.
            # If height is passed (e.g. 50), it makes a huge button. We must remove it.
            if 'height' in kwargs:
                kwargs.pop('height') 
                
            return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, 
                           font=font, activebackground=bg, activeforeground=fg, 
                           relief="solid", bd=2, highlightbackground="black", highlightthickness=2, **kwargs)

    def start_button_flash(self, button, color1, color2):
        """Starts a flashing animation on a specific button."""
        button.flash_active = True
        self._flash_button(button, color1, color2)
    
    def stop_button_flash(self, button, final_color):
        """Stops the flashing animation for a specific button."""
        button.flash_active = False
        if MacButton and isinstance(button, MacButton):
            button.configure(bg=final_color)
        else:
            button.config(bg=final_color)

    def start_entry_flash(self, entry, color1, color2):
        """Starts flashing the entry border."""
        entry.flash_active = True
        self._flash_entry_border(entry, color1, color2)

    def stop_entry_flash(self, entry, final_color):
        """Stops flashing the entry border."""
        entry.flash_active = False
        try:
            entry.config(highlightbackground=final_color)
        except:
            pass

    def _flash_entry_border(self, entry, color1, color2):
        """Internal method to toggle entry border color."""
        if not getattr(entry, 'flash_active', False):
            return
        try:
            current = entry.cget('highlightbackground')
            new_color = color2 if current == color1 else color1
            entry.config(highlightbackground=new_color)
            self.after(500, lambda: self._flash_entry_border(entry, color1, color2))
        except:
            pass
    
    def _flash_button(self, button, color1, color2):
        """Internal method to toggle button colors."""
        try:
            if not button.winfo_exists() or not getattr(button, 'flash_active', False):
                return
                
            current_color = button.cget("bg")
            next_color = color2 if current_color == color1 else color1
            
            if MacButton and isinstance(button, MacButton):
                button.configure(bg=next_color)
            else:
                button.config(bg=next_color)
                
            self.after(500, lambda: self._flash_button(button, color1, color2))
        except Exception:
            pass

    def show_login(self):
        """Displays the login screen."""
        self.clear_container()
        
        frame = tk.Frame(self.container, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="♠ ♥ Blackjack Game ♣ ♦", font=("Arial", 32, "bold"), fg="#2E8B57", bg="white").pack(pady=20)
        
        tk.Label(frame, text="Step 1: Create or Load Profile", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=(0, 10))
        tk.Label(frame, text="Enter your Name to Begin:", font=("Arial", 14), bg="white").pack(anchor="w")

        
        # Detailed Instructions
        instr_text = (
            "• Valid: Letters (A-Z), Numbers (0-9), Spaces\n"
            "• Invalid: Symbols (@, #, $, !)\n"
            "• Good: 'John Doe', 'Player1'\n"
            "• Bad: 'User$Name', 'Winner!'"
        )
        tk.Label(frame, text=instr_text, font=("Arial", 11, "italic"), bg="#f0f0f0", fg="#555555", 
                 justify="left", padx=10, pady=5, relief="solid", bd=1).pack(anchor="w", pady=5, fill="x")
        self.name_var = tk.StringVar()
        self.entry_login = tk.Entry(frame, textvariable=self.name_var, font=("Arial", 14),
                         relief="sunken", bd=3, bg="white", fg="black", insertbackground="black",
                         highlightthickness=2, highlightcolor="#4CAF50", highlightbackground="#cccccc")
        self.entry_login.pack(fill="x", pady=5)
        self.entry_login.bind("<Return>", lambda event: self.login())
        
        # Start flashing the entry border to attract attention
        self.start_entry_flash(self.entry_login, "#4CAF50", "#cccccc")
        
        self.btn_start = self.create_colored_button(frame, text="Start Playing", command=self.login, 
                        font=("Arial", 14, "bold"), bg="#4CAF50", fg="black")
        self.btn_start.pack(pady=10, fill="x")
        # Start flashing animation
        self.start_button_flash(self.btn_start, "#4CAF50", "#81C784")

        # Exit Button
        self.create_colored_button(frame, text="EXIT GAME", command=self.on_closing,
                             font=("Arial", 12, "bold"), bg="#D32F2F", fg="white").pack(pady=5, fill="x")

    def login(self):
        try:
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a name.", parent=self)
                return
                
            # Validation: Alphanumeric only (letters, numbers, spaces)
            if not name.replace(" ", "").isalnum():
                 messagebox.showerror("Error", "Name can only contain letters, numbers, and spaces.\n\nExample: 'John Doe'", parent=self)
                 return
            
            # Stop flashing before proceeding
            self.stop_entry_flash(self.entry_login, "#cccccc")
            
            self.player = self.db.get_player(name)
            self.show_game_interface()
            
        except Exception as e:
            messagebox.showerror("Login Error", f"An unexpected error occurred during login:\n{e}", parent=self)
            print(f"Login Crash: {e}") # Log to console for debugging

    def show_game_interface(self):
        """Displays the main game table."""
        self.clear_container()
        
        # --- Main horizontal layout: Table on left, Controls on right ---
        main_frame = tk.Frame(self.container, bg="#2E8B57")
        main_frame.pack(fill="both", expand=True)
        
        # --- Left Side: Game Table (Canvas) ---
        table_frame = tk.Frame(main_frame, bg="#35654d")
        table_frame.pack(side="left", fill="both", expand=True)
        
        self.canvas = tk.Canvas(table_frame, bg="#35654d", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Right Side: Controls Panel ---
        # Fixed width to prevent resizing weirdness
        control_panel = tk.Frame(main_frame, bg="#225533", padx=10, pady=10, width=220)
        control_panel.pack(side="right", fill="y")
        control_panel.pack_propagate(False) # Force fixed width
        
        # 1. TOP CONTAINER (Stats & Betting)
        top_container = tk.Frame(control_panel, bg="#225533")
        top_container.pack(side="top", fill="x")

        # Player Info
        self.lbl_player = tk.Label(top_container, text=f"Player: {self.player.name}", 
                                   font=("Arial", 12, "bold"), fg="white", bg="#225533")
        self.lbl_player.pack(pady=(0, 5))
        
        self.lbl_balance = tk.Label(top_container, text=f"Balance: ${self.player.balance:.2f}",
                                    font=("Arial", 16, "bold"), fg="#FFD700", bg="#225533")
        self.lbl_balance.pack(pady=2)

        # Statistics Panel
        self.stats_frame = tk.Frame(top_container, bg="#1a402a", padx=5, pady=5, relief="flat")
        self.stats_frame.pack(fill="x", pady=5)
        
        self.lbl_win_rate = tk.Label(self.stats_frame, text="Win Rate: 0.0%", font=("Arial", 10), fg="#81C784", bg="#1a402a")
        self.lbl_win_rate.pack(anchor="w")
        
        self.lbl_record = tk.Label(self.stats_frame, text="W: 0 | L: 0", font=("Arial", 10), fg="white", bg="#1a402a")
        self.lbl_record.pack(anchor="w")
        
        self.lbl_net_earnings = tk.Label(self.stats_frame, text="Total Net: $0.00", font=("Arial", 10, "bold"), fg="#FFB74D", bg="#1a402a")
        self.lbl_net_earnings.pack(anchor="w", pady=(5, 0))

        # Divider
        tk.Frame(top_container, height=2, bg="#3a6b52").pack(fill="x", pady=10)
        
        # Betting Controls
        tk.Label(top_container, text="Enter Bet:", font=("Arial", 12, "bold"), 
                 bg="#225533", fg="white").pack(pady=2)
        
        self.bet_var = tk.StringVar(value="20.0")
        entry_container = tk.Frame(top_container, bg="white", padx=2, pady=2)
        entry_container.pack(pady=5)
        self.bet_entry = tk.Entry(entry_container, textvariable=self.bet_var, width=10, font=("Arial", 14),
                           relief="sunken", bd=2, bg="white", fg="black", insertbackground="black")
        self.bet_entry.pack()
        self.bet_entry.bind("<Return>", lambda event: self.start_hand())
        
        self.btn_deal = self.create_colored_button(top_container, text="DEAL", command=self.start_hand, 
                  font=("Arial", 14, "bold"), bg="#9C27B0", fg="white", width=130, height=50)
        self.btn_deal.pack(pady=5)
        self.start_button_flash(self.btn_deal, "#9C27B0", "#CE93D8")
        
        self.lbl_locked = tk.Label(top_container, text="", font=("Arial", 10, "italic"), bg="#225533", fg="#FFD700")
        self.lbl_locked.pack(pady=2)

        # 2. SPACER SPRING (Pushes Bottom Container Down)
        self.spacer = tk.Frame(control_panel, bg="#225533")
        self.spacer.pack(side="top", fill="both", expand=True)

        # 3. BOTTOM CONTAINER (Status, Gameplay, Exit)
        # Packed Side Bottom to Anchor it
        self.bottom_container = tk.Frame(control_panel, bg="#225533")
        self.bottom_container.pack(side="bottom", fill="x", pady=10)

        # Status Label
        self.lbl_status = tk.Label(self.bottom_container, text="Place your bet!", 
                                   font=("Arial", 12, "bold"), fg="white", bg="#225533", wraplength=180, justify="center")
        self.lbl_status.pack(pady=(0, 10), fill="x")

        # Gameplay Controls (Hit/Stand) - Initially Hidden
        # We create it inside bottom_container so it pushes Exit triggers
        self.play_frame = tk.Frame(self.bottom_container, bg="#225533")
        # will pack play_frame in start_hand
        
        self.btn_hit = self.create_colored_button(self.play_frame, text="HIT", command=self.player_hit, 
                  font=("Arial", 14, "bold"), bg="#2196F3", fg="white", width=130, height=50)
        self.btn_hit.pack(pady=5)
        
        self.btn_stand = self.create_colored_button(self.play_frame, text="STAND", command=self.player_stand, 
                  font=("Arial", 14, "bold"), bg="#FFC107", fg="black", width=130, height=50)
        self.btn_stand.pack(pady=5)

        # Divider
        tk.Frame(self.bottom_container, height=2, bg="#3a6b52").pack(fill="x", pady=10)

        # Exit Button
        self.create_colored_button(self.bottom_container, text="EXIT", command=self.on_closing,
                  font=("Arial", 12, "bold"), bg="#D32F2F", fg="white", width=130, height=40).pack(side="bottom")

        # Initial Stats
        self.update_info_labels()
        
        # Draw background
        self.draw_table_background() 
        self.container.after(100, self.draw_table)

    def draw_table_background(self):
        """Draws static background elements only."""
        self.canvas.delete("all")

    def draw_table(self):
        """Alias for draw_table_background to satisfy game loop calls."""
        self.draw_table_background()
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 100: w = 800
        if h < 100: h = 600

        # Rail
        arc_x1 = 50; arc_y1 = -200; arc_x2 = w - 50; arc_y2 = h - 150
        self.canvas.create_arc(arc_x1, arc_y1, arc_x2, arc_y2, start=180, extent=180, style="arc", outline="white", width=3)

        self.draw_dealer_chips()
        if self.player:
            self.draw_player_chips()
        else:
             self.draw_player_chips(override_balance=1000)
             
        self.draw_deck()

        # Dealer's Rack
        rack_w = 400; rack_x = (w - rack_w) / 2
        self.canvas.create_rectangle(rack_x, 20, rack_x + rack_w, 80, fill="#1a3326", outline="#112219")
        self.canvas.create_text(w/2, 40, text="Dealer Pays 2:1", font=("Arial", 14, "bold"), fill="#FFD700")
        self.canvas.create_text(w/2, 65, text="Dealer must draw to 16 and stand on 17", font=("Arial", 11, "bold"), fill="#F0F0F0")

        # Symbols
        symbols = ["♦", "♥", "♣", "♠"]
        sym_y = h / 2
        start_sym_x = w/2 - 75
        for i, sym in enumerate(symbols):
            self.canvas.create_text(start_sym_x + i*50, sym_y, text=sym, font=("Arial", 48), fill="#4a8b6a")

        # Hands
        dealer_y = 90
        player_y = h - 200
        cards_x = 120
        self.draw_hand(self.game.dealer_hand, cards_x, dealer_y, "Dealer")
        self.draw_hand(self.game.player_hand, cards_x, player_y, "Player")

        # Dynamic Chip Stacks
        self.draw_player_chips()
        self.draw_dealer_chips()

    def draw_player_chips(self, override_balance=None):
        """Draws chip stacks proportional to player balance."""
        if override_balance is not None:
            balance = override_balance
        elif self.player:
             balance = int(self.player.balance)
        else:
             return
             
        # Calculate counts with $50 red chips
        num_black = min(balance // 100, 15)
        rem = balance % 100
        num_red50 = min(rem // 50, 15)  # Red $50 chips
        rem = rem % 50
        num_green = min(rem // 25, 15)
        rem = rem % 25
        num_red5 = min(rem // 5, 15)
        
        # Player chips: FAR BOTTOM LEFT corner (tight to corner)
        start_x = 5
        start_y = self.canvas.winfo_height() - 45  # Very bottom
        if start_y < 100: start_y = 450
        
        # Draw compact stacks
        self.draw_chip_stack(start_x, start_y, min(num_black, 8), "black", "100", messy=True)
        self.draw_chip_stack(start_x + 38, start_y, min(num_red50, 8), "red", "50", messy=True)
        self.draw_chip_stack(start_x + 76, start_y, min(num_green, 8), "green", "25", messy=True)

    def draw_dealer_chips(self):
        """Draws House Bank in FAR TOP LEFT corner with all 4 chip colors."""
        start_x = 5
        start_y = 55  # Top left corner
        
        # All 4 chip colors: black, red, blue, green
        self.draw_chip_stack(start_x, start_y, 6, "black", "100")
        self.draw_chip_stack(start_x + 38, start_y, 6, "red", "50")
        self.draw_chip_stack(start_x + 76, start_y, 6, "blue", "500")
        self.draw_chip_stack(start_x + 114, start_y, 6, "green", "25")

    def draw_chip_stack(self, x, y, count, color, val, messy=False):
        for i in range(count):
            rx = 0
            ry = 0
            if messy:
                rx = random.randint(-2, 2)
                ry = random.randint(-1, 1)
            # Stacking upwards with smaller spacing
            self.draw_chip(x + rx, y - (i * 3) + ry, color, val)

    def draw_chip(self, x, y, color, val):
        # Smaller chips: 35px instead of 50px
        size = 35
        self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="white", width=1)
        self.canvas.create_oval(x+3, y+3, x+size-3, y+size-3, outline="white", width=1, dash=(2, 2))
        self.canvas.create_text(x+size/2, y+size/2, text=val, fill="white", font=("Arial", 8, "bold"))

    def draw_hand(self, hand, start_x, start_y, label):
        x_offset = 0
        card_count = 0
        card_height = 140
        
        if hand and hand.cards:
            for card in hand.cards:
                self.draw_card(start_x + x_offset, start_y, card)
                x_offset += 110 # Card width + spacing
                card_count += 1
        else:
            # Draw placeholder face-down cards when no game is active
            for i in range(2):
                self.draw_placeholder_card(start_x + i * 110, start_y)
                x_offset = (i + 1) * 110

        # Label position: Under first card for Dealer, Above first card for Player
        label_x = start_x + 50  # Center of first card
        
        if label == "Dealer":
            # Label BELOW the dealer's first card
            label_y = start_y + card_height + 25
            label_x = start_x + 50 
        else:
            # Label ABOVE the player's hand
            label_y = start_y - 25
            label_x = start_x + 100 
        
        # Only show points if there are actual cards
        if hand and hand.cards:
            total_val = f"{hand.points}"
            if label == "Dealer" and hand.cards:
                 # Check for hidden card
                 if hand.cards[-1].hidden:
                      if len(hand.cards) > 0:
                         c = hand.cards[0]
                         v = c.value
                         if c.rank in ["Jack", "Queen", "King"]: v = 10
                         elif c.rank == "Ace": v = 11
                         total_val = f"{v} + ?"
                
            # Use outlined text for visibility
            self.create_outlined_text(label_x, label_y, 
                                    text=f"{label}: {total_val}", 
                                    font=("Arial", 18, "bold"), fill="#FFD700", anchor="center")
        else:
            # Show label even without cards
            self.create_outlined_text(label_x, label_y, 
                                    text=f"{label}", 
                                    font=("Arial", 18, "bold"), fill="#FFD700", anchor="center")

    def create_outlined_text(self, x, y, text, **kwargs):
        """Helper to draw text with a white outline."""
        fill = kwargs.pop("fill", "black")
        font = kwargs.pop("font", ("Arial", 10))
        anchor = kwargs.pop("anchor", "center")
        
        # Outline
        outline = "white"
        # Special case: If main text is yellow/gold, use black outline for better contrast
        if fill in ["#FFD700", "yellow", "gold"]:
            outline = "black"
            
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
             self.canvas.create_text(x+dx, y+dy, text=text, fill=outline, font=font, anchor=anchor, **kwargs)
        
        # Main Text
        self.canvas.create_text(x, y, text=text, fill=fill, font=font, anchor=anchor, **kwargs)

    def draw_card(self, x, y, card):
        """Draws a visual representation of a card with pips and 4-corner labels."""
        width = 100
        height = 140
        
        # Card Background - Thicker Border
        self.canvas.create_rectangle(x, y, x + width, y + height, fill="white", outline="black", width=3)
        
        if card.hidden:
            # Patterned back
            self.canvas.create_rectangle(x+3, y+3, x+width-3, y+height-3, fill="#8B0000", outline="black")
            for i in range(0, 100, 10):
                 self.canvas.create_line(x+3, y+3+i, x+3+i, y+3, fill="#B22222", width=2)
            return

        # Text Color
        val_color = "black"
        if card.suit in ["Hearts", "Diamonds"]:
            val_color = "red"
            
        suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
        symbol = suit_symbols.get(card.suit, "?")
        
        # --- 4 Corner Labels (Outlined) - Moved Inwards ---
        # TL: Rank + Symbol
        self.create_outlined_text(x + 20, y + 25, text=f"{card.rank}\n{symbol}", 
                                font=("Arial", 10, "bold"), fill=val_color, justify="center")
        # TR: Suit + Symbol
        self.create_outlined_text(x + width - 20, y + 25, text=f"{card.suit}\n{symbol}", 
                                font=("Arial", 7, "bold"), fill=val_color, justify="center")
        # BL: Symbol + Suit (Symbol on Top)
        self.create_outlined_text(x + 20, y + height - 25, text=f"{symbol}\n{card.suit}", 
                                font=("Arial", 7, "bold"), fill=val_color, justify="center")
        # BR: Symbol + Rank (Symbol on Top)
        self.create_outlined_text(x + width - 20, y + height - 25, text=f"{symbol}\n{card.rank}", 
                                font=("Arial", 10, "bold"), fill=val_color, justify="center")
        # --- Center Content ---
        if card.rank == "Ace":
             self.canvas.create_text(x + width/2, y + height/2, text=symbol, 
                                    font=("Arial", 70), fill=val_color)
        elif card.rank in ["Jack", "Queen", "King"]:
            # Face Card Box
            self.canvas.create_rectangle(x + 25, y + 35, x + width - 25, y + height - 35, 
                                       outline="#FFD700", width=2)
            # Center Letter
            self.canvas.create_text(x + width/2, y + height/2, text=card.rank[0], 
                                  font=("Times New Roman", 56, "bold"), fill=val_color)
            # Symbols Above and Below
            self.canvas.create_text(x + width/2, y + height/2 - 40, text=symbol, 
                                  font=("Arial", 24), fill=val_color)
            self.canvas.create_text(x + width/2, y + height/2 + 40, text=symbol, 
                                  font=("Arial", 24), fill=val_color)
        else:
            # Numbered Pips
            try:
                rank_int = int(card.rank)
                self.draw_pips(x, y, rank_int, symbol, val_color)
            except:
                pass

    def draw_pips(self, x, y, rank, symbol, color):
        """Draws the correct number of pips on the card."""
        # Positions: (x_offset, y_offset) relative to card center (50, 70)
        # Grid roughly: cols at 30, 70. rows at 30, 50, 70, 90, 110
        pips = []
        if rank == 2: pips = [(50, 30), (50, 110)]
        elif rank == 3: pips = [(50, 30), (50, 70), (50, 110)]
        elif rank == 4: pips = [(30, 30), (70, 30), (30, 110), (70, 110)]
        elif rank == 5: pips = [(30, 30), (70, 30), (50, 70), (30, 110), (70, 110)]
        elif rank == 6: pips = [(30, 30), (70, 30), (30, 70), (70, 70), (30, 110), (70, 110)]
        elif rank == 7: pips = [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70), (30, 110), (70, 110)]
        elif rank == 8: pips = [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70), (50, 90), (30, 110), (70, 110)]
        elif rank == 9: pips = [(30, 30), (70, 30), (30, 50), (70, 50), (50, 70), (30, 90), (70, 90), (30, 110), (70, 110)]
        elif rank == 10: pips = [(30, 30), (70, 30), (50, 45), (30, 60), (70, 60), (30, 80), (70, 80), (50, 95), (30, 110), (70, 110)] # Adjusted for 10
        
        for px, py in pips:
            # Adjust offsets if using simplified grid logic
            self.canvas.create_text(x + px, y + py, text=symbol, font=("Arial", 20), fill=color)

    def draw_placeholder_card(self, x, y):
        """Draws an empty card slot outline."""
        width = 100
        height = 140
        
        # Empty slot dashed outline
        self.canvas.create_rectangle(x, y, x + width, y + height, fill="", outline="#3a6b52", width=2, dash=(4, 4))
        self.canvas.create_text(x + width/2, y + height/2, text="EMPTY", font=("Arial", 10, "bold"), fill="#2e5540")

    def start_hand(self):
        """Starts a new hand."""
        try:
            bet_amount = float(self.bet_var.get())
            if bet_amount <= 0:
                messagebox.showerror("Error", "Bet must be positive.", parent=self)
                return
            if bet_amount > self.player.balance:
                messagebox.showerror("Error", "Insufficient funds.", parent=self)
                return
            
            self.current_bet = bet_amount
            self.db.update_player_balance(self.player, -self.current_bet)
            
            self.game.start_new_hand()
            
            # UI Updates
            self.stop_button_flash(self.btn_deal, "#cccccc")
            self.bet_entry.config(state="disabled")
            if MacButton and isinstance(self.btn_deal, MacButton):
                 self.btn_deal.configure(bg="#cccccc", fg="#666666") 
            else:
                 self.btn_deal.config(state="disabled", bg="#cccccc")
                 
            self.lbl_locked.config(text=f"Bet Locked: ${self.current_bet:.2f}")
            
            self.draw_table()
            self.update_info_labels()
            
            # CHECK FOR INSTANT BLACKJACK
            if self.game.player_hand.points == 21:
                 # Natural Blackjack!
                 # Reveal dealer cards for visual completeness
                 for card in self.game.dealer_hand.cards:
                     card.hidden = False
                 self.draw_table()
                 
                 # Finalize and set custom message
                 self.finalize_hand_results()
                 
                 # OVERRIDE the status text with the requested flashy one
                 self.lbl_status.config(text="♥ ♦ Blackjack 3:2 ♣ ♠", fg="#FFD700") 
                 return

            # SHOW PLAY CONTROLS
            # Insert them into the bottom_container
            self.play_frame.pack(after=self.lbl_status, pady=10, fill="x")

            self.start_button_flash(self.btn_hit, "#2196F3", "#64B5F6")
            self.start_button_flash(self.btn_stand, "#FFC107", "#FFD54F")
            
            self.lbl_status.config(text=f"Player has {self.game.player_hand.points}. Hit or Stand?", fg="white")
        
        except ValueError:
             messagebox.showerror("Invalid Bet", "Please enter a valid number for your bet.\n\nExample: 20", parent=self)
        except Exception as e:
            messagebox.showerror("Game Error", f"Failed to start hand: {e}", parent=self)
            self.end_hand()

    def update_info_labels(self):
        self.lbl_balance.config(text=f"Balance: ${self.player.balance:.2f}")
        
        # Stats Calculation
        total_games = self.player.wins + self.player.losses
        if total_games > 0:
            win_rate = (self.player.wins / total_games) * 100
        else:
            win_rate = 0.0
            
        self.lbl_win_rate.config(text=f"Win Rate: {win_rate:.1f}%")
        self.lbl_record.config(text=f"Wins: {self.player.wins} | Losses: {self.player.losses}")
        
        # Net Earnings (assuming 1000 start)
        net = self.player.balance - 1000.0
        sign = "+" if net >= 0 else "-"
        color = "#FFB74D" # Orange default
        if net > 0: color = "#81C784" # Green
        elif net < 0: color = "#E57373" # Red
            
        self.lbl_net_earnings.config(text=f"Total Net: {sign}${abs(net):.2f}", fg=color)
        
        # Sync Win Rate color with Net Earnings for visual consistency
        self.lbl_win_rate.config(fg=color)

    def player_hit(self):
        """Player takes another card (Synchronous - No Animation)."""
        if self.game.is_game_over:
            return
            
        # Add card logically
        new_card = self.game.deck.deal()
        self.game.player_hand.add_card(new_card)
        # self.game.player_hand.adjust_for_ace() # REMOVED: Managed by property
        
        # Update Visuals Immediately
        self.draw_table()
        self.update_info_labels()
        
        if self.game.player_hand.points > 21:
            self.lbl_status.config(text="BUST! You went over 21.")
            
            # Reveal dealer card visuals
            if self.game.dealer_hand.cards:
                for card in self.game.dealer_hand.cards:
                    card.hidden = False
            self.draw_table()
            
            try:
                self.db.update_player_balance(self.player, 0, loss=True)
            except Exception as e:
                print(f"Error saving loss: {e}") # Non-critical UI feedback
            self.update_info_labels()
            self.end_hand()
        else:
            self.lbl_status.config(text=f"Player has {self.game.player_hand.points}. Hit or Stand?")

    def player_stand(self):
        """Player stands, dealer plays (with simple delay)."""
        if self.game.is_game_over:
             return

        # Stop button flash immediately
        self.stop_button_flash(self.btn_hit, "#2196F3")
        self.stop_button_flash(self.btn_stand, "#FFC107")

        # Reveal dealer's hole card immediately
        if self.game.dealer_hand.cards:
             for card in self.game.dealer_hand.cards:
                  card.hidden = False
        self.draw_table()
        
        # Start delayed dealer drawing (1 second)
        self.after(1000, self.animate_dealer_draw)

    def animate_dealer_draw(self):
        """Dealer draws with simple delay (No slide, just pause)."""
        if self.game.dealer_hand.points < 17:
             # Add card
             new_card = self.game.deck.deal()
             self.game.dealer_hand.add_card(new_card)
             self.draw_table()
             
             # Simple Delay loop
             self.after(1000, self.animate_dealer_draw)
        else:
             # Dealer done, finalize
             self.finalize_hand_results()

    def finalize_hand_results(self):
        """Calculates results and ends the hand."""
        self.game.is_game_over = True
        
        result, multiplier = self.game.get_result()
        payout = self.current_bet * multiplier
        
        try:
            if multiplier > 0:
                self.db.update_player_balance(self.player, payout, win=(multiplier > 1))
            else:
                self.db.update_player_balance(self.player, 0, loss=True)
        except Exception as e:
             messagebox.showerror("Save Error", f"Failed to save game results: {e}")
        
        self.update_info_labels()
        
        if multiplier > 1:
            self.lbl_status.config(text=f"{result} You win ${payout:.2f}!")
        elif multiplier == 1:
            self.lbl_status.config(text=f"{result} Bet returned.")
        else:
            self.lbl_status.config(text=result)
        
        self.end_hand()

    def end_hand(self):
        """Reset controls for next hand."""
        self.play_frame.pack_forget()
        
        # Stop HIT/STAND buttons flash
        self.stop_button_flash(self.btn_hit, "#2196F3")
        self.stop_button_flash(self.btn_stand, "#FFC107")
        
        # UNLOCK BETTING CONTROLS
        self.bet_entry.config(state="normal")
        if MacButton and isinstance(self.btn_deal, MacButton):
            self.btn_deal.configure(bg="#9C27B0", fg="white")  # Restore Purple
        else:
            self.btn_deal.config(state="normal", bg="#9C27B0")
        
        # Restart DEAL button flashing
        self.start_button_flash(self.btn_deal, "#9C27B0", "#CE93D8")
            
        self.lbl_locked.config(text="") # Clear locked message
        self.current_bet = 0.0

    def draw_deck(self):
        """Draws a stack of cards representing the deck/shoe."""
        deck_x = self.canvas.winfo_width() - 150
        deck_y = 50
        
        # Draw a few offset rectangles to simulate depth
        for i in range(5):
            offset = i * 2
            self.canvas.create_rectangle(deck_x - offset, deck_y - offset, 
                                       deck_x + 100 - offset, deck_y + 140 - offset, 
                                       fill="#8B0000", outline="black", width=1)
            # Pattern
            self.canvas.create_line(deck_x - offset + 5, deck_y - offset + 5, deck_x + 100 - offset - 5, deck_y + 140 - offset - 5, fill="#a00000")
            
        # Top card of the deck (Face down)
        self.canvas.create_rectangle(deck_x, deck_y, deck_x + 100, deck_y + 140, fill="#8B0000", outline="black", width=2)
        self.canvas.create_text(deck_x + 50, deck_y + 70, text="DECK", font=("Arial", 12, "bold"), fill="#B22222")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def on_closing(self):
        """Safely close the application."""
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            if self.db:
                self.db.close()
            self.destroy()

if __name__ == "__main__":
    try:
        app = BlackjackApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"An unexpected error occurred:\n{e}")
        print(f"CRASH REPORT: {e}")
