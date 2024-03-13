from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
from tkinter.ttk import *
import re


# ##############################################
# MODELO
# ##############################################

def conexion():
    con = sqlite3.connect("spotmusic.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE spotmusic
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             playlist varchar(20) NOT NULL,
             artista varchar(20),
             cancion varchar(20))
    """
    cursor.execute(sql)
    con.commit()

try:
    conexion()
    crear_tabla()
except:
    print("DB ya existe")



def consultar_cancion(playlist, artista, cancion):
    con = conexion()
    cursor = con.cursor()
    data=(artista, cancion, playlist)
    sql = "SELECT playlist from spotmusic WHERE artista= ? AND cancion= ? AND playlist = ?"
    try:
        result=cursor.execute(sql,data)
        result=result.fetchall()
        return len(result)
    except:
        print('except consultar_cancion - cancion no esta')
        return False



def actualizar_playlist(playlist,artista,cancion): 
    con=conexion()
    cursor=con.cursor()
    if consultar_cancion(playlist, artista, cancion)== 0: 
        data=(playlist, artista, cancion)
        sql="INSERT INTO spotmusic (playlist, artista, cancion) VALUES(?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        showinfo('Agregar','Cancion agregada')
        actualizar_treeview(tree)
    else:
        showerror('WARNING', 'Esta canción ya existe en esta PLAYLIST, podes agregarla en otra')


def alta(playlist, artista, cancion, tree):
    playlist,artista, cancion=playlist.upper(), artista.upper(), cancion.upper()
    if playlist:
        if re.match('^[a-zA-Z0-9_]*$',playlist): #Regex to match just alphanumeric and whitespace caracters
            if artista:
                    if cancion:              
                            actualizar_playlist(playlist,artista,cancion)                             
                    else:
                        showerror('WARNING', 'Campo CANCION no puede estar vacio')
            else:
                showerror('WARNING', 'Campo ARTISTA no puede estar vacio')
        else:
            showerror('WARNING', 'Usar solo caracteres ALPHANUMERICOS para campo PLAYLIST')
    else:
        showerror('WARNING', 'Campo PLAYLIST no puede estar vacio')
    

def consultar(playlist, artista, cancion, mitreview):
    playlist, artista, cancion = playlist.upper(), artista.upper(), cancion.upper()
    
    for row in mitreview.get_children():
        mitreview.delete(row)
    
    if not (playlist or artista or cancion):
        showerror('WARNING', 'Debe indicar el nombre de la PLAYLIST, ARTISTA o CANCION a consultar')
        return

    con = conexion()
    cursor = con.cursor()

    if playlist:
        sql = "SELECT * FROM spotmusic WHERE playlist = ?"
        data = (playlist,)
        datos = cursor.execute(sql, data)
        execute_query(datos, mitreview)

    if artista:
        sql = "SELECT * FROM spotmusic WHERE artista = ?"
        data = (artista,)
        datos = cursor.execute(sql, data)
        execute_query(datos, mitreview)

    if cancion:
        sql = "SELECT * FROM spotmusic WHERE cancion = ?"
        data = (cancion,)
        datos = cursor.execute(sql, data)
        execute_query(datos, mitreview)
    a_val.set("")
    b_val.set("")
    c_val.set("")
    con.close()

def execute_query(datos, mitreview):
    resultado = datos.fetchall()
    for fila in resultado:
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
  

def modificar(playlist, artista, cancion,tree):
    playlist,artista, cancion=playlist.upper(), artista.upper(), cancion.upper()
    valor = tree.selection()
    item = tree.item(valor)

    if not valor:
        showerror("Error", "Seleccione el registro a Modificar")
        return
    
    if playlist== "" or artista == "" or cancion == "":
        showerror("Error", "Por favor, complete todos los campos.")
        return
    
    con = conexion()
    cursor = con.cursor()
    mi_id = item['text']
    data = (artista, cancion, mi_id)
    sql='''UPDATE spotmusic SET artista = ?, cancion = ? WHERE id = ?'''
    cursor.execute(sql,data)
    con.commit()
    con.close()
    actualizar_treeview(tree)


def borrar(playlist,tree):
    valor = tree.selection()
    item = tree.item(valor)
    
    if not valor:
        showerror("Error", "Seleccione el registro a borrar")
        return    

    con=conexion()
    cursor=con.cursor()
    mi_id = item['text']
    data = (mi_id,)
    sql = "DELETE FROM spotmusic WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    showinfo('Eliminar','Cancion eliminada')
    tree.delete(valor)
    

def actualizar_treeview(mitreview):
    for row in tree.get_children():
        tree.delete(row)

    sql = "SELECT * FROM spotmusic ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)
    execute_query(datos, mitreview)
    
    a_val.set("")
    b_val.set("")
    c_val.set("")

def actualizar(evento):
    selection=tree.selection()
    if selection:
        playlist_seleccionada=tree.item(selection[0],"values")[0]
        a_val.set(playlist_seleccionada)
    b_val.set("")
    c_val.set("")



# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("SPOTMUSIC")
        
titulo = Label(root, text="Almacená tus canciones favoritas",anchor=CENTER, background="chocolate1", foreground="black", font=("Almacena tus canciones favoritas",10,'roman'))
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

playlist = Label(root, text="Playlist")
playlist.grid(row=1, column=0, sticky=W)
artista=Label(root, text="Artista")
artista.grid(row=2, column=0, sticky=W)
cancion=Label(root, text="Canción")
cancion.grid(row=3, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val = StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable = a_val, width = w_ancho) 
entrada1.grid(row = 1, column =1 )
entrada2 = Entry(root, textvariable = b_val, width = w_ancho) 
entrada2.grid(row = 2, column = 1)
entrada3 = Entry(root, textvariable = c_val, width = w_ancho) 
entrada3.grid(row = 3, column = 1)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"]=("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)


tree.heading("#0", text="ID")
tree.heading("col1", text="Playlist")
tree.heading("col2", text="Artista")
tree.heading("col3", text="Canción")
tree.grid(row=100, column=0, columnspan=4)

style = Style()
style.configure('TButton', font =
               ('calibri', 12, 'bold'),
                    borderwidth = '4')

style.map('TButton', foreground = [('active', '!disabled', 'orange')],
                     background = [('active', 'black')])

boton_alta=Button(root, text="Alta", command=lambda:alta(a_val.get(), b_val.get(), c_val.get(), tree))
boton_alta.grid(row=7, column=0)

boton_consulta=Button(root, text="Consultar", command=lambda:consultar(a_val.get(),b_val.get(),c_val.get(),tree))
boton_consulta.grid(row=7, column=1)

boton_modificar=Button(root, text="Modificar", command=lambda:modificar(a_val.get(), b_val.get(), c_val.get(), tree))
boton_modificar.grid(row=7, column=2)

boton_borrar=Button(root, text="Borrar", command=lambda:borrar(a_val.get(),tree))
boton_borrar.grid(row=7, column=3)

boton_consultar_lista_playlist=Button(root, text="Consultá tus playlist",command=lambda:actualizar_treeview(tree))
boton_consultar_lista_playlist.grid(row=2, column=3)

tree.bind("<<TreeviewSelect>>", actualizar)


root.mainloop()


