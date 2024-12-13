document.getElementById("addTable").addEventListener("click",()=>{
    // db add table function needed 
    document.querySelector("ul").innerHTML += `
    <li class="table" id="t${10}">${"new"}</li>
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
    listSearch("tablesList","tableInput")
});
const navBtns = document.querySelectorAll(".navBtn"),
    sections = document.querySelectorAll("section");

navBtns.forEach((btn)=>{
    btn.addEventListener("click",(e)=>{
        if(e.target.classList.contains('active')){return}
        navBtns.forEach((btnCheck)=>{btnCheck.classList.remove("active")});
        e.target.classList.add("active");
        sections.forEach((sec)=>{sec.style.display="none"});
        document.getElementById(e.target.value).style.display="flex";
    })
});