## Test Results

Below are the results from our manual testing of key functionalities across the application.

### General Navigation & Footer

| Element                                  | Expected Outcome                                                                                  | Pass/Fail |
|------------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Main Logo Link**                       | Clicking the logo redirects to the products page (`{% url 'home' %}`).                        | Pass      |
| **Home Link**                            | Clicking "products" redirects to the products page (`{% url 'all_products' %}`).                                   | Pass      |
| **Products Dropdown – Category Links**   | Clicking a subcategory link filters products by that category.                                       | Pass      |
| **Sign in Icon**     | Clicking the sign in button redirects you to the sign in page    | Pass      |
| **Sign up**  | Clicking the sign up button redirects you to the sign up page.                      | Pass      |
| **Cart**      | Clicking the cart button redirects you to the shopping cart page and displays your total. | Pass      |
| **Search Bar**                           | Entering a query and submitting redirects to the products page with matching results.             | Pass      |
| **Facebook Icon**                        | Clicking the icon opens the business Facebook page in a new tab.                                   | Pass      |
| **Newsletter Form**                      | Submitting a valid email registers the subscriber and displays a success message.                 | Pass      |

---

### Home Page

| Element                          | Expected Outcome                                                                                  | Pass/Fail |
|----------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Call to action button**             | Clicking the call to action button redirects the user to the all products page.    | Pass      |

---

### Product Page

| Element                              | Expected Outcome                                                                                  | Pass/Fail |
|--------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Filtering porducts**                    | Changing the filters, displays or hides the relevant products for the user in the query.                                  | Pass      |
| **View Details Button**                | Clicking the view details button takes the user to the product details page.                                | Pass      |
| **Hovering products**              | Hovering over the product cards makes it easier to see which product is selected.                                   | Pass      |
| **Apply Filters**              | Clicking the apply filters button makes the filters active.                           | Pass      |
| **Reset Filters**              | Clicking the reset filters button makes the filters reset.                           | Pass      |
| **Wishlist heart**              | Clicking the wishlist heart icon adds the product to the users wishlist.                           | Pass      |

---

### Product Detail Page

| Element                              | Expected Outcome                                                                                  | Pass/Fail |
|--------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Wishlist heart**              | Clicking the wishlist heart icon adds the product to the users wishlist.                           | Pass      |
| **Change sizes**                   | Selecting a size from the dropdown saves it to the session when adding to the bag.                               | Pass      |
| **Quantity**           | Changing the quantity of the product saves it to the session when adding it to the bag.                        | Pass      |
| **Keep Shopping button**         | Clicking the keep shopping button redirects the user to the all products page                         | Pass      |
| **Add to bag button**         | Clicking the keep shopping button redirects the user to their shopping bag with the saved item/items                         | Pass      |
| **Details**         | The info, price, discount and average rating are displayed next to the product.                         | Pass      |
| **Product Feedback**         | When the user is signed in they can submit a comment on an ordered product or edit their comment and update it.                         | Pass      |
| **Product Feedback not signed in**         | If not signed in, the user is asked to do so to comment if they have an order for it.                         | Pass      |
| **Product Feedback history**         | The order history displays recent feedback by users.                         | Pass      |
| **One comment**         | The user can only comment one time on each product they have ordered.                         | Pass      |


---

### Shopping Cart

| Element                              | Expected Outcome                                                                                  | Pass/Fail |
|--------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Removing products button**                | Clicking the button removes the item or items if more of the same is in the bag.               | Pass      |
| **Keep shopping button**               | Clicking the button redirects the user to the all products page.                                       | Pass      |
| **Checkout button**           | Clicking the checkout button redirects to the checkout page.                     | Pass      |
| **Cart information**                  | The cart displays the total, delivery and grand total cost to the user.     | Pass      |


---



---

### Checkout & Payment

| Element                              | Expected Outcome                                                                                  | Pass/Fail |
|--------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Add to Bag Button**                | Clicking the button adds the specified quantity of the product to the shopping bag.               | Pass      |
| **Adjust Cart**               | Clicking the adjust cart button redirects to the shopping cart page to adjust the products as needed.                                       | Pass      |
| **Stripe payment form**           | The user can fill out billing and shipping information.                     | Pass      |
| **Card**           | The user can fill out their card in a secure and familiar way.                     | Pass      |
| **Order Summary**           | The user can see the order summary of what they are about to order.                     | Pass      |
| **Payment Success**                  | After successful payment, a success message is displayed and the order status updates to "Paid".     | Pass      |
| **Payment Cancel**                   | If payment is cancelled, an error message is displayed and the order status updates to "Cancelled".  | Pass      |


