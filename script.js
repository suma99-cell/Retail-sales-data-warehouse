const baseURL = "http://127.0.0.1:5000";


window.onload = function () {
    loadAnalytics();
};

function showSection(section) {
    document.getElementById("analytics").classList.add("hidden");
    document.getElementById("reports").classList.add("hidden");
    document.getElementById("warehouse").classList.add("hidden");

    document.getElementById(section).classList.remove("hidden");
}


function loadAnalytics() {

    fetch(`${baseURL}/total_sales`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("totalSales").innerText =
                "Total Revenue: ₹ " + data.total_sales;
        });

    fetch(`${baseURL}/sales_by_customer`)
        .then(res => res.json())
        .then(data => {

            const labels = Object.keys(data);
            const values = Object.values(data);

            new Chart(document.getElementById("chart"), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sales',
                        data: values,
                        backgroundColor: "#3b82f6"
                    }]
                }
            });
        });
}


function showReports() {
    showSection('reports');

    fetch(`${baseURL}/sales_details`)
        .then(res => res.json())
        .then(data => {

            let table = document.getElementById("reportTable");
            table.innerHTML = "";

            data.forEach(row => {
                table.innerHTML += `
                    <tr>
                        <td>${row.customer || ""}</td>
                        <td>${row.product || ""}</td>
                        <td>${row.date || ""}</td>
                        <td>${row.amount || ""}</td>
                    </tr>
                `;
            });
        });
}

function renderTable(headers, data) {
    let head = document.getElementById("tableHead");
    let body = document.getElementById("tableBody");

    head.innerHTML = "";
    body.innerHTML = "";

    
    let hRow = "<tr>";
    headers.forEach(h => hRow += `<th>${h}</th>`);
    hRow += "</tr>";
    head.innerHTML = hRow;

    
    data.forEach(row => {
        let tr = "<tr>";
        headers.forEach(h => {
            tr += `<td>${row[h] ?? ""}</td>`; 
        });
        tr += "</tr>";
        body.innerHTML += tr;
    });
}


function loadDimCustomer() {
    showSection('warehouse');

    fetch(`${baseURL}/dim_customer`)
        .then(res => res.json())
        .then(data => {
            renderTable(
                ["customer_key","customer_name","gender","city","state","country","customer_type"],
                data
            );
        });
}


function loadDimProduct() {
    showSection('warehouse');

    fetch(`${baseURL}/dim_product`)
        .then(res => res.json())
        .then(data => {
            renderTable(
                ["product_key","product_name","category","brand","unit_price"],
                data
            );
        });
}


function loadDimDate() {
    showSection('warehouse');

    fetch(`${baseURL}/dim_date`)
        .then(res => res.json())
        .then(data => {
            renderTable(
                ["date_key","full_date","day","month","quarter","year"],
                data
            );
        });
}


function loadFactSales() {
    showSection('warehouse');

    fetch(`${baseURL}/fact_sales`)
        .then(res => res.json())
        .then(data => {
            renderTable(
                [
                    "sale_id",
                    "customer_key",
                    "product_key",
                    "date_key",
                    "quantity_sold",
                    "sales_amount",
                    "discount_amount"
                ],
                data
            );
        });
}
