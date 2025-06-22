document.addEventListener('DOMContentLoaded', () => {
    let cartItems = JSON.parse(localStorage.getItem("cart")) || [];

    const defaultButton = document.querySelector('.packaging-options button');
    if (defaultButton) selectOption(defaultButton);

    document.querySelectorAll('.packaging-options button').forEach(button => {
        button.addEventListener('click', () => selectOption(button));
    });

    function selectOption(button) {
        document.querySelectorAll('.packaging-options button').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');

        const weight = button.dataset.weight || button.textContent;
        const price = button.dataset.price || document.getElementById('selectedPrice')?.value || "0";

        const parsedPrice = parseFloat(price);
        if (!isNaN(parsedPrice)) {
            document.querySelector('.current-price').innerText = `${parsedPrice.toFixed(2)} грн`;
            document.getElementById('selectedPrice').value = parsedPrice;
            document.getElementById('selectedWeight').value = weight;
        }
    }

    const addBtn = document.querySelector('.add-to-cart');
    if (addBtn) {
        addBtn.addEventListener('click', () => {
            const name = document.getElementById('productName')?.value || "Невідомо";
            const price = parseFloat(document.getElementById('selectedPrice')?.value);
            const image = document.getElementById('productImage')?.value || "";

            if (isNaN(price)) {
                console.error("⛔️ Ціна не є числом!", price);
                alert("Ціна товару недійсна");
                return;
            }

            const existingItem = cartItems.find(item => item.name === name);
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cartItems.push({ name, price, image, quantity: 1 });
            }

            localStorage.setItem("cart", JSON.stringify(cartItems));
            updateCart();
            showNotification(`✅ Товар "${name}" додано у кошик`);
            openCart();
        });
    }

    function updateCart() {
        const cartList = document.getElementById('cartItems');
        const totalPrice = document.getElementById('cartTotal');
        if (!cartList || !totalPrice) return;

        cartList.innerHTML = '';
        let total = 0;

        cartItems.forEach(item => {
            total += item.price * item.quantity;

            cartList.insertAdjacentHTML('beforeend', `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                    <div class="item-info">
                        <p>${item.name}</p>
                        <p>${item.price.toFixed(2)} грн × ${item.quantity}</p>
                    </div>
                    <div class="item-controls">
                        <button onclick="decreaseQuantity('${item.name}')">−</button>
                        <span>${item.quantity}</span>
                        <button onclick="increaseQuantity('${item.name}')">+</button>
                    </div>
                    <button class="item-remove" onclick="removeItem('${item.name}')">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `);
        });

        totalPrice.innerText = `Загальна сума: ${total.toFixed(2)} грн`;
    }

    window.increaseQuantity = function (name) {
        const item = cartItems.find(i => i.name === name);
        if (item) item.quantity += 1;
        localStorage.setItem("cart", JSON.stringify(cartItems));
        updateCart();
    };

    window.decreaseQuantity = function (name) {
        const item = cartItems.find(i => i.name === name);
        if (item && item.quantity > 1) item.quantity -= 1;
        else cartItems = cartItems.filter(i => i.name !== name);
        localStorage.setItem("cart", JSON.stringify(cartItems));
        updateCart();
    };

    window.removeItem = function (name) {
        cartItems = cartItems.filter(i => i.name !== name);
        localStorage.setItem("cart", JSON.stringify(cartItems));
        updateCart();
        showNotification(`❌ Товар "${name}" видалено з кошика`);
    };

    function showNotification(message) {
        const notification = document.getElementById('notification');
        if (!notification) return;

        notification.innerText = message;
        notification.classList.add('show');
        setTimeout(() => notification.classList.remove('show'), 2000);
    }

    function openCart() {
        const cartMenu = document.getElementById('cartMenu');
        if (cartMenu) cartMenu.classList.add('active');
    }

    const checkoutBtn = document.querySelector('.main-button');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            fetch("/go-to-orders", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(cartItems)
            })
            .then(res => res.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            });
        });
    }

    updateCart(); // ініціалізація при завантаженні
});
