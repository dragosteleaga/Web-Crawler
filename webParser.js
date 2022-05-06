fetch("file.json")
    .then(response => response.json())
    .then(data => {
        let list=document.getElementById("wrap");
        data.forEach(element=>{
            list.innerHTML+=`
            <li>
            <h2>${element.numeJob}</h2>
            <p>${element.descriere}</p>
            </li>
            `
            console.log(list);
        })
    })
