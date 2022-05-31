import resolvedor
from tkinter import *

alg= resolvedor.SA()
 
window = Tk()
window.title("Alocação de Produtos")
window.geometry("300x250")
window.configure(background= "#474A51")

text1= Label(window,text = "Insira um arquivo:",background="#474A51",foreground="#fff")
text1.grid(column=0,row=0)

button = Button(text ="Abrir Arquivo", command=alg.arm.openFile)
button.grid(column=0,row=1)

button2 = Button(text ="Imprimir", command = alg.arm.imprimir)
button2.grid(column=0,row=2)

button3 = Button(text="Resolver",command=alg.sa)
button3.grid(column=0,row=5)


window.mainloop()