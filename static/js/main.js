document.addEventListener('DOMContentLoaded', () => {
    // Вимкнення autocomplete у полі пошуку
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        searchInput.addEventListener('focus', function () {
            this.setAttribute('autocomplete', 'off');
        });
    }

    const menuButton = document.querySelector('.menu-btn');
    if (menuButton) {
        menuButton.addEventListener('click', () => {
            document.getElementById('dashboardMenu').classList.toggle('active');
        });
    }

    const savedTheme = localStorage.getItem('darkMode');
    if (savedTheme === 'enabled') {
        document.body.classList.add('dark-mode');
        document.querySelectorAll(
            'body, .header, .cart-menu, .dashboard-menu, .product-card, .search-container, #searchInput, .search-container button'
        ).forEach(el => el.classList.add('dark-mode'));

        const themeToggleIcon = document.querySelector('.night-mode-toggle i');
        if (themeToggleIcon) {
            themeToggleIcon.classList.remove('fa-moon');
            themeToggleIcon.classList.add('fa-sun');
        }
    }

    const themeToggle = document.querySelector('.night-mode-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const elements = document.querySelectorAll(
                'body, .header, .cart-menu, .dashboard-menu, .product-card, .search-container, #searchInput, .search-container button'
            );
            elements.forEach(el => el.classList.toggle('dark-mode'));

            const icon = themeToggle.querySelector('i');
            const isDark = document.body.classList.contains('dark-mode');
            if (icon) {
                icon.classList.toggle('fa-moon', !isDark);
                icon.classList.toggle('fa-sun', isDark);
            }
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
        });
    }

    const cartButton = document.getElementById('cartButton');
    if (cartButton) {
        cartButton.addEventListener('click', () => {
            document.getElementById('cartMenu').classList.toggle('active');
        });
    }

    const closeCartBtn = document.querySelector('.close-cart');
    if (closeCartBtn) {
        closeCartBtn.addEventListener('click', () => {
            document.getElementById('cartMenu').classList.remove('active');
        });
    }

    const checkoutBtn = document.querySelector('.main-button');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', submitCart);
    }
});

function searchProducts() {
    const query = document.getElementById("searchInput").value.trim().toLowerCase();
    const searchResults = document.getElementById("searchResults");

    if (query === "") {
        searchResults.style.display = "none";
        searchResults.innerHTML = "";
        return;
    }

    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.length === 0) {
                searchResults.innerHTML = "<p>Нічого не знайдено</p>";
            } else {
                const list = data.map(item => `
                    <li onclick="window.location.href='${item.url}'">
                        <img src="${item.image}" alt="${item.name}">
                        <span>${item.name} — ${item.price} грн</span>
                    </li>
                `).join("");
                searchResults.innerHTML = `<ul>${list}</ul>`;
            }

            searchResults.style.display = "block";
        })
        .catch(err => {
            searchResults.innerHTML = "<p>Помилка пошуку</p>";
            searchResults.style.display = "block";
        });
}



let cartItems = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(productName, productPrice, productImage, productWeight = "") {
    if (isNaN(productPrice)) {
        console.error("Ціна не є числом! price =", productPrice);
        return;
    }

    const existingItem = cartItems.find(item => item.name === productName && item.weight === productWeight);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cartItems.push({
            name: productName,
            price: parseFloat(productPrice),
            image: productImage,
            quantity: 1,
            weight: productWeight  // ⬅️ Додаємо вагу сюди
        });
    }

    localStorage.setItem("cart", JSON.stringify(cartItems));
    updateCart();
    showNotification(`Товар "${productName}" додано до кошика!`);
    openCart();
}


