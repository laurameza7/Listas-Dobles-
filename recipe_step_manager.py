"""
Recipe Step Manager
===================
Case study for DOUBLY LINKED LISTS (listas dobles) using only Python.

Author: Laura Sofía Meza Reinoso
Course: Data Structures (Estructuras de Datos) - Universidad Cooperativa de Colombia

Real-life idea
--------------
A recipe is a sequence of steps. While cooking, you move to the NEXT step,
go back to the PREVIOUS step to check something, and sometimes you must
insert a forgotten step in the middle or remove one. That is exactly what a
doubly linked list does well.

    NULL <- [prev | RecipeStep | next] <-> [prev | RecipeStep | next] -> NULL
                  ^ head                          ^ tail

Classes
-------
1. RecipeStep      -> the NODE (data + two pointers: prev and next)
2. Recipe          -> the DOUBLY LINKED LIST (head, tail, length, current)
3. RecipeCanvas    -> draws the list (boxes and arrows) on the screen
4. RecipeStepApp   -> the main window (buttons, forms, log)

Run it with:  python recipe_step_manager.py
(Tkinter comes included with Python, no extra installation needed.)
"""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

# ---------------------------------------------------------------------------
# Colors and fonts (all in one place so they are easy to change)
# ---------------------------------------------------------------------------
BG = "#FFF7ED"
WHITE = "#FFFFFF"
DARK = "#292524"
MUTED = "#78716C"
PRIMARY = "#EA580C"
PRIMARY_DARK = "#C2410C"
PRIMARY_SOFT = "#FFEDD5"
TEAL = "#0D9488"
TEAL_SOFT = "#CCFBF1"
PURPLE = "#7C3AED"
PURPLE_SOFT = "#EDE9FE"
GREEN_SOFT = "#DCFCE7"
RED = "#DC2626"
RED_DARK = "#B91C1C"
BORDER = "#D6D3D1"

FONT = "Helvetica"


# ---------------------------------------------------------------------------
# 1. NODE
# ---------------------------------------------------------------------------
class RecipeStep:
    """One node of the list: it stores data and two pointers."""

    def __init__(self, step_id, title, description, minutes, needs_heat):
        # Data (several attributes)
        self.step_id = step_id
        self.title = title
        self.description = description
        self.minutes = minutes
        self.needs_heat = needs_heat

        # Pointers (references to other nodes)
        self.next = None  # points to the next step
        self.prev = None  # points to the previous step

    def heat_text(self):
        return "Yes" if self.needs_heat else "No"


