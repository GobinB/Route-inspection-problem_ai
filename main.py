import tkinter as tk
from tkinter import filedialog
# from solverccp import main_genetic_algorithm
from visual import  draw_graph
from test3 import main_genetic_algorithm
from test2 import Graph

def run_application():
    root = tk.Tk()
    root.title("Genetic Algorithm for Chinese Postman Problem")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=1)

    filename = filedialog.askopenfilename(title="Select a .txt file for CPP", filetypes=[("Text files", "*.txt")])
    
    if filename:
       # best_circuit, best_fitness = main_genetic_algorithm(filename)
        #plot_data(best_circuit, best_fitness, frame)
        draw_graph(filename)

    root.mainloop()

if __name__ == "__main__":
    run_application()
