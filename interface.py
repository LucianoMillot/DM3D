import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from mesh_generator import generate_bottom_enclousure, generate_power_strip

def create_interface():
    def modelise():
        
        plug = type_combobox.get()
        
        try:
            number_of_plugs = int(number_of_plugs_entry.get())
            if number_of_plugs < 2 or number_of_plugs > 8:
                raise ValueError("Number of plugs must be an integer between 2 and 8")

            di1 = float(d1.get())
            if di1 < 5 or di1 > 60:
                raise ValueError("D1 must be between 5 and 60")
            
            di2 = float(d2.get())
            if di2 < 5 or di2 > 20:
                raise ValueError("D2 must be between 5 and 60")
            
            di3 = float(d3.get())
            if di3 < 5 or di3 > 20:
                raise ValueError("D3 must be between 5 and 60")


        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return  
        
        
        generate_power_strip(num_plugs=number_of_plugs, plug_type=plug,lateral_gap=di2, vertical_gap=di3, distance_between_plugs=di1)
        generate_bottom_enclousure(num_plugs=number_of_plugs,lateral_gap=di2, vertical_gap=di3, distance_between_plugs=di1, path="")
        messagebox.showinfo("Modelisation Completed", "Your powerstrip has been modelled successfully!")

    # Create the main window
    root = tk.Tk()
    root.title("Powerstrip Model")

    text_frame = ttk.Frame(root)
    text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    doc_text = ttk.Label(text_frame, text="Welcome to the Power Strip Model Generator.")
    doc_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a frame for the image on the left
    main_image_frame = ttk.Frame(root)
    main_image_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Load the image
    powerstrip = tk.PhotoImage(file="Images/powerstrip.png")

    # Display the image
    powerstrip_label = tk.Label(main_image_frame, image=powerstrip)
    powerstrip_label.pack()

    # Create a frame for the form on the right
    right_frame = ttk.Frame(root)
    right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    form_frame = ttk.Frame(right_frame)
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    # Form title
    form_title = ttk.Label(form_frame, text="Enter Your Parameters", width=20, font=("bold", 20))
    form_title.grid(row=0, columnspan=2, padx=5, pady=5)

    # Dropdown menu for plug type
    type_label = ttk.Label(form_frame, text="Type:")
    type_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    type_values = ["European", "American"]
    type_combobox = ttk.Combobox(form_frame, values=type_values, state="readonly")
    type_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    type_combobox.current(0)  # Select the first element by default

    # Entry field for the number of plugs
    number_of_plugs_label = ttk.Label(form_frame, text="Number of Plugs:")
    number_of_plugs_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    number_of_plugs_entry = ttk.Entry(form_frame)
    number_of_plugs_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Entry field for the distance between plugs
    d1_label = ttk.Label(form_frame, text="D1 (mm) :")
    d1_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    d1 = ttk.Entry(form_frame)
    d1.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    d2_label = ttk.Label(form_frame, text="D2 (mm) :")
    d2_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    d2 = ttk.Entry(form_frame)
    d2.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    d3_label = ttk.Label(form_frame, text="D3 (mm) :")
    d3_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
    d3 = ttk.Entry(form_frame)
    d3.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Button to initiate modelling
    modelise_button = ttk.Button(form_frame, text="Modelise", command=modelise)
    modelise_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    root.mainloop()
