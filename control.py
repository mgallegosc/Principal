# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 15:02:21 2023

@author: m987987
"""
# --------------------------------------------------------------------
# -------------------- Control de Flujo-------------------------------
# ----------------------Importaciones---------------------------------
from generador_inventario_clientes import obtener_inventario_clientes
from generador_inventario_productos import obtener_inventario_productos
from funciones_utiles import crear_id
from producto_clase import Producto
from carrito_clase import Carrito
import json
import pickle
#--------------Obeter los inventarios de clientes y Productos---------
inventario_clientes = obtener_inventario_clientes()
inventario_productos = obtener_inventario_productos()
def inventarios_Productos_integers():
    inventario_productos['leche']['disponible']=5
    inventario_productos['arroz']['disponible']=10
    inventario_productos['azucar']['disponible']=15
    inventario_productos['leche']['costo_unitario']=1000
    inventario_productos['arroz']['costo_unitario']=2000
    inventario_productos['azucar']['costo_unitario']=1500
inventarios_Productos_integers()          
                 
#----------------------Menu de Opciones Main Loop---------------------
Menu_Opciones = {1:'Agregar Productos al carrito',
                 2:'Pagar',3:'Facturar | Detalle',0:'Salir'}
# ---------------------Inicializar Variables--------------------------
inventario_de_carritos = {}
# -------------------Funciones/Acciones-------------------------------
#-1 Obtener carritos del cliente
def obtener_carritos(cedula_cliente):
    lista_carritos = []
    for carrito in inventario_de_carritos.values():
        cedula = carrito.get('cliente').get('cedula')
        if cedula_cliente == cedula:
            lista_carritos.append(carrito)
    return lista_carritos

def obtener_carrito__por_id(id):
    mi_carrito = None
    for carrito in inventario_de_carritos.values():
        if id == carrito.identificador:
            mi_carrito = carrito
    return mi_carrito

#-2 Agregar Carrito al inventario de carritos
def agregar_carrito_al_inventario(cedula_cliente):
    id_nuevo_carrito = crear_id()
    # quien es el cliente?
    # buscar el cliente -> en el inventario de clientes
    inventario_clientes = obtener_inventario_clientes()
    el_cliente = inventario_clientes.get(cedula_cliente)
    # aqui va los parametros de la clase carrito
    inventario_de_carritos.update({id_nuevo_carrito: Carrito(cliente=el_cliente)})

#-3 revisar disponible en inventario de productos
def revisar_inventario_productos(producto, cantidad):
    if inventario_productos[producto]['disponible'] < cantidad:
        return 0
    if inventario_productos[producto]['disponible'] >= cantidad:
        return 1

#-4 Actualizar inventario productos
def actualizar_invetario_productos(producto,cantidad):
    inventario_productos[producto]['disponible'] -= cantidad


# # # ----------------------Control de flujo-------------------------------
def control_flujo():
    cliente_cedula = 0
    option = 0
    ML_Control = 0
    #-------------Peedir Datos a cliente ----------------------
    print('Por Favor ingrese su numero de cedula')
    cliente_cedula = input('Cedula:')
    #-------------Verificar si, cliente No existe, salir-------       
    if cliente_cedula not in inventario_clientes:
        print('El Cliente con cedula:',cliente_cedula,' No existe')
        ML_Control = 0
    #-------------si cliente existe, continuar ----------------    
    if cliente_cedula in inventario_clientes:
        print('Bienvenido Cliente :', cliente_cedula)        
    #-------------Obtener los carritos del cliente----------------------
        lista_carritos_del_cliente = obtener_carritos(cedula_cliente=cliente_cedula)
        if len(lista_carritos_del_cliente) == 0:       
    #-------------Si no tiene Carritos, crear uno----------------------
            agregar_carrito_al_inventario(cedula_cliente=cliente_cedula)
        mi_carrito = obtener_carritos(cedula_cliente=cliente_cedula)[0]
        print('info carrito :', obtener_carritos(cedula_cliente=cliente_cedula))
        ML_Control = 1
    
    #---------------------Loop Principal --------------------------      
    while ML_Control == 1:
    #---------------------Menu de Opciones-------------------------
        print('*'*50)
        print('Por Favor seleccione una opcion del menu:')
        for opciones in Menu_Opciones:
            print(opciones,":",Menu_Opciones.get(opciones))
        option = int(input('Opcion:' )) 
        print('*'*50)
        print('A seleccionado la opcion #', option,":", Menu_Opciones.get(option))
        print('*'*50)
    #---------------------Ejecutar Opciones -----------------------
        #Agregar productos al carrito
        if option == 1:
              print('por favor ingrese producto y cantidad')
              producto1= input('Producto:' ) #'leche' 
              cantidad1 = int(input('Cantidad:' )) #2 
               #Ejecutar funcion: revisar inventario de productos
              if revisar_inventario_productos(producto1, cantidad1) == 0:
                  print('la cantidad de', producto1, 'es mayor al disponible')
                  print(inventario_productos.get(producto1))
                  ML_Control = 1                 
              if revisar_inventario_productos(producto1,cantidad1) == 1:
              #Obtner item de invetario productos
                  item = inventario_productos.get(producto1)
                  #Agregar item a carrito de cliente
                  mi_carrito.agregar_item(Producto(nombre= item, cantidad=cantidad1))
                  print('Producto agregado satisfactoriamente')                  
                  ML_Control = 1
        #Procesar pago
        if option == 2:
            saldo = 0
            for p in mi_carrito.lista_articulos:
                saldo += p['nombre']['costo_unitario']*p['cantidad']
            print('El Monto total es de $:', saldo)
            ML_Control = 1
            
        #Facturar los productos al carrito
        if option == 3:
             saldo1 = 0
             for p in mi_carrito.lista_articulos:
                 producto = p['nombre']['producto']
                 cantidad = p['cantidad']
                 costo = p['nombre']['costo_unitario']
                 saldo1 = p['nombre']['costo_unitario']*p['cantidad']
                 print(producto, cantidad,'x', costo,'| total',producto,':','$',saldo1)
             print('*'*50)
             print('Total $:',saldo)
             json.dump(mi_carrito.lista_articulos, open("factura_cliente.txt",'w'))
             print('La Factura Cliente #:',cliente_cedula,'ah sido creada' )
             ML_Control = 1
        #Salir del menu
        if option == 0:
            print('Hasta Luego gracias por su compra')
            ML_Control = 0

#-------------Fin del Codigo, salir-------------------------        




    