import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import random
import io
import base64

class FakeMSPaint:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Epic Artist Simulator")
        self.root.geometry("900x700")
        
        # Drawing state
        self.current_tool = "brush"
        self.current_colour = "#000000"
        self.brush_size = 3
        self.last_x = None
        self.last_y = None
        
        # Create PIL image and GUI
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        self.setup_toolbar()
        self.setup_canvas()
        
        # Bind events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
    
    def setup_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#a3acb0", height=80)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        
        # Tools frame
        tools_frame = tk.Frame(toolbar, bg="#a3acb0")
        tools_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(tools_frame, text="Tools:", bg="#a3acb0", font=("Arial", 9)).pack(anchor=tk.W)
        
        tools_row = tk.Frame(tools_frame, bg="#a3acb0")
        tools_row.pack()
        
        # Tool buttons
        tk.Button(tools_row, text="Brush", command=lambda: self.set_tool("brush"), 
                 width=8, relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_row, text="Fill", command=lambda: self.set_tool("fill"), 
                 width=8, relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_row, text="Eraser", command=lambda: self.set_tool("eraser"), 
                 width=8, relief=tk.RAISED).pack(side=tk.LEFT, padx=2)
        
        # Brush sizes
        sizes_row = tk.Frame(tools_frame, bg="#a3acb0")
        sizes_row.pack(pady=5)
        
        tk.Label(sizes_row, text="Size:", bg="#a3acb0", font=("Arial", 8)).pack(side=tk.LEFT)
        tk.Button(sizes_row, text="S", command=lambda: self.set_brush_size(1), 
                 width=3, relief=tk.RAISED, font=("Arial", 8)).pack(side=tk.LEFT, padx=1)
        tk.Button(sizes_row, text="M", command=lambda: self.set_brush_size(5), 
                 width=3, relief=tk.RAISED, font=("Arial", 8)).pack(side=tk.LEFT, padx=1)
        tk.Button(sizes_row, text="L", command=lambda: self.set_brush_size(10), 
                 width=3, relief=tk.RAISED, font=("Arial", 8)).pack(side=tk.LEFT, padx=1)
        
        # Colours frame
        colours_frame = tk.Frame(toolbar, bg="#a3acb0")
        colours_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(colours_frame, text="colours:", bg="#a3acb0", font=("Arial", 9)).pack(anchor=tk.W)
        
        # Windows-style colour palette
        colours_grid = tk.Frame(colours_frame, bg="#a3acb0")
        colours_grid.pack()
        
        # Classic Windows colours
        colours = [
            ["#000000", "#808080", "#800000", "#808000", "#008000", "#008080", "#000080", "#800080"],
            ["#FFFFFF", "#C0C0C0", "#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
        ]
        
        for row_idx, colour_row in enumerate(colours):
            row_frame = tk.Frame(colours_grid, bg="#a3acb0")
            row_frame.pack()
            for colour in colour_row:
                btn = tk.Button(row_frame, bg=colour, width=3, height=1,
                              relief=tk.RAISED, bd=1,
                              command=lambda c=colour: self.set_colour(c))
                btn.pack(side=tk.LEFT, padx=1, pady=1)
        
        # File operations
        file_frame = tk.Frame(toolbar, bg="#a3acb0")
        file_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Button(file_frame, text="Clear", command=self.clear_canvas, 
                 width=8, relief=tk.RAISED).pack(pady=2)
        tk.Button(file_frame, text="Save", command=self.save_file, 
                 width=8, relief=tk.RAISED, bg="#e0e0ff").pack(pady=2)
        
        # Current tool/colour display
        status_frame = tk.Frame(toolbar, bg="#f0f0f0")
        status_frame.pack(side=tk.LEFT, padx=20)
        
        self.status_label = tk.Label(status_frame, text="Tool: Brush | Size: 3px", bg="#f0f0f0", font=("Arial", 9))
        self.status_label.pack()
        
        self.colour_display = tk.Frame(status_frame, bg=self.current_colour, width=30, height=20, relief=tk.SUNKEN, bd=2)
        self.colour_display.pack(pady=5)
    
    def setup_canvas(self):
        canvas_frame = tk.Frame(self.root, bg="#c0c0c0", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=800, height=600)
        self.canvas.pack(padx=5, pady=5)
    
    def set_tool(self, tool):
        self.current_tool = tool
        self.status_label.config(text=f"Tool: {tool.capitalize()} | Size: {self.brush_size}px")
    
    def set_brush_size(self, size):
        self.brush_size = size
        self.status_label.config(text=f"Tool: {self.current_tool.capitalize()} | Size: {size}px")
    
    def set_colour(self, colour):
        self.current_colour = colour
        self.colour_display.config(bg=colour)
    
    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y
        
        if self.current_tool == "fill":
            self.flood_fill(event.x, event.y)
    
    def draw_motion(self, event):
        if self.current_tool == "brush":
            if self.last_x and self.last_y:
                # Draw on canvas
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                      width=self.brush_size, fill=self.current_colour, 
                                      capstyle=tk.ROUND, smooth=tk.TRUE)
                # Draw on PIL img
                self.draw.line([(self.last_x, self.last_y), (event.x, event.y)], 
                             fill=self.current_colour, width=self.brush_size)
        
        elif self.current_tool == "eraser":
            if self.last_x and self.last_y:
                # Erase on canvas
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                      width=self.brush_size, fill="white", 
                                      capstyle=tk.ROUND, smooth=tk.TRUE)
                # Erase on PIL image
                self.draw.line([(self.last_x, self.last_y), (event.x, event.y)], 
                             fill="white", width=self.brush_size)
        
        self.last_x = event.x
        self.last_y = event.y
    
    def stop_draw(self, event):
        self.last_x = None
        self.last_y = None
    
    def flood_fill(self, x, y):
        # Get the colour at the clicked mouse position
        if x < 0 or x >= 800 or y < 0 or y >= 600:
            return
            
        # Get the target colour
        target_colour = self.image.getpixel((x, y))
        fill_colour = self.hex_to_rgb(self.current_colour)
        
        # Don't fill if clicking on the same colour
        if target_colour == fill_colour:
            return
        
        # Flood fill
        self.flood_fill_iterative(x, y, target_colour, fill_colour)
        
        # Update
        self.update_canvas_from_image()
    
    def hex_to_rgb(self, hex_colour):
        """Convert hex colour to RGB tuple"""
        hex_colour = hex_colour.lstrip('#')
        return tuple(int(hex_colour[i:i+2], 16) for i in (0, 2, 4))
    
    def flood_fill_iterative(self, start_x, start_y, target_colour, fill_colour):
        
        stack = [(start_x, start_y)]
        filled = set()  # Keep track of filled pixels to avoid infinite loops
        
        while stack:
            x, y = stack.pop()
            
            # Check bounds
            if x < 0 or x >= 800 or y < 0 or y >= 600:
                continue
            
            # Skip if already processed
            if (x, y) in filled:
                continue
                
            # Check if current pixel matches target colour
            try:
                current_colour = self.image.getpixel((x, y))
                if current_colour != target_colour:
                    continue
            except:
                continue
            
            # Fill the pixel
            self.image.putpixel((x, y), fill_colour)
            filled.add((x, y))
            
            # Add adjacent pixels to stack (4-directional)
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    
    def update_canvas_from_image(self):
        """Update the tkinter canvas to match the PIL image"""
        # Convert PIL image to PhotoImage for display
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
    
    def save_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filename:
            
            pee_image = self.create_random_pee()
            pee_image.save(filename)
            messagebox.showinfo("Save Complete", f"Image saved as {filename}")
    
    
    def create_random_pee(self):
        # x1 = 100, y1 = 195, x2 = 200, y2 = 280
        randomX = random.randint(150,185)
        randomX2 = random.randint(210,250)
        randLen = random.randint(50,110)

        # Create a new image for the pee
        pee_img = Image.new("RGB", (400, 300), "pink")
        pee_draw = ImageDraw.Draw(pee_img)
        
        # Add some colour
        colours = ["#FF6B6B", "#3D2721", "#748169", "#FA11F2", "#725643"]
        accent_colour = random.choice(colours)
        
        # Deeznuts
        pee_draw.ellipse([100, 195, 200, 280], fill=accent_colour)
        pee_draw.ellipse([200, 195, 300, 270], fill=accent_colour)

        # Get the shaft
        pee_draw.rectangle([randomX,195-randLen,randomX2,250], fill=accent_colour)

        # Bellend
        pee_draw.ellipse([randomX-12, 205-(randLen+35), 210, 205-randLen], fill="#F88484")
        pee_draw.ellipse([190, 205-(randLen+35), randomX2+12, 205-randLen], fill="#F88484")

        # Pissah
        pee_draw.line([200,205-(randLen+25),203,205-(randLen+10)],fill="black")
        
        # Add the text
        try:
            # Try to add text (might not work on all systems without PIL fonts)
            pee_draw.text((150, 50), "Oui oui, bonne peepee!!", fill="black")
        except:
            # If text fails, just add a simple heart
            pass
        
        return pee_img
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FakeMSPaint()
    app.run()