document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('currencyForm');
    const resultDiv = document.querySelector('.result');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const amount = form.amount.value;
        const fromCurrency = form.from_currency.value;
        const toCurrency = form.to_currency.value;

        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount,
                from_currency: fromCurrency,
                to_currency: toCurrency
            })
        });

        const data = await response.json();

        if (data.converted_amount) {
            resultDiv.innerHTML = `<h3>Converted Amount: ${data.converted_amount} ${toCurrency}</h3>`;
        } else {
            resultDiv.innerHTML = `<p class="error">${data.error_message}</p>`;
        }
    });
});
