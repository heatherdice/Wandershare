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

//show that an image was added to the new wandering form
file.addEventListener("change", function () {
    if(file.value) {
        document.getElementById('input-div').style.border = '2px solid green';
        fileLabel.innerText = "Image selected";
    }
})