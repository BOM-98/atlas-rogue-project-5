document.addEventListener("DOMContentLoaded", function () {
  var stripePublicKey = document
    .getElementById("id_stripe_public_key")
    .textContent.trim()
    .slice(1, -1);
  var clientSecret = document
    .getElementById("id_client_secret")
    .textContent.trim()
    .slice(1, -1);
  var stripe = Stripe(stripePublicKey);
  var elements = stripe.elements();
  var style = {
    base: {
      color: "#000",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545",
    },
  };
  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  // Handle realtime validation errors on the card element
  card.addEventListener("change", function (event) {
    var errorDiv = document.getElementById("card-errors");
    if (event.error) {
      var html = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
        `;
      errorDiv.innerHTML = html;
    } else {
      errorDiv.textContent = "";
    }
  });

  // Handle form submit
  const form = document.getElementById("payment-form");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    card.update({ disabled: true });
    document.getElementById("submit-button").disabled = true;
    stripe
      .confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
        },
      })
      .then(function (result) {
        if (result.error) {
          var errorDiv = document.getElementById("card-errors");
          var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
          errorDiv.innerHTML = html;
          card.update({ disabled: false });
          document.getElementById("submit-button").disabled = false;
        } else {
          if (result.paymentIntent.status === "succeeded") {
            form.submit();
          }
        }
      });
  });
});
