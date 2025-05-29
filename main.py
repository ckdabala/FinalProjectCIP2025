import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# ==== Stadium Data ====
stadiums = {
    "Los Angeles": {
        "name": "SoFi Stadium",
        "location": "Inglewood, CA",
        "address": "1001 Stadium Dr, Inglewood, CA 90301",
        "capacity": 70000,
        "image": "sofi_stadium.jpg"
    },
    "Atlanta": {
        "name": "Mercedes-Benz Stadium",
        "location": "Atlanta, GA",
        "address": "1 AMB Dr NW, Atlanta, GA 30313",
        "capacity": 71000,
        "image": "mercedes_benz.jpg"
    },
    "Dallas": {
        "name": "AT&T Stadium",
        "location": "Arlington, TX",
        "address": "1 AT&T Way, Arlington, TX 76011",
        "capacity": 80000,
        "image": "att_stadium.jpg"
    },
    "New York": {
        "name": "MetLife Stadium",
        "location": "East Rutherford, NJ",
        "address": "1 MetLife Stadium Dr, East Rutherford, NJ 07073",
        "capacity": 82500,
        "image": "metlife.jpg"
    }
}

# ==== Match Data ====
matches = [
    {"date": "June 15, 2025", "time": "18:00", "club1": "Manchester City", "club2": "Al Ahly", "venue": "Los Angeles"},
    {"date": "June 16, 2025", "time": "20:00", "club1": "Fluminense", "club2": "Urawa Red Diamonds", "venue": "Atlanta"},
    {"date": "June 17, 2025", "time": "19:00", "club1": "FC Bayern Munich", "club2": "Wydad Casablanca", "venue": "Dallas"},
    {"date": "June 18, 2025", "time": "17:00", "club1": "Al Hilal", "club2": "Club América", "venue": "Miami"},
    {"date": "June 19, 2025", "time": "21:00", "club1": "Auckland City", "club2": "Seattle Sounders", "venue": "Houston"},
    {"date": "June 21, 2025", "time": "19:00", "club1": "Real Madrid", "club2": "Winner R1", "venue": "New York"},
    {"date": "June 22, 2025", "time": "21:00", "club1": "Chelsea", "club2": "Winner R2", "venue": "Seattle"},
    {"date": "June 23, 2025", "time": "20:00", "club1": "FC Bayern Munich", "club2": "Winner R3", "venue": "Orlando"},
    {"date": "June 25, 2025", "time": "20:00", "club1": "Semi-Final 1", "club2": "TBD", "venue": "San Francisco"},
    {"date": "June 26, 2025", "time": "20:00", "club1": "Semi-Final 2", "club2": "TBD", "venue": "Chicago"},
    {"date": "June 29, 2025", "time": "21:00", "club1": "Final", "club2": "TBD", "venue": "Los Angeles"},
]

# ==== GUI Application ====
def create_gui():
    root = tk.Tk()
    root.title("🌍 FIFA Club World Cup 2025")
    root.geometry("1200x650")
    root.configure(bg="#1e1e2f")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#2e2e3f", foreground="white", rowheight=25, fieldbackground="#2e2e3f")
    style.map('Treeview', background=[('selected', '#4caf50')])
    style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Arial", 14))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TCombobox", fieldbackground="white", background="white")

    title = ttk.Label(root, text="🏆 FIFA Club World Cup 2025 Schedule", font=("Arial", 20, "bold"))
    title.pack(pady=10)

    control_frame = ttk.Frame(root)
    control_frame.pack(pady=5)

    ttk.Label(control_frame, text="Select Club:").grid(row=0, column=0, padx=5)
    clubs = sorted(set(m["club1"] for m in matches) | set(m["club2"] for m in matches))
    club_var = tk.StringVar()
    club_dropdown = ttk.Combobox(control_frame, textvariable=club_var, values=clubs, state="readonly", width=30)
    club_dropdown.grid(row=0, column=1, padx=5)

    def populate_table(filtered=None):
        clear_table()
        for match in (filtered if filtered else matches):
            tree.insert("", tk.END, values=(match["date"], match["time"], match["club1"], match["club2"], match["venue"]))

    def clear_table():
        for item in tree.get_children():
            tree.delete(item)

    def show_all():
        populate_table()

    def filter_by_club():
        selected = club_var.get()
        if selected:
            filtered = [m for m in matches if selected in (m["club1"], m["club2"])]
            populate_table(filtered)

    ttk.Button(control_frame, text="Show All Matches", command=show_all).grid(row=0, column=2, padx=5)
    ttk.Button(control_frame, text="Filter Club Matches", command=filter_by_club).grid(row=0, column=3, padx=5)
    ttk.Button(control_frame, text="Clear", command=clear_table).grid(row=0, column=4, padx=5)

    # Layout: Left stadium panel and right match table
    content_frame = tk.Frame(root, bg="#1e1e2f")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # === Left: Stadium Panel ===
    stadium_panel = tk.Frame(content_frame, width=350, bg="#2e2e3f")
    stadium_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

    tk.Label(stadium_panel, text="🏟 Stadium Info", font=("Arial", 16, "bold"), bg="#2e2e3f", fg="white").pack(pady=10)

    listbox = tk.Listbox(stadium_panel, font=("Arial", 12), width=30, height=5)
    for city in stadiums:
        listbox.insert(tk.END, city)
    listbox.pack(pady=5)

    image_label = tk.Label(stadium_panel, bg="#2e2e3f")
    image_label.pack(pady=10)

    text_label = tk.Label(stadium_panel, text="", font=("Arial", 11), bg="#2e2e3f", fg="white", justify="left", wraplength=300)
    text_label.pack()

    def show_info(event):
        selection = listbox.get(listbox.curselection())
        stadium = stadiums[selection]

        try:
            img = Image.open(stadium["image"])
            img = img.resize((300, 180))
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo
        except:
            image_label.config(text="Image not found", image="", bg="#2e2e3f", fg="white")

        text_label.config(
            text=f"{stadium['name']}\n"
                 f"📍 Location: {stadium['location']}\n"
                 f"🏠 Address: {stadium['address']}\n"
                 f"👥 Capacity: {stadium['capacity']} people"
        )

    listbox.bind("<<ListboxSelect>>", show_info)

    # === Right: Match Table ===
    tree_frame = tk.Frame(content_frame, bg="#1e1e2f")
    tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    columns = ("date", "time", "club1", "club2", "venue")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor=tk.CENTER, width=140)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    populate_table()

    root.mainloop()

# Run app
if __name__ == "__main__":
    create_gui()
