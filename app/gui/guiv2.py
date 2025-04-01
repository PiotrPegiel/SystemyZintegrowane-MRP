import ttkbootstrap as ttk
from tksheet import Sheet
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from ttkbootstrap.tableview import Tableview

class DataEntryForm(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.Items=[]
        self.pack(fill=BOTH, expand=YES)
        self.colors = app.style.colors

        # form variables

        self.nazwa = ttk.StringVar(value="")
        self.stan_magazynowy = ttk.IntVar(value=0)
        self.czas_produkcji = ttk.IntVar(value=0)
        self.wielkosc_partii = ttk.IntVar(value=0)

        # form header
        self.product_form = ttk.Frame(self, style='bg.TFrame')
        self.product_form.pack(fill=X, side=LEFT)
        hdr_txt = "Please enter info" 
        hdr = ttk.Label(master=self.product_form, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=0)


        self.create_form_entry("Nazwa Produktu", self.nazwa, self.product_form)
        self.create_form_entry("Stan magazynowy", self.stan_magazynowy, self.product_form)
        self.create_form_entry("Czas produkcji", self.czas_produkcji, self.product_form)
        self.create_form_entry("Wielkosc partii", self.wielkosc_partii, self.product_form)

        self.create_buttonbox(self.product_form)

        

        # product list
        self.product_list = ttk.Frame(self.product_form, style='bg.TFrame')
        self.product_list.pack(fill=X)

        ## backup summary (collapsible)
        self.bus_cf = CollapsingFrame(self.product_list)
        self.bus_cf.pack(fill=X, pady=1)

        ## container
        self.bus_frm = ttk.Frame(self.bus_cf, padding=5)
        self.bus_frm.columnconfigure(1, weight=1)
        self.bus_cf.add(
            child=self.bus_frm, 
            title='Produkty:', 
            bootstyle=SECONDARY)

        sub_btn = ttk.Button(
            master=self.product_list,
            text="Calculate",
            bootstyle=SUCCESS,
            command=self.on_generate_GHP,
            width=10,
            
        )
        sub_btn.pack(side=RIGHT, padx=15, pady=(0, 15))

        

    def create_form_entry(self, label, variable, mast):
        """Create a single form entry"""
        container = ttk.Frame(master=mast)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=20)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self, mast):
        """Create the application buttonbox"""
        container = ttk.Frame(master=mast)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="Dodaj",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):
        """Print the contents to console and return the values."""
        print("Nazwa Produktu:", self.nazwa.get())
        print("Stan Magazynowy:", self.stan_magazynowy.get())
        print("Czas Produkcji:", self.czas_produkcji.get())
        print("Wielkość Partii:", self.wielkosc_partii.get())
        Item={'Nazwa': self.nazwa.get(),
              'Stan': self.stan_magazynowy.get(),
              'Czas': self.czas_produkcji.get(),
              'Partia':self.wielkosc_partii.get()}
        self.Items.append(Item)
        self.update_item_list()
        print(self.Items)
        # print("Element Nadrzędny:", self.cbo.get())

    def update_item_list(self):
        for i in range(len(self.Items)):
            lbl = ttk.Label(self.bus_frm, text=self.Items[i]["Nazwa"])
            lbl.grid(row=i*2, column=0, sticky=W, pady=2)
            lbl = ttk.Label(self.bus_frm, text=self.Items[i]["Stan"])
            lbl.grid(row=i*2, column=1, sticky=EW, padx=5, pady=2)
            # self.setvar('Stan', self.Items[i]["Stan"])
            sep = ttk.Separator(self.bus_frm, bootstyle=SECONDARY, orient="horizontal")
            sep.grid(row=i*2+1, column=0, columnspan=2, pady=10, sticky=EW)

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()

    def on_generate_GHP(self):
        self.frame = tk.Frame(self)
        self.frame.pack(padx=20, pady=20, side=RIGHT)

        for i in range(len(self.Items)):
            self.headers= ["1","2","3","4","5","6","7","8","9","10"]
            self.indexes= ['Przewidywany popyt','Produkcja','Dostępne']
            self.table_data = [['', "", "","",28,"",40,"","",""],
                            ['', "", "","",28,"",30,"","",""],
                            [2,2,2,2,10,10,0,0,0,0]]
            self.i = Sheet(self.frame,
                            data = self.table_data,width=800,default_column_width=60,
                            default_row_index_width=300, row_index_align="e")
            self.i.enable_bindings()
            self.i.pack(padx=20, pady=20)
            self.i.set_header_data(self.headers)
            self.i.set_index_data(self.indexes)

        # poprzednie rozwiązanie tabeli
        # coldata = [
        #     "Okres","1","2","3","4","5","6","7","8","9","10"
        # ]

        # rowdata = [
        #     ('Przewidywany popyt', '', "", "","",29,"",40,"","",""),
        #     ('Produkcja', '', "", "","",28,"",30,"","",""),
        #     ('Dostępne', 2,2,2,2,10,10,0,0,0,0),
        # ]

        # dt = Tableview(
        #     master=app,
        #     coldata=coldata,
        #     rowdata=rowdata,
        #     bootstyle=PRIMARY,
        #     stripecolor=("blue", None),
        #     autofit=True
        # )
        # dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0



    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button 
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure()
        else:
            child.grid()
            child.btn.configure()



if __name__ == "__main__":

    app = ttk.Window("Data Entry", "litera", resizable=(False, False))
    DataEntryForm(app)
    app.mainloop()
