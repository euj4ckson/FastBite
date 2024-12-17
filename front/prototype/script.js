document.getElementById("addTable").addEventListener("click",()=>{
    // db add table function needed
    //id should be db index or sequential number?
    document.querySelector("ul").innerHTML += `
    <li class="table" id="t${10}">
        <span class="tableName">${"new"}</span>
        <div class="tableStatus" value >free</div>
    </li>   
    `;
});

const dialog = document.querySelector("dialog");
document.querySelectorAll(".table").forEach((table)=>{
    table.addEventListener("click",(e)=>{
        //db select table/order info call
        dialog.querySelector("span").textContent = e.target.id;
        dialog.querySelector(".deleteTableBtn").id = `d${e.target.id}`;
        dialog.show();
    })
});
document.querySelectorAll(".add,.remove").forEach((btn)=>{
    btn.addEventListener('click',(e)=>{
        const span = e.target.parentNode.querySelector('span');
        if(e.target.className==='add'){
            span.textContent = parseInt(span.textContent)+1;
            return
        }
        if(span.textContent!=0){
            span.textContent = parseInt(span.textContent)-1;
        }

    })
})
document.querySelector(".closeDialogBtn").addEventListener("click",(e)=>{
    dialog.close();
});
document.querySelector(".deleteTableBtn").addEventListener("click",(e)=>{

    //db delete table call
    document.getElementById("tablesList").removeChild(document.getElementById(e.target.id.slice(1)))
});
function listSearch(list,input){
    const li = document.getElementById(list).querySelectorAll("li"),
        filter = document.getElementById(input),
        search = filter.value.toUpperCase();
    document.querySelectorAll("li").forEach((_,index) => {
        li[index].style.display = li[index].textContent.toUpperCase().indexOf(search) > -1 ? "flex" : "none";
    });
}
document.getElementById("tableInput").addEventListener("keyup",()=>{
    listSearch("tablesList","tableInput")
});
const navBtns = document.querySelectorAll(".navBtn"),
    sections = document.querySelectorAll("section");

navBtns.forEach((btn)=>{
    btn.addEventListener("click",(e)=>{
        dialog.close();
        if(e.target.classList.contains('active')){return}
        navBtns.forEach((btnCheck)=>{btnCheck.classList.remove("active")});
        e.target.classList.add("active");
        sections.forEach((sec)=>{sec.style.display="none"});
        document.getElementById(e.target.value).style.display="flex";
    })
});
document.getElementById("configsBtn").addEventListener("click",(e)=>{
    navBtns.forEach((btnCheck)=>{btnCheck.classList.remove("active")});
    sections.forEach((sec)=>{sec.style.display="none"});
    document.getElementById(e.target.value).style.display="flex";
});

document.getElementById("createOrder").addEventListener('click',()=>{
    createOrder("list",document.querySelector('[name="clientName"]').value,document.querySelector('[name="orderDetails"]').value);
    //db insert new order
})
function createOrder(products,client,obs){
    console.log(products,client,obs);
}