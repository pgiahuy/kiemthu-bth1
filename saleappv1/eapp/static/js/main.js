function addToCart(id, name, price) {
    fetch("/api/carts", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let elems = document.getElementsByClassName("cart-counter");
        for (let e of elems)
            e.innerText = data.total_quantity;
    });
}

function updateCart(id, obj) {
    fetch(`/api/carts/${id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let elems = document.getElementsByClassName("cart-counter");
        for (let e of elems)
            e.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName("cart-amount");
        for (let e of amounts)
            e.innerText = data.total_amount.toLocaleString("en");
    })
}

function deleteCart(id) {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
        fetch(`/api/carts/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let elems = document.getElementsByClassName("cart-counter");
            for (let e of elems)
                e.innerText = data.total_quantity;

            let amounts = document.getElementsByClassName("cart-amount");
            for (let e of amounts)
                e.innerText = data.total_amount.toLocaleString("en");

            let item = document.getElementById(`cart${id}`);
            item.style.display = "none";
        });
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        fetch("/api/pay", {
            method: "post"
        }).then(res => {
            if (res.status === 200)
                location.reload();
            else
                alert("Hệ thống bị loi!");
        })
    }
}