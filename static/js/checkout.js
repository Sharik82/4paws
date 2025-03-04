document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/cart")
        .then(response => response.json())
        .then(cart => {
            let checkoutCart = document.getElementById("checkoutCart");
            let checkoutTotal = document.getElementById("checkoutTotal");

            if (cart.length === 0) {
                checkoutCart.innerHTML = "<p>Кошик порожній.</p>";
                return;
            }

            let total = 0;
            cart.forEach(item => {
                let itemElement = document.createElement("div");
                itemElement.classList.add("checkout-item");
                itemElement.innerHTML = `
                    <p>${item.name} - ${item.price} грн</p>
                `;
                checkoutCart.appendChild(itemElement);
                total += parseFloat(item.price);
            });

            checkoutTotal.innerText = `${total.toFixed(2)} грн`;
        })
        .catch(error => console.error("Помилка при завантаженні кошика:", error));
});
