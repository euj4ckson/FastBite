const menuIcon = document.getElementById('burgerMenu'),
    menu = menuIcon.querySelector('nav'),
    searchBar = document.getElementById('searchBar'),
    searchIcon = searchBar.querySelector('search')

menuIcon.addEventListener('click',()=>{
    menu.style.width='200px'
    menu.style.height='200px'
    console.log()
})
searchBar.addEventListener('click',()=>{
    searchIcon.style.width='100px'
})