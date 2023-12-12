import matplotlib.pyplot as plt
import pandas as pd

def create_modulo_group_table(p):
    # Create a DataFrame with p-1 rows and p-1 columns (excluding g^0 and the 0 element)
    # First column is the elements of Zp (1 to p-1)
    # Other columns are g^1, g^2, ..., g^(p-1) mod p for each g
    columns = [r'$g^{{{}}}$'.format(i) for i in range(1, p)]
    data = {columns[i-1]: [(x) ** i % p for x in range(1, p)] for i in range(1, p)}
    df = pd.DataFrame(data)
    df.index = df.index + 1  # Start indexing from 1 instead of 0
    df.index.name = 'Zp'
    return df

def display_table(df):
    # Plot DataFrame as a table and display it
    fig, ax = plt.subplots(figsize=(12, 8))  # set size frame
    ax.axis('off')  # Hide axes
    
    # Apply blue color to the header row and grey to the header column
    cell_colors = [['w' for _ in range(len(df.columns))] for _ in range(len(df))]
    header_row_colors = ['#ADD8E6' for _ in range(len(df.columns))]
    header_column_colors = ['#D3D3D3' for _ in range(len(df))]
    
    table_data = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center', colColours=header_row_colors, rowColours=header_column_colors, cellColours=cell_colors)
    table_data.auto_set_font_size(False)
    table_data.set_fontsize(10)
    table_data.scale(1.2, 1.2)  # Adjust scaling if necessary
    
    # Adjust layout to make sure the table is displayed fully
    plt.tight_layout()
    
    plt.show()

def main():
    # Get the order of the group from the user
    p = int(input("Enter the order p of the group: "))
    
    # Generate the modulo group table as a DataFrame
    df = create_modulo_group_table(p)
    
    # Display the table
    display_table(df)

if __name__ == "__main__":
    main()