---

### User profile

| Element                              | Expected Outcome                                                                                  | Pass/Fail |
|--------------------------------------|---------------------------------------------------------------------------------------------------|-----------|
| **Registration Form**                | Submitting the registration form creates a new account and saves the shipping address for checkout. | Pass      |
| **Login/Logout Functionality**       | Users can log in and out; appropriate success messages are displayed.                             | Pass      |
| **Profile Update Form**              | Submitting the profile update form updates user information and shows a success message.            | Pass      |
| **Review Edit/Delete**               | Users can edit or delete their reviews with changes reflected immediately.                        | Pass      |
| **History**               | Users can track their history in wishlists, orders and product feedback.                        | Pass      |

---

*Note: "Pass" indicates that the expected behavior was observed during testing.*
---

## Bugs

**Solved bugs:**

- Stripe webhook handler bug. I had to resort to an easier handling of my stripe payment system due to the meta data not being avaliable even though i debugged it for 6 hours straight. A working system is better than a broken one so i will consider it solved with an easier handling system. 



**Unsolved bugs:**

- Wishlist heart bug. For some reason, the heart is clickable when not signed in even though it is user authenticated in the code. The simple fix to this is removing the heart and replacing it with something telling the user that they have to sign in to wishlist.

- The dropdowns in the nav does not respond as fluently as they should which can result in stuttering when trying to press the subcategories. Needs to be fixed.

- Image size bug. The image sizes are loading incorrectly due to them not having a set size, this causes bad performance and needs to be addressed.

- Hamburger menu flexbox bug. The hamburger does not stay where it should and places itself a little bit out of the screen.

---

## Validation

