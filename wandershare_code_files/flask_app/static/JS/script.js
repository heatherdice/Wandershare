//changes image file on edit page
function fileChange(element) {
    let fileChangeSpan = document.getElementById("file-change")
    if(element.value !== "") {
        let fileName = element.value.split("\\").pop()
        fileChangeSpan.innerText = fileName
    }
    else {
        fileChangeSpan.innerText = ""
    }
}