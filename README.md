# Wine-Recommendation-App

## Project Overview
This Wine Recommendation System is part of a larger project focused on wine dataset analysis. It uses a cleaned dataset to suggest wines that align with user preferences. Preferences are collected through a Graphical User Interface (GUI), developed using Python and several libraries for an interactive, user-friendly experience.

## Installation
### Prerequisites
- Python 3
- Libraries: pandas, matplotlib, seaborn, tkinter, ttkthemes, custom module RangeSlider

To install the required libraries, run the following command:
```
pip install pandas matplotlib seaborn tk ttkthemes
```
*Note: The tkinter library usually comes pre-installed with Python. The custom module RangeSlider is part of the project.*

## Usage
### Running the Application
1. Clone the repository and navigate to the directory containing the `wine_recommendation_project.py` script.
2. Run the command:
   ```
   python wine_recommendation_project.py
   ```
3. The GUI will appear for user interaction.

### Using the GUI
1. **Enter Username**: Input your unique username.
2. **Select Preferences**: Choose your preferences across various categories (Fruitiness, Oak Influence, etc.).
3. **Set Price Range**: Use the slider to define your preferred wine price range.
4. **Save Preferences**: Click 'Save Preferences' to store your choices.
5. **Get Wine Recommendations**: Click 'Recommend Wines' to receive a list of the top 5 wines based on your preferences.

### Data Files
Ensure you have the necessary datasets (`cleaned_wine_data.csv`, `user_preferences.csv`) in the same directory as the script.

## Features
- Interactive GUI for preference input.
- Personalized wine recommendations based on user preferences and price range.
- Easy-to-use interface with clear instructions and feedback messages.

## Challenges & Solutions
- **Missing Data**: Rows with missing values in key columns were removed to maintain data accuracy.
- **GUI Development**: Tkinter, along with ttkthemes and RangeSlider, was used to create a functional and aesthetically pleasing interface.

## Future Developments
- Improved recommendation algorithms.
- Integration with online wine stores for direct purchase options.
- User login and preference tracking for enhanced personalization.