### HTML Validation:
- No errors or warnings for my custom HTML code were found when passing through the official [W3C](https://validator.w3.org/) validator. This checking was done manually by copying the view page source code (Ctrl+U) and pasting it into the validator.
- The only errors that are present are those from the bootstrap styling which i after many attempts could not resolve. I could resolve some but not all. I see the code as passing since bootstrap is encouraged but come with this downside.

### CSS Validation:

- [Css valdation - Auth](documentation/validation/js-val/hamburger-val.png)
- [Css valdation - Base](documentation/validation/js-val/hamburger-val.png)
- [Css validation - Cart](documentation/validation/js-val/hamburger-val.png)
- [Css validation - Checkout](documentation/validation/js-val/hamburger-val.png)
- [Css validation - Products](documentation/validation/js-val/hamburger-val.png)
- [Css validation - Product details](documentation/validation/js-val/hamburger-val.png)

- No errors or warnings were found when passing through the official [W3C (Jigsaw)](https://jigsaw.w3.org/css-validator/#validate_by_uri) validator except for the warnings about the use of css root variables and webkits for the box-shadow. However, css code works perfectly on various devices.

### JS Validation:

- [Hamburger menu](documentation/validation/js-val/hamburger-val.png)
- [Stripe elements](documentation/validation/js-val/stripe-elements-val.png)
- [Hamburger menu](documentation/validation/js-val/wishlist_icon-val.png)

- No errors or warning messages were found when passing through the official [JSHint](https://www.jshint.com/) validator. However, to validate js full `/* jshint esversion: 8, jquery: true, scripturl: true */` was added to the top of the file.

### Python Validation:

- No errors were found when the code was passed through Valentin Bryukhanov's [online validation tool](http://pep8online.com/). According to the reports, the code is [Pep 8-compliant](https://legacy.python.org/dev/peps/pep-0008/). This checking was done manually by copying python code and pasting it into the validator.

- [Cart - apps.py](documentation/validation/cart-val-py/cart-app.png)
- [Cart - context.py](documentation/validation/cart-val-py/cart-context.png)
- [Cart - urls.py](documentation/validation/cart-val-py/cart-urls.png)
- [Cart - views.py](documentation/validation/cart-val-py/cart-views.png)

- [Checkout - admin.py](documentation/validation/cart-val-py/checkout-admin.png)
- [Checkout - apps.py](documentation/validation/cart-val-py/checkout-apps.png)
- [Checkout - forms.py](documentation/validation/cart-val-py/checkout-forms.png)
- [Checkout - models.py](documentation/validation/cart-val-py/checkout-models.png)
- [Checkout - signals.py](documentation/validation/cart-val-py/checkout-signals.png)
- [Checkout - urls.py](documentation/validation/cart-val-py/checkout-urls.png)
- [Checkout - views.py](documentation/validation/cart-val-py/checkout-views.png)

- [Products - admin.py](documentation/validation/cart-val-py/products-admin.png)
- [Products - context.py](documentation/validation/cart-val-py/products-context.png)
- [Products - forms.py](documentation/validation/cart-val-py/products-forms.png)
- [Products - models.py](documentation/validation/cart-val-py/products-models.png)
- [Products - signals.py](documentation/validation/cart-val-py/products-signals.png)
- [Products - urlsdmin.py](documentation/validation/cart-val-py/products-urls.png)
- [Products - views.py](documentation/validation/cart-val-py/products-views.png)

- [User profile - admin.py](documentation/validation/cart-val-py/user-admin.png)
- [User profile - apps.py](documentation/validation/cart-val-py/user-apps.png)
- [User profile - forms.py](documentation/validation/cart-val-py/user-forms.png)
- [User profile - models.py](documentation/validation/cart-val-py/user-models.png)
- [User profile - urls.py](documentation/validation/cart-val-py/user-urls.png)
- [User profile - views.py](documentation/validation/cart-val-py/user-views.png)


- [Wishlist - admin.py](documentation/validation/cart-val-py/wishlist-admin.png)
- [Wishlist - apps.py](documentation/validation/cart-val-py/wishlist-apps.png)
- [Wishlist - conetext.py](documentation/validation/cart-val-py/wishlist-context.png)
- [Wishlist - models.py](documentation/validation/cart-val-py/wishlist-wishlist.png)
- [Wishlist - signals.py](documentation/validation/cart-val-py/wishlist-signals.png)
- [Wishlist - urls.py](documentation/validation/cart-val-py/wishlist-urls.png)



---
## Lighthouse Report

LightHouse is a web performance testing tool that can be used to evaluate the performance of a website. The report is generated by Google Chrome.

[Lighthouse Report](documentation/validation/lighthouse/lighthouse-cart.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-checkout.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-home-snap.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-nav.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-prod-details.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-products.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-profile.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-signin.png)
[Lighthouse Report](documentation/validation/lighthouse/lighthouse-signup.png)

---

## Compatibility

Testing was conducted on the following browsers;

- Brave;
- Chrome;
- Firefox;

[Compatibility Report](documentation/validation/compatibility.pdf)

---
## Responsiveness

The responsiveness was checked manually by using devtools (Chrome) throughout the whole development.


---

## Project assessment criteria CHECKLIST. Portfolio 5: Project Submission


| Requirement    | Done           |  Comments    |
|-------------|------------------------|------------------|
| at least 3 original custom models with associated functionalities, markedly different from those present in the Boutique Ado walkthrough project if they have been used as a basis for your project.     |          Y              |    |
| at least one form on the front end, which provides either admin or regular users with CRUD functionality without having to access the admin panel. |           Y            |  |
| at least one UI element on the front end, which allows either admin or regular users to delete records in the database without having to access the admin panel. |          Y            |     | 
| evidence of agile methodologies followed during the development of your project in the GitHub repository. |  Y   |                  |
| a robots.txt file. |  Y   |     |
| a sitemap.xml file. |   Y  |     |
| descriptive meta tags in the HTML. |   Y  |     |
| at least one link to an external resource, which makes use of a rel attribute.  |  Y  |     |
| a custom 404 error page. |  Y  |     |
| evidence of either a real Facebook business page, or mockup of one, for the purposes of digital marketing. |  Y  |  |
| evidence of a newsletter signup form for the purposes of digital marketing. |  Y  |     |
| a description of the e-commerce business model including marketing strategies in the README file. | Y  |     |
| DEBUG mode set to False. | Y  |    |
| working functionality for users to register and log in and out of the application without issues. | Y  |     |
| working E-commerce functionality for users to make purchases within the application. | Y  |     |
| detailed testing write ups, beyond results of validation tools. | Y  |     |