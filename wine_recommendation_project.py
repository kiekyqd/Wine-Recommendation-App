import csv
import os
import tkinter as tk
import pandas as pd
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from RangeSlider.RangeSlider import RangeSliderH
from tkinter import BOTH, Y


def get_wine_recommendations(preferences, min_price=0, max_price=5000):
    """
    Recommends wines based on the user's preferences and price range.
    """    
    # Load the wine data
    df = pd.read_csv('cleaned_wine_data.csv')

    # Initialize a score for each wine
    df['score'] = 0

    # For each preference, add 1 to the score of each wine that mentions the preference in its description
    for preference in preferences.values():
        df['score'] += df['Description'].str.contains(preference, case=False, na=False)
    
    # Filter the wines by price
    df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
    
    # Drop the duplicates
    df.drop_duplicates(subset=['Winery', 'Variety', 'Country', 'Points', 'Description'], keep='first', inplace=True)

    # Sort wines by score and points
    df = df.sort_values(['score', 'Points'], ascending=[False, False])

    # Return the top 5 wines as a list of dictionaries
    recommendations = df.head(5)[['Winery', 'Variety', 'Country', 'Points', 'Description', 'Price']].apply(lambda row: {
    "Winery": row['Winery'],
    "Variety": row['Variety'],
    "Country": row['Country'],
    "Points": row['Points'],
    "Description": row['Description'],
    "Price": row['Price']
    }, axis=1)

    return recommendations.tolist()




