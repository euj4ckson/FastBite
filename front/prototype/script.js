document.getElementById("addTable").addEventListener("click",()=>{
    // db add table function
    document.querySelector("ul").innerHTML += `
    <li class="table" id="t1">${"new"}</li>
    `;
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
    listSearch("tables","tableInput")
});