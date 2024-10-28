import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt

def mostrar_calculadora():
    root.deiconify() # Muestra la ventana de la calculadora de flujo máximo

def mostrar_creditos():
    creditos = tk.Toplevel(menu_principal)
    creditos.title("Créditos")
    creditos.geometry("400x300")
    label_creditos = tk.Label(creditos, text="Calculadora de Flujo Máximo\nIntegrantes: \nContreras Quijua, Jhohandri Jhunior-U2021D925\nDiaz Quispe, Matias Sebastian-U202311938\nChipana Huarancca, Emanuel-U202214074\nElescano Leon, Piero Hugo-U202313354\nNieto Sivincha, Lina Mariseli-U202323427", font=("Helvetica", 12))
    label_creditos.pack(pady=20)
    button_volver = tk.Button(creditos, text="Volver", command=creditos.destroy)
    button_volver.pack(pady=10)

def salir():
    menu_principal.destroy()

def generar_matriz_aleatoria():
    try:
        n = int(entry.get())
        nueva_matriz = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i != j:
                    valor = random.randint(0, 9)
                    nueva_matriz[i][j] = valor
                    nueva_matriz[j][i] = valor
        matriz_str = '\n'.join([' '.join(map(str, fila)) for fila in nueva_matriz])
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, matriz_str)
        global matriz
        matriz = nueva_matriz
        return matriz
    except ValueError:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Por favor, ingrese un número válido.")
        return None

def leer_matriz_desde_text_box():
    try:
        matriz_str = text_box.get(1.0, tk.END).strip()
        nueva_matriz = [list(map(int, fila.split())) for fila in matriz_str.split('\n')]
        global matriz
        matriz = nueva_matriz
        return matriz
    except ValueError:
        text_box2.delete(1.0, tk.END)
        text_box2.insert(tk.END, "Por favor, ingrese una matriz válida.")
        return None

def generar_grafo_y_calcular_flujo():
    try:
        leer_matriz_desde_text_box()
        G = nx.DiGraph()
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                if matriz[i][j] > 0:
                    G.add_edge(i, j, capacity=matriz[i][j])
        
        source = int(entry_source.get())
        sink = int(entry_sink.get())
        
        flow_value, flow_dict = nx.maximum_flow(G, source, sink)
        
        text_box2.delete(1.0, tk.END)
        text_box2.insert(tk.END, f"Flujo máximo: {flow_value}\n")
        for u in flow_dict:
            for v in flow_dict[u]:
                text_box2.insert(tk.END, f"Flujo de {u} a {v}: {flow_dict[u][v]}\n")
        
        pos = nx.spring_layout(G)
        node_colors = ['red' if node == source else 'lightgreen' if node == sink else 'lightblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'capacity')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
    except ValueError:
        text_box2.delete(1.0, tk.END)
        text_box2.insert(tk.END, "Por favor, ingrese nodos válidos.")
    except nx.NetworkXError as e:
        text_box2.delete(1.0, tk.END)
        text_box2.insert(tk.END, f"Error en el cálculo del flujo: {e}")

# Ventana de menú principal
menu_principal = tk.Tk()
menu_principal.title("Flujo Maximo")
menu_principal.geometry("400x400")

label_menu = tk.Label(menu_principal, text="Menu Principal", font=("Helvetica", 16, "bold"))
label_menu.pack(pady=20) 

button_calculadora = tk.Button(menu_principal, text="Calculadora de Flujo Máximo", command=mostrar_calculadora, width=30, height=2, font=("Helvetica", 14), bd=5)
button_calculadora.pack(pady=10)

button_creditos = tk.Button(menu_principal, text="Créditos", command=mostrar_creditos, width=30, height=2, font=("Helvetica", 14), bd=5)
button_creditos.pack(pady=10)

button_salir = tk.Button(menu_principal, text="Salir", command=salir, width=30, height=2, font=("Helvetica", 14), bd=5)
button_salir.pack(pady=10)

# Ventana de calculadora de flujo máximo
root = tk.Toplevel(menu_principal)
root.title("Calculadora de flujo máximo")
root.geometry("800x600")
root.withdraw()

label = tk.Label(root, text="Bienvenido a la calculadora de flujo máximo", font=("Helvetica", 12, "bold"))
label.pack()

label_t = tk.Label(root, text="Ingrese la matriz de adyacencia en el cuadro de texto o genere una matriz aleatoria")
label_t.pack()

frame_n = tk.Frame(root)
frame_n.pack(pady=10)  

label_n = tk.Label(frame_n, text="Tamaño de la matriz (n x n):")
label_n.pack(side=tk.LEFT, padx=5)  

entry = tk.Entry(frame_n, width=3)
entry.pack(side=tk.LEFT, padx=5)  

button_aleatoria = tk.Button(frame_n, text="Generar matriz aleatoria", command=generar_matriz_aleatoria)
button_aleatoria.pack(side=tk.LEFT, padx=5)  

text_box = tk.Text(root, height=15, width=40)
text_box.pack()

label_explain = tk.Label(root, text="Los nodos del grafo van desde 0 hasta n-1 (n es el tamaño de la matriz)")
label_explain.pack()

label_explain2 = tk.Label(root, text="Para calcular el flujo máximo, ingrese el nodo fuente y el nodo sumidero")
label_explain2.pack()

frame_source_sink = tk.Frame(root)
frame_source_sink.pack(pady=10)

label_source = tk.Label(frame_source_sink, text="Nodo fuente:")
label_source.pack(side=tk.LEFT, padx=5)
entry_source = tk.Entry(frame_source_sink, width=3)
entry_source.pack(side=tk.LEFT, padx=5)

label_sink = tk.Label(frame_source_sink, text="Nodo sumidero:")
label_sink.pack(side=tk.LEFT, padx=5)
entry_sink = tk.Entry(frame_source_sink, width=3)
entry_sink.pack(side=tk.LEFT, padx=5)

button_grafo = tk.Button(root, text="Generar grafo", command=generar_grafo_y_calcular_flujo)
button_grafo.pack()

text_box2 = tk.Text(root, height=15, width=40)
text_box2.pack()

root.mainloop()