def check_username(username):
    """
    Checks if a username already exists in 'user_preferences.csv'.
    """    
    if not os.path.exists('user_preferences.csv'):  # If file does not exist, no usernames exist yet
        return False
    with open('user_preferences.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == username:  # Check if username is in the first column of a row
                return True
    return False

def submit():
    """
    Submits user input from the form, validates it, and stores it in 'user_preferences.csv'.
    """    
    # Get user input
    username = entry1.get()
    if check_username(username):
        messagebox.showerror("Error", "Username already exists!")
        return
    preferences = {key: var.get() for key, var in vars.items()}
    
    # Check if at least one preference is chosen
    if all(not val for val in preferences.values()):
        messagebox.showerror("Error", "At least one preference must be chosen!")
        return
    
    # Get the price range values
    min_price, max_price = price_slider.getValues()

    # Store in CSV
    with open('user_preferences.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username] + list(preferences.values()) + [min_price, max_price])
        
    # Show a message box
    messagebox.showinfo("Success", "Preferences saved successfully!")


def show_preferences():
    """
    Displays the preferences of a specific user in a new window.
    """    
    username = entry1.get()
    if not check_username(username):
        messagebox.showerror("Error", "Username does not exist!")
        return
    # Create a new window
    new_window = tk.Toplevel(window)
    with open('user_preferences.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:  # Find the user's row
                for i, preference in enumerate(row[1:len(preference_categories)+1], start=1):  # Start at 1 to skip username
                    label = tk.Label(new_window, text=f"{list(preference_categories.keys())[i-1]}: {preference}", 
                                     font=("Work Sans", 10), anchor="w", justify=tk.LEFT)
                    label.pack(fill='x')
                min_price, max_price = float(row[-2]), float(row[-1])
                price_label = tk.Label(new_window, text=f"Price Range: ${min_price:.1f} - ${max_price:.1f}", font=("Work Sans", 10), anchor="w", justify=tk.LEFT)
                price_label.pack(fill='x')



def clear_preferences():
    """
    Removes the preferences of a specific user from 'user_preferences.csv'.
    """    
    username = entry1.get()
    if not check_username(username):
        messagebox.showerror("Error", "Username does not exist!")
        return
    # Read all data
    with open('user_preferences.csv', 'r') as f:
        data = list(csv.reader(f))
    # Write only data for other users
    with open('user_preferences.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            if row[0] != username:
                writer.writerow(row)
    messagebox.showinfo("Success", "Preferences cleared successfully!")
    
    # Clear the input fields
    entry1.delete(0, tk.END)
    for var in vars.values():
        var.set("")          
    
def recommend_wines():
    """
    Displays wine recommendations for a specific user in a new window.
    """    
    username = entry1.get()
    if not check_username(username):
        messagebox.showerror("Error", "Username does not exist!")
        return
    with open('user_preferences.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:  # Find the user's row
                preferences = {list(preference_categories.keys())[i]: preference 
                               for i, preference in enumerate(row[1: len(preference_categories)+1])}
                min_price, max_price = float(row[-2]), float(row[-1])
                recommendations = get_wine_recommendations(preferences, min_price, max_price)
                # Create a new window to display the recommendations
                new_window = tk.Toplevel(window)
                
                # Display user preferences
                preferences_label = tk.Label(new_window, text=f"Cheers, {username}!  Welcome to VinoSuggest!\nYour Preferences:", font=("Work Sans", 10, 'bold'), justify=tk.LEFT)
                preferences_label.pack(anchor='w')
                for category, preference in preferences.items():
                    preference_label = tk.Label(new_window, text=f"{category}: {preference}", font=("Work Sans", 10), anchor='w')
                    preference_label.pack(fill='x')
                
                # Display selected price range
                price_range_label = tk.Label(new_window, text=f"Selected Price Range: ${min_price:.1f} - ${max_price:.1f}", font=("Work Sans", 10), anchor='w')
                price_range_label.pack(fill='x')
                
                top_five_label = tk.Label(new_window, text="Here are the top 5 wines recommended for you, based on high ratings in user reviews:", font=("Work Sans", 12, 'bold'), anchor="w")
                top_five_label.pack(fill='x')
                
                for recommendation in recommendations:
                    recommendation_header = f"{recommendation['Winery']} {recommendation['Variety']} from {recommendation['Country']} (Points: {recommendation['Points']}, Price: ${recommendation['Price']})"
                    recommendation_description = f"\nDescription: {recommendation['Description']}"
                    
                    frame = tk.Frame(new_window)  # Create a frame to contain the Text and Scrollbar widgets
                    frame.pack(fill=BOTH)
                
                    scrollbar = tk.Scrollbar(frame)  # Create the scrollbar in the frame
                    scrollbar.pack(side=tk.RIGHT, fill=Y)
                
                    text = tk.Text(frame, height=6, width=100, font=('Work Sans', 10), yscrollcommand=scrollbar.set)  # Add the scrollbar to the Text widget
                    text.tag_configure("bold", font=('Work Sans', 10, 'bold'))  # Configure a tag for bold text
                    text.insert(1.0, recommendation_header, "bold")  # Insert the header with the "bold" tag
                    text.insert(tk.END, recommendation_description)  # Insert the description without the "bold" tag
                    text.configure(state='disabled')  # Disable editing of the text
                    text.pack(side=tk.LEFT, fill=BOTH)
                
                    scrollbar.config(command=text.yview)  # Make the scrollbar scroll the Text widget

          
            # Clear the input fields
            entry1.delete(0, tk.END)
            for var in vars.values():
                var.set("")            




# Create a GUI window
window = ThemedTk(theme="arc")


# Custom styling
style = ttk.Style()
style.configure('TLabel', background='#b11226', foreground='white', font=('Work Sans', 10, 'bold'))
style.configure('TButton', background='#b11226', font=('Work Sans', 10, 'bold'))
style.configure('TCombobox', background='#b11226', font=('Work Sans', 10))
style.configure('Attention.TButton', background='#b11226', foreground='black', font=('Work Sans', 12, 'bold'))

# Window settings
window.title("Wine Recommendation App")
window.configure(background='#b11226')

# Add welcome text
welcome_frame = tk.Frame(window, background='#b11226')
welcome_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
welcome_label1 = ttk.Label(welcome_frame, text="Welcome to VinoSuggest!", 
                          font=("Work Sans", 14, 'bold'), foreground='white', background='#b11226')
welcome_label1.pack()

welcome_label2 = ttk.Label(welcome_frame, text="Please input your preferences below.", 
                          font=("Work Sans", 10), foreground='white', background='#b11226')
welcome_label2.pack()



# Create text entry fields
entry1 = ttk.Entry(window)

# Position the text entry fields on the window
entry1.grid(row=1, column=1, padx=10, pady=10)

# Create labels
label1 = ttk.Label(window, text="Username")

# Position the labels on the window
label1.grid(row=1, column=0, padx=10, pady=10)

# Create dropdown lists for preferences
preference_categories = {
    "Fruitiness/Flavor Profile": ["Fruit", "Cherry", "Blackberry", "Plum", "Citrus", "Apple", "Peach", "Pear", "Pineapple", "Lemon", "Orange", "Melon", "Apricot", "Strawberry", "Raspberry", "Blueberry"],
    "Oak Influence/Spices": ["Oak", "Spice", "Vanilla", "Chocolate", "Cinnamon", "Tobacco", "Coffee", "Toast", "Mocha", "Caramel"],
    "Acidity/Freshness": ["Acidity", "Fresh", "Crisp", "Citrus", "Lemon", "Lime", "Grapefruit"],
    "Tannin Structure/Texture": ["Tannins", "Palate", "Dry", "Soft", "Firm", "Tannic", "Smooth"],
    "Body/Intensity": ["Rich", "Full", "Medium", "Dense", "Heavy", "Light"]
}

# Add text above the slider
price_range_label = ttk.Label(window, text="Please select your price range:",
                              font=("Work Sans", 10), foreground='white', background='#b11226')
price_range_label.grid(row=len(preference_categories) + 2, column=0, columnspan=2, padx=10, pady=(5,0))

# Create a range slider for price
hVar1 = tk.DoubleVar()  # left handle variable
hVar2 = tk.DoubleVar()  # right handle variable
price_slider = RangeSliderH(window, [hVar1, hVar2], min_val=0, max_val=500,Height=60,padX=40, bgColor='#b11226', line_s_color = '#ffffff', font_family = "Work Sans", font_size = 12, suffix = "$")
price_slider.grid(row=len(preference_categories) + 3, column=0, columnspan=2, sticky='ew', pady=(0,10))

vars = {}
for i, (category, options) in enumerate(preference_categories.items()):
    label = ttk.Label(window, text=category)
    label.grid(row=i+2, column=0, padx=10, pady=10)
    var = tk.StringVar()
    vars[category] = var
    dropdown = ttk.Combobox(window, textvariable=var, values=options, state='readonly')
    dropdown.grid(row=i+2, column=1, padx=10, pady=10)
    
# Create a submit button
submit_button = ttk.Button(window, text="Save Preferences", command=submit)
submit_button.grid(row=len(preference_categories)+5, column=0, columnspan=2, padx=10, pady=10)

# Create a show preferences button
show_button = ttk.Button(window, text="Show Preferences", command=show_preferences)
show_button.grid(row=len(preference_categories)+6, column=0, columnspan=2, padx=10, pady=10)

# Create a clear preferences button
clear_button = ttk.Button(window, text="Clear Preferences", command=clear_preferences)
clear_button.grid(row=len(preference_categories)+7, column=0, columnspan=2, padx=10, pady=10)

# Create a "Recommend Wines" button with the new style
recommend_button = ttk.Button(window, text="Recommend Wines", command=recommend_wines, style='Attention.TButton')
recommend_button.grid(row=len(preference_categories)+8, column=0, columnspan=2, padx=10, pady=10)


# Start the Tkinter event loop
window.mainloop()
