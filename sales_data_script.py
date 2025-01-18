import pandas as pd

# Input data
data = {
    "Product": [
        "Budweiser Can (Pack of 6)", "Budweiser Bottle (Pack of 6)", "Budweiser Can (Pack of 12)",
        "Stella Artois Can (Pack of 6)", "Stella Artois Bottle (Pack of 6)", "Stella Artois Can (Pack of 12)",
        "Competitor Can (Pack of 6)", "Competitor Bottle (Pack of 6)", "Competitor Can (Pack of 12)"
    ],
    "Store A": [20, 6, 8, 123, 108, 78, 68, 37, 12],
    "Store B": [65, 35, 24, 163, 105, 28, 274, 143, 53],
    "Store C": [163, 82, 74, 32, 10, 5, 11, 8, 8]
}

# Assumptions for pricing and volume
pricing = {
    "Budweiser Can": 100,
    "Budweiser Bottle": 130,
    "Stella Artois Can": 150,
    "Stella Artois Bottle": 190,
    "Competitor Can": 130,
    "Competitor Bottle": 170
}

volume = {
    "Can": 500,  # in ml
    "Bottle": 650  # in ml
}

def process_data(data, pricing, volume):
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Melt data for easier processing
    df = df.melt(id_vars=["Product"], var_name="Store", value_name="Units Sold")

    # Extract details from the Product column
    df["Type"] = df["Product"].str.extract(r'(Can|Bottle)')
    df["Brand"] = df["Product"].str.extract(r'^(Budweiser|Stella Artois|Competitor)')
    df["Pack Size"] = df["Product"].str.extract(r'\((Pack of \d+)\)')
    df["Pack Size"] = df["Pack Size"].str.extract(r'(\d+)').astype(int)

    # Calculate price per unit and total revenue
    df["Price per Unit"] = df["Brand"] + " " + df["Type"]
    df["Price per Unit"] = df["Price per Unit"].map(pricing)
    df["Total Revenue"] = df["Units Sold"] * df["Pack Size"] * df["Price per Unit"]

    # Calculate volume and revenue per liter
    df["Volume per Unit"] = df["Type"].map(volume)
    df["Total Volume (L)"] = (df["Units Sold"] * df["Pack Size"] * df["Volume per Unit"]) / 1000
    df["Revenue per Liter"] = df["Total Revenue"] / df["Total Volume (L)"]

    # Reorganize columns
    df = df[[
        "Store", "Brand", "Type", "Pack Size", "Units Sold", "Total Revenue",
        "Total Volume (L)", "Revenue per Liter"
    ]]

    return df

# Process the data
processed_df = process_data(data, pricing, volume)

# Save to CSV
processed_df.to_csv("processed_sales_data.csv", index=False)

print("CSV file 'processed_sales_data.csv' has been generated.")


# Extract only the beer prices for the three brands
beer_prices = {
    "Product": [
        "Budweiser Can", "Budweiser Bottle", "Stella Artois Can",
        "Stella Artois Bottle", "Competitor Can", "Competitor Bottle"
    ],
    "Price": [
        pricing["Budweiser Can"], pricing["Budweiser Bottle"],
        pricing["Stella Artois Can"], pricing["Stella Artois Bottle"],
        pricing["Competitor Can"], pricing["Competitor Bottle"]
    ]
}

# # Convert to DataFrame
# beer_prices_df = pd.DataFrame(beer_prices)
#
# # Save to CSV
# beer_prices_csv_path = "/Users/rahulsharma/Developer/PythonProject3/beer_prices.csv"
# beer_prices_df.to_csv(beer_prices_csv_path, index=False)
#
# beer_prices_csv_path