# ---------------------------------------------------------------------------
# 2. DOUBLY LINKED LIST
# ---------------------------------------------------------------------------
class Recipe:
    """A doubly linked list of RecipeStep nodes, plus a pointer to the current step."""

    def __init__(self, name="Classic Pancakes"):
        self.name = name
        self.head = None      # first step
        self.tail = None      # last step
        self.current = None   # step the cook is doing right now
        self.length = 0

    def is_empty(self):
        return self.length == 0

    # ---- add to the end -------------------------------------------------
    def append(self, new_step):
        if self.head is None:                 # empty list
            self.head = new_step
            self.tail = new_step
            self.current = new_step           # cooking starts at the first step
        else:
            new_step.prev = self.tail         # new step looks back at old tail
            self.tail.next = new_step         # old tail looks forward at new step
            self.tail = new_step              # new step is the new tail
        self.length += 1

    # ---- add to the start -----------------------------------------------
    def prepend(self, new_step):
        if self.head is None:                 # empty list
            self.head = new_step
            self.tail = new_step
            self.current = new_step
        else:
            new_step.next = self.head         # new step looks forward at old head
            self.head.prev = new_step         # old head looks back at new step
            self.head = new_step              # new step is the new head
        self.length += 1

    # ---- go to a position -----------------------------------------------
    def traverse_to_index(self, index):
        """Return the node at 'index' (0-based).

        Because the list is double, we start from the closest end:
        from the head if the index is in the first half, otherwise from the tail.
        """
        if index < 0 or index >= self.length:
            raise IndexError("Position out of range")

        if index <= self.length // 2:
            current_node = self.head
            i = 0
            while i != index:
                current_node = current_node.next
                i += 1
        else:
            current_node = self.tail
            i = self.length - 1
            while i != index:
                current_node = current_node.prev
                i -= 1
        return current_node

    # ---- insert in any position -----------------------------------------
    def insert(self, index, new_step):
        if index <= 0:
            self.prepend(new_step)
        elif index >= self.length:
            self.append(new_step)
        else:
            leader = self.traverse_to_index(index - 1)   # step before
            follower = leader.next                       # step after
            leader.next = new_step
            new_step.prev = leader
            new_step.next = follower
            follower.prev = new_step
            self.length += 1

    # ---- remove from any position ---------------------------------------
    def remove(self, index):
        """Remove the step at 'index' and return it."""
        if index < 0 or index >= self.length:
            raise IndexError("Position out of range")

        node_to_remove = self.traverse_to_index(index)

        # If the cook is in the step that will disappear, move the pointer first
        if node_to_remove is self.current:
            if node_to_remove.next is not None:
                self.current = node_to_remove.next
            else:
                self.current = node_to_remove.prev

        if self.length == 1:                  # only one step
            self.head = None
            self.tail = None
        elif node_to_remove is self.head:     # first step
            self.head = node_to_remove.next
            self.head.prev = None
        elif node_to_remove is self.tail:     # last step
            self.tail = node_to_remove.prev
            self.tail.next = None
        else:                                 # step in the middle
            leader = node_to_remove.prev
            follower = node_to_remove.next
            leader.next = follower
            follower.prev = leader

        # Cut the removed node's pointers so it is fully disconnected
        node_to_remove.next = None
        node_to_remove.prev = None
        self.length -= 1
        return node_to_remove

    # ---- move the current step (uses next / prev pointers) --------------
    def move_forward(self):
        if self.current is not None and self.current.next is not None:
            self.current = self.current.next
            return True
        return False

    def move_backward(self):
        if self.current is not None and self.current.prev is not None:
            self.current = self.current.prev
            return True
        return False

    def move_to_start(self):
        self.current = self.head

    def move_to_end(self):
        self.current = self.tail

    # ---- helpers ----------------------------------------------------------
    def index_of(self, target):
        """Position (0-based) of a node, or -1 if it is not in the list."""
        node = self.head
        index = 0
        while node is not None:
            if node is target:
                return index
            node = node.next
            index += 1
        return -1

    def find_by_title(self, text):
        """Position (0-based) of the first step whose title contains 'text'."""
        text = text.strip().lower()
        node = self.head
        index = 0
        while node is not None:
            if text in node.title.lower():
                return index
            node = node.next
            index += 1
        return -1

    def total_minutes(self):
        total = 0
        node = self.head
        while node is not None:
            total += node.minutes
            node = node.next
        return total

    def titles_forward(self):
        """Titles from head to tail, following the 'next' pointers."""
        titles = []
        node = self.head
        while node is not None:
            titles.append(node.title)
            node = node.next
        return titles

    def titles_backward(self):
        """Titles from tail to head, following the 'prev' pointers."""
        titles = []
        node = self.tail
        while node is not None:
            titles.append(node.title)
            node = node.prev
        return titles


# ---------------------------------------------------------------------------
# 3. DRAWING OF THE LIST
# ---------------------------------------------------------------------------
def shorten(text, limit):
    """Cut long texts so they fit inside a box."""
    return text if len(text) <= limit else text[: limit - 1] + "…"


