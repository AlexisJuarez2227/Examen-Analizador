from flask import Flask, render_template_string, request

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Productos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        h1, h2 {
            color: #333;
        }
        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f8f8f8;
        }
        .error {
            color: red;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Agregar Producto</h1>
    <form method="POST">
        <label for="product_info">Producto y Precio (formato: Producto,Precio):</label>
        <input type="text" id="product_info" name="product_info" pattern="[A-Za-z ]+,[0-9]+(\.[0-9]{1,2})?" required>
        <button type="submit">Agregar Producto</button>
    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    {% if products %}
        <h2>Lista de Productos</h2>
        <table>
            <tr>
                <th>Producto</th>
                <th>Precio</th>
                <th>IVA</th>
                <th>Total con IVA</th>
            </tr>
            {% for product in products %}
                <tr>
                    <td>{{ product.product_name }}</td>
                    <td>{{ product.price | round(2) }}</td>
                    <td>{{ product.iva | round(2) }}</td>
                    <td>{{ product.total_with_iva | round(2) }}</td>
                </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

products = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global products
    error = None
    if request.method == 'POST':
        product_info = request.form.get('product_info')

        if product_info:
            try:
                product_name, price_str = product_info.split(',')
                product_name = product_name.strip()
                price = float(price_str.strip())

                if not product_name.replace(" ", "").isalpha():
                    error = "El nombre del producto solo debe contener letras y espacios."
                elif price < 0:
                    error = "El precio debe ser un número positivo."
                else:
                    iva = price * 0.16  # Suponiendo un IVA del 16%
                    total_with_iva = price + iva

                    product = {
                        'product_name': product_name,
                        'price': price,
                        'iva': iva,
                        'total_with_iva': total_with_iva
                    }
                    products.append(product)
            except ValueError:
                error = "Entrada inválida. Asegúrese de usar el formato: Producto,Precio."
        else:
            error = "Entrada no válida."

    return render_template_string(html_template, products=products, error=error)

if __name__ == '__main__':
    app.run(debug=True)
