import pandas as pd

# Load the dataframes
df1 = pd.read_csv("./nutration/Recommended_Nutrient_Intake_by_Age_Group.csv")
df2 = pd.read_csv("./nutration/Nutrient_Values_for_Each_Food.csv")

# Clean up column names and data
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()
df1['AGE (YEARS)'] = df1['AGE (YEARS)'].str.strip()

# User input
user_age_group = input("Enter your age group: ").strip()
breakfast = input("Enter food items consumed for breakfast (comma-separated, with amounts in grams): ").split(", ")
lunch = input("Enter food items consumed for lunch (comma-separated, with amounts in grams): ").split(", ")
snacks = input("Enter food items consumed for snacks (comma-separated, with amounts in grams): ").split(", ")
supper = input("Enter food items consumed for supper (comma-separated, with amounts in grams): ").split(", ")

# Print inputs for debugging
print(f"\nAge group: {user_age_group}")
print(f"Breakfast foods: {breakfast}")
print(f"Lunch foods: {lunch}")
print(f"Snacks foods: {snacks}")
print(f"Supper foods: {supper}")

# Inspect available age groups
print("\nAvailable age groups in the dataset:")
print(df1['AGE (YEARS)'].unique())

# Filter the required nutrition data based on age group
required_nutrition = df1[df1['AGE (YEARS)'].str.contains(user_age_group, case=False, na=False)]

# Check if required_nutrition is empty or not
if required_nutrition.empty:
    print(f"No data found for age group '{user_age_group}'. Please check the input.")
    exit()

required_nutrition = required_nutrition.iloc[0]  # Select the first row as a Series

# Convert required_nutrition to numeric, coercing errors
required_nutrition = pd.to_numeric(required_nutrition, errors='coerce').fillna(0)

# Define nutrients to track
nutrients = ['Thiamine (mg)', 'ENERGY (KCAL)', 'PROTEIN (G)', 'Niacin (mg)', 
             'Calcium (mg)', 'Iron (mg)', 'Vitamin A (μg)', 'Riboflavin (mg)', 
             'Ascorbic Acid (mg)']

# Initialize a dictionary to store total intake
total_intake = {nutrient: 0 for nutrient in nutrients}

# Function to calculate intake from a list of foods with amounts
def calculate_intake(food_items):
    intake = {nutrient: 0 for nutrient in nutrients}
    
    # Check if the list is empty
    if not food_items or (len(food_items) == 1 and food_items[0] == ''):
        return intake  # Return zero intake for all nutrients
    
    for item in food_items:
        if item:  # Skip empty strings
            food, amount = item.rsplit(' ', 1)
            amount = float(amount) 
            print(f"\nLooking up food: '{food}' with amount: {amount}g")
            food_data = df2[df2['FOOD COMMODITY'].str.strip().str.lower() == food.lower()]
            if not food_data.empty:
                food_data = food_data.iloc[0]
                for nutrient in nutrients:
                    nutrient_value = food_data.get(nutrient, 0)
                    intake[nutrient] += (nutrient_value * amount) / 100  
                    print(f"  Adding {nutrient_value * amount / 100:.2f} of {nutrient} from '{food}'")
            else:
                print(f"Warning: '{food}' not found in the food list.")
    return intake

# Calculate total intake from all meals
for meal in [breakfast, lunch, snacks, supper]:
    meal_intake = calculate_intake(meal)
    for nutrient in nutrients:
        total_intake[nutrient] += meal_intake[nutrient]

# Calculate the deficit
deficit = {nutrient: required_nutrition[nutrient] - total_intake[nutrient] for nutrient in nutrients}

# Display results
print("\nNutrient Intake Summary:")
for nutrient in nutrients:
    required_value = required_nutrition.get(nutrient, 0)
    consumed_value = total_intake[nutrient]
    deficit_value = deficit[nutrient]
    print(f"{nutrient}: Consumed = {consumed_value:.2f}, Required = {required_value:.2f}, Deficit = {deficit_value:.2f}")
