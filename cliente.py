from threading import Thread
from socket import socket, error
# import hashlib
import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import time
from datetime import datetime


class Servidor(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent
        self.initialize_user_interface()

        self.host = '127.0.0.1'
        self.name = 'supermercado'
        self.user = 'root'
        self.password = ''
        self.usuario = ''
        self.conn = None
        self.conn = mysql.connector.connect(user=str(self.user),
                                            passwd=str(self.password),
                                            host=str(self.host),
                                            db=str(self.name))

        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def initialize_user_interface(self):
        self.frame = Frame(self.parent)
        self.parent.title("Supermercado Python Tkinter")
        self.parent.geometry("350x90")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        self.label_user = Label(self.parent, text="Usuario: ", anchor=W, background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_password = Label(self.parent, text="Clave:", anchor=W, background="dark slate gray",
                                    foreground="white", font="Helvetica 8  bold")

        self.label_user.grid(row=0, column=0, sticky=E + W)
        self.label_password.grid(row=1, column=0, sticky=E + W)

        self.dbuser = Entry(self.parent)
        self.dbpassword = Entry(self.parent, show="*")

        self.dbuser.grid(row=0, column=1, sticky=E + W)
        self.dbpassword.grid(row=1, column=1, sticky=E + W)

        self.connectb = Button(self.parent, text="Ingresar", font="Helvetica 10 bold", command=self.dbconnexion)

        self.connectb.grid(row=2, column=1, sticky=W)
        # self.cancelb.grid(row=2,column=2)

    def dbconnexion(self):

        self.usuario = self.dbuser.get()
        # clave = self.dbpassword.get()
        passw = self.dbpassword.get()
        # p = hashlib.new('md5', clave)
        # passw = p.hexdigest()

        sql = "SELECT * FROM (usuarios AS U INNER JOIN tipo_usuario AS TU ON U.tipo_user = TU.id) WHERE email = '" + self.usuario + "' AND pass='" + passw + "'"
        # print sql
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # print result
        if result:
            intento = 'ok'
            hoy = time.strftime("%Y%m%d")
            hora = time.strftime("%H:%M:%S")
            # ip = socket.gethostbyname(socket.gethostname())

            sqlcon = 'INSERT INTO logs (fecha_ingreso,usuario,intentos,hora_ingreso) VALUES ("%s","%s","%s","%s")' % (
                hoy, self.usuario, intento, hora)
            self.cursor.execute(sqlcon)
            self.conn.commit()

            for registro in result:
                self.datosUser = registro
            tipo_usuario = self.datosUser[4]
        else:
            tipo_usuario = 0

            intento = 'Fallo'
            hoy = time.strftime("%Y%m%d")
            hora = time.strftime("%H:%M:%S")

            sqlcon = 'INSERT INTO logs (fecha_ingreso,usuario,intentos,hora_ingreso) VALUES ("%s","%s","%s","%s")' % (
                hoy, self.usuario, intento, hora)
            self.cursor.execute(sqlcon)
            self.conn.commit()

        if tipo_usuario == 1:  # Si es Administrador
            self.parent.destroy()
            self.MenuAdmin()

        elif tipo_usuario == 2:  # Si es cliente
            self.parent.destroy()
            self.MenuCajero()

        elif tipo_usuario == 3:  # Si es cliente
            self.parent.destroy()
            self.MenuInventario()

        else:
            self.initialize_user_interface()

    def MenuAdmin(self):

        self.admin = Tk()
        self.menu = Menu(self.admin)
        self.admin.config(menu=self.menu)
        self.admin.geometry("500x500+0+0")
        self.admin.title("Administración - "+ self.datosUser[3])
        self.alertas = Menu(self.menu)  # un item del menu
        self.menu.add_cascade(label="Alertas",
                              menu=self.alertas)  # se agrega el menu alertas como una casacada del menu principal
        self.alertas.add_command(label="Productos con Stock Mínimo", command=self.alertas_Productos)

        self.ventas = Menu(self.menu)
        self.menu.add_cascade(label="Ventas", menu=self.ventas)
        self.ventas.add_command(label="Ver Listado de Facturas", command=self.Listar_Facturas)
        self.ventas.add_command(label="Ver Detalle de las Facturas", command=self.Listar_Det_Facturas)
        self.ventas.add_command(label="Ver Total de Ventas del Día", command=self.Total_Ventas)

        self.clientes = Menu(self.menu)
        self.menu.add_cascade(label="Clientes", menu=self.clientes)
        self.clientes.add_command(label="Registrar un Cliente", command=self.agregar_cliente)
        self.clientes.add_command(label="Actualizar un Cliente", command=self.actualizar_cliente)
        self.clientes.add_command(label="Eliminar un Cliente", command=self.eliminar_cliente)
        self.clientes.add_command(label="Lista de Clientes", command=self.listar_clientes)

        self.usuarios = Menu(self.menu)
        self.menu.add_cascade(label="Usuarios", menu=self.usuarios)
        self.usuarios.add_command(label="Actualizar mis Datos", command=self.Actualizar_Usuario)
        self.usuarios.add_command(label="Ver Listado de Usuarios", command=self.Listar_Usuarios)
        self.usuarios.add_command(label="Crear Usuario", command=self.crear_user)

        self.salir = Menu(self.menu)
        self.menu.add_cascade(label="Salir", menu=self.salir)
        self.salir.add_command(label="Cerrar Sesión", command=self.cierra_admin)

    def cierra_admin(self):
        self.admin.destroy()

    def cierra_invent(self):
        self.invent.destroy()

    def alertas_Productos(self):

        self.alert = Tk()
        self.alert.wm_title("Productos con Stock Mínimo")
        self.alert.grid_rowconfigure(0, weight=1)
        self.alert.grid_columnconfigure(0, weight=1)

        sql = "SELECT id, producto, descripcion, val_unit, stock, stock_minimo FROM productos where stock < stock_minimo"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()

        self.S = Scrollbar(self.alert)
        self.T = Text(self.alert, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if self.result:
            self.datos = self.result

        else:
            self.datos = 'No Hay alerta de productos minimos'

        self.T.insert(END, "ID - Producto - Descripción - Valor Unit - Stock - Stock Mínimo")
        self.T.insert(END, "\n")
        for i in self.datos:
            self.T.insert(END, i)
            self.T.insert(END, "\n")

        mainloop()

    def Listar_Usuarios(self):

        self.listaru = Tk()
        self.listaru.wm_title("Listado de Usuarios")
        self.listaru.grid_rowconfigure(0, weight=1)
        self.listaru.grid_columnconfigure(0, weight=1)

        sql = "SELECT email,nombre,tipo FROM (usuarios AS U INNER JOIN tipo_usuario AS TU ON U.tipo_user = TU.id)"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()

        self.S = Scrollbar(self.listaru)
        self.T = Text(self.listaru, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if self.result:
            self.datos = self.result

        else:
            self.datos = 'No Hay Usuarios Creados'

        self.T.insert(END, "Email (Usuario) - Nombre - Tipo")
        self.T.insert(END, "\n")
        for i in self.datos:
            self.T.insert(END, i)
            self.T.insert(END, "\n")

        mainloop()

    def crear_user(self):
        self.actuser = Tk()
        self.actuser.wm_title("Crear Usuario")
        self.actuser.grid_rowconfigure(0, weight=1)
        self.actuser.grid_columnconfigure(0, weight=1)

        self.label_email = Label(self.actuser, text="Email: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_contraseña = Label(self.actuser, text="Contraseña:", anchor=W,
                                      background="dark slate gray",
                                      foreground="white", font="Helvetica 8  bold")
        self.label_nombre = Label(self.actuser, text="Nombre:", anchor=W,
                                  background="dark slate gray",
                                  foreground="white", font="Helvetica 8  bold")
        self.label_tipo_usuario = Label(self.actuser, text="Tipo de Usuario:", anchor=W,
                                            background="dark slate gray",
                                            foreground="white", font="Helvetica 8  bold")

        self.label_email.grid(row=1, column=0, sticky=E + W)
        self.label_contraseña.grid(row=2, column=0, sticky=E + W)
        self.label_nombre.grid(row=3, column=0, sticky=E + W)
        self.label_tipo_usuario.grid(row=4, column=0, sticky=E + W)

        self.txtemail = Entry(self.actuser)
        self.txtcontra = Entry(self.actuser, show="*")
        self.txtnombre = Entry(self.actuser)
        self.txttipousuario = Entry(self.actuser)

        self.txtemail.grid(row=1, column=1, sticky=E + W)
        self.txtcontra.grid(row=2, column=1, sticky=E + W)
        self.txtnombre.grid(row=3, column=1, sticky=E + W)
        self.txttipousuario.grid(row=4, column=1, sticky=E + W)

        self.connectb = Button(self.actuser, text="Crear", font="Helvetica 10 bold", command=self.CrearUs)

        self.connectb.grid(row=6, column=1, sticky=W)

    def CrearUs(self):
        email = self.txtemail.get()
        passw = self.txtcontra.get()
        nombre = self.txtnombre.get()
        tipoUs = self.txttipousuario.get()

        hoy = time.strftime("%Y%m%d")

        if email == '' or passw == '' or nombre == '' or tipoUs == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.actuser.destroy(0, END)
        else:
            if int(tipoUs) < 1 or int(tipoUs) > 3:
                messagebox.showerror("error", "El tipo de usuario fuera de rango (1 -3)")
                self.actuser.destroy(0, END)
            else:    
                sql = "INSERT INTO usuarios (email, pass, nombre, tipo_user, fecha_registro) VALUES ('%s','%s','%s','%s','%s') " % (
                    email, passw, nombre, tipoUs, hoy)
                self.cursor.execute(sql)
                self.conn.commit()

                if sql:
                    messagebox.showinfo("Información", "Usuario Creado")
                    self.txtemail.delete(0, END)
                    self.txtcontra.delete(0, END)
                    self.txtnombre.delete(0, END)
                    self.txttipousuario.delete(0, END)
                    self.actuser.destroy()
                else:
                    messagebox.showerror("error", "Error al Crear Usuario")
        pass


    def Listar_Productos(self):

        self.listarp = Tk()
        self.listarp.wm_title("Listado de Productos")
        self.listarp.grid_rowconfigure(0, weight=1)
        self.listarp.grid_columnconfigure(0, weight=1)

        sql = "SELECT * FROM productos"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()

        self.S = Scrollbar(self.listarp)
        self.T = Text(self.listarp, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if self.result:
            self.datos = self.result

        else:
            self.datos = 'No Hay alerta de productos minimos'

        self.T.insert(END, "ID - Producto - Descripción - Valor Unit - Stock - Stock Mínimo")
        self.T.insert(END, "\n")
        for i in self.datos:
            self.T.insert(END, i)
            self.T.insert(END, "\n")

        mainloop()

    def Crear_Productos(self):

        self.crearp = Tk()
        self.crearp.wm_title("Crear Productos")
        self.crearp.geometry("350x230")
        self.crearp.grid_rowconfigure(0, weight=1)
        self.crearp.grid_columnconfigure(0, weight=1)

        self.label_prod = Label(self.crearp, text="Producto: ", anchor=W, background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_desc = Label(self.crearp, text="Descripción:", anchor=W,
                                background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_valor = Label(self.crearp, text="Valor:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_stockmin = Label(self.crearp, text="Stock Mínimo:", anchor=W,
                                    background="dark slate gray",
                                    foreground="white", font="Helvetica 8  bold")
        self.label_stock = Label(self.crearp, text="Stock:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_upfile = Label(self.crearp, text="Imagen:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_namefile = Label(self.crearp, text="", anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 8  bold", state="disable")

        self.label_prod.grid(row=0, column=0, sticky=E + W, pady=3)
        self.label_desc.grid(row=1, column=0, sticky=E + W, pady=3)
        self.label_valor.grid(row=2, column=0, sticky=E + W, pady=3)
        self.label_stockmin.grid(row=3, column=0, sticky=E + W, pady=3)
        self.label_stock.grid(row=4, column=0, sticky=E + W, pady=3)
        self.label_upfile.grid(row=5, column=0, sticky=E + W, pady=3)
        self.label_namefile.grid(row=5, column=1, sticky=E + W, pady=3)

        self.txtprod = Entry(self.crearp)
        self.txtdesc = Entry(self.crearp)
        self.txtvlr = Entry(self.crearp)
        self.txtsmin = Entry(self.crearp)
        self.txtstck = Entry(self.crearp)

        self.txtprod.grid(row=0, column=1, sticky=E + W, pady=3)
        self.txtdesc.grid(row=1, column=1, sticky=E + W, pady=3)
        self.txtvlr.grid(row=2, column=1, sticky=E + W, pady=3)
        self.txtsmin.grid(row=3, column=1, sticky=E + W, pady=3)
        self.txtstck.grid(row=4, column=1, sticky=E + W, pady=3)

        self.upfile = Button(self.crearp, text="Cargar Imagen", font="Helvetica 10 bold", command=self.abrir_navegador)

        self.upfile.grid(row=6, column=1, sticky=E + W, pady=3)


        self.connectb = Button(self.crearp, text="Registrar", font="Helvetica 10 bold", command=self.GuardarP)

        self.connectb.grid(row=7, column=1, sticky=W)

    def abrir_navegador(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Seleccione una Imagen",filetypes = (("png files","*.png"),("jpeg files","*.jpg")))
        if self.filename:
            #se convierte de digital a binario
            with open(self.filename, 'rb') as file:
                self.binaryData = file.read()
                file.close()
            self.label_namefile.config(text=self.filename)

            self.binaryData = str(self.binaryData).strip("b")
        else: 
            self.binaryData  = ""
            self.label_namefile.config(text="")


    def GuardarP(self):

        prod = self.txtprod.get()
        desc = self.txtdesc.get()
        valor = self.txtvlr.get()
        stockmin = self.txtsmin.get()
        stock = self.txtstck.get()

        if prod == '' or desc == '' or valor == '' or stockmin == '' or stock == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.txtprod.delete(0, END)
        else:
            sql = 'INSERT INTO productos (producto,descripcion,val_unit,stock,stock_minimo, imagen) VALUES ("%s","%s","%s","%s","%s",%s)' % (
                prod, desc, valor, stock, stockmin, self.binaryData)
            self.cursor.execute(sql)
            self.conn.commit()

            if sql:
                messagebox.showinfo("Información", "Productos Registrado")
                self.txtprod.delete(0, END)
                self.txtdesc.delete(0, END)
                self.txtvlr.delete(0, END)
                self.txtsmin.delete(0, END)
                self.txtstck.delete(0, END)
                self.txtprod.delete(0, END)
                self.crearp.destroy()
            else:
                messagebox.showerror("error", "Error al guardar el Producto")

    def Act_Productos(self):


        self.actp = Tk()
        self.actp.wm_title("Actualizar Productos")
        self.actp.grid_rowconfigure(0, weight=1)
        self.actp.grid_columnconfigure(0, weight=1)

        self.label_codid = Label(self.actp, text="ID Producto a Modificar: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_prod = Label(self.actp, text="Producto: ", anchor=W, background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_desc = Label(self.actp, text="Descripción:", anchor=W,
                                background="dark slate gray",
                                foreground="white", font="Helvetica 8  bold")
        self.label_valor = Label(self.actp, text="Valor:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_stockmin = Label(self.actp, text="Stock Mínimo:", anchor=W,
                                    background="dark slate gray",
                                    foreground="white", font="Helvetica 8  bold")
        self.label_stock = Label(self.actp, text="Stock:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_codid.grid(row=0, column=0, sticky=E + W)
        self.label_prod.grid(row=1, column=0, sticky=E + W)
        self.label_desc.grid(row=2, column=0, sticky=E + W)
        self.label_valor.grid(row=3, column=0, sticky=E + W)
        self.label_stockmin.grid(row=4, column=0, sticky=E + W)
        self.label_stock.grid(row=5, column=0, sticky=E + W)

        self.txtcodid = Entry(self.actp)
        self.txtprod = Entry(self.actp)
        self.txtdesc = Entry(self.actp)
        self.txtvlr = Entry(self.actp)
        self.txtsmin = Entry(self.actp)
        self.txtstck = Entry(self.actp)

        self.txtcodid.grid(row=0, column=1, sticky=E + W)
        self.txtprod.grid(row=1, column=1, sticky=E + W)
        self.txtdesc.grid(row=2, column=1, sticky=E + W)
        self.txtvlr.grid(row=3, column=1, sticky=E + W)
        self.txtsmin.grid(row=4, column=1, sticky=E + W)
        self.txtstck.grid(row=5, column=1, sticky=E + W)

        self.connectb = Button(self.actp, text="Registrar", font="Helvetica 10 bold", command=self.ActuaP)

        self.connectb.grid(row=6, column=1, sticky=W)

    def Elim_Productos(self):
        self.elimp = Tk()
        self.elimp.wm_title("Eliminar Producto")
        self.elimp.grid_rowconfigure(0, weight=1)
        self.elimp.grid_columnconfigure(0, weight=1)

        self.label_codid = Label(self.elimp, text="ID Producto a Eliminar: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_codid.grid(row=0, column=0, sticky=E + W)

        self.txtcodid = Entry(self.elimp)

        self.txtcodid.grid(row=0, column=1, sticky=E + W)

        self.connectb = Button(self.elimp, text="Eliminar", font="Helvetica 10 bold", command=self.ElimP)

        self.connectb.grid(row=6, column=1, sticky=W)

    def exis_Productos(self):

        self.aggstock = Tk()
        self.aggstock.wm_title("Agregar Exisrencia de Productos")
        self.aggstock.grid_rowconfigure(0, weight=1)
        self.aggstock.grid_columnconfigure(0, weight=1)

        self.label_codid = Label(self.aggstock, text="ID Producto a Modificar: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_stock = Label(self.aggstock, text="Nueva Cantidad:", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_codid.grid(row=0, column=0, sticky=E + W)
        self.label_stock.grid(row=5, column=0, sticky=E + W)

        self.txtcodid = Entry(self.aggstock)
        self.txtstck = Entry(self.aggstock)

        self.txtcodid.grid(row=0, column=1, sticky=E + W)
        self.txtstck.grid(row=5, column=1, sticky=E + W)

        self.connectb = Button(self.aggstock, text="Agregar", font="Helvetica 10 bold", command=self.AggStock)

        self.connectb.grid(row=6, column=1, sticky=W)

    def ElimP(self):
        idprod = self.txtcodid.get()
        if idprod == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.txtprod.delete(0, END)
        else:
            sql = "DELETE FROM productos WHERE id = %i" % int(idprod)
            self.cursor.execute(sql)
            self.conn.commit()
            if sql:
                messagebox.showinfo("Información", "Producto Eliminado")
                self.txtcodid.delete(0, END)  # Limpiar Cajas de Texto
                self.elimp.destroy()
            else:
                messagebox.showerror("error", "Error al Eliminar el Producto")


    def ActuaP(self):

        idprod = self.txtcodid.get()
        prod = self.txtprod.get()
        desc = self.txtdesc.get()
        valor = self.txtvlr.get()
        stockmin = self.txtsmin.get()
        stock = self.txtstck.get()

        if idprod == '' or prod == '' or desc == '' or valor == '' or stockmin == '' or stock == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.txtprod.delete(0, END)
        else:
            sql = "UPDATE productos SET producto='%s',descripcion='%s',val_unit='%s',stock='%s',stock_minimo='%s' WHERE id = %i" % (
                prod, desc, valor, stock, stockmin, int(idprod))
            self.cursor.execute(sql)
            self.conn.commit()

            if sql:
                messagebox.showinfo("Información", "Producto Actualizado")
                self.txtcodid.delete(0, END)  # Limpiar Cajas de Texto
                self.txtprod.delete(0, END)
                self.txtdesc.delete(0, END)
                self.txtvlr.delete(0, END)
                self.txtsmin.delete(0, END)
                self.txtstck.delete(0, END)
                self.txtprod.delete(0, END)
                self.actp.destroy()
            else:
                messagebox.showerror("error", "Error al Actualizar el Producto")

    def AggStock(self):

        idprod = self.txtcodid.get()
        stock = self.txtstck.get()

        if idprod == '' or stock == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.txtstck.delete(0, END)
        else:
            sql = "UPDATE productos SET stock='%s' WHERE id = %i" % (stock, int(idprod))
            self.cursor.execute(sql)
            self.conn.commit()

            if sql:
                messagebox.showinfo("Información", "Producto Actualizado")
                self.txtcodid.delete(0, END)  # imprimir información
                self.txtstck.delete(0, END)
                self.aggstock.destroy()
            else:
                messagebox.showerror("error", "Error al Actualizar el Producto")

    def Listar_Facturas_cte(self):

        self.listarf = Tk()
        self.listarf.wm_title("Listado de Facturas")
        self.listarf.grid_rowconfigure(0, weight=1)
        self.listarf.grid_columnconfigure(0, weight=1)

        consulta = 'SELECT id_fatura,fecha_factura,total FROM factura '
        self.cursor.execute(consulta)
        self.result = self.cursor.fetchall()

        self.S = Scrollbar(self.listarf)
        self.T = Text(self.listarf, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if self.result:
            self.datos = self.result

        else:
            self.datos = 'No hay Facturas Creadas'

        self.T.insert(END, "ID - Fecha Creación  - Total")
        self.T.insert(END, "\n")
        for i in self.datos:
            self.T.insert(END, i)
            self.T.insert(END, "\n")

        mainloop()

    def Listar_Facturas(self):

        self.listarf = Tk()
        self.listarf.wm_title("Listado de Facturas")
        self.listarf.grid_rowconfigure(0, weight=1)
        self.listarf.grid_columnconfigure(0, weight=1)

        consulta = 'SELECT f.id_fatura,f.fecha_factura,u.nombres, u.apellidos,f.total FROM factura as f INNER JOIN clientes as u ON f.cliente_doc = u.documento_id'
        self.cursor.execute(consulta)
        self.result = self.cursor.fetchall()

        self.S = Scrollbar(self.listarf)
        self.T = Text(self.listarf, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if self.result:
            self.datos = self.result

        else:
            self.datos = 'No hay Facturas Creadas'

        self.T.insert(END, "ID - Fecha Creación - Nombres - Apellidos - Total")
        self.T.insert(END, "\n")
        for i in self.datos:
            self.T.insert(END, i)
            self.T.insert(END, "\n")

        mainloop()

    def Listar_Det_Facturas(self):

        self.listardetf = Tk()
        self.listardetf.wm_title("Detalle de Facturas")
        self.listardetf.grid_rowconfigure(0, weight=1)
        self.listardetf.grid_columnconfigure(0, weight=1)
        self.listardetf.geometry("200x70+800+0")

        self.label_idfact = Label(self.listardetf, text="ID Factura:", anchor=W,
                                  background="dark slate gray",
                                  foreground="white", font="Helvetica 8  bold")

        self.label_idfact.grid(row=0, column=0, sticky=E + W)

        self.txtid = Entry(self.listardetf)

        self.txtid.grid(row=0, column=1, sticky=E + W)

        self.connectb = Button(self.listardetf, text="Consultar", font="Helvetica 10 bold", command=self.Consultar_DetF)

        self.connectb.grid(row=1, column=1, sticky=W)

    def Consultar_DetF(self):

        idfact = self.txtid.get()

        self.listardetallefact = Tk()
        self.listardetallefact.wm_title("Listado de Facturas")
        self.listardetallefact.grid_rowconfigure(0, weight=1)
        self.listardetallefact.grid_columnconfigure(0, weight=1)

        self.S = Scrollbar(self.listardetallefact)
        self.T = Text(self.listardetallefact, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if idfact == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")

        else:
            sql = "SELECT p.producto, p.descripcion, df.cantidad, p.val_unit, df.valor FROM (detalle_factura as df INNER JOIN productos as p ON df.id_producto = p.id) WHERE df.id_factura=%i" % (
                int(idfact))
            # print sql
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()

            if self.result:
                # self.i = 0
                self.datos = self.result

                self.T.insert(END, "Producto - Descripción - Cantidad - Vlr Unit - Valor Total")
                self.T.insert(END, "\n")
                for i in self.datos:
                    self.T.insert(END, i)
                    self.T.insert(END, "\n")
            else:
                # self.datos = 'No hay Facturas Creadas'
                # self.T.insert(END, self.datos)
                messagebox.showerror("error", "Numero de factura no existe")
                self.listardetallefact.destroy()
            mainloop()

    def Total_Ventas(self):

        self.totvent = Tk()
        self.totvent.wm_title("Total de Ventas Diarias")
        self.totvent.grid_rowconfigure(0, weight=1)
        self.totvent.grid_columnconfigure(0, weight=1)

        self.label_fecha = Label(self.totvent, text="Fecha (AAAA-MM-DD)", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_fecha.grid(row=0, column=0, sticky=E + W)

        self.txtfecha = Entry(self.totvent)

        self.txtfecha.grid(row=0, column=1, sticky=E + W)

        self.buscar = Button(self.totvent, text="Consultar", font="Helvetica 10 bold",
                             command=self.Consultar_Ventas)

        self.buscar.grid(row=1, column=1, sticky=W)

    def Consultar_Ventas(self):

        fecha = self.txtfecha.get()

        self.conventas = Tk()
        self.conventas.wm_title("Listado de Facturas")
        self.conventas.grid_rowconfigure(0, weight=1)
        self.conventas.grid_columnconfigure(0, weight=1)

        self.S = Scrollbar(self.conventas)
        self.T = Text(self.conventas, height=10, width=80)
        self.S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        if fecha == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")

        else:
            sql = "SELECT SUM(total) as Total FROM `factura` WHERE `fecha_factura` LIKE '%" + fecha + "%'"
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()

            if self.result:
                self.datos = self.result

                self.T.insert(END, "Total Ventas del Día")
                self.T.insert(END, "\n")
                for i in self.datos:
                    self.T.insert(END, i)
                    self.T.insert(END, "\n")
            else:
                self.datos = 'No hay Ventas en esta Fecha'
                self.T.insert(END, self.datos)

            mainloop()

    def Genera_factura(self):

        hoy = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "SELECT sum(valor) as total FROM detalle_compra_temp WHERE user='" + self.usuario + "'"
        self.cursor.execute(sql)
        self.conn.commit()
        self.resultado = self.cursor.fetchall()
        if (self.resultado):
            for regi in self.resultado:
                total = regi[0]

            print(total)
            if total > 0:
                sqlprod = 'INSERT INTO factura (user,total,fecha_factura) VALUES ("%s","%s","%s")' % (
                    self.usuario, int(total), hoy)
                self.cursor.execute(sqlprod)
                self.conn.commit()

                querynf = "SELECT MAX( id_fatura ) FROM factura"
                self.cursor.execute(querynf)
                self.conn.commit()

                self.result3 = self.cursor.fetchall()

                for resu in self.result3:
                    idfact = resu[0]

                query2 = "insert into detalle_factura (id_producto,cantidad,valor,user,fecha_registro,id_factura) select id_producto,cantidad,valor,user,fecha_registro,%i " % (
                    int(idfact)) + " from detalle_compra_temp where user='" + self.usuario + "'"
                self.cursor.execute(query2)
                self.conn.commit()

                messagebox.showinfo("Información", "Factura Generada")
                deltemp = "delete from  detalle_compra_temp where user='%s'" % self.usuario

                self.cursor.execute(deltemp)
                self.conn.commit()

                selprod = "select * from detalle_factura where id_factura=%i " % int(idfact)

                self.cursor.execute(selprod)
                self.conn.commit()

                self.runsq = self.cursor.fetchall()

                for prod in self.runsq:
                    idprod = prod[1]
                    cant = prod[2]
                    seldp = "select * from productos where id= %i" % int(idprod)
                    # runpd = run_query(seldp)
                    self.cursor.execute(seldp)
                    self.conn.commit()

                    self.runpd = self.cursor.fetchall()
                    for dprod in self.runpd:
                        cantold = dprod[4]
                    ncant = int(cantold) - int(cant)
                    actudeta = "update productos set stock= %i where id=%i" % (int(ncant), int(idprod))
                    # runacp = run_query(actudeta)
                    self.cursor.execute(actudeta)
                    self.conn.commit()
            else:
                messagebox.showerror("error", "No hay compras pendientes")
        else:
            messagebox.showerror("error", "No hay compras pendientes")


    def MenuCajero(self):

        self.cliente = Tk()
        self.cliente.geometry("500x500+0+0")
        self.cliente.title("Cajero - "+ self.datosUser[3])
        self.menu = Menu(self.cliente)
        self.cliente.config(menu=self.menu)


        self.facturas = Menu(self.menu)
        self.menu.add_cascade(label="Facturas", menu=self.facturas)
        self.facturas.add_command(label="Ver Listado de Facturas", command=self.Listar_Facturas_cte)
        self.facturas.add_command(label="Detalle de las Facturas", command=self.Listar_Det_Facturas)
        self.facturas.add_command(label="Ver Total de Ventas del Día", command=self.Total_Ventas)

            
        self.estado_cajero()

        if self.band_estado_cajero == "open":
            self.mercado = Menu(self.menu)
            self.menu.add_cascade(label="Ventas", menu=self.mercado)
            self.mercado.add_command(label="Registrar Venta", command=self.registrar_venta)

        self.caja = Menu(self.menu)
        if self.band_estado_cajero != "close":
            self.menu.add_cascade(label="Caja", menu=self.caja)
            if self.band_estado_cajero == "none":
                self.caja.add_command(label="Iniciar Caja", command=self.iniciar_caja)
            elif self.band_estado_cajero == "open":
                self.caja.add_command(label="Cerrar Caja", command=self.cerrar_caja)



        self.clientes = Menu(self.menu)
        self.menu.add_cascade(label="Clientes", menu=self.clientes)
        self.clientes.add_command(label="Registrar un Cliente", command=self.agregar_cliente)
        self.clientes.add_command(label="Actualizar un Cliente", command=self.actualizar_cliente)
        self.clientes.add_command(label="Eliminar un Cliente", command=self.eliminar_cliente)
        self.clientes.add_command(label="Lista de Clientes", command=self.listar_clientes)


        self.usuarios = Menu(self.menu)
        self.menu.add_cascade(label="Perfil", menu=self.usuarios)
        self.usuarios.add_command(label="Actualizar Datos Personales", command=self.Actualizar_Usuario)

        self.salir = Menu(self.menu)
        self.menu.add_cascade(label="Salir", menu=self.salir)
        self.salir.add_command(label="Cerrar Sesión", command=self.cierra_cajero)

    def cierra_cajero(self):
        self.cliente.destroy()

    def estado_cajero(self):
        hoy = time.strftime("%Y%m%d")
        consulta = 'SELECT estado_caja FROM ventas WHERE fecha_registro = "%s" AND codigo_cajero = "%s"' % (hoy, str(self.datosUser[0]))
        self.cursor.execute(consulta)
        self.result = self.cursor.fetchall()

        if self.result:
            for estado in self.result:
                self.band_estado_cajero = str(estado[0])
        else:
            self.band_estado_cajero = "none"

    def facturar(self):
        hoy = time.strftime("%Y - %m - %d ")
        cedula_cliente = self.doccliente
        for i in self.result_client:
            nombres = i[0]
            apellidos = i[1]
        cajero = self.datosUser[3]


        self.listarproductos.destroy()
        self.factura = Tk()
        self.factura.title("Factura")

        self.encabezado = Frame(self.factura)
        self.encabezado.grid(row=0, column=0, sticky=E + W, pady=5)
        self.label_fecha = Label(self.encabezado, text="Fecha: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 10  bold")
        self.label_fecha.grid(row=0, column=0, sticky=E + W, pady=5)
        self.label_fecha2 = Label(self.encabezado, text=hoy, anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 10  bold")
        self.label_fecha2.grid(row=0, column=1, sticky=E + W, pady=5)

        self.nombres_cliente = Label(self.encabezado, text="Nombre: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 10  bold")
        self.nombres_cliente.grid(row=1, column=0, sticky=E + W, pady=5)
        self.nombres_cliente2 = Label(self.encabezado, text='%s %s' % (nombres, apellidos), anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 10  bold")
        self.nombres_cliente2.grid(row=1, column=1, sticky=E + W, pady=5)

        self.docume_cliente = Label(self.encabezado, text="Documento: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 10  bold")
        self.docume_cliente.grid(row=2, column=0, sticky=E + W, pady=5)
        self.docume_cliente2 = Label(self.encabezado, text=cedula_cliente, anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 10  bold")
        self.docume_cliente2.grid(row=2, column=1, sticky=E + W, pady=5)

        self.nombre_cajero = Label(self.encabezado, text="Cajero: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 10  bold")
        self.nombre_cajero.grid(row=3, column=0, sticky=E + W, pady=5)
        self.nombre_cajero2 = Label(self.encabezado, text=cajero, anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 10  bold")
        self.nombre_cajero2.grid(row=3, column=1, sticky=E + W, pady=5)


        self.tablefact = ttk.Treeview(self.factura, height=8)
        self.tablefact["column"] = ('Producto', 'Descripcion', 'valor Und.','cantidad','Valor Total')
        self.tablefact.heading("#0", text="Codigo")
        self.tablefact.column("#0", stretch=NO, width=60, anchor="w")
        self.tablefact.heading("Producto", text="Producto")
        self.tablefact.column("Producto", width=100, anchor="center")
        self.tablefact.heading("Descripcion", text="Descripción")
        self.tablefact.column("Descripcion", width=120, anchor="center")
        self.tablefact.heading("valor Und.", text="Valor Und.")
        self.tablefact.column("valor Und.", width=90, anchor="center")
        self.tablefact.heading("cantidad", text="Cantidad")
        self.tablefact.column("cantidad", width=90, anchor="center")
        self.tablefact.heading("Valor Total", text="Valor Total")
        self.tablefact.column("Valor Total", width=90, anchor="center")
        self.tablefact.grid(row=1, column=0, padx=5, pady=5)


        self.ysb = ttk.Scrollbar(self.factura, orient="vertical", command=self.tablefact.yview)
        self.tablefact.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=1, column=1, sticky='ns')


        self.piepag = Frame(self.factura)
        self.piepag.grid(row=3, column=0, sticky=E + W, pady=5)
        self.total_pagar = Label(self.piepag, text="Total a Pagar: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 10  bold")
        self.total_pagar.grid(row=0, column=0, sticky=W, pady=5)
        self.total_pagar2 = Label(self.piepag, text="", anchor=W,
                                 background="white",
                                 foreground="black", font="Helvetica 10  bold")
        self.total_pagar2.grid(row=0, column=1, sticky=W, pady=5)


        self.cancelar_factura = Button(self.piepag, text="Cancelar Factura", font="Helvetica 10 bold", command=self.cancelar_fact)
        self.cancelar_factura.grid(row=1, column=1, sticky=W)

        self.cargar_tabla_factura()
        mainloop()

    def cancelar_fact(self):
        update = 'UPDATE factura SET estado = "liquidado" WHERE id_fatura = %i' % int(self.id_factura)
        self.cursor.execute(update)
        self.conn.commit()

        if update:
            messagebox.showinfo("Información", "Factura Cancelada")
            self.factura.destroy()
        else:
            messagebox.showerror("Error", "Error Al cancelar la Factura")
            self.factura.destroy()


    def cargar_tabla_factura(self):
        hoy = time.strftime("%Y%m%d")
        consulta = 'SELECT id_fatura,total FROM factura WHERE cliente_doc = "%s" AND fecha_factura = "%s" AND estado = "sin_pagar"' % (self.doccliente, hoy)
        self.cursor.execute(consulta)
        result = self.cursor.fetchall()
        
        if result:

            for x in result:
                self.id_factura = x[0]
                total = x[1]

            consulta = 'SELECT productos.id, productos.producto, productos.descripcion, productos.val_unit, detalle_factura.cantidad, detalle_factura.valor FROM detalle_factura INNER JOIN productos ON detalle_factura.id_producto=productos.id WHERE detalle_factura.id_factura=%i' % self.id_factura
            self.cursor.execute(consulta)
            self.result = self.cursor.fetchall()

            if self.result:
                self.datosP = self.result
                for i in self.datosP:
                    self.tablefact.insert("", END, text=i[0], values=(i[1],i[2],i[3],i[4],i[5]))
                self.total_pagar2.config(text=total)
                self.cancelar_factura.config(state="active")
            else:
                self.datos = 'NO HAY REGISTROS'
                self.tablefact.insert("", END, text=indice, values= self.datos)
        else:
            self.tablefact.destroy()
            self.resultado = Label(self.encabezado, text="Aun no se han seleccionado productos", anchor=W,
                                     background="white",
                                     foreground="black", font="Helvetica 10  bold")
            self.resultado.grid(row=4, column=1, sticky=E + W, pady=5)
            self.cancelar_factura.config(state="disable")


    def registrar_venta(self):
        self.regVenta = Tk()
        self.regVenta.wm_title("Indicar Cliente")
        self.regVenta.grid_rowconfigure(0, weight=1)
        self.regVenta.grid_columnconfigure(0, weight=1)

        self.label_doccliente = Label(self.regVenta, text="Número documento del cliente: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_doccliente.grid(row=0, column=0, sticky=E + W, pady=5)

        self.txtdoccliente = Entry(self.regVenta)

        self.txtdoccliente.grid(row=0, column=1, sticky=E + W, padx=2, pady=5)

        self.connectb = Button(self.regVenta, text="Seleccionar Productos", font="Helvetica 10 bold", command=self.Seleccionar_productos)

        self.connectb.grid(row=6, column=1, sticky=W, pady=3)

    def Seleccionar_productos(self):
        hoy = time.strftime("%Y%m%d")
        self.doccliente = self.txtdoccliente.get()
        self.doccliente = self.doccliente.strip()

        self.regVenta.destroy()
        consulta = 'SELECT nombres,apellidos FROM clientes WHERE documento_id= "%s"' % self.doccliente
        self.cursor.execute(consulta)
        self.result_client = self.cursor.fetchall()

        if self.result_client:
            self.listarproductos = Tk()
            self.listarproductos.title("Listado de productos")

            self.busqueda = Frame(self.listarproductos)
            self.busqueda.grid(row=0, column=0, sticky=E + W, pady=5)
            self.label_busqueda = Label(self.busqueda, text="Buscar por nombre: ", anchor=W,
                                     background="dark slate gray",
                                     foreground="white", font="Helvetica 8  bold")

            self.label_busqueda.grid(row=0, column=0, sticky=E + W)
            self.txtnomprod = Entry(self.busqueda)
            self.txtnomprod.grid(row=0, column=1, sticky=E + W)
            self.buscar = Button(self.busqueda, text="Buscar", font="Helvetica 10 bold", command=self.buscar_producto)
            self.buscar.grid(row=0, column=2,  sticky=E + W, padx=2)
            self.restablecerp = Button(self.busqueda, text="Restablecer", font="Helvetica 10 bold", command=self.restablecer_productos)
            self.restablecerp.grid(row=0, column=3,  sticky=E + W, padx=2)
            self.terminarcar = Button(self.busqueda, text="Terminar", font="Helvetica 10 bold", command=self.facturar)
            self.terminarcar.grid(row=0, column=5,  sticky=E + W, padx=2)


            self.tableprod = ttk.Treeview(self.listarproductos, height=10)
            self.tableprod["column"] = ('Codigo','Producto', 'Descripción', 'Valor Und.','imagen')
            self.tableprod.heading("#0", text="Indice")
            self.tableprod.column("#0", stretch=NO, width=60, anchor="w")
            self.tableprod.heading("Codigo", text="Codigo")
            self.tableprod.column("Codigo", width=100, anchor="center")
            self.tableprod.heading("Producto", text="Producto")
            self.tableprod.column("Producto", width=120, anchor="center")
            self.tableprod.heading("Descripción", text="Descripción")
            self.tableprod.column("Descripción", width=120, anchor="center")
            self.tableprod.heading("Valor Und.", text="Valor Und.")
            self.tableprod.column("Valor Und.", width=100, anchor="center")
            self.tableprod.heading("imagen", text="Imagen")
            self.tableprod.column("imagen", width=100, anchor="center")
            self.tableprod.grid(row=1, column=0, padx=5, pady=5)


            self.ysb = ttk.Scrollbar(self.listarproductos, orient="vertical", command=self.tableprod.yview)
            self.tableprod.configure(yscroll=self.ysb.set)
            self.ysb.grid(row=1, column=1, sticky='ns')

            self.cargar_tabla_productos()

            mainloop()
        else:
            messagebox.showerror("Error", "Error el Cliente no esta Registrado")
            self.agregar_cliente()

    def buscar_producto(self):
        nomprod = self.txtnomprod.get()
        nomprod = nomprod.strip()
        if nomprod == '':
            self.restablecer_productos()
        else:
            x = self.tableprod.get_children() #variable para almacenar diccionario
            if x != '()': #verifica si hay almenos una fila
                for item in x:
                    values_values = (self.tableprod.item(item)["values"])
                    if str(values_values[1]) != nomprod:
                        self.tableprod.delete(item)

    def restablecer_productos(self):
        x = self.tableprod.get_children() #variable para almacenar diccionario
        if x != '()': #verifica si hay almenos una fila
            for item in x:
                self.tableprod.delete(item)
            self.cargar_tabla_productos()
            self.txtnomprod.delete(0, END)

    def cargar_tabla_productos(self):
        consulta = 'SELECT * FROM productos'
        self.cursor.execute(consulta)
        self.result = self.cursor.fetchall()

        indice = 1
        if self.result:
            self.datosP = self.result
            for i in self.datosP:
                if i[6] != None:
                    with open("image.png", 'wb') as f:
                        f.write(i[6])
                self.tableprod.insert("", END, text=indice, values=(i[0],i[1], i[2],i[3],i[6]))
                indice += 1
            self.tableprod.bind("<Double-1>", self.cant_prod)

        else:
            self.datos = 'NO HAY REGISTROS'
            self.tableprod.insert("", END, text=indice, values= self.datos)

    def cant_prod(self, event):
        item = self.tableprod.selection()[0]
        self.data_producto = self.tableprod.item(item,"values")
        self.cantidad_p = Tk()
        self.cantidad_p.wm_title("Cantidad de Productos")
        self.cantidad_p.geometry("250x80")
        self.cantidad_p.grid_rowconfigure(0, weight=1)
        self.cantidad_p.grid_columnconfigure(0, weight=1)

        self.label_unida = Label(self.cantidad_p, text="Cantidad de %s: " % self.data_producto[1], anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_unida.grid(row=0, column=0, sticky=E + W, padx=2, pady=5)

        self.txtunidades = Entry(self.cantidad_p)

        self.txtunidades.grid(row=0, column=1, sticky=E + W, padx=2, pady=5)

        self.connectb = Button(self.cantidad_p, text="Agregar", font="Helvetica 10 bold", command=self.aggdetalle_factura)

        self.connectb.grid(row=6, column=1, sticky=W, pady=3)

    def aggdetalle_factura(self):
        unidades = self.txtunidades.get()
        if unidades == '':
            messagebox.showerror("Error", "Diligencie Todos los Campos")
            self.txtunidades.delete(0, END)
        else:
            try:
                hoy = time.strftime("%Y%m%d")
                unidades = unidades.strip()
                valor = int(unidades) * int(self.data_producto[3])
                id_producto = int(self.data_producto[0])

                select = 'SELECT stock FROM productos WHERE id = %i' % int(id_producto)
                self.cursor.execute(select)
                result_select = self.cursor.fetchall()
                for j in result_select:
                    stock = int(j[0])
                stock -= int(unidades)

                if stock > 0:
                    update1 = 'UPDATE productos SET stock = %i WHERE id = %i' % (int(stock), int(id_producto))
                    self.cursor.execute(update1)
                    self.conn.commit()

                    consulta = 'SELECT id_fatura, total FROM factura WHERE cliente_doc = "%s" AND fecha_factura = "%s" AND estado = "sin_pagar"' % (self.doccliente, hoy)
                    self.cursor.execute(consulta)
                    result = self.cursor.fetchall()
                    # print(result)
                    if result:
                        for i in result:
                            self.id_factura = i[0]
                            total = i[1]
                        insert = 'INSERT INTO detalle_factura (id_producto, cantidad, valor, id_factura) VALUES (%i,%i,%i,%i)' % (int(id_producto), int(unidades), int(valor), int(self.id_factura))
                        self.cursor.execute(insert)
                        self.conn.commit()


                        valor += int(total)
                        update = 'UPDATE factura SET total = %i WHERE id_fatura = %i' % (int(valor), int(self.id_factura))
                        self.cursor.execute(update)
                        self.conn.commit()
                    else:
                        sql = "INSERT INTO factura (cliente_doc, total, fecha_factura, estado) VALUES ('%s',%i,'%s','sin_pagar')" % (self.doccliente, int(valor), hoy)
                        self.cursor.execute(sql)
                        self.conn.commit()

                        self.cursor.execute(consulta)
                        result = self.cursor.fetchall()
                        for i in result:
                            self.id_factura = i[0]
                        insert = 'INSERT INTO detalle_factura (id_producto, cantidad, valor, id_factura) VALUES (%i,%i,%i,%i)' % (int(id_producto), int(unidades), int(valor), int(self.id_factura))
                        
                        self.cursor.execute(insert)
                        self.conn.commit()

                    
                    if insert:
                        messagebox.showinfo("Información", "Producto agregado a la Factura")
                        self.txtunidades.delete(0, END)  # Limpiar Cajas de Texto
                        self.cantidad_p.destroy()
                        self.restablecer_productos()
                    else:
                        messagebox.showerror("Error", "Error Al agregar producto")
                        self.cantidad_p.destroy()
                        self.restablecer_productos()
                else:
                    messagebox.showerror("Error", "No hay suficientes productos")
                    self.txtunidades.delete(0, END)
                    self.cantidad_p.destroy()
            except:
                messagebox.showerror("Error", "Error agregar producto a la factura")
                self.txtunidades.delete(0, END)
                self.cantidad_p.destroy()
                self.restablecer_productos()


    def iniciar_caja(self):
        self.iniciarCaja = Tk()
        self.iniciarCaja.wm_title("Iniciar Caja")
        self.iniciarCaja.grid_rowconfigure(0, weight=1)
        self.iniciarCaja.grid_columnconfigure(0, weight=1)

        self.label_monto = Label(self.iniciarCaja, text="Base: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_monto.grid(row=0, column=0, sticky=E + W, padx=2, pady=5)

        self.txtmonto = Entry(self.iniciarCaja)

        self.txtmonto.grid(row=0, column=1, sticky=E + W, padx=2, pady=5)

        self.connectb = Button(self.iniciarCaja, text="Iniciar", font="Helvetica 10 bold", command=self.iniCaja)

        self.connectb.grid(row=6, column=1, sticky=W, pady=3)


    def iniCaja(self):
        hoy = time.strftime("%Y%m%d")
        monto = self.txtmonto.get()
        monto = monto.strip()
        if monto == '':
            messagebox.showerror("Error", "Diligencie Todos los Campos")
            self.txtprod.delete(0, END)
        else:
            try:
                sql = "INSERT INTO ventas (inicio_caja, fin_caja, fecha_registro, estado_caja, codigo_cajero) VALUES ('%i',NULL,'%s','open','%i')" % (int(monto), hoy, int(self.datosUser[0]))
                self.cursor.execute(sql)
                self.conn.commit()
                if sql:
                    messagebox.showinfo("Información", "Inicio de caja registrado")
                    self.txtmonto.delete(0, END)  # Limpiar Cajas de Texto
                    self.iniciarCaja.destroy()
                    self.cliente.destroy()
                    self.MenuCajero()
                else:
                    messagebox.showerror("Error", "Error al Iniciar Caja")
                    self.iniciarCaja.destroy()
            except:
                messagebox.showerror("Error", "Error al Iniciar Caja")
                self.iniciarCaja.destroy()

    def cerrar_caja(self):
        hoy = time.strftime("%Y%m%d")
        try:
            sql = "SELECT SUM(total) FROM factura WHERE fecha_factura = '%s' AND estado = 'liquidado'" % hoy
            self.cursor.execute(sql)
            result_sql = self.cursor.fetchall()
            if result_sql:
                for j in result_sql:
                    totaldia = j[0]

                sql = "SELECT inicio_caja, codigo FROM ventas WHERE fecha_registro = '%s' AND estado_caja = 'open'" % hoy
                self.cursor.execute(sql)
                result_sql2 = self.cursor.fetchall()
                for i in result_sql2:
                    base = int(i[0])
                    id_venta = int(i[1])

                totaldia += base

                sql = "UPDATE ventas SET fin_caja = %i, estado_caja = 'close' WHERE codigo = %i" % (int(totaldia), int(id_venta))
                self.cursor.execute(sql)
                self.conn.commit()
                if sql:
                    messagebox.showinfo("Información", "Caja Cerrada")
                    self.cliente.destroy()
                    self.MenuCajero()
            else:
                print("mal")
                messagebox.showerror("Error", "No se pudo cerrar la Caja")
        except:
            messagebox.showerror("Error", "Error al Cerrar la Caja")
        

    def listar_clientes(self):

        self.listarclient = Tk()
        self.listarclient.title("Listado de Clientes")

        self.busqueda = Frame(self.listarclient)
        self.busqueda.grid(row=0, column=0, sticky=E + W, pady=5)
        self.label_busqueda = Label(self.busqueda, text="Buscar por documento: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_busqueda.grid(row=0, column=0, sticky=E + W)
        self.txtdocumid = Entry(self.busqueda)
        self.txtdocumid.grid(row=0, column=1, sticky=E + W)
        self.buscar = Button(self.busqueda, text="Buscar", font="Helvetica 10 bold", command=self.buscar_cliente)
        self.buscar.grid(row=0, column=2,  sticky=E + W, padx=2)
        self.restablecer = Button(self.busqueda, text="Restablecer", font="Helvetica 10 bold", command=self.restablecer_clientes)
        self.restablecer.grid(row=0, column=3,  sticky=E + W, padx=2)


        self.table = ttk.Treeview(self.listarclient, height=10)
        self.table["column"] = ('Nombres', 'Apellidos', 'Documento Id')
        self.table.heading("#0", text="Indice")
        self.table.column("#0", stretch=NO, width=60, anchor="w")
        self.table.heading("Nombres", text="Nombres")
        self.table.column("Nombres", width=120, anchor="center")
        self.table.heading("Apellidos", text="Apellidos")
        self.table.column("Apellidos", width=120, anchor="center")
        self.table.heading("Documento Id", text="Documento Id")
        self.table.column("Documento Id", width=100, anchor="center")
        self.table.grid(row=1, column=0, padx=5, pady=5)


        self.ysb = ttk.Scrollbar(self.listarclient, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=1, column=1, sticky='ns')

        self.cargar_tabla_clientes()

        
        mainloop()

    def cargar_tabla_clientes(self):
        consulta = 'SELECT nombres,apellidos,documento_id FROM clientes'
        self.cursor.execute(consulta)
        self.result = self.cursor.fetchall()

        indice=1
        if self.result:
            self.datos = self.result
            for i in self.datos:
                self.table.insert("", END, text=indice, values= i)
                indice += 1

        else:
            self.datos = 'NO HAY REGISTROS'
            self.table.insert("", END, text=indice, values= self.datos)



    def buscar_cliente(self):
        documid = self.txtdocumid.get()
        documid = documid.strip()
        if documid == '':
            self.restablecer_clientes()
        else:
            x = self.table.get_children() #variable para almacenar diccionario
            if x != '()': #verifica si hay almenos una fila
                for item in x:
                    values_values = (self.table.item(item)["values"])
                    if str(values_values[2]) != documid:
                        self.table.delete(item)

    def restablecer_clientes(self):
        x = self.table.get_children() #variable para almacenar diccionario
        if x != '()': #verifica si hay almenos una fila
                for item in x:
                    self.table.delete(item)
                self.cargar_tabla_clientes()


    def eliminar_cliente(self):
        self.elimcliente = Tk()
        self.elimcliente.wm_title("Eliminar Producto")
        self.elimcliente.grid_rowconfigure(0, weight=1)
        self.elimcliente.grid_columnconfigure(0, weight=1)

        self.label_documid = Label(self.elimcliente, text="Documento de Id. del cliente a Eliminar: ", anchor=W,
                                 background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")

        self.label_documid.grid(row=0, column=0, sticky=E + W)

        self.txtdocumid = Entry(self.elimcliente)

        self.txtdocumid.grid(row=0, column=1, sticky=E + W)

        self.connectb = Button(self.elimcliente, text="Eliminar", font="Helvetica 10 bold", command=self.ElimCliente)

        self.connectb.grid(row=6, column=1, sticky=W)


    def ElimCliente(self):
        documid = self.txtdocumid.get()
        documid = documid.strip()
        if documid == '':
            messagebox.showerror("Error", "Diligencie Todos los Campos")
            self.txtprod.delete(0, END)
        elif len(documid) > 10:
            messagebox.showerror("Error", "Ingrese un documento valido")
            self.txtprod.delete(0, END)
        else:
            sql = "DELETE FROM clientes WHERE documento_id = %s" % documid
            self.cursor.execute(sql)
            self.conn.commit()
            if sql:
                messagebox.showinfo("Información", "Cliente Eliminado")
                self.txtdocumid.delete(0, END)  # Limpiar Cajas de Texto
                self.elimcliente.destroy()
            else:
                messagebox.showerror("Error", "Error al Eliminar el Cliente")

    def agregar_cliente(self):
        self.agg_cliente = Tk()
        self.agg_cliente.wm_title("Agregar Cliente")
        self.agg_cliente.grid_rowconfigure(0, weight=1)
        self.agg_cliente.grid_columnconfigure(0, weight=1)

        self.label_nombres = Label(self.agg_cliente, text="Nombres: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_apellidos = Label(self.agg_cliente, text="Apellidos: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_documento = Label(self.agg_cliente, text="Num. Documento:", anchor=W,
                                      background="dark slate gray",
                                      foreground="white", font="Helvetica 8  bold")
        
        self.label_nombres.grid(row=1, column=0, sticky=E + W)
        self.label_apellidos.grid(row=2, column=0, sticky=E + W)
        self.label_documento.grid(row=3, column=0, sticky=E + W)
        
        self.txtnombres = Entry(self.agg_cliente)
        self.txtapellidos = Entry(self.agg_cliente)
        self.txtdocum = Entry(self.agg_cliente)
        
        self.txtnombres.grid(row=1, column=1, sticky=E + W)
        self.txtapellidos.grid(row=2, column=1, sticky=E + W)
        self.txtdocum.grid(row=3, column=1, sticky=E + W)
        

        self.connectb = Button(self.agg_cliente, text="Registrar", font="Helvetica 10 bold", command=self.aggCliente)

        self.connectb.grid(row=4, column=1, sticky=W)

    def aggCliente(self):
        nombres = self.txtnombres.get()
        apellidos = self.txtapellidos.get()
        docum = self.txtdocum.get()
        docum=docum.strip()

        if nombres == '' or apellidos == '' or docum == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.agg_cliente.destroy(0, END)
        elif len(docum)>10:
            messagebox.showerror("error", "El número de documento es incorrecto")
            self.agg_cliente.destroy(0, END)
        else:
            sql = "INSERT INTO clientes (codigo, nombres, apellidos, documento_id) VALUES ('', '%s', '%s', '%s')" % (
                nombres, apellidos, docum)
            self.cursor.execute(sql)
            self.conn.commit()


            if sql:
                messagebox.showinfo("Información", "Cliente Registrado")
                self.txtnombres.delete(0, END)
                self.txtapellidos.delete(0, END)
                self.txtdocum.delete(0, END)
                self.agg_cliente.destroy()
            else:
                messagebox.showerror("error", "Error al Registrar el Cliente")

    def actualizar_cliente(self):
        self.act_cliente = Tk()
        self.act_cliente.wm_title("Actualizar Cliente")
        self.act_cliente.grid_rowconfigure(0, weight=1)
        self.act_cliente.grid_columnconfigure(0, weight=1)

        self.label_nombres = Label(self.act_cliente, text="Nombres: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_apellidos = Label(self.act_cliente, text="Apellidos: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_documento = Label(self.act_cliente, text="Num. Documento:", anchor=W,
                                      background="dark slate gray",
                                      foreground="white", font="Helvetica 8  bold")
        
        self.label_nombres.grid(row=1, column=0, sticky=E + W)
        self.label_apellidos.grid(row=2, column=0, sticky=E + W)
        self.label_documento.grid(row=3, column=0, sticky=E + W)
        
        self.txtnombres = Entry(self.act_cliente)
        self.txtapellidos = Entry(self.act_cliente)
        self.txtdocum = Entry(self.act_cliente)
        
        self.txtnombres.grid(row=1, column=1, sticky=E + W)
        self.txtapellidos.grid(row=2, column=1, sticky=E + W)
        self.txtdocum.grid(row=3, column=1, sticky=E + W)
        

        self.connectb = Button(self.act_cliente, text="Actualizar", font="Helvetica 10 bold", command=self.actCliente)

        self.connectb.grid(row=4, column=1, sticky=W)

    def actCliente(self):
        nombres = self.txtnombres.get()
        apellidos = self.txtapellidos.get()
        docum = self.txtdocum.get()
        docum=docum.strip()

        if nombres == '' or apellidos == '' or docum == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.act_cliente.destroy(0, END)
        elif len(docum)>10:
            messagebox.showerror("error", "El número de documento es incorrecto")
            self.act_cliente.destroy(0, END)
        else:
            sql = "UPDATE clientes SET nombres='%s', apellidos='%s' WHERE documento_id=%s" % (
                nombres, apellidos, docum)
            self.cursor.execute(sql)
            self.conn.commit()

            if sql:
                messagebox.showinfo("Información", "Cliente Actualizado")
                self.txtnombres.delete(0, END)
                self.txtapellidos.delete(0, END)
                self.txtdocum.delete(0, END)
                self.act_cliente.destroy()
            else:
                messagebox.showerror("error", "Error al Actualizar el Cliente")

    def MenuInventario(self):

        self.invent = Tk()
        self.invent.title("Menu Inventario")
        self.menu = Menu(self.invent)
        self.invent.config(menu=self.menu)
        self.invent.geometry("500x500+0+0")
        self.invent.title("Inventario - " + self.datosUser[3])
        self.alertas = Menu(self.menu)  # un item del menu
        self.menu.add_cascade(label="Alertas",
                              menu=self.alertas)  # se agrega el menu alertas como una casacada del menu principal
        self.alertas.add_command(label="Productos con Stock Mínimo", command=self.alertas_Productos)

        self.inventario = Menu(self.menu)
        self.menu.add_cascade(label="Inventario", menu=self.inventario)
        self.inventario.add_command(label="Ver Listado de Productos", command=self.Listar_Productos)
        self.inventario.add_command(label="Agregar Producto", command=self.Crear_Productos)
        self.inventario.add_command(label="Actualizar Producto", command=self.Act_Productos)
        self.inventario.add_command(label="Eliminar Producto", command=self.Elim_Productos)
        self.inventario.add_command(label="Agregar Existencia de Productos", command=self.exis_Productos)

        self.clientes = Menu(self.menu)
        self.menu.add_cascade(label="Clientes", menu=self.clientes)
        self.clientes.add_command(label="Registrar un Cliente", command=self.agregar_cliente)
        self.clientes.add_command(label="Actualizar un Cliente", command=self.actualizar_cliente)
        self.clientes.add_command(label="Eliminar un Cliente", command=self.eliminar_cliente)
        self.clientes.add_command(label="Lista de Clientes", command=self.listar_clientes)

        self.usuarios = Menu(self.menu)
        self.menu.add_cascade(label="Perfil", menu=self.usuarios)
        self.usuarios.add_command(label="Actualizar Datos Personales", command=self.Actualizar_Usuario)

        self.salir = Menu(self.menu)
        self.menu.add_cascade(label="Salir", menu=self.salir)
        self.salir.add_command(label="Cerrar Sesión", command=self.cierra_invent)

    def Actualizar_Usuario(self):
        self.actuser = Tk()
        self.actuser.wm_title("Actualizar Datos")
        self.actuser.grid_rowconfigure(0, weight=1)
        self.actuser.grid_columnconfigure(0, weight=1)

        self.label_email = Label(self.actuser, text="Email: ", anchor=W, background="dark slate gray",
                                 foreground="white", font="Helvetica 8  bold")
        self.label_contraseña = Label(self.actuser, text="Contraseña:", anchor=W,
                                      background="dark slate gray",
                                      foreground="white", font="Helvetica 8  bold")
        self.label_nombre = Label(self.actuser, text="Nombre:", anchor=W,
                                  background="dark slate gray",
                                  foreground="white", font="Helvetica 8  bold")
        
        self.label_email.grid(row=1, column=0, sticky=E + W)
        self.label_contraseña.grid(row=2, column=0, sticky=E + W)
        self.label_nombre.grid(row=3, column=0, sticky=E + W)
        
        self.txtemail = Entry(self.actuser)
        self.txtcontra = Entry(self.actuser, show="*")
        self.txtnombre = Entry(self.actuser)
        
        self.txtemail.grid(row=1, column=1, sticky=E + W)
        self.txtcontra.grid(row=2, column=1, sticky=E + W)
        self.txtnombre.grid(row=3, column=1, sticky=E + W)
        

        self.connectb = Button(self.actuser, text="Actualizar", font="Helvetica 10 bold", command=self.ActuaUs)

        self.connectb.grid(row=6, column=1, sticky=W)

    def ActuaUs(self):
        idUser = self.datosUser[0]
        email = self.txtemail.get()
        passw = self.txtcontra.get()
        nombre = self.txtnombre.get()

        if email == '' or passw == '' or nombre == '':
            messagebox.showerror("error", "Diligencie Todos los Campos")
            self.actuser.destroy(0, END)
        else:
            sql = "UPDATE usuarios SET email='%s', pass='%s', nombre='%s' WHERE id = %i" % (
                email, passw, nombre, int(idUser))
            self.cursor.execute(sql)
            self.conn.commit()

            if sql:
                messagebox.showinfo("Información", "Usuario Actualizado")
                self.txtemail.delete(0, END)
                self.txtcontra.delete(0, END)
                self.txtnombre.delete(0, END)
                self.actuser.destroy()
            else:
                messagebox.showerror("error", "Error al Actualizar el Producto")


def main():
    s = socket()
    s.connect(("localhost", 35000))

    while True:
        output_data = input("Desea Ingresar al Supermercado (S/N):  ")

        if output_data == 's' or output_data == 'S':

            try:
                s.send(output_data)
            except TypeError:
                s.send(bytes(output_data, "utf-8"))

            # Recibir respuesta.
            input_data = s.recv(1024)
            if input_data == bytes("1", "utf-8"):
                root = Tk()
                app = Servidor(root)
                root.mainloop()
        else:
            print("Terminando Conexión")
            exit()


if __name__ == "__main__":
    main()
