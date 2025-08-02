from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    print("Received data for prediction:", data)
    
    funding = float(data.get('funding', 0))
    founders = int(data.get('founders', 1))
    age = int(data.get('age', 0))
    employees = int(data.get('employees', 1))
    burnRate = float(data.get('burnRate', 1))
    industry = data.get('industry', 'Other')
    founderExperience = data.get('founderExperience', 'No')
    founderDegree = data.get('founderDegree', 'Bachelor')
    marketSize = data.get('marketSize', 'Small')
    businessModel = data.get('businessModel', 'B2C')
    customerRetention = float(data.get('customerRetention', 0))
    marketingExpense = float(data.get('marketingExpense', 0))

    prediction = 'Failure'
    probability = 0
    advice = ''

    runway = funding / (burnRate if burnRate > 0 else 1)

    score = 0

    if funding > 1000000: score += 2
    if founders > 1: score += 1.5
    if age > 24: score += 1
    if employees > 10: score += 1
    if runway > 12: score += 2

    if founderExperience == 'Yes': score += 1.5
    if founderDegree in ['Master', 'PhD']: score += 1
    if marketSize == 'Large': score += 1.5
    if customerRetention > 70: score += 2
    if marketingExpense > 0 and (marketingExpense / funding) < 0.2: score += 0.5

    if industry in ['Software', 'FinTech']: score += 1
    if businessModel == 'B2B': score += 0.5

    if score > 8:
        probability = 85 + random.randint(0, 10)
        prediction = 'Success'
        advice = f"""
            <h3 class="font-bold text-lg text-green-700">Congratulations! Your startup shows strong potential for success.</h3>
            <p>Based on our analysis, your startup has a strong foundation. To capitalize on this, we recommend focusing on:</p>
            <ul class="list-disc list-inside space-y-1 mt-2">
                <li>**Market Expansion:** Explore new markets or customer segments to scale your growth.</li>
                <li>**Operational Efficiency:** Continue to monitor your burn rate and optimize your business processes.</li>
                <li>**Talent Acquisition:** Attract top talent to support your next phase of growth.</li>
                <li>**Securing Next Round of Funding:** Start building relationships with investors early for your next funding round.</li>
            </ul>
        """
    else:
        probability = 20 + random.randint(0, 30)
        prediction = 'Failure'
        advice_list = []
        if runway < 6:
            advice_list.append('**Aggressive Cost Reduction:** Your financial runway is short. Perform a thorough audit of all expenses and cut non-essential spending immediately.')
        if customerRetention < 50:
            advice_list.append('**Re-evaluate the Business Model:** Your low customer retention rate suggests a potential issue with product-market fit. Gather customer feedback and consider a strategic pivot.')
        if founderExperience == 'No' or founderDegree == 'Bachelor':
            advice_list.append('**Seek Mentorship:** A lack of prior experience or advanced education in the founding team can be a risk factor. Seek out experienced mentors or advisors to guide your decisions.')
        if marketingExpense == 0:
            advice_list.append('**Develop a Marketing Strategy:** Even with a great product, it won\'t sell itself. Develop a clear plan for reaching your target audience and communicating your value proposition.')

        advice_list.append('**Seek Professional Advice:** Consider engaging a financial advisor or consultant to help manage cash flow and navigate potential debt restructuring.')
        advice_list.append('**Communicate with Stakeholders:** Be transparent with your team and investors about the challenges and your plan to address them.')
        
        advice = f"""
            <h3 class="font-bold text-lg text-red-700">Warning: Your startup is facing significant risks.</h3>
            <p>Based on our analysis, your startup may be at risk. It's crucial to take immediate action to mitigate these challenges. We strongly recommend:</p>
            <ul class="list-disc list-inside space-y-1 mt-2">
                {''.join([f"<li>{item}</li>" for item in advice_list])}
            </ul>
        """

    response = {
        'prediction': prediction,
        'probability': probability,
        'advice': advice
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
