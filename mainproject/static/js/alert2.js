document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-button');
    const updateButtons = document.querySelectorAll('.button-18');
    const deleteModal = document.getElementById('deleteModal');
    const updateModal = document.getElementById('updateModal');
    const closeButtons = document.querySelectorAll('.close-button');
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const cancelDeleteButton = document.getElementById('cancelDeleteButton');
    const confirmUpdateButton = document.getElementById('confirmUpdateButton');
    const cancelUpdateButton = document.getElementById('cancelUpdateButton');
    const productDetails = document.getElementById('productDetails');
    const modalProductImage = document.getElementById('modalProductImage');
    const updateProductImage = document.getElementById('updateProductImage');
    const updateProductImageFile = document.getElementById('updateProductImageFile');
    const updateProductName = document.getElementById('updateProductName');
    const updateProductCategory = document.getElementById('updateProductCategory');
    const updateProductPrice = document.getElementById('updateProductPrice');
    const updateProductQuantity = document.getElementById('updateProductQuantity');
    const updateProductOffer = document.getElementById('updateProductOffer');
    let productIdToDelete;
    let productToUpdate;

    // Function to handle file input changes
    updateProductImageFile.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                updateProductImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const productId = event.target.getAttribute('data-id');
            const productName = event.target.getAttribute('data-name');
            const productCategory = event.target.getAttribute('data-category');
            const productPrice = event.target.getAttribute('data-price');
            const productImage = event.target.getAttribute('data-image');

            productIdToDelete = productId;
            productDetails.innerText = `ID: ${productId}\nName: ${productName}\nCategory: ${productCategory}\nPrice: ${productPrice}`;
            modalProductImage.src = productImage;

            deleteModal.style.display = 'block';
        });
    });

    updateButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const row = event.target.closest('tr');
            const productId = row.querySelector('td:nth-child(2)').innerText;
            const productName = row.querySelector('td:nth-child(3) .truncate').innerText;
            const productCategory = row.querySelector('td:nth-child(4)').innerText;
            const productPrice = row.querySelector('td:nth-child(6)').innerText;
            const productQuantity = row.querySelector('td:nth-child(7)').innerText;
            const productImage = row.querySelector('img').src;
            const productOffer = row.querySelector('td:nth-child(5)').innerText;

            productToUpdate = { productId, productName, productCategory, productPrice, productQuantity, productImage, productOffer };

            updateProductName.value = productName;
            updateProductCategory.value = productCategory;
            updateProductPrice.value = productPrice;
            updateProductQuantity.value = productQuantity;
            updateProductImage.src = productImage;
            updateProductImageFile.value = ''; // Clear file input value
            updateProductOffer.value = productOffer;

            updateModal.style.display = 'block';
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-modal');
            document.getElementById(modalId).style.display = 'none';
        });
    });

    cancelUpdateButton.addEventListener('click', () => {
        updateModal.style.display = 'none';
    });

    confirmUpdateButton.addEventListener('click', () => {
        // Code to update the product
        const updatedName = updateProductName.value;
        const updatedCategory = updateProductCategory.value;
        const updatedPrice = updateProductPrice.value;
        const updatedQuantity = updateProductQuantity.value;
        const updatedImageUrl = updateProductImage.src; // Get image URL from the preview
        const updatedOffer = updateProductOffer.value;

        alert(`Product ${productToUpdate.productId} updated successfully.\nName: ${updatedName}\nCategory: ${updatedCategory}\nPrice: ${updatedPrice}\nQuantity: ${updatedQuantity}\nImage URL: ${updatedImageUrl}\nOffer: ${updatedOffer}`);
        updateModal.style.display = 'none';
    });

    cancelDeleteButton.addEventListener('click', () => {
        deleteModal.style.display = 'none';
    });

    confirmDeleteButton.addEventListener('click', () => {
        // Code to delete the product
        alert(`Product ${productIdToDelete} deleted successfully.`);
        deleteModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        } else if (event.target === updateModal) {
            updateModal.style.display = 'none';
        }
    });
});
