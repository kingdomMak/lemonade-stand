from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Add this configuration
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

# Add this list of drinks (you can modify the drinks as needed)
DRINKS = [
    {
        'name': 'Classic Lemonade',
        'price': 3.99,
        'description': 'Our signature fresh-squeezed lemonade with honey',
        'image': 'classic-lemonade.jpg',
        'keywords': ['classic', 'original', 'lemon', 'honey']
    },
    {
        'name': 'Strawberry Lemonade',
        'price': 4.99,
        'description': 'Fresh strawberries blended with our classic lemonade',
        'image': 'strawberry-lemonade.jpg',
        'keywords': ['strawberry', 'berry', 'fruit', 'pink']
    },
    {
        'name': 'Blueberry Lemonade',
        'price': 4.99,
        'description': 'Sweet blueberries mixed with our classic lemonade',
        'image': 'blueberry-lemonade.jpg',
        'keywords': ['blueberry', 'berry', 'fruit', 'blue']
    }
]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/menu')
def menu():
    return render_template("menu.html")

@app.route('/order')
def order():
    return render_template("order.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# 🙏 Thank-you page
@app.route('/thankyou')
def thankyou():
    name = request.args.get('name')
    drink = request.args.get('drink')
    size = request.args.get('size')
    ice = request.args.get('ice')
    addons = request.args.getlist('addons')  # This gets multiple checkbox values
    
    # Format addons for display
    addons_text = ", ".join(addons) if addons else "no add-ons"
    
    # Save to orders.txt
    with open('orders.txt', 'a') as f:
        f.write(f"Order: {name} ordered {size} {drink} with {ice} ice and {addons_text}\n")
    
    return f'''
    <h1>Thank you for your order, {name}!</h1>
    <p>Order Details:</p>
    <ul>
        <li>Drink: {drink}</li>
        <li>Size: {size}</li>
        <li>Ice Level: {ice}</li>
        <li>Add-ons: {addons_text}</li>
    </ul>
    <p>Your drink is being freshly squeezed! 🍋</p>
    <p><a href="/">Back to Home</a></p>
    '''

@app.route('/shop')
def shop():
    return render_template("shop.html")

@app.route('/our-story')
def our_story():
    return render_template("our-story.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('menu'))
    
    # Search through drinks
    results = []
    for drink in DRINKS:
        # Check if query matches name, description, or keywords
        if (query in drink['name'].lower() or 
            query in drink['description'].lower() or 
            any(query in keyword.lower() for keyword in drink['keywords'])):
            results.append(drink)
    
    return render_template('search.html', drinks=results, query=query)

# Add this route to serve images
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
