import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional
import itertools
import math
import matplotlib.patches as mpatches

# 1) Station and metro network classes

class Station: #Represents a single station with an ID, name, line, coordinates, and a list of neighboring stations (with travel times).
    
    def __init__(self, idx: str, name: str, line: str, x: float = 0.0, y: float = 0.0):
        self.idx = idx
        self.name = name
        self.line = line
        self.x = x
        self.y = y
        self.neighbors: List[Tuple['Station', int]] = []  # (station, travel_time)

    def add_neighbor(self, station: 'Station', travel_time: int):# Adds a neighbor station along with travel time to get there.
        
        self.neighbors.append((station, travel_time))


class MetroNetwork:#Holds all stations and lines. Allows adding stations, connections, and searching for routes with different algorithms.

    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    def add_station(self, idx: str, name: str, line: str, x: float = 0.0, y: float = 0.0) -> None: #Creates and stores a new Station object if it doesn't already exist.
        
        if idx not in self.stations:
            station = Station(idx, name, line, x, y)
            self.stations[idx] = station
            self.lines[line].append(station)

    def add_connection(self, station1_id: str, station2_id: str, travel_time: int) -> None: #Creates a bidirectional connection between two stations with a given travel time.
    
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbor(station2, travel_time)
        station2.add_neighbor(station1, travel_time)

    def find_min_transfers_route(self, start_id: str, end_id: str) -> Optional[List[Station]]:
        #Uses a 0-1 BFS approach to find a route with the minimum number of line transfers.
        #Cost = 0 if the next station is on the same line, otherwise cost = 1.
        
        if start_id not in self.stations or end_id not in self.stations:
            return None

        start_station = self.stations[start_id]
        end_station = self.stations[end_id]

        dq = deque()
        dq.append((start_station, [start_station], 0))
        best = {(start_station.idx, start_station.line): 0}

        while dq:
            current, route, transfers = dq.popleft()
            if current.idx == end_station.idx:
                return route

            for neighbor, _ in current.neighbors:
                cost = 0 if neighbor.line == current.line else 1
                new_transfers = transfers + cost
                key = (neighbor.idx, neighbor.line)
                if key not in best or new_transfers < best[key]:
                    best[key] = new_transfers
                    if cost == 0:
                        dq.appendleft((neighbor, route + [neighbor], new_transfers))
                    else:
                        dq.append((neighbor, route + [neighbor], new_transfers))

        return None

    def find_fastest_route(self, start_id: str, end_id: str) -> Optional[Tuple[List[Station], int]]:
        #Uses an A* search to find the fastest route based on travel times.
        #An Euclidean distance heuristic is applied, using station coordinates.
        
        if start_id not in self.stations or end_id not in self.stations:
            return None

        start_station = self.stations[start_id]
        end_station = self.stations[end_id]

        def heuristic(current: Station, goal: Station) -> float:
            dx = current.x - goal.x
            dy = current.y - goal.y
            return math.sqrt(dx * dx + dy * dy)

        counter = itertools.count()
        initial_g = 0
        initial_f = initial_g + heuristic(start_station, end_station)
        pq = [(initial_f, next(counter), initial_g, start_station, [start_station])]
        best = {start_station.idx: 0}

        while pq:
            f, _, g, current, route = heapq.heappop(pq)
            if current.idx == end_station.idx:
                return route, g

            if g > best.get(current.idx, float('inf')):
                continue

            for neighbor, travel_time in current.neighbors:
                new_g = g + travel_time
                if new_g < best.get(neighbor.idx, float('inf')):
                    best[neighbor.idx] = new_g
                    new_f = new_g + heuristic(neighbor, end_station)
                    heapq.heappush(pq, (new_f, next(counter), new_g, neighbor, route + [neighbor]))

        return None


def collapse_route(route: List[Station]) -> List[str]: #Takes a list of Station objects and returns a list of station names,avoiding direct repetitions when station names are the same.
    if not route:
        return []
    collapsed = [route[0].name]
    for st in route[1:]:
        if st.name != collapsed[-1]:
            collapsed.append(st.name)
    return collapsed


