import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

# Load the dataframes
df1 = pd.read_csv("./nutration/Recommended_Nutrient_Intake_by_Age_Group.csv")
df2 = pd.read_csv("./nutration/Nutrient_Values_for_Each_Food.csv")

# Clean up column names and data
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()
df1['AGE (YEARS)'] = df1['AGE (YEARS)'].str.strip()


@app.route('/age-groups', methods=['GET'])
def get_age_groups():
    age_groups = df1['AGE (YEARS)'].unique().tolist()
    return jsonify(age_groups)


@app.route('/foods', methods=['GET'])
def get_foods():
    foods = df2['FOOD COMMODITY'].unique().tolist()
    return jsonify(foods)
    

@app.route('/nutrient-intake', methods=['POST'])
def nutrient_intake():
    data = request.json

    user_age_group = data.get('ageGroup').strip()
    breakfast = data.get('breakfast').split(",")
    lunch = data.get('lunch').split(",")
    snacks = data.get('snacks').split(",")
    supper = data.get('supper').split(",")


    # # Filter the required nutrition data based on age group
    required_nutrition = df1[df1['AGE (YEARS)'].str.contains(user_age_group, case=False, na=False)]

    if required_nutrition.empty:
        return jsonify({"error": f"No data found for age group '{user_age_group}'. Please check the input."}), 400

    required_nutrition = required_nutrition.iloc[0]
    required_nutrition = pd.to_numeric(required_nutrition, errors='coerce').fillna(0)

    nutrients = ['Thiamine (mg)', 'ENERGY (KCAL)', 'PROTEIN (G)', 'Niacin (mg)', 
                 'Calcium (mg)', 'Iron (mg)', 'Vitamin A (μg)', 'Riboflavin (mg)', 
                 'Ascorbic Acid (mg)']

    total_intake = {nutrient: 0 for nutrient in nutrients}

    def calculate_intake(food_items):
        intake = {nutrient: 0 for nutrient in nutrients}
        if not food_items or (len(food_items) == 1 and food_items[0] == ''):
            return intake
        
        for item in food_items:
            if item:
                food, amount = item.rsplit(' ', 1)
                amount = float(amount)
                food_data = df2[df2['FOOD COMMODITY'].str.strip().str.lower() == food.lower()]
                if not food_data.empty:
                    food_data = food_data.iloc[0]
                    for nutrient in nutrients:
                        nutrient_value = food_data.get(nutrient, 0)
                        intake[nutrient] += (nutrient_value * amount) / 100
                else:
                    print(f"Warning: '{food}' not found in the food list.")
        return intake

    for meal in [breakfast, lunch, snacks, supper]:
        print(meal)
        meal_intake = calculate_intake(meal)
        for nutrient in nutrients:
            total_intake[nutrient] += meal_intake[nutrient]

    deficit = {nutrient: required_nutrition[nutrient] - total_intake[nutrient] for nutrient in nutrients}



    nutrient_summary = {
        nutrient: {
            "Consumed": round(total_intake[nutrient], 2),
            "Required": round(required_nutrition[nutrient], 2),
            "Deficit": round(deficit[nutrient], 2)
        }
        for nutrient in nutrients
    }

    return jsonify(nutrient_summary)

if __name__ == '__main__':
    app.run(debug=True)

