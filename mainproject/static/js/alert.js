// Get the modal
var modal = document.getElementById("deleteModal");
// Get the <span> element that closes the modal
var closeButton = document.querySelector(".close-button");
// Get the confirm button
var confirmDeleteButton = document.getElementById("confirmDeleteButton");

// Function to show modal and populate product details
document.querySelectorAll(".delete-button").forEach(function(button) {
    button.addEventListener("click", function() {
        var id = this.getAttribute("data-id");
        var name = this.getAttribute("data-name");
        var category = this.getAttribute("data-category");
        var price = this.getAttribute("data-price");

        // Populate product details in the modal
        var productDetails = document.getElementById("productDetails");
        productDetails.innerHTML = `
            <strong>Product ID:</strong> ${id} <br>
            <strong>Name:</strong> ${name} <br>
            <strong>Category:</strong> ${category} <br>
            <strong>Price:</strong> ${price}
        `;

        // Show the modal
        modal.style.display = "block";

        // Set the confirm button action
        confirmDeleteButton.setAttribute("data-id", id);
    });
});

// When the user clicks on <span> (x), close the modal
closeButton.addEventListener("click", function() {
    modal.style.display = "none";
});

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});

// Handle the confirm delete button click
confirmDeleteButton.addEventListener("click", function() {
    var id = this.getAttribute("data-id");
    // Implement the delete action here, such as making an AJAX request to delete the item
    console.log("Deleting product with ID:", id);
    // Close the modal after confirming delete
    modal.style.display = "none";
});

// Handle the cancel button click
document.getElementById("cancelButton").addEventListener("click", function() {
    modal.style.display = "none";
});