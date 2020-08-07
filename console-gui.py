import tkinter

console_font = "Segoe 8"

consoleGUI = tkinter.Tk()
consoleGUI.title ("GoogleAssistant2Windows Console")
consoleGUI.iconbitmap(default=".files\\GA2W-logo.ico")
consoleGUI.resizable(True, True)
consoleGUI.geometry("800x260")
consoleGUI.configure (bg="white")

console_output = tkinter.Text (consoleGUI, bg="white", height=16, bd=1,
    font=console_font, borderwidth = 1, relief="solid")

console_prompt = tkinter.Entry (consoleGUI, bd=0, font=console_font, borderwidth = 1, relief="solid")

console_output.pack (fill="x", padx=5, pady=5)
console_prompt.pack (fill="x", padx=5)

consoleGUI.mainloop()