class RecipeCanvas(tk.Frame):
    """Draws every node as a box [prev | data | next] with arrows."""

    NODE_W = 176
    NODE_H = 128
    ROW_H = 28
    GAP = 78
    NULL_W = 54
    MARGIN = 24
    TOP = 120
    HEIGHT = 300

    def __init__(self, parent, on_select):
        super().__init__(parent, bg=WHITE)
        self.on_select = on_select  # function called when a node is clicked

        self.canvas = tk.Canvas(self, bg=WHITE, height=self.HEIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scrollbar.set)
        self.canvas.pack(fill="both", expand=True)
        scrollbar.pack(fill="x")

    # ---- main drawing function ------------------------------------------
    def redraw(self, recipe, selected_index):
        c = self.canvas
        c.delete("all")

        prev_row_y = self.TOP + self.ROW_H / 2
        next_row_y = self.TOP + self.NODE_H - self.ROW_H / 2
        first_x = self.MARGIN + self.NULL_W + self.GAP

        self._draw_legend()

        if recipe.head is None:
            c.create_text(
                330, self.TOP + 50,
                text="The recipe is empty.\nAdd your first step or load the sample recipe.",
                font=(FONT, 13), fill=MUTED, justify="center",
            )
            c.configure(scrollregion=(0, 0, 660, self.HEIGHT))
            return

        # NULL box on the left (head.prev is None)
        self._draw_null(self.MARGIN, prev_row_y)
        c.create_line(first_x, prev_row_y, self.MARGIN + self.NULL_W, prev_row_y,
                      arrow=tk.LAST, fill=PURPLE, width=2)

        # Walk the list with the next pointers and draw every node
        node = recipe.head
        index = 0
        while node is not None:
            x0 = first_x + index * (self.NODE_W + self.GAP)
            self._draw_node(node, index, x0, recipe, index == selected_index)

            x_right = x0 + self.NODE_W
            # forward arrow (next)
            c.create_line(x_right, next_row_y, x_right + self.GAP, next_row_y,
                          arrow=tk.LAST, fill=TEAL, width=2)
            if node.next is not None:
                # backward arrow (prev) of the next node
                c.create_line(x_right + self.GAP, prev_row_y, x_right, prev_row_y,
                              arrow=tk.LAST, fill=PURPLE, width=2)
            else:
                # last node: next points to NULL
                self._draw_null(x_right + self.GAP, next_row_y)
            node = node.next
            index += 1

        total_width = first_x + index * (self.NODE_W + self.GAP) + self.NULL_W + self.MARGIN
        c.configure(scrollregion=(0, 0, total_width, self.HEIGHT))
        self._scroll_to_current(recipe, total_width, first_x)

    # ---- one node ---------------------------------------------------------
    def _draw_node(self, node, index, x0, recipe, is_selected):
        c = self.canvas
        tag = f"node_{index}"
        top, w, h, row = self.TOP, self.NODE_W, self.NODE_H, self.ROW_H
        is_current = node is recipe.current

        prev_title = shorten(node.prev.title, 14) if node.prev else "NULL"
        next_title = shorten(node.next.title, 14) if node.next else "NULL"

        # soft shadow
        c.create_rectangle(x0 + 3, top + 3, x0 + w + 3, top + h + 3,
                           fill="#E7E5E4", outline="", tags=tag)
        # prev row (purple)
        c.create_rectangle(x0, top, x0 + w, top + row, fill=PURPLE_SOFT, outline="", tags=tag)
        c.create_text(x0 + 10, top + row / 2, anchor="w", text=f"prev → {prev_title}",
                      font=(FONT, 9, "bold"), fill=PURPLE, tags=tag)
        # data area (green when the cook is here, like the slide)
        data_fill = GREEN_SOFT if is_current else WHITE
        c.create_rectangle(x0, top + row, x0 + w, top + h - row, fill=data_fill, outline="", tags=tag)
        c.create_text(x0 + 10, top + row + 16, anchor="w", text=shorten(node.title, 20),
                      font=(FONT, 11, "bold"), fill=DARK, tags=tag)
        c.create_text(x0 + 10, top + row + 34, anchor="w", text=shorten(node.description, 26),
                      font=(FONT, 9), fill=MUTED, tags=tag)
        c.create_text(x0 + 10, top + row + 50, anchor="w",
                      text=f"Time: {node.minutes} min    Heat: {node.heat_text()}",
                      font=(FONT, 9), fill=DARK, tags=tag)
        # next row (teal)
        c.create_rectangle(x0, top + h - row, x0 + w, top + h, fill=TEAL_SOFT, outline="", tags=tag)
        c.create_text(x0 + 10, top + h - row / 2, anchor="w", text=f"next → {next_title}",
                      font=(FONT, 9, "bold"), fill=TEAL, tags=tag)
        # border (thicker and orange when selected)
        c.create_rectangle(x0, top, x0 + w, top + h, outline=PRIMARY if is_selected else BORDER,
                           width=3 if is_selected else 1, tags=tag)

        # position number above the node
        c.create_text(x0, top - 14, anchor="w", text=f"Step {index + 1}  ·  {node.step_id}",
                      font=(FONT, 9, "bold"), fill=MUTED, tags=tag)

        # "NOW" marker over the current step
        if is_current:
            cx = x0 + w / 2
            c.create_rectangle(cx - 34, top - 58, cx + 34, top - 32, fill=PRIMARY, outline="")
            c.create_text(cx, top - 45, text="NOW", font=(FONT, 10, "bold"), fill=WHITE)
            c.create_polygon(cx - 8, top - 32, cx + 8, top - 32, cx, top - 22,
                             fill=PRIMARY, outline="")

        # HEAD / TAIL badges
        badges = []
        if node is recipe.head:
            badges.append("HEAD")
        if node is recipe.tail:
            badges.append("TAIL")
        if badges:
            c.create_text(x0 + w / 2, top + h + 20, text=" / ".join(badges),
                          font=(FONT, 10, "bold"), fill=PRIMARY)

        # clicking any part of the node selects it
        c.tag_bind(tag, "<Button-1>", lambda event, i=index: self.on_select(i))
        c.tag_bind(tag, "<Enter>", lambda event: c.config(cursor="hand2"))
        c.tag_bind(tag, "<Leave>", lambda event: c.config(cursor=""))

    def _draw_null(self, x, y):
        c = self.canvas
        c.create_rectangle(x, y - 15, x + self.NULL_W, y + 15, fill="#FAFAF9", outline=MUTED, width=2)
        c.create_text(x + self.NULL_W / 2, y, text="NULL", font=(FONT, 9, "bold"), fill=MUTED)

    def _draw_legend(self):
        c = self.canvas
        y = self.HEIGHT - 28
        c.create_line(self.MARGIN, y, self.MARGIN + 36, y, arrow=tk.LAST, fill=TEAL, width=2)
        c.create_text(self.MARGIN + 44, y, anchor="w", text="next pointer", font=(FONT, 9), fill=MUTED)
        c.create_line(self.MARGIN + 140, y, self.MARGIN + 176, y, arrow=tk.LAST, fill=PURPLE, width=2)
        c.create_text(self.MARGIN + 184, y, anchor="w", text="prev pointer", font=(FONT, 9), fill=MUTED)
        c.create_text(self.MARGIN + 290, y, anchor="w",
                      text="Click a step to select it  ·  green box = current step",
                      font=(FONT, 9), fill=MUTED)

    def _scroll_to_current(self, recipe, total_width, first_x):
        """Keep the current step visible when the recipe is longer than the window."""
        current_index = recipe.index_of(recipe.current)
        if current_index < 0:
            return
        current_x = first_x + current_index * (self.NODE_W + self.GAP) + self.NODE_W / 2
        self.canvas.update_idletasks()  # make sure the real width is known
        view_width = max(self.canvas.winfo_width(), 1)
        fraction = (current_x - view_width / 2) / total_width
        self.canvas.xview_moveto(max(0.0, fraction))


