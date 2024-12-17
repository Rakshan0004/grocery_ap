var productModal = $("#productModal");

// Load Product List on Page Load
$(function () {
    // Fetch JSON data and populate the table
    $.get(productListApiUrl, function (response) {
        if (response) {
            var table = '';
            $.each(response, function (index, product) {
                table += '<tr data-id="' + product.product_id + '" data-name="' + product.name + '" data-unit="' + product.uom_id + '" data-price="' + product.price_per_unit + '">' +
                    '<td>' + product.name + '</td>' +
                    '<td>' + product.uom_name + '</td>' +
                    '<td>' + product.price_per_unit + '</td>' +
                    '<td>' +
                    '<span class="btn btn-xs btn-danger delete-product">Delete</span> ' +
                    '<span class="btn btn-xs btn-warning edit-product">Edit</span>' +
                    '</td>' +
                    '</tr>';
            });
            $("table").find('tbody').empty().html(table);
        }
    });
});

// Save Product (Add or Update)
$("#saveProduct").on("click", function () {
    var data = $("#productForm").serializeArray();
    var requestPayload = {
        product_id: $("#id").val(), // Check for product ID
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };

    // Map form values to JSON payload
    for (var i = 0; i < data.length; ++i) {
        var element = data[i];
        switch (element.name) {
            case 'name':
                requestPayload.product_name = element.value;
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;
                break;
        }
    }

    // Call API to Add or Update product
    callApi("POST", productSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});

// Edit Product Functionality
$(document).on("click", ".edit-product", function () {
    var tr = $(this).closest('tr');
    var product_id = tr.data('id'); // Existing product_id
    var product_name = tr.data('name');
    var uom_id = tr.data('unit');
    var price_per_unit = tr.data('price');

    // Populate the form with existing values
    $("#id").val(product_id); // Hidden input for product_id
    $("#name").val(product_name);
    $("#uoms").val(uom_id);
    $("#price").val(price_per_unit);

    // Open the modal
    $("#productModal").find('.modal-title').text('Edit Product');
    $("#productModal").modal('show');
});

// Modify Save Product to handle both insert and edit
$("#saveProduct").on("click", function () {
    // Prepare the request payload
    var requestPayload = {
        product_id: $("#id").val(), // This will be the key difference for edit vs insert
        name: $("#name").val(),
        uom_id: $("#uoms").val(),
        price_per_unit: $("#price").val()
    };

    // Determine the API endpoint based on whether product_id exists
    var apiUrl = requestPayload.product_id ? '/editProduct' : '/insertProduct';

    // Send the request
    $.ajax({
        url: apiUrl,
        method: 'POST',
        data: {
            'data': JSON.stringify(requestPayload)
        },
        success: function (response) {
            alert(response.message);
            location.reload(); // Refresh the product list
        },
        error: function (xhr, status, error) {
            alert('An error occurred: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Unknown error'));
        }
    });
});


// Delete Product
$(document).on("click", ".delete-product", function () {
    var tr = $(this).closest('tr');
    var data = {
        product_id: tr.data('id')
    };

    var isDelete = confirm("Are you sure to delete " + tr.data('name') + " item?");
    if (isDelete) {
        callApi("POST", productDeleteApiUrl, data);
    }
});

// Product Modal - Clear Fields on Close
productModal.on('hide.bs.modal', function () {
    $("#id").val('0'); // Reset product ID
    $("#name, #uoms, #price").val('');
    productModal.find('.modal-title').text('Add New Product');
});

// Populate UOM Options when Modal is Shown
productModal.on('show.bs.modal', function () {
    $.get(uomListApiUrl, function (response) {
        if (response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function (index, uom) {
                options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
            });
            $("#uoms").empty().html(options);
        }
    });
});

// Function to Call API
function callApi(method, url, data) {
    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (response) {
            alert(response.message || 'Operation completed successfully');
            location.reload(); // Reload table after operation
        },
        error: function (error) {
            alert('Something went wrong! Please try again.');
        }
    });
}
