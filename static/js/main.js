document.addEventListener("DOMContentLoaded", function () {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    updateCartUI();

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            const product = this.closest(".product");
            const item = {
                id: product.dataset.id,
                name: product.querySelector(".product-title").innerText,
                price: parseFloat(product.querySelector(".product-price").innerText.replace(" грн", "")),
                image: product.querySelector(".product-image").src,
                quantity: 1
            };

            const existingItem = cart.find(i => i.id === item.id);
            if (existingItem) {
                existingItem.quantity++;
            } else {
                cart.push(item);
            }

            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartUI();
            openCart();
        });
    });

    function updateCartUI() {
        const cartContainer = document.querySelector(".cart-items");
        const totalContainer = document.querySelector(".cart-total");
        cartContainer.innerHTML = "";
        let total = 0;

        cart.forEach(item => {
            total += item.price * item.quantity;
            cartContainer.innerHTML += `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <p>${item.quantity} x ${item.price} грн</p>
                    </div>
                    <button class="remove-from-cart" data-id="${item.id}">×</button>
                </div>
            `;
        });

        totalContainer.innerText = `Загальна сума: ${total.toFixed(2)} грн`;

        document.querySelectorAll(".remove-from-cart").forEach(button => {
            button.addEventListener("click", function () {
                const itemId = this.dataset.id;
                const itemIndex = cart.findIndex(i => i.id === itemId);
                if (itemIndex !== -1) {
                    cart.splice(itemIndex, 1);
                    localStorage.setItem("cart", JSON.stringify(cart));
                    updateCartUI();
                }
            });
        });
    }

    function openCart() {
        document.querySelector(".cart").classList.add("open");
    }

    document.querySelector(".checkout-button").addEventListener("click", function () {
        fetch("/api/cart", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(cart)
        }).then(response => response.json())
          .then(data => {
              console.log("Кошик на сервері оновлено", data);
              window.location.href = "/checkout";
          });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();

        if (query.length < 2) {  // Починати пошук після 2 символів
            searchResults.style.display = "none";
            return;
        }

        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    let resultsHTML = "<ul>";
                    data.forEach(product => {
                        resultsHTML += `
                            <li onclick="window.location.href='/product/${product.id}'">
                                <img src="/${product.image}" alt="${product.name}">
                                <span>${product.name} — ${product.price} грн</span>
                            </li>`;
                    });
                    resultsHTML += "</ul>";
                    searchResults.innerHTML = resultsHTML;
                    searchResults.style.display = "block";
                } else {
                    searchResults.innerHTML = "<p>Нічого не знайдено</p>";
                    searchResults.style.display = "block";
                }
            })
            .catch(error => console.error("Помилка пошуку:", error));
    });

    // Закриваємо результати пошуку при кліку за межами
    document.addEventListener("click", function (event) {
        if (!searchResults.contains(event.target) && event.target !== searchInput) {
            searchResults.style.display = "none";
        }
    });
});
