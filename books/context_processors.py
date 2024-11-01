# books/context_processors.py
def cart_contents(request):
    try:
        cart = request.session.get('cart', {})
        cart_count = sum(item.get('quantity', 0) for item in cart.values())
        cart_total = sum(item.get('quantity', 0) * float(item.get('price', 0)) for item in cart.values())
        return {
            'cart_count': cart_count,
            'cart_total': round(cart_total, 2)
        }
    except Exception as e:
        print(f"Error in cart_contents: {e}")
        return {'cart_count': 0, 'cart_total': 0.00}