# 2) Building the graph for visualization
def build_collapsed_graph(metro: MetroNetwork):
    
    #Combines stations that share the same name into a single node.
    #Preserves edge colors based on the line name.
    #Averages the (x, y) positions for stations that share the same name.
    
    line_colors = {
        "Kırmızı Hat": "red",
        "Mavi Hat": "blue",
        "Turuncu Hat": "orange",
        "Yeşil Hat": "green",
        "Sarı Hat": "yellow",
        "Mor Hat": "purple",
        "Lacivert Hat": "darkblue"
    }

    station_by_name = defaultdict(list)
    for st in metro.stations.values():
        station_by_name[st.name].append(st)

    G = nx.Graph()
    station_lines = {}
    pos_map = {}

    # Create nodes
    for name, st_list in station_by_name.items():
        all_lines = {st.line for st in st_list}
        station_lines[name] = all_lines
        G.add_node(name)
        # Compute average x,y to represent this station name
        avg_x = sum(st.x for st in st_list) / len(st_list)
        avg_y = sum(st.y for st in st_list) / len(st_list)
        pos_map[name] = (avg_x, avg_y)

    # Build edges
    edge_map = {}
    for name, st_list in station_by_name.items():
        for st in st_list:
            for neighbor, travel_time in st.neighbors:
                neighbor_name = neighbor.name
                if name == neighbor_name:
                    continue
                edge_key = tuple(sorted((name, neighbor_name)))
                same_line = st.line if st.line == neighbor.line else None

                if edge_key not in edge_map:
                    edge_map[edge_key] = (travel_time, set())
                    if same_line:
                        edge_map[edge_key][1].add(same_line)
                else:
                    old_time, old_lines = edge_map[edge_key]
                    new_time = min(old_time, travel_time)
                    new_line_set = set(old_lines)
                    if same_line:
                        new_line_set.add(same_line)
                    edge_map[edge_key] = (new_time, new_line_set)

    # Assign edges and colors
    for (a, b), (t, lines_set) in edge_map.items():
        if len(lines_set) == 1:
            single_line = list(lines_set)[0]
            edge_color = line_colors.get(single_line, "black")
        else:
            edge_color = "black"
        G.add_edge(a, b, weight=t, color=edge_color)

    return G, station_lines, pos_map


