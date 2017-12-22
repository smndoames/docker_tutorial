function formaction(checkbox){
    document.getElementById("todos").action = checkbox.value;
    document.getElementById("todos").submit()
}