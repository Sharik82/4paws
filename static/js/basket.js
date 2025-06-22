const checkoutBtn = document.querySelector('.checkout-btn');
const modal = document.getElementById('checkoutModal');
const closeModal = document.getElementById('closeModal');
const paymentSelect = document.getElementById('payment');
const savedCards = document.getElementById('savedCards');
const newCard = document.getElementById('newCard');
const successMessage = document.getElementById('successMessage');

checkoutBtn.onclick = function() {
    modal.style.display = 'block';
}

closeModal.onclick = function() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

paymentSelect.onchange = function() {
    if (paymentSelect.value === 'card') {
        savedCards.style.display = 'block';
        newCard.style.display = 'none';
    } else {
        savedCards.style.display = 'none';
        newCard.style.display = 'none';
    }
}

document.getElementById('addNewCard').onclick = function() {
    newCard.style.display = 'block';
}


document.getElementById('checkoutForm').onsubmit = function(event) {
    event.preventDefault(); 
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    

    successMessage.style.display = 'block';
    modal.style.display = 'none'; 
}
