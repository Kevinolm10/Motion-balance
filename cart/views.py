from django.shortcuts import render, redirect

# Create your views here.

# The view_cart function will render the cart.html template
def view_cart(request):
    """ A view to return the cart page """
    return render(request, 'cart/cart.html')


# The add_to_cart function will add a product to the cart
def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """
    quantity = int(request.POST.get('quantity', 1))  # Get quantity, default to 1 if not provided
    size = request.POST.get('size')  # Get size selected
    redirect_url = request.POST.get('redirect_url')  # Redirect URL after adding to cart
    cart = request.session.get('cart', {})

    # Ensure the cart is a dictionary
    if not isinstance(cart, dict):
        cart = {}

    # Ensure item_id is stored as a string for consistency
    item_id = str(item_id)

    if item_id not in cart:
        cart[item_id] = {}  # Initialize product entry as a dictionary for sizes

    if size in cart[item_id]:
        cart[item_id][size] += quantity  # Increase quantity if size exists
    else:
        cart[item_id][size] = quantity  # Add new size entry

    request.session['cart'] = cart  # Save cart back to session
    request.session.modified = True  # Ensure session updates

    print(f"Cart after adding: {request.session['cart']}")  # Debugging print

    return redirect(redirect_url)  # Redirect to the specified URL


# The delete_from_cart function will remove a product from the cart
def delete_from_cart(request, item_id, size):
    """ Remove a specific size of the product from the shopping cart """
    cart = request.session.get('cart', {})

    item_id = str(item_id)  # Ensure it's a string

    if item_id in cart:
        if size in cart[item_id]:
            del cart[item_id][size]  #  Remove only the selected size

            # If no sizes remain for this product, remove the product entry
            if not cart[item_id]:  
                del cart[item_id]

    request.session['cart'] = cart
    request.session.modified = True  #  Force session update

    print(f"Cart after deletion: {request.session.get('cart', {})}")  #  Debugging print

    return redirect('view_cart')