# ---------------------------------------------------------------------------
# 4. MAIN WINDOW
# ---------------------------------------------------------------------------
class RecipeStepApp:
    def __init__(self, root):
        self.root = root
        self.recipe = Recipe()
        self.next_step_number = 1      # used to create ids like ST-001
        self.selected_index = None     # step selected by the user

        self._configure_window()
        self._configure_styles()
        self._build_header()
        self._build_body()
        self.load_sample_recipe()

    # ---- window and styles ------------------------------------------------
    def _configure_window(self):
        self.root.title("Recipe Step Manager - Doubly Linked List | Laura Sofía Meza Reinoso")
        self.root.geometry("1360x740")
        self.root.minsize(1120, 660)
        self.root.configure(bg=BG)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background=WHITE)
        style.configure("Card.TLabel", background=WHITE, foreground=DARK, font=(FONT, 10))
        style.configure("Muted.TLabel", background=WHITE, foreground=MUTED, font=(FONT, 9))
        style.configure("Title.TLabel", background=WHITE, foreground=DARK, font=(FONT, 13, "bold"))
        style.configure("Card.TCheckbutton", background=WHITE, foreground=DARK, font=(FONT, 10))

        for name, color, hover in [
            ("Primary", PRIMARY, PRIMARY_DARK),
            ("Danger", RED, RED_DARK),
            ("Teal", TEAL, "#0F766E"),
        ]:
            style.configure(f"{name}.TButton", background=color, foreground=WHITE,
                            font=(FONT, 10, "bold"), padding=(10, 8), borderwidth=0)
            style.map(f"{name}.TButton", background=[("active", hover)])

        style.configure("Soft.TButton", background=PRIMARY_SOFT, foreground=PRIMARY_DARK,
                        font=(FONT, 10, "bold"), padding=(10, 8), borderwidth=0)
        style.map("Soft.TButton", background=[("active", "#FED7AA")])

    # ---- header -------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=PRIMARY, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Recipe Step Manager", bg=PRIMARY, fg=WHITE,
                 font=(FONT, 20, "bold")).pack(side="left", padx=24)
        tk.Label(header, text="Doubly linked list case study  ·  by Laura Sofía Meza Reinoso",
                 bg=PRIMARY, fg="#FFEDD5", font=(FONT, 11)).pack(side="left")

        self.stats_label = tk.Label(header, text="", bg=PRIMARY, fg=WHITE, font=(FONT, 11, "bold"))
        self.stats_label.pack(side="right", padx=24)

    # ---- body -----------------------------------------------------------------
    def _build_body(self):
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=16)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_form_panel(body)
        self._build_center_panel(body)
        self._build_info_panel(body)

    def _card(self, parent, **grid_options):
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(**grid_options)
        return card

    # ---- left panel: form -------------------------------------------------------
    def _build_form_panel(self, body):
        card = self._card(body, row=0, column=0, sticky="ns", padx=(0, 12))
        ttk.Label(card, text="Step data", style="Title.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Label(card, text="Step title", style="Card.TLabel").pack(anchor="w")
        self.title_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.title_var, width=30).pack(fill="x", pady=(2, 8))

        ttk.Label(card, text="Instructions", style="Card.TLabel").pack(anchor="w")
        self.description_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.description_var, width=30).pack(fill="x", pady=(2, 8))

        ttk.Label(card, text="Minutes needed", style="Card.TLabel").pack(anchor="w")
        self.minutes_var = tk.StringVar(value="5")
        ttk.Spinbox(card, from_=0, to=600, textvariable=self.minutes_var, width=8).pack(anchor="w", pady=(2, 8))

        self.heat_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text="Needs heat (stove / oven)", variable=self.heat_var,
                        style="Card.TCheckbutton").pack(anchor="w", pady=(0, 10))

        add_row = ttk.Frame(card, style="Card.TFrame")
        add_row.pack(fill="x", pady=3)
        add_row.columnconfigure((0, 1), weight=1, uniform="add")
        ttk.Button(add_row, text="Add at START", style="Primary.TButton",
                   command=self.add_at_start).grid(row=0, column=0, sticky="ew", padx=(0, 3))
        ttk.Button(add_row, text="Add at END", style="Primary.TButton",
                   command=self.add_at_end).grid(row=0, column=1, sticky="ew", padx=(3, 0))

        ttk.Separator(card).pack(fill="x", pady=8)

        ttk.Label(card, text="Position (1 = first step)", style="Card.TLabel").pack(anchor="w")
        self.position_var = tk.StringVar(value="1")
        ttk.Spinbox(card, from_=1, to=500, textvariable=self.position_var, width=8).pack(anchor="w", pady=(2, 8))

        ttk.Button(card, text="Insert at position", style="Teal.TButton",
                   command=self.insert_at_position).pack(fill="x", pady=3)
        ttk.Button(card, text="Remove step at position", style="Danger.TButton",
                   command=self.remove_at_position).pack(fill="x", pady=3)

        ttk.Separator(card).pack(fill="x", pady=8)

        ttk.Label(card, text="Find a step by title", style="Card.TLabel").pack(anchor="w")
        search_row = ttk.Frame(card, style="Card.TFrame")
        search_row.pack(fill="x", pady=(2, 8))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_row, textvariable=self.search_var)
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda event: self.search_step())
        ttk.Button(search_row, text="Find", style="Soft.TButton", command=self.search_step).pack(side="left", padx=(6, 0))

        recipe_row = ttk.Frame(card, style="Card.TFrame")
        recipe_row.pack(fill="x", pady=3)
        recipe_row.columnconfigure((0, 1), weight=1, uniform="recipe")
        ttk.Button(recipe_row, text="Sample recipe", style="Soft.TButton",
                   command=self.load_sample_recipe).grid(row=0, column=0, sticky="ew", padx=(0, 3))
        ttk.Button(recipe_row, text="Clear recipe", style="Soft.TButton",
                   command=self.clear_recipe).grid(row=0, column=1, sticky="ew", padx=(3, 0))

    # ---- center panel: drawing and cooking controls ------------------------------------
    def _build_center_panel(self, body):
        center = tk.Frame(body, bg=BG)
        center.grid(row=0, column=1, sticky="nsew")
        center.rowconfigure(0, weight=1)
        center.columnconfigure(0, weight=1)

        draw_card = ttk.Frame(center, style="Card.TFrame", padding=16)
        draw_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        self.recipe_title = ttk.Label(draw_card, text="", style="Title.TLabel")
        self.recipe_title.pack(anchor="w", pady=(0, 8))
        self.recipe_canvas = RecipeCanvas(draw_card, on_select=self.select_step)
        self.recipe_canvas.pack(fill="both", expand=True)

        controls = ttk.Frame(center, style="Card.TFrame", padding=16)
        controls.grid(row=1, column=0, sticky="ew")
        ttk.Label(controls, text="Cooking controls", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.current_label = ttk.Label(controls, text="", style="Card.TLabel")
        self.current_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 10))

        buttons = [
            ("<  Previous step", self.go_backward, "Primary.TButton"),
            ("Next step  >", self.go_forward, "Primary.TButton"),
            ("List recipe forward", self.show_forward, "Teal.TButton"),
            ("|<  Go to first step", self.go_to_start, "Soft.TButton"),
            ("Go to last step  >|", self.go_to_end, "Soft.TButton"),
            ("List recipe backward", self.show_backward, "Teal.TButton"),
        ]
        for number, (text, command, style) in enumerate(buttons):
            row, column = 2 + number // 3, number % 3
            ttk.Button(controls, text=text, style=style, command=command).grid(
                row=row, column=column, padx=4, pady=3, sticky="ew")
        for column in range(3):
            controls.columnconfigure(column, weight=1, uniform="cook")

    # ---- right panel: details and log ---------------------------------------------------
    def _build_info_panel(self, body):
        card = self._card(body, row=0, column=2, sticky="ns", padx=(12, 0))
        card.configure(width=310)

        ttk.Label(card, text="Step details", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        self.details_label = ttk.Label(card, text="", style="Card.TLabel", justify="left", wraplength=280)
        self.details_label.pack(anchor="w", fill="x")

        ttk.Separator(card).pack(fill="x", pady=12)

        ttk.Label(card, text="Activity log", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        log_frame = tk.Frame(card, bg=WHITE)
        log_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_frame, width=36, height=18, wrap="word", bg="#FAFAF9", fg=DARK,
                                font=(FONT, 9), relief="flat", padx=8, pady=8, state="disabled")
        log_scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

    # =====================================================================
    # Helpers
    # =====================================================================
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def refresh(self):
        """Update everything that is shown on the screen."""
        self.recipe_canvas.redraw(self.recipe, self.selected_index)
        self.recipe_title.configure(text=f"Recipe: {self.recipe.name}")

        current_title = self.recipe.current.title if self.recipe.current else "-"
        self.stats_label.configure(
            text=f"Steps: {self.recipe.length}     Total time: {self.recipe.total_minutes()} min"
                 f"     Now: {current_title}")

        if self.recipe.current:
            position = self.recipe.index_of(self.recipe.current) + 1
            self.current_label.configure(
                text=f"You are at '{self.recipe.current.title}' (step {position} of {self.recipe.length}).")
        else:
            self.current_label.configure(text="The recipe is empty, so there is no current step.")

        self.update_details()

    def update_details(self):
        if self.selected_index is not None and self.selected_index < self.recipe.length:
            step = self.recipe.traverse_to_index(self.selected_index)
            title = "Selected step"
        else:
            step = self.recipe.current
            title = "Current step"

        if step is None:
            self.details_label.configure(text="No steps yet.")
            return

        prev_title = step.prev.title if step.prev else "NULL (this is the head)"
        next_title = step.next.title if step.next else "NULL (this is the tail)"
        self.details_label.configure(text=(
            f"{title}\n\n"
            f"ID: {step.step_id}\n"
            f"Title: {step.title}\n"
            f"Instructions: {step.description}\n"
            f"Minutes: {step.minutes}\n"
            f"Needs heat: {step.heat_text()}\n\n"
            f"prev points to: {prev_title}\n"
            f"next points to: {next_title}"
        ))

    def read_step_form(self):
        """Read and validate the form. Returns a new RecipeStep or None."""
        title = self.title_var.get().strip()
        description = self.description_var.get().strip()
        if not title:
            messagebox.showwarning("Missing data", "Please write the title of the step.")
            return None
        if not description:
            description = "No instructions"
        try:
            minutes = int(self.minutes_var.get())
            if minutes < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid number", "Minutes must be a whole number (0 or more).")
            return None

        step = RecipeStep(f"ST-{self.next_step_number:03d}", title, description,
                          minutes, self.heat_var.get())
        self.next_step_number += 1
        return step

    def read_position(self, maximum):
        """Read the position (1-based) and validate it. Returns an int or None."""
        try:
            position = int(self.position_var.get())
        except ValueError:
            messagebox.showwarning("Invalid position", "The position must be a whole number.")
            return None
        if position < 1 or position > maximum:
            messagebox.showwarning("Invalid position", f"The position must be between 1 and {maximum}.")
            return None
        return position

    def clear_form(self):
        self.title_var.set("")
        self.description_var.set("")
        self.minutes_var.set("5")

    # =====================================================================
    # Actions (buttons)
    # =====================================================================
    def add_at_start(self):
        step = self.read_step_form()
        if step is None:
            return
        self.recipe.prepend(step)
        self.selected_index = 0
        self.log(f"Added '{step.title}' at the START. The new step's next now points to the old head, "
                 f"and the old head's prev points back to the new step.")
        self.clear_form()
        self.refresh()

    def add_at_end(self):
        step = self.read_step_form()
        if step is None:
            return
        self.recipe.append(step)
        self.selected_index = self.recipe.length - 1
        self.log(f"Added '{step.title}' at the END. The new step's prev points to the old tail, "
                 f"and the old tail's next points to the new step.")
        self.clear_form()
        self.refresh()

    def insert_at_position(self):
        position = self.read_position(self.recipe.length + 1)
        if position is None:
            return
        step = self.read_step_form()
        if step is None:
            return
        self.recipe.insert(position - 1, step)
        self.selected_index = self.recipe.index_of(step)
        self.log(f"Inserted '{step.title}' at position {position}. Four pointers were updated: "
                 f"leader.next, new.prev, new.next and follower.prev.")
        self.clear_form()
        self.refresh()

    def remove_at_position(self):
        if self.recipe.is_empty():
            messagebox.showinfo("Empty recipe", "There are no steps to remove.")
            return
        position = self.read_position(self.recipe.length)
        if position is None:
            return
        step_title = self.recipe.traverse_to_index(position - 1).title
        if not messagebox.askyesno("Remove step", f"Remove '{step_title}' from the recipe?"):
            return
        removed = self.recipe.remove(position - 1)
        self.selected_index = None
        self.log(f"Removed '{removed.title}' (position {position}). Its neighbors now point to each other.")
        self.refresh()

    def search_step(self):
        text = self.search_var.get().strip()
        if not text:
            return
        index = self.recipe.find_by_title(text)
        if index == -1:
            self.log(f"No step found with the text '{text}'.")
            messagebox.showinfo("Not found", f"No step contains '{text}'.")
            return
        self.select_step(index)
        self.log(f"Found '{self.recipe.traverse_to_index(index).title}' at position {index + 1}.")

    def select_step(self, index):
        self.selected_index = index
        self.position_var.set(str(index + 1))
        self.refresh()

    # ---- cooking controls ---------------------------------------------------------
    def go_forward(self):
        if self.recipe.move_forward():
            self.log(f"Moved FORWARD (current = current.next) to '{self.recipe.current.title}'.")
        else:
            self.log("You are already at the last step (next is NULL).")
        self.refresh()

    def go_backward(self):
        if self.recipe.move_backward():
            self.log(f"Moved BACKWARD (current = current.prev) to '{self.recipe.current.title}'.")
        else:
            self.log("You are already at the first step (prev is NULL).")
        self.refresh()

    def go_to_start(self):
        self.recipe.move_to_start()
        self.log("Moved to the first step (head).")
        self.refresh()

    def go_to_end(self):
        self.recipe.move_to_end()
        self.log("Moved to the last step (tail).")
        self.refresh()

    def show_forward(self):
        titles = self.recipe.titles_forward()
        self.log("Forward (head → tail, using next):\n" + (" → ".join(titles) if titles else "empty recipe"))

    def show_backward(self):
        titles = self.recipe.titles_backward()
        self.log("Backward (tail → head, using prev):\n" + (" → ".join(titles) if titles else "empty recipe"))

    # ---- sample data ----------------------------------------------------------------
    def clear_recipe(self):
        if not self.recipe.is_empty():
            if not messagebox.askyesno("Clear recipe", "Remove ALL steps from the recipe?"):
                return
        self.recipe = Recipe()
        self.next_step_number = 1
        self.selected_index = None
        self.log("The recipe was cleared.")
        self.refresh()

    def load_sample_recipe(self):
        self.recipe = Recipe()
        self.next_step_number = 1
        self.selected_index = None
        sample = [
            ("Gather ingredients", "Flour, milk, eggs, sugar, butter", 5, False),
            ("Mix dry ingredients", "Combine flour, sugar and salt", 3, False),
            ("Add milk and eggs", "Whisk until smooth", 4, False),
            ("Rest the batter", "Let it rest in the bowl", 10, False),
            ("Heat the pan", "Medium heat with a little butter", 3, True),
            ("Cook each pancake", "About 2 minutes per side", 12, True),
            ("Serve and decorate", "Add fruit and honey", 4, False),
        ]
        for title, description, minutes, heat in sample:
            step = RecipeStep(f"ST-{self.next_step_number:03d}", title, description, minutes, heat)
            self.next_step_number += 1
            self.recipe.append(step)
        self.log("Sample recipe loaded with 7 steps. Try the buttons on the left and the cooking controls below!")
        self.refresh()


# ---------------------------------------------------------------------------
# Program entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    window = tk.Tk()
    app = RecipeStepApp(window)
    window.mainloop()
