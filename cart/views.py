from django.shortcuts import render, redirect

def view_cart(request):
    """ A view to return the cart page """
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """
    quantity = int(request.POST.get('quantity', 1))  # Get quantity, default to 1 if not provided
    size = request.POST.get('size')  # Get size selected
    redirect_url = request.POST.get('redirect_url')  # Redirect URL after adding to cart
    cart = request.session.get('cart', {})

    # Initialize the cart if it's not a dictionary
    if not isinstance(cart, dict):
        cart = {}

    if item_id in cart:
        # If the product is already in the cart, update the size and quantity
        if size in cart[item_id]:
            cart[item_id][size] += quantity  # Increment quantity
        else:
            cart[item_id][size] = quantity  # Add new size
    else:
        # If it's a new product, add it with the selected size and quantity
        cart[item_id] = {size: quantity}

    request.session['cart'] = cart  # Save cart back to session
    return redirect(redirect_url)  # Redirect to the specified URL




def delete_from_cart(request, item_id):
    """ Remove the specified product from the shopping cart """
    cart = request.session.get('cart', {})

    item_id = str(item_id)  # Ensure it's a string

    if item_id in cart:
        del cart[item_id]

    request.session['cart'] = cart
    request.session.modified = True  # ✅ Force Django to save session changes

    print(f"Cart after deletion: {request.session.get('cart', {})}")  # Debugging print

    return redirect('view_cart') 