function updateCart() {
    const cartList = document.getElementById('cartItems');
    const totalPriceElement = document.getElementById('cartTotal');
    let total = 0;
    let cartHTML = '';

    cartItems.forEach(item => {
        total += item.price * item.quantity;
        cartHTML += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="item-info">
                    <p>${item.name}</p>
                    <p>${item.price.toFixed(2)} грн x${item.quantity}</p>
                </div>
                <div class="item-controls">
                    <button class="quantity-btn" onclick="decreaseQuantity('${item.name}')">−</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="increaseQuantity('${item.name}')">+</button>
                </div>
                <button class="item-remove" onclick="removeItem('${item.name}')">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        `;
    });

    if (cartList && totalPriceElement) {
        cartList.innerHTML = cartHTML;
        totalPriceElement.innerText = `Загальна сума: ${total.toFixed(2)} грн`;
    }
}

function increaseQuantity(productName) {
    const item = cartItems.find(item => item.name === productName);
    if (item) {
        item.quantity += 1;
        localStorage.setItem("cart", JSON.stringify(cartItems));
        updateCart();
    }
}

function decreaseQuantity(productName) {
    const item = cartItems.find(item => item.name === productName);
    if (item && item.quantity > 1) {
        item.quantity -= 1;
    } else if (item) {
        removeItem(productName);
        return;
    }
    localStorage.setItem("cart", JSON.stringify(cartItems));
    updateCart();
}

function removeItem(productName) {
    cartItems = cartItems.filter(item => item.name !== productName);
    localStorage.setItem("cart", JSON.stringify(cartItems));
    updateCart();
    showNotification(`Товар "${productName}" видалено з кошика!`);
}

function showNotification(message) {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.innerText = message;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 2000);
}

function openCart() {
    const cartMenu = document.getElementById('cartMenu');
    if (cartMenu) cartMenu.classList.add('active');
}

function closeCart() {
    const cartMenu = document.getElementById('cartMenu');
    if (cartMenu) cartMenu.classList.remove('active');
}

function submitCart() {
    fetch("/go-to-orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cartItems)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    updateCart();
});



let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('active', i === index);
  });
}

function changeSlide(direction) {
  currentSlide = (currentSlide + direction + slides.length) % slides.length;
  showSlide(currentSlide);
}

setInterval(() => changeSlide(1), 5000);




function scrollCategories(direction) {
    const track = document.getElementById('categoryTrack');
    const scrollAmount = 200; 
    track.scrollBy({
      left: direction * scrollAmount,
      behavior: 'smooth'
    });
  }
  






  document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.querySelector(".add-to-cart");

    if (addBtn) {
        addBtn.addEventListener("click", () => {
            const name = document.getElementById("productName").value;
            const image = document.getElementById("productImage").value;
            const selectedWeight = document.getElementById("selectedWeight").value;
            const selectedPrice = parseFloat(document.getElementById("selectedPrice").value);

            if (!selectedWeight || isNaN(selectedPrice)) {
                alert("Будь ласка, оберіть фасування перед додаванням у кошик!");
                return;
            }

            addToCart(`${name} (${selectedWeight})`, selectedPrice, image, selectedWeight);
        });
    }

    // Обробка плиток фасування
    const weightButtons = document.querySelectorAll(".weight-tile");
    const selectedWeightInput = document.getElementById("selectedWeight");
    const selectedPriceInput = document.getElementById("selectedPrice");
    const dynamicPriceDisplay = document.getElementById("dynamicPrice");

    weightButtons.forEach((button) => {
        button.addEventListener("click", () => {
            weightButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            const selectedWeight = button.getAttribute("data-weight");
            const selectedPrice = button.getAttribute("data-price");

            if (selectedWeightInput) selectedWeightInput.value = selectedWeight;
            if (selectedPriceInput) selectedPriceInput.value = selectedPrice;

            if (dynamicPriceDisplay) {
                dynamicPriceDisplay.textContent = `${selectedPrice} грн`;
            }
        });
    });

    // Перемикання фото
    const thumbnails = document.querySelectorAll(".thumbnail");
    const mainPhoto = document.getElementById("mainPhoto");
    thumbnails.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            if (mainPhoto) {
                mainPhoto.src = thumb.src;
                thumbnails.forEach(t => t.classList.remove("active"));
                thumb.classList.add("active");
            }
        });
    });

    // Нічна тема
    const savedTheme = localStorage.getItem("darkMode");
    if (savedTheme === "enabled") {
        document.body.classList.add("dark-mode");
        document.querySelectorAll(
            "body, .header, .cart-menu, .dashboard-menu, .product-card, .search-container, #searchInput, .search-container button"
        ).forEach(el => el.classList.add("dark-mode"));
        const icon = document.querySelector(".night-mode-toggle i");
        if (icon) icon.classList.replace("fa-moon", "fa-sun");
    }
});


 
 