let products = [];


// ============================
// TOAST MESSAGE
// ============================

function toast(message) {

    const t = document.getElementById("toast");

    t.textContent = message;

    t.classList.add("show");

    setTimeout(() => {
        t.classList.remove("show");
    }, 1800);
}


// ============================
// ESCAPE HTML
// ============================

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ============================
// GET ALL PRODUCTS
// ============================

async function loadProducts() {

    try {

        const response = await fetch("/getProducts");

        if (!response.ok) {
            throw new Error("Failed to load products");
        }

        products = await response.json();

        renderProducts();

    } catch (error) {

        console.error(error);

        toast("Could not load products");
    }
}


// ============================
// DISPLAY PRODUCTS
// ============================

function renderProducts() {

    const grid =
        document.getElementById("product-grid");

    const count =
        document.getElementById("count");


    count.textContent =
        products.length +
        (products.length === 1
            ? " item"
            : " items");


    if (products.length === 0) {

        grid.innerHTML = `
            <div class="empty">
                <div class="big">
                    No products yet
                </div>

                Add your first product above.
            </div>
        `;

        return;
    }


    grid.innerHTML = "";


    products.forEach(product => {

        const div =
            document.createElement("div");

        div.className = "product";


        div.innerHTML = `
            <div>

                <div class="p-name">
                    ${escapeHtml(product.name)}
                </div>

                <div class="p-unit">
                    per ${escapeHtml(product.uom_name)}
                </div>

            </div>

            <div class="p-row">

                <div class="p-price">
                    ₹${Number(
                        product.price_per_unit
                    ).toFixed(2)}
                </div>

                <button
                    class="p-del"
                    data-id="${product.product_id}"
                    aria-label="Delete product"
                >
                    ×
                </button>

            </div>
        `;


        grid.appendChild(div);
    });


    // Delete buttons

    document
        .querySelectorAll(".p-del")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const productId =
                        button.dataset.id;

                    deleteProduct(productId);
                }
            );

        });
}


// ============================
// ADD PRODUCT
// ============================

async function addProduct() {

    const name =
        document
            .getElementById("p-name")
            .value
            .trim();


    const unit =
        document
            .getElementById("p-unit")
            .value;


    const price =
        parseFloat(
            document
                .getElementById("p-price")
                .value
        );


    // Validation

    if (!name) {

        toast("Enter a product name");

        return;
    }


    if (isNaN(price) || price < 0) {

        toast("Enter a valid price");

        return;
    }


    try {

        const response =
            await fetch(
                "/createProduct",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name: name,

                        unit: unit,

                        price_per_unit: price
                    })
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Failed to create product"
            );
        }


        console.log(result);


        toast("Product added");


        // Clear inputs

        document
            .getElementById("p-name")
            .value = "";


        document
            .getElementById("p-price")
            .value = "";


        document
            .getElementById("p-name")
            .focus();


        // Reload products

        await loadProducts();

    } catch (error) {

        console.error(error);

        toast("Could not add product");
    }
}


// ============================
// DELETE PRODUCT
// ============================

async function deleteProduct(productId) {

    try {

        const response =
            await fetch(
                `/deleteProduct/${productId}`,
                {
                    method: "DELETE"
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Failed to delete product"
            );
        }


        console.log(result);


        toast("Product removed");


        await loadProducts();

    } catch (error) {

        console.error(error);

        toast("Could not delete product");
    }
}


// ============================
// ADD BUTTON
// ============================

document
    .getElementById("add-btn")
    .addEventListener(
        "click",
        addProduct
    );


// ============================
// ENTER KEY - NAME
// ============================

document
    .getElementById("p-name")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                addProduct();
            }
        }
    );


// ============================
// ENTER KEY - PRICE
// ============================

document
    .getElementById("p-price")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                addProduct();
            }
        }
    );


// ============================
// LOAD PRODUCTS
// ============================

loadProducts();