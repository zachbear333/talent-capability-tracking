// var a;
function test() {
    element_id = event.srcElement.id
    select_item = document.getElementById(element_id)
    select_item.addEventListener('click', add_level)
    console.log(element_id)
    function add_level(event) {
        if (event) {
            event.preventDefault()
        }
        // now add a new empty form
        const formCopyTarget = document.getElementById('hahaha')
        console.log("fja")
        const emptyForm = document.getElementById('hidden').cloneNode(true)
        emptyForm.setAttribute('id', 'another')
        formCopyTarget.append(emptyForm)
        console.log(formCopyTarget)
    }
}   
