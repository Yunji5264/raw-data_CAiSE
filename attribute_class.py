import pandas as pd
import tkinter as tk
from tkinter import ttk
from class_predefine import *
from uml_class import Complementary_Information, Spatial_Parameter, Temporal_Parameter, Existing_Indicator


# Define classes for data storage
class ThemeSelection:
    def __init__(self, main_theme, subtheme=None):
        self.main_theme = main_theme
        self.subtheme = subtheme

    def to_dict(self):
        return {"main_theme": self.main_theme, "subtheme": self.subtheme}

class ColumnClassification:
    def __init__(self, column_name, data_type, additional_info=None):
        self.column_name = column_name
        self.data_type = data_type
        self.additional_info = additional_info

    def to_dict(self):
        return {
            "column_name": self.column_name,
            "data_type": self.data_type,
            "additional_info": self.additional_info.to_dict() if self.additional_info else None,
        }

def infer_data_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "int"
    elif pd.api.types.is_float_dtype(series):
        return "float"
    elif pd.api.types.is_string_dtype(series):
        return "text"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    else:
        return "unknown"

class ThemeSelectionPopup:
    def __init__(self, parent, theme_structure):
        """Initialize the popup with a scrollable theme selection."""
        self.theme_structure = theme_structure
        self.selected_theme = None

        # Create popup window
        self.popup = tk.Toplevel(parent)
        self.popup.title("Select Theme")

        # Add label
        tk.Label(self.popup, text="Select a Theme").pack(pady=5)

        # Create scrollable frame
        frame = tk.Frame(self.popup)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Radio button variable
        self.theme_var = tk.StringVar(value="")  # To store the selected theme path

        # Dynamically create nested radio buttons
        self.create_radiobuttons(self.theme_structure, self.scrollable_frame)

        # Add confirm button
        confirm_btn = tk.Button(self.popup, text="Confirm", command=self.confirm_selection)
        confirm_btn.pack(pady=10)

    def create_radiobuttons(self, structure, parent, path=""):
        """Recursively create radio buttons for themes."""
        for key, substructure in structure.items():
            current_path = f"{path}/{key}".strip("/")
            tk.Radiobutton(
                parent,
                text=key,
                variable=self.theme_var,
                value=current_path
            ).pack(anchor="w", pady=2)

            if isinstance(substructure, dict) and substructure:  # If there are sub-themes
                sub_frame = tk.Frame(parent)
                sub_frame.pack(anchor="w", padx=20)  # Indent for sub-themes
                self.create_radiobuttons(substructure, sub_frame, current_path)

    def confirm_selection(self):
        """Confirm the user's selection and close the popup."""
        self.selected_theme = self.theme_var.get()
        self.popup.destroy()

    def get_selection(self):
        """Return the selected theme path."""
        self.popup.wait_window()  # Wait for the popup to close
        return self.selected_theme

class ColumnClassifierApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df

        # Lists to store classified column objects by type
        self.complementary_info_list = []
        self.spatial_parameters_list = []
        self.temporal_parameters_list = []
        self.indicators_list = []

        self.column_objects = []  # General list for all classified columns

        self.result = None

        # Counters for auto-generating codes
        self.spatial_counter = 1
        self.temporal_counter = 1
        self.ci_counter = 1
        self.indicator_counter = 1

        self.used_levels = set()  # To track used levels across all hierarchies

        self.root.title("Column Classifier")
        self.root.geometry("800x600")  # Set window size

        tk.Label(root, text="Classify Columns", font=("Helvetica", 16)).pack(pady=10)

        # Scrollable frame setup
        container = tk.Frame(root)
        container.pack(expand=True, fill="both", padx=10, pady=10)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate scrollable frame with column classifiers
        for i, col in enumerate(self.df.columns):
            tk.Label(scrollable_frame, text=f"{col} (Type: {infer_data_type(self.df[col])}):", font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", padx=5, pady=5)

            combo = ttk.Combobox(
                scrollable_frame,
                values=["Spatial Parameter", "Temporal Parameter", "Complementary Information", "Indicator"],
                state="readonly"
            )
            combo.grid(row=i, column=1, padx=5, pady=5)
            combo.set("Select")
            combo.bind("<<ComboboxSelected>>", lambda e, col=col, combo=combo: self.handle_selection(combo, col))

        # Add submit button
        submit_button = tk.Button(root, text="Submit", command=self.submit)
        submit_button.pack(pady=10)

    def handle_selection(self, combo, col):
        selected_value = combo.get()
        col_type = infer_data_type(self.df[col])
        if selected_value == "Spatial Parameter":
            self.create_spatial_parameter(col, col_type)
        elif selected_value == "Temporal Parameter":
            self.create_temporal_parameter(col, col_type)
        elif selected_value == "Complementary Information":
            self.create_complementary_info(col, col_type)
        elif selected_value == "Indicator":
            self.create_indicator(col, col_type)

    def create_complementary_info(self, col, col_type):
        ci_code = f"comp{self.ci_counter}"
        self.ci_counter += 1

        obj = Complementary_Information(
            dataName=col,
            dataDescription=f"Description for {col}",
            dataType=col_type,
            ciCode=ci_code
        )
        self.complementary_info_list.append(obj)
        self.column_objects.append(obj)

    def create_spatial_parameter(self, col, col_type):
        param_code = f"sp{self.spatial_counter}"
        self.spatial_counter += 1

        # Combine and deduplicate spatial levels
        available_levels = {level for group in hS_F for _, level in group} - self.used_levels
        spatial_level = self.select_level("Select Spatial Level", sorted(available_levels))
        self.used_levels.add(spatial_level)

        obj = Spatial_Parameter(
            dataName=col,
            dataDescription=f"Description for {col}",
            dataType=col_type,
            parameterCode=param_code,
            spatialLevel=spatial_level
        )
        self.spatial_parameters_list.append(obj)
        self.column_objects.append(obj)

    def create_temporal_parameter(self, col, col_type):
        param_code = f"tp{self.temporal_counter}"
        self.temporal_counter += 1

        # Combine and deduplicate temporal levels
        available_levels = {level for group in hT_F for _, level in group} - self.used_levels
        temporal_level = self.select_level("Select Temporal Level", sorted(available_levels))
        self.used_levels.add(temporal_level)

        obj = Temporal_Parameter(
            dataName=col,
            dataDescription=f"Description for {col}",
            dataType=col_type,
            parameterCode=param_code,
            temporalLevel=temporal_level
        )
        self.temporal_parameters_list.append(obj)
        self.column_objects.append(obj)

    def create_indicator(self, col, col_type):
        indicator_code = f"ind{self.indicator_counter}"
        self.indicator_counter += 1

        # Open theme selection popup
        theme_popup = ThemeSelectionPopup(self.root, theme_folder_structure)
        theme = theme_popup.get_selection()

        obj = Existing_Indicator(
            dataName=col,
            dataDescription=f"Description for {col}",
            dataType=col_type,
            indicatorCode=indicator_code,
            indicatorTheme=theme
        )
        self.indicators_list.append(obj)
        self.column_objects.append(obj)

    def select_level(self, title, available_levels):
        level_window = tk.Toplevel(self.root)
        level_window.title(title)

        level_listbox = tk.Listbox(level_window, height=10, width=50)
        for level in available_levels:
            level_listbox.insert(tk.END, level)
        level_listbox.pack(pady=10)

        selected_level = tk.StringVar()

        def confirm_selection():
            selected = level_listbox.curselection()
            if selected:
                selected_level.set(level_listbox.get(selected))
            level_window.destroy()

        confirm_btn = tk.Button(level_window, text="Confirm", command=confirm_selection)
        confirm_btn.pack(pady=10)

        level_window.wait_window()
        return selected_level.get()

    def submit(self):
        # Prepare the result dictionary
        self.result = {
            "Spatial Parameters": self.spatial_parameters_list,
            "Temporal Parameters": self.temporal_parameters_list,
            "Complementary Information": self.complementary_info_list,
            "Indicators": self.indicators_list
        }

        # Print the classified data (optional)
        print("Classified Columns:")

        print("\nSpatial Parameters:")
        for obj in self.spatial_parameters_list:
            print(obj.to_dict())

        print("\nTemporal Parameters:")
        for obj in self.temporal_parameters_list:
            print(obj.to_dict())

        print("\nComplementary Information:")
        for obj in self.complementary_info_list:
            print(obj.to_dict())

        print("\nIndicators:")
        for obj in self.indicators_list:
            print(obj.to_dict())

        self.root.destroy()  # Close the Tkinter window

    def get_result(self):
        return self.result