# 3) Tkinter GUI
class MetroSimulationGUI:
    """
    Tkinter-based GUI for visualizing and interacting with the MetroNetwork.
    Features:
      - Fastest Route (A*) and Minimum Transfers Route (0-1 BFS)
      - Axis-based Zoom In/Out + Reset Zoom
      - Dark/Light Mode Toggle
      - Route Animation
      - Save Graph as PNG
      - Toggle Legend
      - Toggle Edge Labels
      - Station Search + Highlight
      - Click on station for info
      - Toggle node size scaling by line count
    """
    def __init__(self, metro: MetroNetwork):
        self.metro = metro
        self.collapsed_graph, self.station_lines, self.pos_map = build_collapsed_graph(metro)

        self.last_route: Optional[List[str]] = None
        self.current_edge_index = 0

        # Dark mode and legend flags
        self.dark_mode = False
        self.show_legend = True
        # Show/hide edge labels
        self.show_edge_labels = True
        # Station highlight name
        self.highlight_station: Optional[str] = None
        # Enable/disable node info on click
        self.node_info_enabled = False
        # Scale node size by line count
        self.scale_nodes_by_line_count = False

        # Main window
        self.window = tk.Tk()
        self.window.title("Driverless Metro Simulation (Coordinate-Based)")
        self.window.geometry("1200x800")

        # Apply custom styles
        self.apply_styles()

        # Create a menu bar
        self.create_menubar()

        # Title label
        self.title_label = ttk.Label(
            self.window,
            text="Driverless Metro Simulation",
            style="TitleLabel.TLabel"
        )
        self.title_label.pack(side=tk.TOP, pady=10)

        # Top frame for controls
        self.frame_controls = ttk.Frame(self.window)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.create_main_controls()

        # Frame for extra buttons (zoom, animation, etc.)
        self.frame_extra = ttk.Frame(self.window)
        self.frame_extra.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.create_extra_controls()

        # Frame for new features (search, node click info, etc.)
        self.frame_new = ttk.Frame(self.window)
        self.frame_new.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.create_new_features_controls()

        # Frame to show route results or messages
        self.frame_result = ttk.Frame(self.window)
        self.frame_result.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))
        self.result_label = ttk.Label(self.frame_result, text="", style="ResultLabel.TLabel")
        self.result_label.pack(side=tk.LEFT, anchor="w", padx=5)

        # Create a matplotlib Figure
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Initial backgrounds
        self.figure.patch.set_facecolor("#F0F0F0")
        self.ax.set_facecolor("#FFFFFF")

        # Create a canvas to embed the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Draw once, then store initial axis limits for "Reset Zoom"
        self.draw_graph()
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        # Connect click event for station info
        self.cid_click = self.canvas.mpl_connect("button_press_event", self.on_click_station)

        # Start the Tk main loop
        self.window.mainloop()

    def apply_styles(self): #Configure ttk styles for a more modern look.
        
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 10))
        style.configure("TButton", background="#007ACC", foreground="#ffffff", font=("Arial", 9, "bold"))
        style.configure("TCombobox", padding=5, font=("Arial", 9))

        style.configure("TitleLabel.TLabel", font=("Arial", 16, "bold"), foreground="#2c3e50")
        style.configure("ResultLabel.TLabel", font=("Arial", 10, "italic"), foreground="#b33f62")

    def create_menubar(self): #Creates a basic menubar with a File menu.
        
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=file_menu)

    def create_main_controls(self): #Main controls for choosing start/end stations and route type.
        
        ttk.Label(self.frame_controls, text="Start:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(
            self.frame_controls,
            textvariable=self.start_var,
            values=self.get_station_names()
        )
        self.start_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_controls, text="End:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(
            self.frame_controls,
            textvariable=self.end_var,
            values=self.get_station_names()
        )
        self.end_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.frame_controls, text="Route Type:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.route_type_var = tk.StringVar()
        self.route_type_combo = ttk.Combobox(
            self.frame_controls,
            textvariable=self.route_type_var,
            values=["Fastest Route", "Minimum Transfers Route"]
        )
        self.route_type_combo.grid(row=0, column=5, padx=5, pady=5)
        self.route_type_combo.current(0)

        self.calc_button = ttk.Button(
            self.frame_controls,
            text="Calculate Route",
            command=self.calculate_route
        )
        self.calc_button.grid(row=0, column=6, padx=5, pady=5)

    def create_extra_controls(self): #Additional buttons for zoom, animation, etc.
    
        self.zoom_in_button = ttk.Button(self.frame_extra, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = ttk.Button(self.frame_extra, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.reset_zoom_button = ttk.Button(self.frame_extra, text="Reset Zoom", command=self.reset_zoom)
        self.reset_zoom_button.pack(side=tk.LEFT, padx=5)

        self.animate_button = ttk.Button(self.frame_extra, text="Animate Route", command=self.animate_route)
        self.animate_button.pack(side=tk.LEFT, padx=5)

        self.dark_mode_button = ttk.Button(self.frame_extra, text="Dark/Light Mode", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(side=tk.LEFT, padx=5)

        self.toggle_legend_button = ttk.Button(self.frame_extra, text="Toggle Legend", command=self.toggle_legend)
        self.toggle_legend_button.pack(side=tk.LEFT, padx=5)

        self.save_png_button = ttk.Button(self.frame_extra, text="Save Graph", command=self.save_graph_as_png)
        self.save_png_button.pack(side=tk.LEFT, padx=5)

    def create_new_features_controls(self): #New feature controls: edge labels toggle, station search, node info toggle, node scaling toggle

        self.toggle_edge_labels_button = ttk.Button(
            self.frame_new,
            text="Toggle Edge Labels",
            command=self.toggle_edge_labels
        )
        self.toggle_edge_labels_button.pack(side=tk.LEFT, padx=5)

        # Station search
        ttk.Label(self.frame_new, text="Search Station:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame_new, textvariable=self.search_var, width=12)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = ttk.Button(
            self.frame_new,
            text="Highlight",
            command=self.search_station
        )
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Enable/disable station info on click
        self.info_toggle_button = ttk.Button(
            self.frame_new,
            text="Enable Node Info",
            command=self.toggle_node_info
        )
        self.info_toggle_button.pack(side=tk.LEFT, padx=10)

        # Scale node size
        self.scale_node_button = ttk.Button(
            self.frame_new,
            text="Scale Nodes by Line Count",
            command=self.toggle_node_scaling
        )
        self.scale_node_button.pack(side=tk.LEFT, padx=10)

    def get_station_names(self): # Returns the sorted list of collapsed station names in the graph.

        return sorted(list(self.collapsed_graph.nodes))

    def draw_graph(self, highlight_route: Optional[List[str]] = None):
        
        #Draws the network graph using matplotlib and networkx.
        #If highlight_route is provided, those edges are highlighted.
        
        self.ax.clear()

        # Handle dark or light mode
        if self.dark_mode:
            self.figure.patch.set_facecolor("#333333")
            self.ax.set_facecolor("#333333")
            label_font_color = "#FFFFFF"
            label_box_color = "#222222"
            single_node_color = "#555555"
            multi_node_color = "#777777"
            edge_node_color = "#FFFFFF"
        else:
            self.figure.patch.set_facecolor("#F0F0F0")
            self.ax.set_facecolor("#FFFFFF")
            label_font_color = "#000000"
            label_box_color = "#FFFFFF"
            single_node_color = "#FFFFFF"
            multi_node_color = "#D3D3D3"
            edge_node_color = "#000000"

        # Retrieve edge colors
        edge_colors = [self.collapsed_graph[u][v]["color"] for u, v in self.collapsed_graph.edges]

        # Identify multi-line vs single-line stations
        multi_line_stations = [n for n in self.collapsed_graph.nodes if len(self.station_lines[n]) > 1]
        single_line_stations = [n for n in self.collapsed_graph.nodes if len(self.station_lines[n]) == 1]

        # Node size logic
        if self.scale_nodes_by_line_count:
            # The more lines a station has, the bigger the node
            # Let's say base size is 600, plus 200 for each line beyond the first
            node_sizes = {}
            for n in self.collapsed_graph.nodes:
                line_count = len(self.station_lines[n])
                node_sizes[n] = 600 + 200*(line_count - 1 if line_count>1 else 0)
        else:
            # All single-line = 600, multi-line = 700
            node_sizes = {}
            for n in single_line_stations:
                node_sizes[n] = 600
            for n in multi_line_stations:
                node_sizes[n] = 700

        # If a station is "searched for," highlight it
        # We'll store a separate dictionary for node colors
        node_colors_map = {}
        for n in self.collapsed_graph.nodes:
            node_colors_map[n] = single_node_color

        for n in multi_line_stations:
            node_colors_map[n] = multi_node_color

        if self.highlight_station and self.highlight_station in self.collapsed_graph.nodes:
            # Let's highlight it in green
            node_colors_map[self.highlight_station] = "#008000"

        # Convert node_colors_map to a list in the same order as .nodes
        node_colors = [node_colors_map[n] for n in self.collapsed_graph.nodes]

        # Convert node_sizes to a list in the same order
        node_sizes_list = [node_sizes[n] for n in self.collapsed_graph.nodes]

        # Draw nodes
        nx.draw_networkx_nodes(
            self.collapsed_graph,
            self.pos_map,
            node_color=node_colors,
            node_shape="o",
            edgecolors=edge_node_color,
            linewidths=1.2,
            node_size=node_sizes_list,
            ax=self.ax
        )

        # Draw edges
        nx.draw_networkx_edges(
            self.collapsed_graph,
            self.pos_map,
            width=2,
            alpha=0.8,
            connectionstyle='arc3,rad=0.1',
            edge_color=edge_colors,
            ax=self.ax
        )

        # Edge labels (travel times)
        if self.show_edge_labels:
            edge_labels = nx.get_edge_attributes(self.collapsed_graph, "weight")
            nx.draw_networkx_edge_labels(
                self.collapsed_graph,
                self.pos_map,
                edge_labels=edge_labels,
                label_pos=0.5,
                font_color=label_font_color,
                font_size=8,
                bbox=dict(boxstyle='round,pad=0.3', fc=label_box_color, ec='none', alpha=0.7),
                ax=self.ax
            )

        # Station (node) labels
        nx.draw_networkx_labels(
            self.collapsed_graph,
            self.pos_map,
            font_size=9,
            font_color=label_font_color,
            ax=self.ax
        )

        # Highlight route if given
        if highlight_route and len(highlight_route) > 1:
            route_edges = [(highlight_route[i], highlight_route[i+1]) for i in range(len(highlight_route) - 1)]
            nx.draw_networkx_edges(
                self.collapsed_graph,
                self.pos_map,
                edgelist=route_edges,
                edge_color="#FF00FF",
                width=4,
                connectionstyle='arc3,rad=0.2',
                ax=self.ax
            )

        # Optionally show legend
        if self.show_legend:
            line_colors = {
                "Kırmızı Hat": "#FF0000",
                "Mavi Hat": "#0000FF",
                "Turuncu Hat": "#FFA500",
                "Yeşil Hat": "#008000",
                "Sarı Hat": "#FFFF00",
                "Mor Hat": "#800080",
                "Lacivert Hat": "#00008B"
            }
            line_patches = [
                mpatches.Patch(color=color, label=line)
                for line, color in line_colors.items()
            ]
            if self.ax.legend_:
                self.ax.legend_.remove()
            self.ax.legend(handles=line_patches, loc="upper left", fontsize=8)

        self.canvas.draw()

    def calculate_route(self):

        #Reads user input for start, end, and route type.
        #Calculates and highlights the route, displaying the result.
        
        start_name = self.start_var.get()
        end_name = self.end_var.get()
        route_type = self.route_type_var.get()

        if not start_name or not end_name:
            self.result_label.config(text="Please select valid start/end stations!")
            return

        # Find the first matching station objects from the MetroNetwork
        start_candidates = [st for st in self.metro.stations.values() if st.name == start_name]
        end_candidates = [st for st in self.metro.stations.values() if st.name == end_name]
        if not start_candidates or not end_candidates:
            self.result_label.config(text="Selected stations are invalid!")
            return

        start_station = start_candidates[0]
        end_station = end_candidates[0]

        if route_type == "Fastest Route":
            result = self.metro.find_fastest_route(start_station.idx, end_station.idx)
            if result:
                route, total_time = result
                collapsed = collapse_route(route)
                self.last_route = collapsed
                self.result_label.config(
                    text=f"Fastest Route: {' -> '.join(collapsed)} ({total_time} min)"
                )
                self.draw_graph(highlight_route=collapsed)
            else:
                self.result_label.config(text="No route found!")
                self.last_route = None
                self.draw_graph()
        else:
            # Minimum Transfers Route
            route = self.metro.find_min_transfers_route(start_station.idx, end_station.idx)
            if route:
                collapsed = collapse_route(route)
                self.last_route = collapsed
                self.result_label.config(
                    text=f"Minimum Transfers Route: {' -> '.join(collapsed)}"
                )
                self.draw_graph(highlight_route=collapsed)
            else:
                self.result_label.config(text="No route found!")
                self.last_route = None
                self.draw_graph()

    def zoom_in(self): #Zoom in by reducing the current axis range (like moving a camera closer).
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Zoom factor < 1 => zoom in
        factor = 0.8

        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        width = (xlim[1] - xlim[0]) * factor
        height = (ylim[1] - ylim[0]) * factor

        self.ax.set_xlim(x_center - width/2, x_center + width/2)
        self.ax.set_ylim(y_center - height/2, y_center + height/2)
        self.canvas.draw()

    def zoom_out(self):#Zoom out by increasing the current axis range (like moving a camera away).
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Zoom factor > 1 => zoom out
        factor = 1.2

        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        width = (xlim[1] - xlim[0]) * factor
        height = (ylim[1] - ylim[0]) * factor

        self.ax.set_xlim(x_center - width/2, x_center + width/2)
        self.ax.set_ylim(y_center - height/2, y_center + height/2)
        self.canvas.draw()

    def reset_zoom(self): #Resets the axis limits to the initial state after the first draw.
        
        self.ax.set_xlim(self.initial_xlim)
        self.ax.set_ylim(self.initial_ylim)
        self.canvas.draw()

    def animate_route(self):
        
        #Starts a simple animation of the last calculated route.
        #Highlights edges one by one in a timed sequence.
        
        if not self.last_route or len(self.last_route) < 2:
            self.result_label.config(text="No valid route to animate!")
            return

        self.current_edge_index = 0
        self._animate_next_edge()

    def _animate_next_edge(self): #Recursive helper function for step-by-step animation using Tkinter's after().
        
        if self.current_edge_index >= len(self.last_route) - 1:
            return

        # Highlight edges up to current index
        partial_route = self.last_route[: self.current_edge_index + 2]
        self.draw_graph(highlight_route=partial_route)
        self.current_edge_index += 1

        # Schedule the next edge highlight
        self.window.after(600, self._animate_next_edge)

    def toggle_dark_mode(self): #Toggles dark mode on/off and redraws the graph.
        
        self.dark_mode = not self.dark_mode
        self.draw_graph(self.last_route)

    def toggle_legend(self): #Toggles the display of the line color legend.
        
        self.show_legend = not self.show_legend
        self.draw_graph(self.last_route)

    def save_graph_as_png(self): #Saves the current figure as a PNG file.
        
        self.figure.savefig("metro_graph.png")
        self.result_label.config(text="Graph saved as 'metro_graph.png'")

    def toggle_edge_labels(self):#Shows or hides the travel-time labels on edges.
        
        self.show_edge_labels = not self.show_edge_labels
        self.draw_graph(self.last_route)

    def search_station(self): #Highlights the station typed in the search box (if it exists).
        
        station_name = self.search_var.get().strip()
        if station_name in self.collapsed_graph.nodes:
            self.highlight_station = station_name
            self.result_label.config(text=f"Station '{station_name}' is highlighted in green.")
        else:
            self.highlight_station = None
            self.result_label.config(text=f"Station '{station_name}' not found!")
        self.draw_graph(self.last_route)

    def toggle_node_info(self): #Toggles whether clicking on a station displays info.
        
        self.node_info_enabled = not self.node_info_enabled
        if self.node_info_enabled:
            self.info_toggle_button.config(text="Disable Node Info")
            self.result_label.config(text="Click near a station to see details.")
        else:
            self.info_toggle_button.config(text="Enable Node Info")
            self.result_label.config(text="Node info on click is disabled.")

    def toggle_node_scaling(self): #Toggles whether node sizes are scaled by the number of lines.
        
        self.scale_nodes_by_line_count = not self.scale_nodes_by_line_count
        self.draw_graph(self.last_route)

    def on_click_station(self, event): #If node info is enabled, checks if the click is near a station and displays station info in the result label.
        if not self.node_info_enabled:
            return

        # Convert mouse click to data coords
        if event.inaxes != self.ax:
            return

        click_x, click_y = event.xdata, event.ydata
        if click_x is None or click_y is None:
            return

        # Doing a small radius check (e.g., 1-2 units) around each station position
        radius = 1.5
        found_station = None
        for station_name, (sx, sy) in self.pos_map.items():
            dist = math.hypot(sx - click_x, sy - click_y)
            if dist < radius:
                found_station = station_name
                break

        if found_station:
            # Show info about this station
            lines = self.station_lines[found_station]
            lines_str = ", ".join(sorted(lines))
            # If we want neighbor info, we can gather from the original BFS data:
            # in collapsed_graph, the neighbors are also collapsed by name.
            neighbors = list(self.collapsed_graph[found_station].keys())
            info = f"Station: {found_station}\nLines: {lines_str}\nNeighbors: {', '.join(neighbors)}"
            self.result_label.config(text=info)

# 4) Data examples and running the code

if __name__ == "__main__":
    metro = MetroNetwork()

    # Example stations
    # -- Kırmızı Hat (Red Line) --
    metro.add_station("K1", "Kızılay",    "Kırmızı Hat", x=50, y=100)
    metro.add_station("K2", "Ulus",       "Kırmızı Hat", x=60, y=120)
    metro.add_station("K3", "Demetevler", "Kırmızı Hat", x=70, y=140)
    metro.add_station("K4", "OSB",        "Kırmızı Hat", x=80, y=160)
    metro.add_station("K5", "Sincan",     "Kırmızı Hat", x=90, y=180)
    metro.add_connection("K1", "K2", 4)
    metro.add_connection("K2", "K3", 6)
    metro.add_connection("K3", "K4", 8)
    metro.add_connection("K4", "K5", 9)

    # -- Mavi Hat (Blue Line) --
    metro.add_station("M1", "AŞTİ",    "Mavi Hat", x=30, y=90)
    metro.add_station("M2", "Kızılay", "Mavi Hat", x=50, y=100)
    metro.add_station("M3", "Sıhhiye", "Mavi Hat", x=50, y=110)
    metro.add_station("M4", "Gar",     "Mavi Hat", x=60, y=130)
    metro.add_station("M5", "Kurtuluş","Mavi Hat", x=70, y=150)
    metro.add_connection("M1", "M2", 5)
    metro.add_connection("M2", "M3", 3)
    metro.add_connection("M3", "M4", 4)
    metro.add_connection("M4", "M5", 5)

    # -- Turuncu Hat (Orange Line) --
    metro.add_station("T1", "Batıkent",   "Turuncu Hat", x=75, y=130)
    metro.add_station("T2", "Demetevler", "Turuncu Hat", x=70, y=140)
    metro.add_station("T3", "Gar",        "Turuncu Hat", x=60, y=130)
    metro.add_station("T4", "Keçiören",   "Turuncu Hat", x=65, y=160)
    metro.add_station("T5", "Gazino",     "Turuncu Hat", x=70, y=180)
    metro.add_connection("T1", "T2", 7)
    metro.add_connection("T2", "T3", 9)
    metro.add_connection("T3", "T4", 5)
    metro.add_connection("T4", "T5", 6)

    # -- Yeşil Hat (Green Line) --
    metro.add_station("Y1", "Bostancı",   "Yeşil Hat", x=10, y=100)
    metro.add_station("Y2", "Moda",       "Yeşil Hat", x=20, y=110)
    metro.add_station("Y3", "Kadıköy",    "Yeşil Hat", x=25, y=120)
    metro.add_station("Y4", "Kozyatağı",  "Yeşil Hat", x=30, y=130)
    metro.add_station("Y5", "Göztepe",    "Yeşil Hat", x=40, y=135)
    metro.add_connection("Y1", "Y2", 6)
    metro.add_connection("Y2", "Y3", 5)
    metro.add_connection("Y3", "Y4", 7)
    metro.add_connection("Y4", "Y5", 4)

    # -- Sarı Hat (Yellow Line) --
    metro.add_station("S1", "Sultanahmet", "Sarı Hat", x=20, y=40)
    metro.add_station("S2", "Eminönü",     "Sarı Hat", x=25, y=50)
    metro.add_station("S3", "Beyazit",     "Sarı Hat", x=25, y=60)
    metro.add_station("S4", "Laleli",      "Sarı Hat", x=25, y=70)
    metro.add_connection("S1", "S2", 3)
    metro.add_connection("S2", "S3", 4)
    metro.add_connection("S3", "S4", 2)

    # -- Mor Hat (Purple Line) --
    metro.add_station("P1", "Dikmen",    "Mor Hat", x=45, y=30)
    metro.add_station("P2", "Öveçler",   "Mor Hat", x=50, y=40)
    metro.add_station("P3", "Konutkent", "Mor Hat", x=60, y=50)
    metro.add_station("P4", "Oran",      "Mor Hat", x=70, y=40)
    metro.add_connection("P1", "P2", 5)
    metro.add_connection("P2", "P3", 7)
    metro.add_connection("P3", "P4", 6)

    # -- Lacivert Hat (Dark Blue Line) --
    metro.add_station("L1", "Bahçelievler", "Lacivert Hat", x=25, y=140)
    metro.add_station("L2", "Emek",         "Lacivert Hat", x=30, y=145)
    metro.add_station("L3", "Bilkent",      "Lacivert Hat", x=35, y=150)
    metro.add_station("L4", "Çayyolu",      "Lacivert Hat", x=40, y=155)
    metro.add_connection("L1", "L2", 3)
    metro.add_connection("L2", "L3", 5)
    metro.add_connection("L3", "L4", 4)

    # -- Inter-line Transfers --
    metro.add_connection("K1", "M2", 2)   # Kızılay (K1) - Kızılay (M2)
    metro.add_connection("K3", "T2", 3)   # Demetevler (K3) - Demetevler (T2)
    metro.add_connection("M4", "T3", 2)   # Gar (M4) - Gar (T3)
    metro.add_connection("Y2", "M2", 4)   # Moda (Y2) - Kızılay (M2)
    metro.add_connection("S2", "K3", 2)   # Eminönü (S2) - Demetevler (K3)
    metro.add_connection("Y3", "S1", 3)   # Kadıköy (Y3) - Sultanahmet (S1)
    metro.add_connection("L1", "M1", 2)   # Bahçelievler (L1) - AŞTİ (M1)
    metro.add_connection("L3", "P3", 5)   # Bilkent (L3) - Konutkent (P3)
    metro.add_connection("Y4", "P4", 6)   # Kozyatağı (Y4) - Oran (P4)
    metro.add_connection("T5", "K5", 10)  # Gazino (T5) - Sincan (K5)

    # Launch the GUI
    MetroSimulationGUI(metro) 
